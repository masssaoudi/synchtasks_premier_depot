import { defineStore } from 'pinia';
import { ref, watch } from 'vue';

export const usePreferencesStore = defineStore('preferences', () => {
  // Préférences utilisateur
  const preferences = ref({
    // Notifications
    notifications: {
      enabled: true,
      sound: true,
      desktop: true,
    },

    // Interface
    interface: {
      compactMode: false,
      showAnimations: true,
      autoSave: true,
    },

    // Performance
    performance: {
      lazyLoading: true,
      preloadImages: false,
      cacheData: true,
    },

    // Accessibilité
    accessibility: {
      highContrast: false,
      largeText: false,
      reducedMotion: false,
    },
  });

  // Initialiser les préférences depuis localStorage
  const initPreferences = () => {
    const saved = localStorage.getItem('user-preferences');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        preferences.value = { ...preferences.value, ...parsed };
      } catch (error) {
        console.warn('Erreur lors du chargement des préférences:', error);
      }
    }
  };

  // Sauvegarder les préférences
  const savePreferences = () => {
    try {
      localStorage.setItem(
        'user-preferences',
        JSON.stringify(preferences.value)
      );
    } catch (error) {
      console.warn('Erreur lors de la sauvegarde des préférences:', error);
    }
  };

  // Mettre à jour une préférence spécifique
  const updatePreference = (category, key, value) => {
    if (preferences.value[category]) {
      preferences.value[category][key] = value;

      // Notification toast
      if (window.$toast) {
        const categoryNames = {
          notifications: 'Notifications',
          interface: 'Interface',
          performance: 'Performance',
          accessibility: 'Accessibilité',
        };
        const keyNames = {
          enabled: 'activées',
          sound: 'son activé',
          desktop: 'notifications bureau',
          compactMode: 'mode compact',
          showAnimations: 'animations',
          autoSave: 'sauvegarde automatique',
          lazyLoading: 'chargement différé',
          preloadImages: 'préchargement images',
          cacheData: 'mise en cache',
          highContrast: 'contraste élevé',
          largeText: 'texte agrandi',
          reducedMotion: 'mouvements réduits',
        };

        const message = `${categoryNames[category]}: ${keyNames[key] || key} ${value ? 'activé' : 'désactivé'}`;
        window.$toast.info('Préférence', message, 2000);
      }
    }
  };

  // Réinitialiser toutes les préférences
  const resetPreferences = () => {
    preferences.value = {
      notifications: {
        enabled: true,
        sound: true,
        desktop: true,
      },
      interface: {
        compactMode: false,
        showAnimations: true,
        autoSave: true,
      },
      performance: {
        lazyLoading: true,
        preloadImages: false,
        cacheData: true,
      },
      accessibility: {
        highContrast: false,
        largeText: false,
        reducedMotion: false,
      },
    };

    if (window.$toast) {
      window.$toast.success('Préférences', 'Préférences réinitialisées', 2000);
    }
  };

  // Obtenir une préférence
  const getPreference = (category, key) => {
    return preferences.value[category]?.[key] ?? null;
  };

  // Appliquer les préférences d'accessibilité
  const applyAccessibilityPreferences = () => {
    const html = document.documentElement;

    // Contraste élevé
    if (preferences.value.accessibility.highContrast) {
      html.classList.add('high-contrast');
    } else {
      html.classList.remove('high-contrast');
    }

    // Texte agrandi
    if (preferences.value.accessibility.largeText) {
      html.classList.add('large-text');
    } else {
      html.classList.remove('large-text');
    }

    // Mouvements réduits
    if (preferences.value.accessibility.reducedMotion) {
      html.classList.add('reduced-motion');
    } else {
      html.classList.remove('reduced-motion');
    }
  };

  // Surveiller les changements pour sauvegarder automatiquement
  watch(
    preferences,
    () => {
      savePreferences();
      applyAccessibilityPreferences();
    },
    { deep: true }
  );

  return {
    preferences,
    initPreferences,
    savePreferences,
    updatePreference,
    resetPreferences,
    getPreference,
    applyAccessibilityPreferences,
  };
});
