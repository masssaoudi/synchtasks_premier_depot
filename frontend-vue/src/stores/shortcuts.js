import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useShortcutsStore = defineStore('shortcuts', () => {
  const isEnabled = ref(true);
  const shortcuts = ref(new Map());

  // Définir les raccourcis par défaut
  const defaultShortcuts = {
    'Ctrl+Shift+T': {
      action: 'toggleTheme',
      description: 'Basculer le thème sombre/clair',
      category: 'Interface',
    },
    'Ctrl+Shift+N': {
      action: 'toggleNotifications',
      description: 'Activer/désactiver les notifications',
      category: 'Notifications',
    },
    'Ctrl+Shift+A': {
      action: 'toggleAccessibility',
      description: 'Activer le mode accessibilité',
      category: 'Accessibilité',
    },
    'Ctrl+Shift+H': {
      action: 'goHome',
      description: "Aller à l'accueil",
      category: 'Navigation',
    },
    Escape: {
      action: 'closeModals',
      description: 'Fermer les modales',
      category: 'Navigation',
    },
  };

  // Initialiser les raccourcis
  const initShortcuts = () => {
    shortcuts.value.clear();

    // Charger les raccourcis depuis localStorage
    const savedShortcuts = localStorage.getItem('shortcuts');
    const shortcutsToUse = savedShortcuts
      ? JSON.parse(savedShortcuts)
      : defaultShortcuts;

    Object.entries(shortcutsToUse).forEach(([key, config]) => {
      shortcuts.value.set(key, config);
    });
  };

  // Gérer les événements clavier
  const handleKeydown = event => {
    if (!isEnabled.value) {
      return;
    }

    const key = getKeyCombo(event);
    const shortcut = shortcuts.value.get(key);

    if (shortcut) {
      event.preventDefault();
      executeShortcut(shortcut.action);
    }
  };

  // Obtenir la combinaison de touches
  const getKeyCombo = event => {
    const parts = [];

    if (event.ctrlKey) {
      parts.push('Ctrl');
    }
    if (event.shiftKey) {
      parts.push('Shift');
    }
    if (event.altKey) {
      parts.push('Alt');
    }
    if (event.metaKey) {
      parts.push('Meta');
    }
    if (
      event.key !== 'Control' &&
      event.key !== 'Shift' &&
      event.key !== 'Alt' &&
      event.key !== 'Meta'
    ) {
      parts.push(event.key.toUpperCase());
    }

    return parts.join('+');
  };

  // Exécuter une action de raccourci
  const executeShortcut = action => {
    console.log('⌨️ Raccourci exécuté:', action);

    switch (action) {
      case 'toggleTheme':
        // Importer et utiliser le store theme
        import('../stores/theme').then(({ useThemeStore }) => {
          const themeStore = useThemeStore();
          themeStore.toggleTheme();
        });
        break;

      case 'toggleNotifications':
        // Importer et utiliser le store preferences
        import('../stores/preferences').then(({ usePreferencesStore }) => {
          const preferencesStore = usePreferencesStore();
          const currentNotifications =
            preferencesStore.preferences.value.notifications.enabled;
          preferencesStore.updatePreference(
            'notifications',
            'enabled',
            !currentNotifications
          );
        });
        break;

      case 'toggleAccessibility':
        // Importer et utiliser le store preferences
        import('../stores/preferences').then(({ usePreferencesStore }) => {
          const preferencesStore = usePreferencesStore();
          const currentAccessibility =
            preferencesStore.preferences.value.accessibility.highContrast;
          preferencesStore.updatePreference(
            'accessibility',
            'highContrast',
            !currentAccessibility
          );
        });
        break;

      case 'goHome':
        // Navigation vers l'accueil
        import('vue-router').then(({ useRouter }) => {
          const router = useRouter();
          router.push('/welcome');
        });
        break;

      case 'closeModals': {
        // Fermer les modales ouvertes
        const modals = document.querySelectorAll('.modal, .toast');
        modals.forEach(modal => {
          if (modal.style.display !== 'none') {
            modal.style.display = 'none';
          }
        });
        break;
      }

      default:
        console.log('Action de raccourci non reconnue:', action);
    }
  };

  // Activer/désactiver les raccourcis
  const toggleShortcuts = () => {
    isEnabled.value = !isEnabled.value;
    localStorage.setItem('shortcuts-enabled', JSON.stringify(isEnabled.value));

    if (window.$toast) {
      const message = isEnabled.value
        ? 'Raccourcis activés'
        : 'Raccourcis désactivés';
      window.$toast.info('Raccourcis', message, 2000);
    }
  };

  // Configurer les raccourcis
  const setupShortcuts = () => {
    // Charger l'état depuis localStorage
    const savedEnabled = localStorage.getItem('shortcuts-enabled');
    if (savedEnabled !== null) {
      isEnabled.value = JSON.parse(savedEnabled);
    }

    initShortcuts();

    // Ajouter les event listeners
    document.addEventListener('keydown', handleKeydown);

    // Retourner la fonction de nettoyage
    return () => {
      document.removeEventListener('keydown', handleKeydown);
    };
  };

  return {
    isEnabled,
    shortcuts,
    initShortcuts,
    setupShortcuts,
    toggleShortcuts,
    executeShortcut,
  };
});
