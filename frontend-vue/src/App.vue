<template>
  <div id="app">
    <!-- 🎯 BARRE DE NAVIGATION CONDITIONNELLE -->
    <NavigationBar v-if="showNav" />

    <!-- 🎯 CONTENU PRINCIPAL -->
    <main :class="['main-content', { 'with-nav': showNav }]">
      <!-- 🎯 LOADING GLOBAL -->
      <div v-if="isLoading" class="global-loading">
        <div class="loading-spinner"></div>
        <p>Chargement...</p>
      </div>
      
      <!-- 🎯 ROUTER VIEW -->
      <router-view v-else />
    </main>

    <!-- 🎯 SYSTÈME DE NOTIFICATIONS -->
    <Toast />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NavigationBar from './components/NavigationBar.vue';
import Toast from './components/Toast.vue';
import { useAuthStore } from './stores/auth';
import { usePerformanceStore } from './stores/performance';
import { usePreferencesStore } from './stores/preferences';
import { useShortcutsStore } from './stores/shortcuts';
import { useTasksStore } from './stores/tasks';
import { useThemeStore } from './stores/theme';

// 🎯 STORES ET ROUTER
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const tasksStore = useTasksStore();
const themeStore = useThemeStore();
const preferencesStore = usePreferencesStore();
const shortcutsStore = useShortcutsStore();
const performanceStore = usePerformanceStore();

// 🎯 ÉTAT RÉACTIF
const isLoading = ref(true);

// 🎯 COMPUTED PROPERTIES
const showNav = computed(() => {
  // Ne pas afficher la nav sur les pages d'auth
  const authPages = ['/login', '/register', '/auth/google/callback'];
  return !authPages.includes(route.path);
});

// 🎯 INITIALISATION DE L'APPLICATION
const initializeApp = async () => {
  try {
    console.log('🚀 Initialisation de SyncTasks...');
    
    // 🎯 INITIALISATION DES STORES
    await Promise.all([
      themeStore.initTheme(),
      preferencesStore.initPreferences(),
      performanceStore.initPerformance(),
      authStore.initAuth()
    ]);

    // 🎯 INITIALISATION DES TÂCHES SI CONNECTÉ
    if (authStore.isAuthenticated && authStore.currentUser) {
      const userId = authStore.currentUser._id || authStore.currentUser.id;
      await tasksStore.fetchTasks();
      tasksStore.initWebSocket(userId);
    }

    // 🎯 CONFIGURATION DES RACCOURCIS
    shortcutsStore.setupShortcuts();

    console.log('✅ Application initialisée avec succès');
  } catch (error) {
    console.error('❌ Erreur lors de l\'initialisation:', error);
  } finally {
    isLoading.value = false;
  }
};

// 🎯 GESTION DE LA DÉCONNEXION
const handleLogout = () => {
  // Nettoyer les WebSockets et les stores
  tasksStore.cleanupWebSocket();
  shortcutsStore.cleanupShortcuts();
  performanceStore.cleanupPerformance();
};

// 🎯 WATCHERS POUR LA BALADE UTILISATEUR
const setupWatchers = () => {
  // Surveiller les changements d'authentification
  watch(() => authStore.isAuthenticated, (isAuth) => {
    if (isAuth) {
      // Utilisateur connecté - initialiser les tâches
      const user = authStore.currentUser;
      if (user) {
        const userId = user._id || user.id;
        tasksStore.fetchTasks();
        tasksStore.initWebSocket(userId);
      }
    } else {
      // Utilisateur déconnecté - nettoyer
      handleLogout();
    }
  });

  // Surveiller les changements de route
  watch(() => route.path, (newPath) => {
    console.log('🔄 Navigation vers:', newPath);
    
    // Mettre à jour les métriques de performance
    performanceStore.trackPageView(newPath);
  });
};

// 🎯 LIFECYCLE HOOKS
onMounted(async () => {
  console.log('🎯 Montage de l\'application');
  
  // Initialiser l'application
  await initializeApp();
  
  // Configurer les watchers
  setupWatchers();
  
  // Vérifier la redirection initiale
  await checkInitialRedirect();
});

onUnmounted(() => {
  console.log('🎯 Démonatge de l\'application');
  
  // Nettoyer les ressources
  handleLogout();
});

// 🎯 VÉRIFICATION DE LA REDIRECTION INITIALE
const checkInitialRedirect = async () => {
  const user = authStore.currentUser;
  
  if (authStore.isAuthenticated && user) {
    // Utilisateur connecté - vérifier le segment
    if (user.segment) {
      // Rediriger vers le bon dashboard
      const dashboardRoute = getDashboardRoute(user.segment);
      if (route.path !== dashboardRoute) {
        router.push(dashboardRoute);
      }
    } else if (route.path !== '/segment-selection') {
      // Pas de segment - rediriger vers la sélection
      router.push('/segment-selection');
    }
  } else if (route.path === '/') {
    // Utilisateur non connecté sur la page d'accueil
    router.push('/login');
  }
};

// 🎯 FONCTION UTILITAIRE POUR DÉTERMINER LE DASHBOARD
const getDashboardRoute = (segment) => {
  const routes = {
    'particuliers': '/dashboard/particuliers',
    'professionnels': '/dashboard/professionnels',
    'etudiants': '/dashboard/etudiants',
    'entreprises': '/dashboard/entreprises',
    'medical': '/dashboard/medical',
    'memoire': '/dashboard/memoire'
  };
  return routes[segment] || '/segment-selection';
};
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.main-content {
  padding: 2rem;
  transition: padding 0.3s ease;
}

.main-content.with-nav {
  padding-top: 80px; /* Espace pour la barre de navigation */
}

/* 🎯 LOADING GLOBAL */
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.global-loading .loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.global-loading p {
  color: #667eea;
  font-size: 1.1rem;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 🎯 RESPONSIVE */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .main-content.with-nav {
    padding-top: 60px;
  }
}

/* 🎯 ANIMATIONS DE TRANSITION */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 🎯 OPTIMISATIONS DE PERFORMANCE */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}

/* 🎯 ACCESSIBILITÉ */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
