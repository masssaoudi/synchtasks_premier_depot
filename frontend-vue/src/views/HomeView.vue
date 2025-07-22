<template>
  <div class="home-container">
    <!-- Section de bienvenue -->
    <div class="welcome-section">
      <h1>Bienvenue sur SyncTasks ! 🎉</h1>
      <p class="welcome-text">
        Bonjour {{ authStore.currentUser?.full_name || authStore.currentUser?.username }}, 
        bienvenue dans votre espace de gestion de tâches intelligent.
      </p>
    </div>

    <div class="quick-actions">
      <div class="action-card">
        <h3>📋 Mes Tâches</h3>
        <p>Gérez vos tâches avec notre interface Kanban intuitive</p>
        <router-link to="/tasks" class="btn btn-primary">Voir mes tâches</router-link>
      </div>
      <div class="action-card">
        <h3>👥 Personnels aidants</h3>
        <p>Gérez votre équipe et vos collaborateurs</p>
        <button @click="showPersonnelFeature" class="btn btn-primary">Fonctionnalité en développement</button>
      </div>
      <div class="action-card">
        <h3>🤖 Assistant IA</h3>
        <p>Obtenez de l'aide et des conseils de notre IA</p>
        <button @click="openAIChat" class="btn btn-primary">Parler à l'IA</button>
        <button @click="testAPI" class="btn btn-secondary" style="margin-top: 10px;">Test API</button>
      </div>
    </div>

    <!-- Modal du chat IA -->
    <div v-if="showChatModal" class="modal-overlay" @click="closeChatModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>🤖 Parler à Lia</h2>
          <button @click="closeChatModal" class="close-btn">&times;</button>
        </div>
        
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(message, index) in chatState.messages" :key="index" 
               :class="['message', message.type]">
            <div class="message-content">
              <div class="message-text">
                <p>{{ message.text }}</p>
              </div>
              
              <!-- Suggestions -->
              <div v-if="message.suggestions && message.suggestions.length > 0" class="suggestions">
                <button 
                  v-for="(suggestion, i) in message.suggestions" 
                  :key="i"
                  @click="sendMessage(suggestion)"
                  class="suggestion-btn"
                >
                  {{ suggestion }}
                </button>
              </div>
              
              <!-- Suggestions de tâches -->
              <div v-if="message.task_suggestions && message.task_suggestions.length > 0" class="task-suggestions">
                <h4>Créer une tâche :</h4>
                <div v-for="(taskSuggestion, i) in message.task_suggestions" :key="i" class="task-suggestion">
                  <span>{{ taskSuggestion.title }}</span>
                  <button @click="createTaskFromSuggestion(taskSuggestion)" class="create-task-btn">
                    Créer
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-input">
          <input 
            v-model="chatState.newMessage" 
            @keyup.enter="sendMessage(chatState.newMessage)"
            placeholder="Dites-moi ce que vous voulez faire..."
            :disabled="chatState.isLoading"
          />
          <button @click="sendMessage(chatState.newMessage)" :disabled="chatState.isLoading">
            <span v-if="chatState.isLoading">⏳</span>
            <span v-else>📤</span>
          </button>
          <button @click="testAPI" class="test-btn">TEST</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, reactive } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'HomeView',
  setup() {
    const authStore = useAuthStore()
    
    const stats = ref({
      totalTasks: 0,
      pendingTasks: 0,
      completedTasks: 0,
      productivity: 0
    })
    
    // Chat IA - Utiliser reactive au lieu de ref
    const showChatModal = ref(false)
    const chatState = reactive({
      messages: [],
      newMessage: '',
      isLoading: false
    })
    
    // Forcer l'initialisation du tableau
    if (!Array.isArray(chatState.messages)) {
      chatState.messages = []
    }
    
    const loadStats = async () => {
      // Simuler le chargement des statistiques
      // Plus tard, on fera un appel API réel
      stats.value = {
        totalTasks: 12,
        pendingTasks: 5,
        completedTasks: 7,
        productivity: 58
      }
    }
    
    const openAIChat = () => {
      console.log('🚀 openAIChat appelé')
      
      // Ouvrir la modale
      showChatModal.value = true
      console.log('✅ Modal ouvert, showChatModal:', showChatModal.value)
      
      // Forcer l'initialisation du tableau
      if (!Array.isArray(chatState.messages)) {
        console.log('🔄 Réinitialisation de chatMessages dans openAIChat')
        chatState.messages = []
      }
      
      // Message de bienvenue
      if (chatState.messages.length === 0) {
        console.log('👋 Ajout du message de bienvenue')
        const welcomeMessage = {
          type: 'ai',
          text: `Bonjour ${authStore.currentUser?.full_name || authStore.currentUser?.username} ! Je suis Lia, votre assistante IA pour SyncTasks. Comment puis-je vous aider aujourd'hui ?`,
          suggestions: [
            "J'ai beaucoup de tâches à faire",
            "Comment organiser mes priorités ?",
            "Je me sens dépassé",
            "Donne-moi des conseils de productivité"
          ]
        }
        // Forcer la réactivité en créant un nouveau tableau
        chatState.messages = [...chatState.messages, welcomeMessage]
        console.log('✅ Message de bienvenue ajouté:', welcomeMessage)
        console.log('📊 chatMessages après ajout:', chatState.messages)
      }
      
      // Forcer la réactivité
      nextTick(() => {
        console.log('🔄 nextTick exécuté, chatMessages:', chatState.messages)
      })
    }
    
    const closeChatModal = () => {
      showChatModal.value = false
    }
    
    const testButton = () => {
      console.log('🔴 BOUTON TEST CLIQUE !')
      alert('Bouton test fonctionne !')
    }
    
    const sendMessage = async (message) => {
      if (!message.trim() || chatState.isLoading) return
      
      try {
        // Vérifier et réinitialiser si nécessaire
        if (!Array.isArray(chatState.messages)) {
          console.log('⚠️ chatMessages n\'est pas un tableau, réinitialisation...')
          chatState.messages = []
        }
        
        // Ajouter le message utilisateur de manière sûre
        const userMessage = {
          type: 'user',
          text: message
        }
        
        console.log('📝 Ajout du message utilisateur:', userMessage)
        // Forcer la réactivité en créant un nouveau tableau
        chatState.messages = [...chatState.messages, userMessage]
        console.log('✅ Message utilisateur ajouté, longueur:', chatState.messages.length)
        
      } catch (error) {
        console.error('❌ Erreur lors de l\'ajout du message utilisateur:', error)
        // Réinitialiser complètement
        chatState.messages = []
        // Forcer la réactivité en créant un nouveau tableau
        chatState.messages = [...chatState.messages, {
          type: 'user',
          text: message
        }]
      }
      
      chatState.newMessage = ''
      chatState.isLoading = true
      
      try {
        console.log('📤 Préparation de la requête...')
        
        const requestData = {
          message: message,
          user_id: authStore.currentUser?.id || 'anonymous'
        }
        
        console.log('📝 Données à envoyer:', requestData)
        
        // Utiliser fetch directement comme dans le test HTML qui fonctionne
        const response = await fetch('http://localhost:8000/api/ia/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        })
        
        console.log('📊 Status reçu:', response.status)
        console.log('📊 OK:', response.ok)
        
        const data = await response.json()
        console.log('📄 Données reçues:', data)
        
        if (response.ok) {
          console.log('✅ Réponse OK, ajout du message IA')
          console.log('📄 Données complètes reçues:', JSON.stringify(data, null, 2))
          
          // Vérifier à nouveau que chatMessages est un tableau
          if (!Array.isArray(chatState.messages)) {
            console.log('⚠️ chatMessages n\'est plus un tableau, réinitialisation...')
            chatState.messages = []
          }
          
          // Ajouter la réponse de l'IA de manière sûre
          const aiMessage = {
            type: 'ai',
            text: data.response || 'Réponse de l\'IA',
            suggestions: data.suggestions || [],
            task_suggestions: data.task_suggestions || []
          }
          
          console.log('🤖 Ajout de la réponse IA:', aiMessage)
          // Forcer la réactivité en créant un nouveau tableau
          chatState.messages = [...chatState.messages, aiMessage]
          console.log('✅ Réponse IA ajoutée, longueur:', chatState.messages.length)
          console.log(' État final de chatMessages:', JSON.stringify(chatState.messages, null, 2))
        } else {
          throw new Error(`Erreur ${response.status}: ${data.detail || 'Erreur inconnue'}`)
        }
        
      } catch (error) {
        console.error('❌ Erreur chat IA:', error)
        
        // Forcer la réactivité en créant un nouveau tableau
        chatState.messages = [...chatState.messages, {
          type: 'ai',
          text: `Désolé, j'ai rencontré une erreur: ${error.message}. Pouvez-vous réessayer ?`,
          suggestions: ["Réessayer", "Contacter le support"]
        }]
      } finally {
        chatState.isLoading = false
        console.log('🏁 Fin sendMessage')
        // Scroll vers le bas
        await nextTick()
        setTimeout(() => {
          const chatContainer = document.querySelector('.chat-messages')
          if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight
          }
        }, 100)
      }
    }
    
    const createTaskFromSuggestion = async (taskSuggestion) => {
      try {
        const response = await axios.post('/api/tasks/', {
          title: taskSuggestion.title,
          description: taskSuggestion.description,
          category: taskSuggestion.category,
          priority: taskSuggestion.priority
        })
        
        // Ajouter un message de confirmation
        // Forcer la réactivité en créant un nouveau tableau
        chatState.messages = [...chatState.messages, {
          type: 'ai',
          text: `✅ Tâche "${taskSuggestion.title}" créée avec succès !`,
          suggestions: ["Créer une autre tâche", "Voir mes tâches", "Merci !"]
        }]
        
      } catch (error) {
        console.error('Erreur création tâche:', error)
        // Forcer la réactivité en créant un nouveau tableau
        chatState.messages = [...chatState.messages, {
          type: 'ai',
          text: "❌ Erreur lors de la création de la tâche. Pouvez-vous réessayer ?",
          suggestions: ["Réessayer", "Créer manuellement"]
        }]
      }
    }
    
    const showPersonnelFeature = () => {
      alert('Fonctionnalité "Personnels aidants" en cours de développement. Bientôt disponible !')
    }
    
    const testAPI = async () => {
      try {
        console.log('🧪 Test de l\'API IA...')
        const response = await axios.get('/api/ia/health')
        console.log('✅ Test API réussi:', response.data)
        alert(`API fonctionne ! Status: ${response.data.status}`)
      } catch (error) {
        console.error('❌ Test API échoué:', error)
        alert(`Erreur API: ${error.response?.status || 'Connexion impossible'}`)
      }
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      authStore,
      stats,
      openAIChat,
      showPersonnelFeature,
      testAPI,
      showChatModal,
      chatState,
      sendMessage,
      closeChatModal,
      createTaskFromSuggestion
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
  color: white;
}

.welcome-section h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.welcome-section p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.stat-card h3 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-card p {
  color: #666;
  font-size: 1rem;
  font-weight: 500;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #667eea;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
  margin: 0.25rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border: 2px solid #667eea;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
  margin: 0.25rem;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

/* Chat Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
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
  margin-bottom: 1rem;
}

.message.user {
  justify-content: flex-end;
}

.message.ai {
  justify-content: flex-start;
}

.message-content {
  max-width: 80%;
  padding: 1rem;
  border-radius: 15px;
  position: relative;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 5px;
}

.message.ai .message-content {
  background: #f8f9fa;
  color: #333;
  border-bottom-left-radius: 5px;
  border: 1px solid #e9ecef;
}

.message-text p {
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
  white-space: pre-wrap;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.suggestion-btn {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border: 1px solid #667eea;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.suggestion-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.task-suggestions {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.task-suggestions h4 {
  margin: 0 0 0.5rem 0;
  color: #667eea;
  font-size: 1rem;
}

.task-suggestion {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 10px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-suggestion span {
  flex: 1;
  margin-right: 10px;
  font-weight: 600;
  color: #333;
}

.create-task-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 15px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-task-btn:hover {
  background: #218838;
  transform: translateY(-1px);
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.chat-input input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e9ecef;
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.chat-input input:focus {
  border-color: #667eea;
}

.chat-input button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-input button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.chat-input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.test-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.test-btn:hover {
  background: #c82333;
  transform: translateY(-2px);
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

.loading-indicator {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 10;
}

.loading-dots {
  display: flex;
  gap: 0.3rem;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #667eea;
  animation: bounce 1.4s ease-in-out infinite both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .quick-actions {
    grid-template-columns: 1fr;
  }
  
  .chat-modal {
    width: 95%;
    height: 90vh;
  }
  
  .message-content {
    max-width: 90%;
  }
}
</style> 