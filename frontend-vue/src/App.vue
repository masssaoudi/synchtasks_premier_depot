<template>
  <div id="app">
    <!-- Barre de navigation globale -->
    <NavigationBar />
    
    <!-- Contenu principal avec padding pour la barre de navigation -->
    <main :class="['main-content', { 'with-nav': showNav }]">
      <router-view />
    </main>
    
    <!-- Système de notifications temps réel -->
    <Toast />
  </div>
</template>

<script>
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { useTasksStore } from './stores/tasks'
import NavigationBar from './components/NavigationBar.vue'
import Toast from './components/Toast.vue'

export default {
  name: 'App',
  components: {
    NavigationBar,
    Toast
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const tasksStore = useTasksStore()
    
    const showNav = computed(() => {
      return route.path !== '/login'
    })
    
    let cleanupWebSocket = null
    
    // Vérifier l'authentification au chargement
    onMounted(async () => {
      await authStore.initAuth()
      
      // Si pas authentifié et pas sur la page de login ou d'accueil, rediriger vers login
      if (!authStore.isAuthenticated && route.path !== '/login' && route.path !== '/') {
        router.push('/login')
      }
      
      // Initialiser WebSocket si authentifié
      if (authStore.isAuthenticated && authStore.currentUser) {
        const userId = authStore.currentUser._id || authStore.currentUser.id
        console.log('🔌 Initialisation WebSocket pour:', userId)
        cleanupWebSocket = tasksStore.initWebSocket(userId)
      }
    })
    
    // Nettoyer WebSocket à la déconnexion
    onUnmounted(() => {
      if (cleanupWebSocket) {
        cleanupWebSocket()
      }
    })
    
    return {
      showNav
    }
  }
}
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
}



.main-content {
  padding: 2rem;
  min-height: calc(100vh - 80px);
}

/* Ajouter le padding-top seulement quand la navigation est visible */
.main-content.with-nav {
  padding-top: 5rem;
}
</style> 