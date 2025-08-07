<template>
  <div v-if="show" class="ai-chat-modal-overlay" @click="closeModal">
    <div class="ai-chat-modal" @click.stop>
      <div class="chat-header">
        <h3>🤖 Assistant IA SyncTasks</h3>
        <button class="close-btn" @click="closeModal">✕</button>
      </div>

      <div class="chat-container">
        <div ref="messagesContainer" class="chat-messages">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message', message.type]"
          >
            <div class="message-avatar">
              <span v-if="message.type === 'user'">👤</span>
              <span v-else>🤖</span>
            </div>
            <div class="message-content">
              <div
                class="message-text"
                v-html="formatMessage(message.text)"
              ></div>
              <div class="message-time">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
          </div>

          <div v-if="loading" class="message ai">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input-container">
          <form class="chat-form" @submit.prevent="sendMessage">
            <div class="input-wrapper">
              <input
                v-model="newMessage"
                placeholder="Posez votre question à l'IA..."
                class="chat-input"
                :disabled="loading"
                @keydown.enter="sendMessage"
              />
              <button
                type="submit"
                class="send-btn"
                :disabled="loading || !newMessage.trim()"
              >
                <span v-if="!loading">📤</span>
                <span v-else>⏳</span>
              </button>
            </div>
          </form>
        </div>
      </div>

      <div class="chat-suggestions">
        <h4>💡 Suggestions rapides</h4>
        <div class="suggestions-grid">
          <button
            v-for="suggestion in quickSuggestions"
            :key="suggestion"
            class="suggestion-btn"
            :disabled="loading"
            @click="sendQuickMessage(suggestion)"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref, nextTick, watch } from 'vue';
  import axios from 'axios';

  export default {
    name: 'AIChatModal',
    props: {
      show: {
        type: Boolean,
        default: false,
      },
    },
    emits: ['close'],
    setup(props, { emit }) {
      const messages = ref([]);
      const newMessage = ref('');
      const loading = ref(false);
      const messagesContainer = ref(null);

      const quickSuggestions = [
        'Comment organiser mes tâches ?',
        'Techniques de productivité',
        'Gérer le stress au travail',
        'Planifier ma semaine',
        'Retrouver la motivation',
      ];

      // Message de bienvenue
      const welcomeMessage = {
        id: 'welcome',
        type: 'ai',
        text: `Bonjour ! Je suis votre assistant IA SyncTasks 🤖

Je peux vous aider avec :
• 📋 Organisation et planification de tâches
• 🎯 Conseils de productivité
• 💪 Techniques de motivation
• 🧘 Gestion du stress
• ⏰ Optimisation du temps

Comment puis-je vous aider aujourd'hui ?`,
        timestamp: new Date(),
      };

      // Initialiser avec le message de bienvenue
      if (messages.value.length === 0) {
        messages.value.push(welcomeMessage);
      }

      const closeModal = () => {
        emit('close');
      };

      const formatMessage = text => {
        // Convertir les emojis et le markdown simple
        return text
          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
          .replace(/\*(.*?)\*/g, '<em>$1</em>')
          .replace(/\n/g, '<br>');
      };

      const formatTime = timestamp => {
        return new Date(timestamp).toLocaleTimeString('fr-FR', {
          hour: '2-digit',
          minute: '2-digit',
        });
      };

      const scrollToBottom = async () => {
        await nextTick();
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop =
            messagesContainer.value.scrollHeight;
        }
      };

      const sendMessage = async () => {
        if (!newMessage.value.trim() || loading.value) {
          return;
        }

        const userMessage = {
          id: Date.now(),
          type: 'user',
          text: newMessage.value,
          timestamp: new Date(),
        };

        messages.value.push(userMessage);
        const messageToSend = newMessage.value;
        newMessage.value = '';
        loading.value = true;

        await scrollToBottom();

        try {
          const response = await axios.post('/api/ia/chat', {
            message: messageToSend,
            context: 'chat',
          });

          const aiMessage = {
            id: Date.now() + 1,
            type: 'ai',
            text: response.data.response,
            timestamp: new Date(),
          };

          messages.value.push(aiMessage);
          await scrollToBottom();
        } catch (error) {
          console.error("Erreur lors de l'envoi du message:", error);
          const errorMessage = {
            id: Date.now() + 1,
            type: 'ai',
            text: '❌ Désolé, je rencontre un problème technique. Veuillez réessayer dans quelques instants.',
            timestamp: new Date(),
          };
          messages.value.push(errorMessage);
          await scrollToBottom();
        } finally {
          loading.value = false;
        }
      };

      const sendQuickMessage = suggestion => {
        newMessage.value = suggestion;
        sendMessage();
      };

      // Scroll automatique quand de nouveaux messages arrivent
      watch(messages, scrollToBottom, { deep: true });

      return {
        messages,
        newMessage,
        loading,
        messagesContainer,
        quickSuggestions,
        closeModal,
        sendMessage,
        sendQuickMessage,
        formatMessage,
        formatTime,
      };
    },
  };
