<template>
  <div class="tasks-container">
    <div class="tasks-header">
      <h1>📋 Mes Tâches</h1>
      <div class="header-actions">
        <button @click="showHistoryModal = true" class="btn btn-secondary">
          🧠 Historique IA
        </button>
        <button @click="showNewTaskModal = true" class="btn btn-primary">
          + Nouvelle tâche
        </button>
      </div>
    </div>

    <!-- Messages d'alerte -->
    <div v-if="alert" :class="['alert', alert.type === 'success' ? 'alert-success' : 'alert-error']">
      {{ alert.message }}
    </div>

    <!-- Indicateur de chargement -->
    <div v-if="loading" class="loading-indicator">
      <div class="loading-spinner"></div>
      <p>Chargement des tâches...</p>
    </div>

    <!-- Tableau Kanban -->
    <div class="kanban-board">
      <div class="kanban-column">
        <h3>📝 À faire</h3>
        <div class="task-list">
          <div 
            v-for="task in tasks.filter(t => t.status === 'todo')" 
            :key="task.id"
            class="task-card"
            @click="editTask(task)"
          >
            <h4>{{ task.title }}</h4>
            <p>{{ task.description }}</p>
            <div class="task-meta">
              <span class="category" :class="`category-${task.category}`">
                {{ getCategoryIcon(task.category) }} {{ getCategoryLabel(task.category) }}
              </span>
              <span class="priority" :class="`priority-${task.priority}`">
                {{ getPriorityLabel(task.priority) }}
              </span>
              <span class="due-date" v-if="task.due_date">
                📅 {{ formatDate(task.due_date) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="kanban-column">
        <h3>🔄 En cours</h3>
        <div class="task-list">
          <div 
            v-for="task in tasks.filter(t => t.status === 'progress')" 
            :key="task.id"
            class="task-card"
            @click="editTask(task)"
          >
            <h4>{{ task.title }}</h4>
            <p>{{ task.description }}</p>
            <div class="task-meta">
              <span class="category" :class="`category-${task.category}`">
                {{ getCategoryIcon(task.category) }} {{ getCategoryLabel(task.category) }}
              </span>
              <span class="priority" :class="`priority-${task.priority}`">
                {{ getPriorityLabel(task.priority) }}
              </span>
              <span class="due-date" v-if="task.due_date">
                📅 {{ formatDate(task.due_date) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="kanban-column">
        <h3>✅ Terminé</h3>
        <div class="task-list">
          <div 
            v-for="task in tasks.filter(t => t.status === 'completed')" 
            :key="task.id"
            class="task-card completed"
            @click="editTask(task)"
          >
            <h4>{{ task.title }}</h4>
            <p>{{ task.description }}</p>
            <div class="task-meta">
              <span class="category" :class="`category-${task.category}`">
                {{ getCategoryIcon(task.category) }} {{ getCategoryLabel(task.category) }}
              </span>
              <span class="priority" :class="`priority-${task.priority}`">
                {{ getPriorityLabel(task.priority) }}
              </span>
              <span class="due-date" v-if="task.due_date">
                📅 {{ formatDate(task.due_date) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal pour nouvelle tâche -->
    <div v-if="showNewTaskModal" class="modal-overlay" @click="showNewTaskModal = false">
      <div class="modal" @click.stop>
        <h3>Nouvelle tâche</h3>
        <form @submit.prevent="createTask">
          <div class="form-group">
            <label for="title">Titre</label>
            <input 
              type="text" 
              id="title" 
              v-model="newTask.title" 
              required
              placeholder="Titre de la tâche"
            >
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea 
              id="description" 
              v-model="newTask.description" 
              rows="3"
              placeholder="Description de la tâche"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="category">Type de tâche</label>
            <select id="category" v-model="newTask.category" required>
              <option value="">Sélectionnez un type</option>
              <option 
                v-for="category in categories" 
                :key="category.value" 
                :value="category.value"
              >
                {{ category.icon }} {{ category.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="priority">Priorité</label>
            <select id="priority" v-model="newTask.priority" required>
              <option 
                v-for="priority in priorities" 
                :key="priority.value" 
                :value="priority.value"
              >
                {{ priority.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="due_date">Date d'échéance</label>
            <input 
              type="date" 
              id="due_date" 
              v-model="newTask.due_date"
            >
          </div>

          <div class="modal-actions">
            <button type="button" @click="showNewTaskModal = false" class="btn btn-secondary">
              Annuler
            </button>
            <button type="submit" class="btn btn-primary">
              Créer la tâche
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal pour l'historique intelligent -->
    <div v-if="showHistoryModal" class="modal-overlay" @click="showHistoryModal = false">
      <div class="modal history-modal" @click.stop>
        <h3>🧠 Historique Intelligent</h3>
        
        <div v-if="historyLoading" class="loading-indicator">
          <div class="loading-spinner"></div>
          <p>Analyse en cours...</p>
        </div>
        
        <div v-else-if="historyData" class="history-content">
          <div class="history-summary">
            <h4>📊 Résumé</h4>
            <p>{{ historyData.summary }}</p>
          </div>
          
          <div class="history-metrics">
            <div class="metric">
              <span class="metric-label">Score de productivité</span>
              <span class="metric-value">{{ historyData.productivity_score.toFixed(1) }}/100</span>
            </div>
            <div class="metric">
              <span class="metric-label">Taux de complétion</span>
              <span class="metric-value">{{ historyData.completion_rate.toFixed(1) }}%</span>
            </div>
          </div>
          
          <div class="history-insights">
            <h4>💡 Insights</h4>
            <ul>
              <li v-for="insight in historyData.insights" :key="insight">{{ insight }}</li>
            </ul>
          </div>
          
          <div class="history-recommendations">
            <h4>🎯 Recommandations</h4>
            <ul>
              <li v-for="rec in historyData.recommendations" :key="rec">{{ rec }}</li>
            </ul>
          </div>
          
          <div class="history-distribution">
            <h4>📈 Distribution par catégorie</h4>
            <div class="distribution-chart">
              <div 
                v-for="(count, category) in historyData.task_distribution" 
                :key="category"
                class="distribution-item"
              >
                <span class="category-name">{{ getCategoryLabel(category) }}</span>
                <div class="distribution-bar">
                  <div 
                    class="distribution-fill" 
                    :style="{ width: (count / Math.max(...Object.values(historyData.task_distribution)) * 100) + '%' }"
                  ></div>
                </div>
                <span class="category-count">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="showHistoryModal = false" class="btn btn-secondary">
            Fermer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import axios from 'axios'

export default {
  name: 'TasksView',
  setup() {
    const tasks = ref([])
    const loading = ref(false)
    const categories = ref([])
    const priorities = ref([])

    const showNewTaskModal = ref(false)
    const alert = ref(null)

    const newTask = reactive({
      title: '',
      description: '',
      category: '',
      priority: 'normale',
      due_date: ''
    })

    const showHistoryModal = ref(false)
    const historyLoading = ref(false)
    const historyData = ref(null)

    const showAlert = (message, type = 'success') => {
      alert.value = { message, type }
      setTimeout(() => {
        alert.value = null
      }, 3000)
    }

    const loadCategories = async () => {
      try {
        const response = await axios.get('/api/tasks/categories/')
        categories.value = response.data.categories
      } catch (error) {
        console.error('Erreur lors du chargement des catégories:', error)
      }
    }

    const loadPriorities = async () => {
      try {
        const response = await axios.get('/api/tasks/priorities/')
        priorities.value = response.data.priorities
        // Définir la priorité par défaut
        if (priorities.value.length > 0) {
          newTask.priority = priorities.value.find(p => p.value === 'normale')?.value || priorities.value[0].value
        }
      } catch (error) {
        console.error('Erreur lors du chargement des priorités:', error)
      }
    }

    const loadTasks = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/tasks/')
        tasks.value = response.data
        showAlert('Tâches chargées avec succès')
      } catch (error) {
        console.error('Erreur lors du chargement des tâches:', error)
        showAlert('Erreur lors du chargement des tâches', 'error')
      } finally {
        loading.value = false
      }
    }

    const createTask = async () => {
      try {
        const taskData = {
          title: newTask.title,
          description: newTask.description,
          priority: newTask.priority,
          category: newTask.category,
          due_date: newTask.due_date ? new Date(newTask.due_date).toISOString() : null
        }
        
        const response = await axios.post('/api/tasks/', taskData)
        tasks.value.push(response.data)
        
        // Réinitialiser le formulaire
        newTask.title = ''
        newTask.description = ''
        newTask.category = ''
        newTask.priority = priorities.value.find(p => p.value === 'normale')?.value || priorities.value[0]?.value || 'normale'
        newTask.due_date = ''
        
        showNewTaskModal.value = false
        showAlert('Tâche créée avec succès')
      } catch (error) {
        console.error('Erreur lors de la création de la tâche:', error)
        showAlert('Erreur lors de la création de la tâche', 'error')
      }
    }

    const editTask = (task) => {
      // Pour l'instant, on affiche juste les détails
      showAlert(`Édition de la tâche: ${task.title}`)
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('fr-FR')
    }

    const getCategoryIcon = (category) => {
      const categoryData = categories.value.find(c => c.value === category)
      return categoryData?.icon || '📋'
    }

    const getCategoryLabel = (category) => {
      const categoryData = categories.value.find(c => c.value === category)
      return categoryData?.label || category
    }

    const getPriorityLabel = (priority) => {
      const priorityData = priorities.value.find(p => p.value === priority)
      return priorityData?.label || priority
    }

    const loadHistory = async () => {
      historyLoading.value = true
      try {
        console.log('🔄 Chargement de l\'historique IA...')
        const response = await axios.get('/api/ia/history')
        
        if (response.data) {
          historyData.value = response.data
          console.log('✅ Historique IA chargé:', historyData.value)
        } else {
          throw new Error('Aucune donnée reçue de l\'API')
        }
      } catch (error) {
        console.error('❌ Erreur lors du chargement de l\'historique:', error)
        // Données de fallback en cas d'erreur
        historyData.value = {
          summary: "Impossible de charger l'analyse IA pour le moment",
          insights: ["Vérifiez votre connexion internet"],
          recommendations: ["Utilisez le chat IA pour obtenir de l'aide"],
          productivity_score: 0.5,
          completion_rate: 0.5,
          task_distribution: {}
        }
        showAlert('Erreur lors du chargement de l\'historique', 'error')
      } finally {
        historyLoading.value = false
      }
    }

    const handleTaskCompletion = async (taskId, action, keepMemory = true) => {
      try {
        const response = await axios.post('/api/ia/complete-task', {
          task_id: taskId,
          action: action,
          keep_memory: keepMemory
        })
        
        if (response.data.success) {
          showAlert(response.data.message)
          await loadTasks() // Recharger les tâches
        }
      } catch (error) {
        console.error('Erreur lors de la gestion de la tâche:', error)
        showAlert('Erreur lors de la gestion de la tâche', 'error')
      }
    }

    onMounted(async () => {
      await loadCategories()
      await loadPriorities()
      await loadTasks()
    })

    // Charger l'historique quand la modal s'ouvre
    watch(showHistoryModal, async (newValue) => {
      if (newValue && !historyData.value) {
        await loadHistory()
      }
    })

    return {
      tasks,
      loading,
      categories,
      priorities,
      showNewTaskModal,
      alert,
      newTask,
      createTask,
      editTask,
      formatDate,
      getCategoryIcon,
      getCategoryLabel,
      getPriorityLabel,
      showHistoryModal,
      historyLoading,
      historyData,
      handleTaskCompletion
    }
  }
}
</script>

<style scoped>
.tasks-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.tasks-header h1 {
  color: #667eea;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-size: 1rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

.alert {
  padding: 1rem 1.5rem;
  border-radius: 15px;
  margin-bottom: 1.5rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.kanban-board {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.kanban-column {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-height: 500px;
}

.kanban-column h3 {
  color: #333;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
  text-align: center;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 400px;
}

.task-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
  position: relative;
  overflow: hidden;
}

.task-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.task-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.task-card.completed {
  opacity: 0.7;
  background: #f8f9fa;
}

.task-card.completed::before {
  background: #28a745;
}

.task-card h4 {
  color: #333;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.task-card p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 1rem 0;
}

.task-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.category, .priority, .due-date {
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.category {
  background: #e3f2fd;
  color: #1976d2;
}

.priority {
  background: #fff3e0;
  color: #f57c00;
}

.priority-high {
  background: #ffebee;
  color: #d32f2f;
}

.priority-medium {
  background: #fff3e0;
  color: #f57c00;
}

.priority-low {
  background: #e8f5e8;
  color: #388e3c;
}

.due-date {
  background: #f3e5f5;
  color: #7b1fa2;
  font-size: 0.75rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
  text-align: center;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.modal-actions .btn {
  flex: 1;
}

.history-modal {
  width: 95%;
  max-width: 800px;
  max-height: 95vh;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow-y: auto;
}

.history-content {
  flex-grow: 1;
  overflow-y: auto;
}

.history-summary h4 {
  color: #667eea;
  margin-bottom: 0.8rem;
}

.history-summary p {
  color: #495057;
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-wrap; /* Preserve line breaks */
}

.history-metrics {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric {
  background: #e9ecef;
  border-radius: 8px;
  padding: 0.8rem 1.2rem;
  text-align: center;
  flex: 1;
  min-width: 150px;
}

.metric-label {
  display: block;
  font-size: 0.75rem;
  color: #6c757d;
  margin-bottom: 0.3rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
}

.history-insights h4,
.history-recommendations h4,
.history-distribution h4 {
  color: #667eea;
  margin-bottom: 0.8rem;
}

.history-insights ul,
.history-recommendations ul {
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
}

.history-insights li,
.history-recommendations li {
  color: #495057;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.history-distribution {
  margin-top: 1.5rem;
}

.distribution-chart {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  color: #495057;
}

.distribution-bar {
  flex-grow: 1;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.distribution-fill {
  height: 100%;
  background: #667eea;
  border-radius: 4px;
}

.category-name {
  font-weight: 500;
  color: #343a40;
}

.category-count {
  font-size: 0.8rem;
  color: #6c757d;
  min-width: 30px;
  text-align: right;
}

@media (max-width: 768px) {
  .tasks-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .kanban-board {
    grid-template-columns: 1fr;
  }
  
  .modal-actions {
    flex-direction: column;
  }

  .header-actions {
    flex-direction: column;
  }
}
</style> 