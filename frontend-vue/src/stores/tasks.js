import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import websocketService from '../services/websocket.js'

export const useTasksStore = defineStore('tasks', () => {
  // State
  const tasks = ref([])
  const loading = ref(false)
  const websocketConnected = ref(false)

  // Getters
  const tasksByStatus = computed(() => {
    const grouped = {
      'À faire': [],
      'En cours': [],
      'Terminé': []
    }
    
    tasks.value.forEach(task => {
      if (grouped[task.status]) {
        grouped[task.status].push(task)
      }
    })
    
    return grouped
  })

  const taskCount = computed(() => tasks.value.length)
  const completedTasks = computed(() => tasks.value.filter(task => task.status === 'Terminé').length)
  const pendingTasks = computed(() => tasks.value.filter(task => task.status !== 'Terminé').length)

  // Actions
  const fetchTasks = async () => {
    loading.value = true
    try {
      const response = await axios.get('/api/tasks')
      if (response.data.success) {
        tasks.value = response.data.data
        console.log('📋 Tâches chargées:', tasks.value.length)
      }
    } catch (error) {
      console.error('❌ Erreur chargement tâches:', error)
    } finally {
      loading.value = false
    }
  }

  const createTask = async (taskData) => {
    try {
      const response = await axios.post('/api/tasks', taskData)
      if (response.data.success) {
        const newTask = response.data.data
        tasks.value.push(newTask)
        console.log('✅ Tâche créée:', newTask.title)
        
        // Notification locale
        if (window.$toast) {
          window.$toast.success(
            'Tâche créée',
            `"${newTask.title}" a été ajoutée avec succès`,
            3000
          )
        }
        
        return { success: true, task: newTask }
      }
    } catch (error) {
      console.error('❌ Erreur création tâche:', error)
      
      // Notification d'erreur
      if (window.$toast) {
        window.$toast.error(
          'Erreur',
          error.response?.data?.detail || 'Erreur lors de la création de la tâche',
          5000
        )
      }
      
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Erreur de création' 
      }
    }
  }

  const updateTask = async (taskId, updates) => {
    try {
      const response = await axios.put(`/api/tasks/${taskId}`, updates)
      if (response.data.success) {
        const updatedTask = response.data.data
        const index = tasks.value.findIndex(task => task._id === taskId)
        if (index !== -1) {
          tasks.value[index] = updatedTask
        }
        console.log('✅ Tâche mise à jour:', updatedTask.title)
        return { success: true, task: updatedTask }
      }
    } catch (error) {
      console.error('❌ Erreur mise à jour tâche:', error)
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Erreur de mise à jour' 
      }
    }
  }

  const deleteTask = async (taskId) => {
    try {
      const response = await axios.delete(`/api/tasks/${taskId}`)
      if (response.data.success) {
        tasks.value = tasks.value.filter(task => task._id !== taskId)
        console.log('✅ Tâche supprimée:', taskId)
        return { success: true }
      }
    } catch (error) {
      console.error('❌ Erreur suppression tâche:', error)
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Erreur de suppression' 
      }
    }
  }

  const toggleTaskStatus = async (taskId) => {
    const task = tasks.value.find(t => t._id === taskId)
    if (!task) return { success: false, message: 'Tâche non trouvée' }

    const newStatus = task.status === 'Terminé' ? 'À faire' : 'Terminé'
    return await updateTask(taskId, { status: newStatus })
  }

  // WebSocket Integration
  const initWebSocket = (userId) => {
    console.log('🔌 Initialisation WebSocket pour utilisateur:', userId)
    
    // Connecter au WebSocket
    websocketService.connect(userId)
    
    // Écouter les mises à jour de tâches
    const unsubscribe = websocketService.onTaskUpdate(({ action, task, task_id }) => {
      console.log('🔄 Mise à jour WebSocket reçue:', action, task || task_id)
      
      switch (action) {
        case 'create':
          if (task && !tasks.value.find(t => t._id === task._id)) {
            tasks.value.push(task)
            console.log('✅ Tâche créée via WebSocket:', task.title)
            
            // Notification temps réel
            if (window.$toast) {
              window.$toast.success(
                'Nouvelle tâche',
                `"${task.title}" a été ajoutée`,
                4000
              )
            }
          }
          break
          
        case 'update':
          if (task) {
            const index = tasks.value.findIndex(t => t._id === task._id)
            if (index !== -1) {
              tasks.value[index] = task
              console.log('✅ Tâche mise à jour via WebSocket:', task.title)
              
              // Notification temps réel
              if (window.$toast) {
                window.$toast.info(
                  'Tâche modifiée',
                  `"${task.title}" a été mise à jour`,
                  3000
                )
              }
            }
          }
          break
          
        case 'delete':
          if (task_id) {
            const deletedTask = tasks.value.find(t => t._id === task_id)
            tasks.value = tasks.value.filter(t => t._id !== task_id)
            console.log('✅ Tâche supprimée via WebSocket:', task_id)
            
            // Notification temps réel
            if (window.$toast && deletedTask) {
              window.$toast.warning(
                'Tâche supprimée',
                `"${deletedTask.title}" a été supprimée`,
                3000
              )
            }
          }
          break
          
        case 'complete':
          if (task) {
            const index = tasks.value.findIndex(t => t._id === task._id)
            if (index !== -1) {
              tasks.value[index] = task
              console.log('✅ Tâche terminée via WebSocket:', task.title)
              
              // Notification temps réel
              if (window.$toast) {
                window.$toast.success(
                  'Tâche terminée',
                  `"${task.title}" a été marquée comme terminée`,
                  4000
                )
              }
            }
          }
          break
      }
    })
    
    // Surveiller l'état de la connexion
    const checkConnection = () => {
      websocketConnected.value = websocketService.getConnectionState() === 'connected'
    }
    
    // Vérifier l'état initial
    checkConnection()
    
    // Vérifier périodiquement
    const interval = setInterval(checkConnection, 5000)
    
    // Retourner une fonction de nettoyage
    return () => {
      unsubscribe()
      clearInterval(interval)
      websocketService.disconnect()
    }
  }

  const disconnectWebSocket = () => {
    websocketService.disconnect()
    websocketConnected.value = false
  }

  return {
    // State
    tasks,
    loading,
    websocketConnected,
    
    // Getters
    tasksByStatus,
    taskCount,
    completedTasks,
    pendingTasks,
    
    // Actions
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskStatus,
    
    // WebSocket
    initWebSocket,
    disconnectWebSocket
  }
}) 