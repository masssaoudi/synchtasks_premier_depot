<template>
  <div class="welcome-container">
    <div class="welcome-card">
      <h1>Bienvenue sur SyncTasks</h1>
      <p>Que souhaitez-vous faire aujourd'hui ?</p>
      
      <div class="action-buttons">
        <button @click="goToTasks" class="action-btn tasks-btn">
          <div class="btn-icon">📋</div>
          <div class="btn-content">
            <h3>Mes Tâches</h3>
            <p>Gérer et organiser vos tâches</p>
          </div>
        </button>
        
        <button @click="goToPersonneAidant" class="action-btn aidant-btn">
          <div class="btn-icon">👥</div>
          <div class="btn-content">
            <h3>Personne Aidant</h3>
            <p>Gérer vos délégations et collaborateurs</p>
          </div>
        </button>
        
        <button @click="goToIA" class="action-btn ia-btn">
          <div class="btn-icon">🤖</div>
          <div class="btn-content">
            <h3>Parler à l'IA</h3>
            <p>Obtenir des conseils et de l'aide</p>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useTasksStore } from '../stores/tasks'

const router = useRouter()
const authStore = useAuthStore()
const tasksStore = useTasksStore()

const goToTasks = () => {
  router.push('/tasks')
}

const goToPersonneAidant = () => {
  router.push('/personne-aidant')
}

const goToIA = () => {
  // Pour l'instant, on peut rediriger vers une page IA ou ouvrir un modal
  alert('Fonctionnalité IA en cours de développement !')
}

// Initialiser WebSocket si pas déjà fait
onMounted(() => {
  if (authStore.isAuthenticated && authStore.currentUser) {
    const userId = authStore.currentUser._id || authStore.currentUser.id
    console.log('🔌 Vérification WebSocket sur WelcomeView pour:', userId)
    
    // Vérifier si le WebSocket est déjà connecté
    if (!tasksStore.websocketConnected) {
      console.log('🔌 Réinitialisation WebSocket...')
      tasksStore.initWebSocket(userId)
    }
  }
})
</script>

<style scoped>
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
}

.welcome-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08);
  padding: 3rem 2.5rem;
  text-align: center;
  max-width: 800px;
  width: 100%;
}

.welcome-card h1 {
  color: #667eea;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.welcome-card p {
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 3rem;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.action-btn {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 16px;
  padding: 2rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #667eea;
}

.tasks-btn:hover {
  border-color: #28a745;
  background: linear-gradient(135deg, #f8fff9, #e8f5e8);
}

.aidant-btn:hover {
  border-color: #007bff;
  background: linear-gradient(135deg, #f8fbff, #e8f4ff);
}

.ia-btn:hover {
  border-color: #6f42c1;
  background: linear-gradient(135deg, #faf8ff, #f0e8ff);
}

.btn-icon {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
}

.tasks-btn .btn-icon {
  background: #e8f5e8;
  color: #28a745;
}

.aidant-btn .btn-icon {
  background: #e8f4ff;
  color: #007bff;
}

.ia-btn .btn-icon {
  background: #f0e8ff;
  color: #6f42c1;
}

.btn-content {
  flex: 1;
}

.btn-content h3 {
  color: #333;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.btn-content p {
  color: #666;
  font-size: 0.95rem;
  margin: 0;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .welcome-card {
    padding: 2rem 1.5rem;
  }
  
  .welcome-card h1 {
    font-size: 2rem;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .action-btn {
    padding: 1.5rem 1rem;
  }
  
  .btn-icon {
    font-size: 2rem;
    width: 50px;
    height: 50px;
  }
}
</style> 