</script>

<style scoped>
  .ai-chat-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .ai-chat-modal {
    width: 95%;
    max-width: 600px;
    height: 80vh;
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .chat-header h3 {
    margin: 0;
    font-size: 1.2rem;
  }

  .close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    transition: background-color 0.2s;
  }

  .close-btn:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  .chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .message {
    display: flex;
    gap: 0.8rem;
    max-width: 80%;
  }

  .message.user {
    align-self: flex-end;
    flex-direction: row-reverse;
  }

  .message.ai {
    align-self: flex-start;
  }

  .message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
  }

  .message.user .message-avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .message.ai .message-avatar {
    background: #f8f9fa;
    color: #667eea;
  }

  .message-content {
    flex: 1;
    min-width: 0;
  }

  .message-text {
    background: #f8f9fa;
    padding: 0.8rem 1rem;
    border-radius: 12px;
    line-height: 1.5;
    color: #333;
  }

  .message.user .message-text {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .message-time {
    font-size: 0.75rem;
    color: #6c757d;
    margin-top: 0.3rem;
    text-align: right;
  }

  .message.ai .message-time {
    text-align: left;
  }

  .typing-indicator {
    display: flex;
    gap: 0.3rem;
    padding: 0.8rem 1rem;
  }

  .typing-indicator span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #667eea;
    animation: typing 1.4s infinite ease-in-out;
  }

  .typing-indicator span:nth-child(1) {
    animation-delay: -0.32s;
  }
  .typing-indicator span:nth-child(2) {
    animation-delay: -0.16s;
  }

  @keyframes typing {
    0%,
    80%,
    100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }

  .chat-input-container {
    padding: 1rem;
    border-top: 1px solid #e9ecef;
  }

  .chat-form {
    display: flex;
    gap: 0.5rem;
  }

  .input-wrapper {
    display: flex;
    flex: 1;
    border: 2px solid #e9ecef;
    border-radius: 25px;
    overflow: hidden;
    transition: border-color 0.2s;
  }

  .input-wrapper:focus-within {
    border-color: #667eea;
  }

  .chat-input {
    flex: 1;
    border: none;
    padding: 0.8rem 1rem;
    font-size: 1rem;
    outline: none;
  }

  .send-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.8rem 1.2rem;
    cursor: pointer;
    transition: opacity 0.2s;
  }

  .send-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .chat-suggestions {
    padding: 1rem;
    border-top: 1px solid #e9ecef;
    background: #f8f9fa;
  }

  .chat-suggestions h4 {
    margin: 0 0 0.8rem 0;
    color: #495057;
    font-size: 0.9rem;
  }

  .suggestions-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .suggestion-btn {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 20px;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
    color: #495057;
  }

  .suggestion-btn:hover:not(:disabled) {
    background: #667eea;
    color: white;
    border-color: #667eea;
  }

  .suggestion-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .ai-chat-modal {
      width: 100%;
      height: 100vh;
      border-radius: 0;
    }

    .message {
      max-width: 90%;
    }

    .suggestions-grid {
      flex-direction: column;
    }
  }
</style>
