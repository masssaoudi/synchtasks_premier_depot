import axios from 'axios';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import websocketService from '../services/websocket';
import { useNotificationsStore } from './notifications';
import { useSegmentsStore } from './segments';

export const useTasksStore = defineStore('tasks', () => {
  // State
  const tasks = ref([]);
  const loading = ref(false);
  const websocketConnected = ref(false);
  const segmentsStore = useSegmentsStore();
  const notificationsStore = useNotificationsStore();

  // Getters
  const tasksByStatus = computed(() => {
    const grouped = {
      'À faire': [],
      'En cours': [],
      Terminé: [],
    };

    tasks.value.forEach(task => {
      if (grouped[task.status]) {
        grouped[task.status].push(task);
      }
    });

    return grouped;
  });

  const taskCount = computed(() => tasks.value.length);
  const completedTasks = computed(
    () => tasks.value.filter(task => task.status === 'Terminé').length
  );
  const pendingTasks = computed(
    () => tasks.value.filter(task => task.status !== 'Terminé').length
  );

  // Getters pour les segments
  const tasksBySegment = computed(() => {
    const currentSegment = segmentsStore.selectedSegment;
    if (!currentSegment) {
      return tasks.value;
    }

    return tasks.value.filter(task => task.segment === currentSegment);
  });

  const segmentCategories = computed(() => {
    return segmentsStore.getSegmentCategories();
  });

  const segmentPriorities = computed(() => {
    return segmentsStore.getSegmentPriorities();
  });

  // Actions
  const fetchTasks = async () => {
    loading.value = true;
    try {
      const response = await axios.get('/api/tasks');
      if (response.data.success) {
        tasks.value = response.data.data;
        console.log('📋 Tâches chargées:', tasks.value.length);
      }
    } catch (error) {
      console.error('❌ Erreur chargement tâches:', error);
    } finally {
      loading.value = false;
    }
  };

  const createTask = async taskData => {
    try {
      // Ajouter le segment sélectionné aux données de la tâche
      const taskWithSegment = {
        ...taskData,
        segment: segmentsStore.selectedSegment,
      };

      const response = await axios.post('/api/tasks', taskWithSegment);
      if (response.data.success) {
        const newTask = response.data.data;
        tasks.value.push(newTask);
        console.log('✅ Tâche créée:', newTask.title);

        // Envoyer la mise à jour via WebSocket
        if (websocketService.isConnected()) {
          websocketService.updateTask(newTask);
        }

        // Notification temps réel avancée
        notificationsStore.addTaskNotification(newTask, 'created');

        return { success: true, task: newTask };
      }
    } catch (error) {
      console.error('❌ Erreur création tâche:', error);

      // Notification d'erreur
      if (window.$toast) {
        window.$toast.error(
          'Erreur',
          error.response?.data?.detail ||
            'Erreur lors de la création de la tâche',
          5000
        );
      }

      return {
        success: false,
        message: error.response?.data?.detail || 'Erreur de création',
      };
    }
  };

  const updateTask = async (taskId, updates) => {
    try {
      const response = await axios.put(`/api/tasks/${taskId}`, updates);
      if (response.data.success) {
        const updatedTask = response.data.data;
        const index = tasks.value.findIndex(task => task._id === taskId);
        if (index !== -1) {
          tasks.value[index] = updatedTask;
        }
        console.log('✅ Tâche mise à jour:', updatedTask.title);

        // Envoyer la mise à jour via WebSocket
        if (websocketService.isConnected()) {
          websocketService.updateTask(updatedTask);
        }

        // Notification temps réel avancée
        notificationsStore.addTaskNotification(updatedTask, 'updated');
        return { success: true, task: updatedTask };
      }
    } catch (error) {
      console.error('❌ Erreur mise à jour tâche:', error);
      return {
        success: false,
        message: error.response?.data?.detail || 'Erreur de mise à jour',
      };
    }
  };

  const deleteTask = async taskId => {
    try {
      const response = await axios.delete(`/api/tasks/${taskId}`);
      if (response.data.success) {
        const deletedTask = tasks.value.find(task => task._id === taskId);
        tasks.value = tasks.value.filter(task => task._id !== taskId);
        console.log('✅ Tâche supprimée:', taskId);

        // Envoyer la suppression via WebSocket
        if (websocketService.isConnected() && deletedTask) {
          websocketService.updateTask({ ...deletedTask, _deleted: true });
        }

        // Notification temps réel avancée
        if (deletedTask) {
          notificationsStore.addTaskNotification(deletedTask, 'deleted');
        }
        return { success: true };
      }
    } catch (error) {
      console.error('❌ Erreur suppression tâche:', error);
      return {
        success: false,
        message: error.response?.data?.detail || 'Erreur de suppression',
      };
    }
  };

  const toggleTaskStatus = async taskId => {
    const task = tasks.value.find(t => t._id === taskId);
    if (!task) {
      return { success: false, message: 'Tâche non trouvée' };
    }

    const newStatus = task.status === 'Terminé' ? 'À faire' : 'Terminé';
    return await updateTask(taskId, { status: newStatus });
  };

  // WebSocket Integration
  // WebSocket - Initialiser la connexion temps réel
  const initWebSocket = async userId => {
    console.log('🔌 Initialisation WebSocket pour utilisateur:', userId);

    // Connecter au WebSocket
    await websocketService.connect(userId);

    // Configurer les handlers de connexion
    websocketService.onConnection('connected', () => {
      websocketConnected.value = true;
      console.log('✅ WebSocket connecté');
      notificationsStore.setConnectionStatus('connected');
    });

    websocketService.onConnection('disconnected', () => {
      websocketConnected.value = false;
      console.log('🔌 WebSocket déconnecté');
      notificationsStore.setConnectionStatus('disconnected');
    });

    websocketService.onConnection('error', () => {
      websocketConnected.value = false;
      console.error('❌ Erreur WebSocket');
      notificationsStore.setConnectionStatus('error');
    });

    // Configurer les handlers de messages
    websocketService.onMessage('task_updated', data => {
      console.log('🔄 Mise à jour tâche reçue:', data);
      const { task_data, user_id } = data;

      if (task_data) {
        const index = tasks.value.findIndex(t => t._id === task_data._id);
        if (index !== -1) {
          tasks.value[index] = task_data;
          console.log('✅ Tâche mise à jour via WebSocket:', task_data.title);

          // Notification temps réel avancée
          notificationsStore.addTaskNotification(task_data, 'updated', user_id);
        }
      }
    });

    websocketService.onMessage('kanban_updated', data => {
      console.log('🔄 Mise à jour Kanban reçue:', data);
      const { kanban_data, user_id } = data;

      // Mettre à jour l'ordre des tâches si nécessaire
      if (kanban_data && kanban_data.tasks) {
        // Logique pour mettre à jour l'ordre des tâches
        console.log('✅ Ordre Kanban mis à jour via WebSocket');
      }
    });

    websocketService.onMessage('user_connected', data => {
      console.log('👤 Utilisateur connecté:', data.user_id);
      notificationsStore.addUserNotification(data.user_id, 'connected');
    });

    websocketService.onMessage('user_disconnected', data => {
      console.log('👤 Utilisateur déconnecté:', data.user_id);
      notificationsStore.addUserNotification(data.user_id, 'disconnected');
    });

    websocketService.onMessage('pa_monitoring_started', data => {
      console.log('👁️ Monitoring PA démarré:', data);
      notificationsStore.addUserNotification(data.monitor_user_id || 'PA', 'monitoring');
    });

    // Heartbeat périodique
    const heartbeatInterval = setInterval(() => {
      if (websocketService.isConnected()) {
        websocketService.ping();
      }
    }, 30000); // Ping toutes les 30 secondes

    // Retourner une fonction de nettoyage
    return () => {
      clearInterval(heartbeatInterval);
      websocketService.disconnect();
    };
  };

  const disconnectWebSocket = () => {
    websocketService.disconnect();
    websocketConnected.value = false;
  };

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
    tasksBySegment,
    segmentCategories,
    segmentPriorities,

    // Actions
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskStatus,

    // WebSocket
    initWebSocket,
    disconnectWebSocket,
  };
});
