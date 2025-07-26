<template>
  <nav v-if="showNavigation" class="navigation-bar">
    <div class="nav-container">
      <!-- Logo et titre -->
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">🤖</span>
          <span class="brand-text">SyncTasks</span>
        </router-link>
      </div>

      <!-- Boutons de navigation -->
      <div class="nav-buttons">
        <button @click="goBack" class="nav-btn nav-btn-secondary" :disabled="!canGoBack">
          <span class="btn-icon">←</span>
          <span class="btn-text">Précédent</span>
        </button>
        
        <button @click="goHome" class="nav-btn nav-btn-primary">
          <span class="btn-icon">📊</span>
          <span class="btn-text">Tableau de bord</span>
        </button>
      </div>

      <!-- Menu utilisateur -->
      <div class="nav-user" v-if="authStore.isAuthenticated">
        <div class="user-info">
          <span class="user-name">{{ authStore.currentUser?.username }}</span>
          <span class="ws-badge" :class="{ connected: websocketConnected, disconnected: !websocketConnected }">
            <span class="ws-dot"></span>
            <span class="ws-text">WebSocket {{ websocketConnected ? 'actif' : 'déconnecté' }}</span>
          </span>
        </div>
        <button @click="logout" class="nav-btn nav-btn-logout">
          <span class="btn-icon">🚪</span>
          <span class="btn-text">Déconnexion</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useTasksStore } from '../stores/tasks'

export default {
  name: 'NavigationBar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const tasksStore = useTasksStore()

    const showNavigation = computed(() => {
      // Ne pas afficher sur la page de login
      return router.currentRoute.value.path !== '/login'
    })

    const canGoBack = computed(() => {
      return window.history.length > 1
    })

    const goBack = () => {
      if (canGoBack.value) {
        router.go(-1)
      }
    }

    const goHome = () => {
      if (authStore.isAuthenticated) {
        router.push('/welcome')
      } else {
        router.push('/')
      }
    }

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const goPersonneAidant = () => {
      router.push('/personne-aidant')
    }

    // Badge WebSocket actif
    const websocketConnected = computed(() => tasksStore.websocketConnected)

    return {
      authStore,
      showNavigation,
      canGoBack,
      goBack,
      goHome,
      logout,
      websocketConnected,
      goPersonneAidant
    }
  }
}
</script>

<style scoped>
.navigation-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 0.5rem 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
}

.brand-icon {
  font-size: 1.5rem;
  margin-right: 0.5rem;
}

.brand-text {
  font-size: 1.3rem;
}

.nav-buttons {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  font-size: 0.9rem;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.nav-btn-primary {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-btn-primary:hover {
  background: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-btn-logout {
  background: rgba(220, 53, 69, 0.9);
  color: white;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.nav-btn-logout:hover {
  background: #dc3545;
  transform: translateY(-1px);
}

.btn-icon {
  font-size: 1rem;
}

.btn-text {
  font-weight: 500;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.user-info {
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-name {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.ws-badge {
  display: flex;
  align-items: center;
  gap: 0.4em;
  margin-left: 0.7em;
  padding: 0.18em 0.7em 0.18em 0.4em;
  border-radius: 16px;
  font-size: 0.85em;
  font-weight: 600;
  background: rgba(255,255,255,0.18);
  color: #fff;
  border: 1.5px solid #bbb;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  transition: background 0.2s, color 0.2s, border 0.2s;
}
.ws-badge.connected {
  background: rgba(76, 175, 80, 0.18);
  color: #4CAF50;
  border-color: #4CAF50;
}
.ws-badge.disconnected {
  background: rgba(180, 180, 180, 0.18);
  color: #aaa;
  border-color: #aaa;
}
.ws-dot {
  width: 0.7em;
  height: 0.7em;
  border-radius: 50%;
  background: #aaa;
  display: inline-block;
  margin-right: 0.3em;
  box-shadow: 0 0 4px #fff2;
  transition: background 0.2s;
}
.ws-badge.connected .ws-dot {
  background: #4CAF50;
}
.ws-badge.disconnected .ws-dot {
  background: #aaa;
}
.ws-text {
  font-size: 0.95em;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 0.5rem;
  }
  
  .btn-text {
    display: none;
  }
  
  .nav-btn {
    padding: 0.5rem;
  }
  
  .user-name {
    display: none;
  }
  
  .nav-buttons {
    gap: 0.25rem;
  }
  .ws-badge {
    font-size: 0.7em;
    padding: 0.12em 0.5em 0.12em 0.3em;
  }
}

@media (max-width: 480px) {
  .brand-text {
    display: none;
  }
  
  .nav-container {
    justify-content: space-between;
  }
  
  .nav-buttons {
    flex: 0;
  }
}
</style> 