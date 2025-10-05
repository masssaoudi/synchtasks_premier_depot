import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const usePerformanceStore = defineStore('performance', () => {
  // État des optimisations
  const isLowPowerMode = ref(false);
  const isReducedMotion = ref(false);
  const isCompactMode = ref(false);
  const isLazyLoading = ref(true);
  const isCachingEnabled = ref(true);

  // Métriques de performance
  const performanceMetrics = ref({
    loadTime: 0,
    memoryUsage: 0,
    cpuUsage: 0,
    networkLatency: 0,
  });

  // Préférences de performance
  const performancePreferences = ref({
    autoOptimize: true,
    aggressiveOptimization: false,
    monitorPerformance: true,
    adaptiveLoading: true,
  });

  // Initialiser les optimisations de performance
  const initPerformance = () => {
    // Charger les préférences depuis localStorage
    const savedPreferences = localStorage.getItem('performance-preferences');
    if (savedPreferences) {
      performancePreferences.value = {
        ...performancePreferences.value,
        ...JSON.parse(savedPreferences),
      };
    }

    // Détecter automatiquement les capacités de l'appareil
    detectDeviceCapabilities();

    // Appliquer les optimisations automatiques si activées
    if (performancePreferences.value.autoOptimize) {
      autoOptimize();
    }

    // Démarrer le monitoring si activé
    if (performancePreferences.value.monitorPerformance) {
      startPerformanceMonitoring();
    }
  };

  // Détecter les capacités de l'appareil
  const detectDeviceCapabilities = () => {
    // Détecter si l'appareil est en mode économie d'énergie
    if ('getBattery' in navigator) {
      navigator.getBattery().then(battery => {
        isLowPowerMode.value =
          battery.level < 0.2 || battery.charging === false;
      });
    }

    // Détecter les préférences de réduction de mouvement
    const prefersReducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches;
    isReducedMotion.value = prefersReducedMotion;

    // Détecter la taille de l'écran pour le mode compact
    const isSmallScreen = window.innerWidth < 768;
    isCompactMode.value = isSmallScreen;
  };

  // Optimisations automatiques
  const autoOptimize = () => {
    console.log('⚡ Application des optimisations automatiques...');

    // Optimisations basées sur les capacités de l'appareil
    if (isLowPowerMode.value) {
      enableLowPowerMode();
    }

    if (isReducedMotion.value) {
      enableReducedMotion();
    }

    if (isCompactMode.value) {
      enableCompactMode();
    }

    // Optimisations générales
    if (isLazyLoading.value) {
      enableLazyLoading();
    }

    if (isCachingEnabled.value) {
      enableCaching();
    }
  };

  // Mode économie d'énergie
  const enableLowPowerMode = () => {
    console.log("🔋 Activation du mode économie d'énergie");

    // Réduire les animations
    document.documentElement.style.setProperty('--animation-duration', '0.1s');

    // Désactiver les effets visuels lourds
    document.documentElement.style.setProperty('--blur-effect', 'none');
    document.documentElement.style.setProperty('--shadow-effect', 'none');

    // Réduire la fréquence de rafraîchissement
    if ('requestIdleCallback' in window) {
      // Utiliser requestIdleCallback pour les tâches non critiques
    }
  };

  // Mode réduction de mouvement
  const enableReducedMotion = () => {
    console.log('🎭 Activation de la réduction de mouvement');

    // Désactiver les animations
    document.documentElement.style.setProperty('--animation-duration', '0s');
    document.documentElement.style.setProperty('--transition-duration', '0s');

    // Appliquer les styles CSS pour la réduction de mouvement
    const style = document.createElement('style');
    style.textContent = `
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }
    `;
    document.head.appendChild(style);
  };

  // Mode compact
  const enableCompactMode = () => {
    console.log('📱 Activation du mode compact');

    // Réduire les espacements
    document.documentElement.style.setProperty('--spacing-unit', '0.5rem');
    document.documentElement.style.setProperty('--border-radius', '4px');

    // Réduire la taille des polices
    document.documentElement.style.setProperty('--font-size-base', '14px');
  };

  // Chargement différé
  const enableLazyLoading = () => {
    console.log('🔄 Activation du chargement différé');

    // Observer les images pour le lazy loading
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            observer.unobserve(img);
          }
        });
      });

      // Observer toutes les images avec la classe 'lazy'
      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    }
  };

  // Mise en cache
  const enableCaching = () => {
    console.log('💾 Activation de la mise en cache');

    // Utiliser le cache du navigateur pour les ressources statiques
    if ('serviceWorker' in navigator) {
      // Enregistrer un service worker pour la mise en cache
      // (à implémenter selon les besoins)
    }
  };

  // Monitoring des performances
  const startPerformanceMonitoring = () => {
    console.log('📊 Démarrage du monitoring des performances');

    // Mesurer le temps de chargement
    window.addEventListener('load', () => {
      const loadTime = performance.now();
      performanceMetrics.value.loadTime = loadTime;
      console.log(`⚡ Temps de chargement: ${loadTime.toFixed(2)}ms`);
    });

    // Mesurer l'utilisation mémoire (si disponible)
    if ('memory' in performance) {
      setInterval(() => {
        performanceMetrics.value.memoryUsage =
          performance.memory.usedJSHeapSize;
        performanceMetrics.value.cpuUsage = performance.memory.totalJSHeapSize;
      }, 5000);
    }

    // Mesurer la latence réseau
    if ('connection' in navigator) {
      const connection = navigator.connection;
      performanceMetrics.value.networkLatency = connection.rtt || 0;
    }
  };

  // Mettre à jour les préférences
  const updatePerformancePreference = (key, value) => {
    performancePreferences.value[key] = value;
    localStorage.setItem(
      'performance-preferences',
      JSON.stringify(performancePreferences.value)
    );
  };

  // Obtenir les métriques de performance
  const getPerformanceMetrics = computed(() => {
    return {
      ...performanceMetrics.value,
      isOptimized:
        isLowPowerMode.value || isReducedMotion.value || isCompactMode.value,
      optimizationLevel: [
        isLowPowerMode.value,
        isReducedMotion.value,
        isCompactMode.value,
        isLazyLoading.value,
        isCachingEnabled.value,
      ].filter(Boolean).length,
    };
  });

  return {
    // État
    isLowPowerMode,
    isReducedMotion,
    isCompactMode,
    isLazyLoading,
    isCachingEnabled,
    performanceMetrics,
    performancePreferences,

    // Getters
    getPerformanceMetrics,

    // Actions
    initPerformance,
    autoOptimize,
    enableLowPowerMode,
    enableReducedMotion,
    enableCompactMode,
    enableLazyLoading,
    enableCaching,
    startPerformanceMonitoring,
    updatePerformancePreference,
  };
});
