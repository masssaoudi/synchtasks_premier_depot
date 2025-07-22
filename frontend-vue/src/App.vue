<template>
  <div id="app">
    <!-- Barre de navigation globale -->
    <NavigationBar />
    
    <!-- Contenu principal avec padding pour la barre de navigation -->
    <main :class="['main-content', { 'with-nav': showNav }]">
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import NavigationBar from './components/NavigationBar.vue'

export default {
  name: 'App',
  components: {
    NavigationBar
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const showNav = computed(() => {
      return route.path !== '/login'
    })
    
    // Vérifier l'authentification au chargement
    onMounted(async () => {
      await authStore.initAuth()
      
      // Si pas authentifié et pas sur la page de login, rediriger vers login
      if (!authStore.isAuthenticated && route.path !== '/login') {
        router.push('/login')
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