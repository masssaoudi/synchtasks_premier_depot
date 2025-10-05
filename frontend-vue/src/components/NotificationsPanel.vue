<template>
  <div class="notifications-panel" :class="{ 'is-open': isOpen }">
    <!-- Bouton pour ouvrir/fermer le panel -->
    <button 
      class="notifications-toggle"
      @click="togglePanel"
      :class="{ 'has-notifications': unreadCount > 0 }"
    >
      <span class="icon">🔔</span>
      <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    </button>

    <!-- Panel des notifications -->
    <div v-if="isOpen" class="notifications-content">
      <div class="notifications-header">
        <h3>Notifications</h3>
        <div class="notifications-actions">
          <button @click="markAllAsRead" class="btn-secondary">
            Tout marquer comme lu
          </button>
          <button @click="clearAll" class="btn-secondary">
            Effacer tout
          </button>
        </div>
      </div>

      <!-- Statut de connexion WebSocket -->
      <div class="connection-status" :class="{ 'connected': isConnected }">
        <span class="status-icon">
          {{ isConnected ? '🔌' : '❌' }}
        </span>
        <span class="status-text">
          {{ isConnected ? 'Temps réel actif' : 'Temps réel inactif' }}
        </span>
      </div>

      <!-- Liste des notifications -->
      <div class="notifications-list">
        <div 
          v-for="notification in recentNotifications" 
          :key="notification.id"
          class="notification-item"
          :class="{ 
            'unread': !notification.read,
            [`priority-${notification.priority}`]: true,
            [`type-${notification.type}`]: true
          }"
          @click="markAsRead(notification.id)"
        >
          <div class="notification-icon">
            {{ notification.icon }}
          </div>
          <div class="notification-content">
            <div class="notification-title">
              {{ notification.title }}
            </div>
            <div class="notification-message">
              {{ notification.message }}
            </div>
            <div class="notification-time">
              {{ formatTime(notification.timestamp) }}
            </div>
          </div>
          <button 
            @click.stop="removeNotification(notification.id)"
            class="notification-close"
          >
            ×
          </button>
        </div>

        <!-- Message si aucune notification -->
        <div v-if="recentNotifications.length === 0" class="no-notifications">
          <span class="icon">📭</span>
          <p>Aucune notification</p>
        </div>
      </div>

      <!-- Statistiques -->
      <div class="notifications-stats">
        <div class="stat">
          <span class="stat-label">Total:</span>
          <span class="stat-value">{{ notificationCount }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Non lues:</span>
          <span class="stat-value">{{ unreadCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useNotificationsStore } from '../stores/notifications';

export default {
  name: 'NotificationsPanel',
  setup() {
    const notificationsStore = useNotificationsStore();
    const isOpen = ref(false);

    // Computed properties
    const notifications = computed(() => notificationsStore.notifications);
    const unreadCount = computed(() => notificationsStore.unreadCount);
    const recentNotifications = computed(() => notificationsStore.recentNotifications);
    const notificationCount = computed(() => notificationsStore.notificationCount);
    const isConnected = computed(() => notificationsStore.isConnected);

    // Actions
    const togglePanel = () => {
      isOpen.value = !isOpen.value;
    };

    const markAsRead = (id) => {
      notificationsStore.markAsRead(id);
    };

    const markAllAsRead = () => {
      notificationsStore.markAllAsRead();
    };

    const removeNotification = (id) => {
      notificationsStore.removeNotification(id);
    };

    const clearAll = () => {
      notificationsStore.clearAll();
    };

    // Utilitaires
    const formatTime = (timestamp) => {
      const now = new Date();
      const time = new Date(timestamp);
      const diff = now - time;

      if (diff < 60000) { // moins d'1 minute
        return 'À l\'instant';
      } else if (diff < 3600000) { // moins d'1 heure
        const minutes = Math.floor(diff / 60000);
        return `Il y a ${minutes} min`;
      } else if (diff < 86400000) { // moins d'1 jour
        const hours = Math.floor(diff / 3600000);
        return `Il y a ${hours}h`;
      } else {
        return time.toLocaleDateString();
      }
    };

    // Fermer le panel en cliquant à l'extérieur
    const handleClickOutside = (event) => {
      if (isOpen.value && !event.target.closest('.notifications-panel')) {
        isOpen.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      isOpen,
      notifications,
      unreadCount,
      recentNotifications,
      notificationCount,
      isConnected,
      togglePanel,
      markAsRead,
      markAllAsRead,
      removeNotification,
      clearAll,
      formatTime
    };
  }
};
</script>

<style scoped>
.notifications-panel {
  position: relative;
  display: inline-block;
}

.notifications-toggle {
  position: relative;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.notifications-toggle:hover {
  background: rgba(0, 0, 0, 0.1);
}

.notifications-toggle.has-notifications {
  animation: pulse 2s infinite;
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.notifications-content {
  position: absolute;
  top: 100%;
  right: 0;
  width: 400px;
  max-height: 500px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

.notifications-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notifications-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.notifications-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-secondary {
  background: #f8f9fa;
  border: 1px solid #ddd;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #e9ecef;
}

.connection-status {
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.connection-status.connected {
  background: #d4edda;
  color: #155724;
}

.notifications-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.notification-item:hover {
  background: #f8f9fa;
}

.notification-item.unread {
  background: #f0f8ff;
  border-left: 3px solid #007bff;
}

.notification-item.priority-high {
  border-left-color: #dc3545;
}

.notification-item.priority-medium {
  border-left-color: #ffc107;
}

.notification-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.notification-message {
  color: #666;
  font-size: 0.85rem;
  line-height: 1.4;
  margin-bottom: 0.25rem;
}

.notification-time {
  color: #999;
  font-size: 0.75rem;
}

.notification-close {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.notification-close:hover {
  background: #f0f0f0;
  color: #666;
}

.no-notifications {
  padding: 2rem;
  text-align: center;
  color: #999;
}

.no-notifications .icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

.notifications-stats {
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
}

.stat {
  display: flex;
  gap: 0.25rem;
}

.stat-label {
  color: #666;
}

.stat-value {
  font-weight: 600;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .notifications-content {
    width: 300px;
    right: -50px;
  }
}
</style> 