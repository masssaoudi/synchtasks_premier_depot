/**
 * Store pour les notifications temps réel
 * Gestion avancée des notifications avec priorité et historique
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useNotificationsStore = defineStore('notifications', () => {
  // State
  const notifications = ref([]);
  const isConnected = ref(false);
  const lastActivity = ref(null);
  const notificationCount = ref(0);

  // Getters
  const unreadCount = computed(() => {
    return notifications.value.filter(n => !n.read).length;
  });

  const recentNotifications = computed(() => {
    return notifications.value
      .slice()
      .reverse()
      .slice(0, 10); // 10 dernières notifications
  });

  const notificationsByType = computed(() => {
    const grouped = {};
    notifications.value.forEach(notification => {
      if (!grouped[notification.type]) {
        grouped[notification.type] = [];
      }
      grouped[notification.type].push(notification);
    });
    return grouped;
  });

  // Actions
  const addNotification = (notification) => {
    const newNotification = {
      id: Date.now() + Math.random(),
      timestamp: new Date(),
      read: false,
      ...notification
    };

    notifications.value.unshift(newNotification);
    notificationCount.value++;

    // Limiter le nombre de notifications (garder les 50 plus récentes)
    if (notifications.value.length > 50) {
      notifications.value = notifications.value.slice(0, 50);
    }

    // Afficher la notification toast si configuré
    if (window.$toast && notification.showToast !== false) {
      const toastType = notification.priority === 'high' ? 'error' : 
                       notification.priority === 'medium' ? 'warning' : 'info';
      
      window.$toast[toastType](
        notification.title,
        notification.message,
        notification.duration || 3000
      );
    }

    return newNotification;
  };

  const markAsRead = (notificationId) => {
    const notification = notifications.value.find(n => n.id === notificationId);
    if (notification) {
      notification.read = true;
    }
  };

  const markAllAsRead = () => {
    notifications.value.forEach(n => n.read = true);
  };

  const removeNotification = (notificationId) => {
    const index = notifications.value.findIndex(n => n.id === notificationId);
    if (index !== -1) {
      notifications.value.splice(index, 1);
      notificationCount.value--;
    }
  };

  const clearAll = () => {
    notifications.value = [];
    notificationCount.value = 0;
  };

  // Notifications spécifiques pour SyncTasks
  const addTaskNotification = (task, action, user = null) => {
    const messages = {
      created: `Nouvelle tâche créée : "${task.title}"`,
      updated: `Tâche mise à jour : "${task.title}"`,
      completed: `Tâche terminée : "${task.title}"`,
      deleted: `Tâche supprimée : "${task.title}"`
    };

    const titles = {
      created: 'Tâche créée',
      updated: 'Tâche modifiée',
      completed: 'Tâche terminée',
      deleted: 'Tâche supprimée'
    };

    return addNotification({
      type: 'task',
      title: titles[action] || 'Tâche',
      message: messages[action] || `Action sur la tâche : "${task.title}"`,
      priority: action === 'completed' ? 'medium' : 'low',
      data: { task, action, user },
      icon: action === 'completed' ? '✅' : action === 'created' ? '➕' : '📝'
    });
  };

  const addUserNotification = (user, action) => {
    const messages = {
      connected: `${user} s'est connecté`,
      disconnected: `${user} s'est déconnecté`,
      monitoring: `${user} surveille vos activités`
    };

    return addNotification({
      type: 'user',
      title: 'Utilisateur',
      message: messages[action] || `Action utilisateur : ${user}`,
      priority: 'low',
      data: { user, action },
      icon: action === 'connected' ? '👤' : action === 'disconnected' ? '👋' : '👁️'
    });
  };

  const addSystemNotification = (title, message, priority = 'low') => {
    return addNotification({
      type: 'system',
      title,
      message,
      priority,
      icon: '🔧'
    });
  };

  const addWebSocketNotification = (status, details = '') => {
    const messages = {
      connected: 'Connexion temps réel établie',
      disconnected: 'Connexion temps réel perdue',
      reconnecting: 'Tentative de reconnexion...',
      error: 'Erreur de connexion temps réel'
    };

    return addNotification({
      type: 'websocket',
      title: 'Temps réel',
      message: `${messages[status]} ${details}`.trim(),
      priority: status === 'error' ? 'high' : 'low',
      data: { status, details },
      icon: status === 'connected' ? '🔌' : status === 'error' ? '❌' : '🔄'
    });
  };

  // Gestion de la connexion WebSocket
  const setConnectionStatus = (status) => {
    isConnected.value = status === 'connected';
    lastActivity.value = new Date();
    
    if (status !== 'connected') {
      addWebSocketNotification(status);
    }
  };

  // Export des données pour sauvegarde
  const exportNotifications = () => {
    return {
      notifications: notifications.value,
      count: notificationCount.value,
      lastActivity: lastActivity.value
    };
  };

  // Import des données
  const importNotifications = (data) => {
    if (data.notifications) {
      notifications.value = data.notifications;
    }
    if (data.count) {
      notificationCount.value = data.count;
    }
    if (data.lastActivity) {
      lastActivity.value = new Date(data.lastActivity);
    }
  };

  return {
    // State
    notifications,
    isConnected,
    lastActivity,
    notificationCount,

    // Getters
    unreadCount,
    recentNotifications,
    notificationsByType,

    // Actions
    addNotification,
    markAsRead,
    markAllAsRead,
    removeNotification,
    clearAll,
    addTaskNotification,
    addUserNotification,
    addSystemNotification,
    addWebSocketNotification,
    setConnectionStatus,
    exportNotifications,
    importNotifications
  };
}); 