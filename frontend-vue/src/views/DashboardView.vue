<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>📊 Dashboard</h1>
      <p class="dashboard-subtitle">Vue d'ensemble de votre productivité</p>
    </div>

    <!-- Bouton Personnels aidants -->
    <div class="personnel-aidants-section">
      <div class="personnel-card">
        <div class="personnel-icon">👥</div>
        <div class="personnel-content">
          <h3>Personnels aidants</h3>
          <p>Gérez votre équipe et vos collaborateurs</p>
          <button @click="showPersonnelFeature" class="btn btn-primary personnel-btn">
            <span class="btn-icon">🔧</span>
            <span class="btn-text">Fonctionnalité en développement</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Activité récente -->
    <div class="recent-activity">
      <h3>🕒 Activité récente</h3>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon" :class="activity.type">
            {{ activity.icon }}
          </div>
          <div class="activity-content">
            <div class="activity-text">{{ activity.text }}</div>
            <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Objectifs et conseils -->
    <div class="insights-section">
      <div class="insight-card">
        <h3>💡 Conseils IA</h3>
        <div class="insight-content">
          <p>{{ currentInsight }}</p>
          <button @click="getNewInsight" class="btn btn-secondary">
            Nouveau conseil
          </button>
        </div>
      </div>

      <div class="insight-card">
        <h3>🎯 Objectifs de la semaine</h3>
        <div class="goals-list">
          <div v-for="goal in weeklyGoals" :key="goal.id" class="goal-item">
            <input 
              type="checkbox" 
              :checked="goal.completed"
              @change="toggleGoal(goal.id)"
            >
            <span :class="{ completed: goal.completed }">{{ goal.text }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'DashboardView',
  setup() {
    const showPersonnelFeature = () => {
      alert('Fonctionnalité "Personnels aidants" en cours de développement. Bientôt disponible !')
    }

    const recentActivities = ref([
      {
        id: 1,
        type: 'completed',
        icon: '✅',
        text: 'Tâche "Configurer le projet" terminée',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000) // 2h ago
      },
      {
        id: 2,
        type: 'created',
        icon: '📝',
        text: 'Nouvelle tâche "Tests unitaires" créée',
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000) // 4h ago
      },
      {
        id: 3,
        type: 'updated',
        icon: '🔄',
        text: 'Tâche "Interface utilisateur" mise à jour',
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000) // 6h ago
      },
      {
        id: 4,
        type: 'completed',
        icon: '✅',
        text: 'Tâche "Authentification" terminée',
        timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000) // 1j ago
      }
    ])

    const weeklyGoals = ref([
      { id: 1, text: 'Terminer 5 tâches importantes', completed: false },
      { id: 2, text: 'Réduire les tâches en retard de 50%', completed: true },
      { id: 3, text: 'Améliorer la productivité de 10%', completed: false },
      { id: 4, text: 'Organiser les priorités', completed: true }
    ])

    const currentInsight = ref('Concentrez-vous sur les tâches de haute priorité pour maximiser votre impact. Les tâches "Interface utilisateur" et "Tests unitaires" sont essentielles pour la suite du projet.')

    const insights = [
      'Planifiez vos tâches les plus difficiles le matin quand votre énergie est au maximum.',
      'Utilisez la technique Pomodoro (25min de travail + 5min de pause) pour rester concentré.',
      'Revoyez vos objectifs hebdomadaires chaque lundi pour vous assurer qu\'ils sont réalistes.',
      'Prenez des pauses régulières pour maintenir votre créativité et éviter l\'épuisement.',
      'Déléguez les tâches répétitives pour vous concentrer sur ce qui apporte le plus de valeur.'
    ]



    const formatTime = (timestamp) => {
      const now = new Date()
      const diff = now - timestamp
      const hours = Math.floor(diff / (1000 * 60 * 60))
      const days = Math.floor(hours / 24)

      if (days > 0) {
        return `Il y a ${days} jour${days > 1 ? 's' : ''}`
      } else if (hours > 0) {
        return `Il y a ${hours} heure${hours > 1 ? 's' : ''}`
      } else {
        return 'À l\'instant'
      }
    }

    const getNewInsight = () => {
      const randomIndex = Math.floor(Math.random() * insights.length)
      currentInsight.value = insights[randomIndex]
    }

    const toggleGoal = (goalId) => {
      const goal = weeklyGoals.value.find(g => g.id === goalId)
      if (goal) {
        goal.completed = !goal.completed
      }
    }

    onMounted(() => {
      // Charger les données du dashboard depuis l'API (à implémenter)
      console.log('Chargement du dashboard...')
    })

    return {
      recentActivities,
      weeklyGoals,
      currentInsight,
      formatTime,
      getNewInsight,
      toggleGoal,
      showPersonnelFeature
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  color: #667eea;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.dashboard-subtitle {
  color: #666;
  font-size: 1.2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #666;
  font-size: 1rem;
}

.personnel-aidants-section {
  margin-bottom: 3rem;
}

.personnel-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
  border: 2px dashed #667eea;
}

.personnel-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.personnel-content h3 {
  color: #667eea;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.personnel-content p {
  color: #6c757d;
  margin-bottom: 1.5rem;
}

.personnel-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.personnel-btn:hover {
  background: #5a67d8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-icon {
  font-size: 1rem;
}

.btn-text {
  font-size: 0.9rem;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chart-card h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
  text-align: center;
}

.progress-item,
.priority-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.progress-label,
.priority-label {
  min-width: 80px;
  font-size: 0.9rem;
  color: #495057;
}

.priority-label.high {
  color: #721c24;
}

.priority-label.medium {
  color: #856404;
}

.priority-label.low {
  color: #0c5460;
}

.progress-bar,
.priority-bar {
  flex: 1;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill,
.priority-fill {
  height: 100%;
  background: #667eea;
  transition: width 0.3s ease;
}

.progress-fill.in-progress {
  background: #ffc107;
}

.progress-fill.completed {
  background: #28a745;
}

.priority-fill.high {
  background: #dc3545;
}

.priority-fill.medium {
  background: #ffc107;
}

.priority-fill.low {
  background: #17a2b8;
}

.progress-value,
.priority-value {
  min-width: 30px;
  text-align: right;
  font-weight: bold;
  color: #495057;
}

.recent-activity {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 3rem;
}

.recent-activity h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
  text-align: center;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #e9ecef;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: #495057;
  margin-bottom: 0.25rem;
}

.activity-time {
  color: #6c757d;
  font-size: 0.9rem;
}

.insights-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.insight-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.insight-card h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
  text-align: center;
}

.insight-content p {
  color: #495057;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.goals-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.goal-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.goal-item span {
  color: #495057;
  flex: 1;
}

.goal-item span.completed {
  text-decoration: line-through;
  color: #6c757d;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .insights-section {
    grid-template-columns: 1fr;
  }
  
  .progress-item,
  .priority-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .progress-label,
  .priority-label {
    min-width: auto;
  }
  
  .progress-bar,
  .priority-bar {
    width: 100%;
  }
}
</style> 