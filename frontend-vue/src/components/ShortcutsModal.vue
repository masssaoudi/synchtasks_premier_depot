<template>
  <div v-if="isVisible" class="shortcuts-modal-overlay" @click="closeModal">
    <div class="shortcuts-modal" @click.stop>
      <div class="modal-header">
        <h2>⌨️ Raccourcis Clavier</h2>
        <button class="close-btn" @click="closeModal">×</button>
      </div>

      <div class="modal-content">
        <div class="shortcuts-section">
          <h3>Interface</h3>
          <div class="shortcut-item">
            <span class="shortcut-key">Ctrl+Shift+T</span>
            <span class="shortcut-description"
              >Basculer le thème sombre/clair</span
            >
          </div>
        </div>

        <div class="shortcuts-section">
          <h3>Notifications</h3>
          <div class="shortcut-item">
            <span class="shortcut-key">Ctrl+Shift+N</span>
            <span class="shortcut-description"
              >Activer/désactiver les notifications</span
            >
          </div>
        </div>

        <div class="shortcuts-section">
          <h3>Accessibilité</h3>
          <div class="shortcut-item">
            <span class="shortcut-key">Ctrl+Shift+A</span>
            <span class="shortcut-description"
              >Activer le mode accessibilité</span
            >
          </div>
        </div>

        <div class="shortcuts-section">
          <h3>Navigation</h3>
          <div class="shortcut-item">
            <span class="shortcut-key">Ctrl+Shift+H</span>
            <span class="shortcut-description">Aller à l'accueil</span>
          </div>
          <div class="shortcut-item">
            <span class="shortcut-key">Escape</span>
            <span class="shortcut-description">Fermer les modales</span>
          </div>
        </div>

        <div class="shortcuts-toggle">
          <label class="toggle-label">
            <input
              v-model="shortcutsEnabled"
              type="checkbox"
              @change="toggleShortcuts"
            />
            <span class="toggle-slider"></span>
            Raccourcis clavier activés
          </label>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-primary" @click="closeModal">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script>
  import { computed } from 'vue';
  import { useShortcutsStore } from '../stores/shortcuts';

  export default {
    name: 'ShortcutsModal',
    props: {
      isVisible: {
        type: Boolean,
        default: false,
      },
    },
    emits: ['close'],
    setup(props, { emit }) {
      const shortcutsStore = useShortcutsStore();

      const shortcutsEnabled = computed({
        get: () => shortcutsStore.isEnabled.value,
        set: value => {
          shortcutsStore.isEnabled.value = value;
        },
      });

      const closeModal = () => {
        emit('close');
      };

      const toggleShortcuts = () => {
        shortcutsStore.toggleShortcuts();
      };

      return {
        shortcutsEnabled,
        closeModal,
        toggleShortcuts,
      };
    },
  };
</script>

<style scoped>
  .shortcuts-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    backdrop-filter: blur(4px);
  }

  .shortcuts-modal {
    background: var(--bg-secondary);
    border-radius: 12px;
    box-shadow: 0 8px 32px var(--shadow-color);
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
    border: 1px solid var(--border-color);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border-color);
  }

  .modal-header h2 {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.5rem;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: var(--text-secondary);
    padding: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s ease;
  }

  .close-btn:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }

  .modal-content {
    padding: 1.5rem;
  }

  .shortcuts-section {
    margin-bottom: 2rem;
  }

  .shortcuts-section h3 {
    color: var(--text-primary);
    margin-bottom: 1rem;
    font-size: 1.1rem;
    border-bottom: 2px solid var(--accent-color);
    padding-bottom: 0.5rem;
  }

  .shortcut-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: var(--bg-tertiary);
    border-radius: 8px;
    border: 1px solid var(--border-color);
  }

  .shortcut-key {
    background: var(--accent-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    font-size: 0.9rem;
  }

  .shortcut-description {
    color: var(--text-secondary);
    font-size: 0.9rem;
  }

  .shortcuts-toggle {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
  }

  .toggle-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    color: var(--text-primary);
    font-weight: 500;
  }

  .toggle-label input {
    display: none;
  }

  .toggle-slider {
    position: relative;
    width: 50px;
    height: 24px;
    background: var(--bg-tertiary);
    border-radius: 12px;
    margin-right: 1rem;
    transition: all 0.3s ease;
    border: 2px solid var(--border-color);
  }

  .toggle-slider:before {
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    background: var(--text-secondary);
    border-radius: 50%;
    top: 1px;
    left: 1px;
    transition: all 0.3s ease;
  }

  .toggle-label input:checked + .toggle-slider {
    background: var(--accent-color);
    border-color: var(--accent-color);
  }

  .toggle-label input:checked + .toggle-slider:before {
    transform: translateX(26px);
    background: white;
  }

  .modal-footer {
    padding: 1.5rem;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: flex-end;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .shortcuts-modal {
      width: 95%;
      max-height: 90vh;
    }

    .shortcut-item {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .shortcut-key {
      align-self: flex-start;
    }
  }

  /* Animation d'entrée */
  .shortcuts-modal-overlay {
    animation: fadeIn 0.3s ease;
  }

  .shortcuts-modal {
    animation: slideIn 0.3s ease;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-20px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
</style>
