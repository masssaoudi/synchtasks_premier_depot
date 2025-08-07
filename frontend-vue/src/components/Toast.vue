<template>
  <div v-if="toasts.length > 0" class="toast-container">
    <TransitionGroup name="toast" tag="div" class="toast-list">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`]"
        @click="removeToast(toast.id)"
      >
        <div class="toast-icon">
          <span v-if="toast.type === 'success'">✅</span>
          <span v-else-if="toast.type === 'error'">❌</span>
          <span v-else-if="toast.type === 'warning'">⚠️</span>
          <span v-else-if="toast.type === 'info'">ℹ️</span>
          <span v-else>🔔</span>
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ toast.title }}</div>
          <div class="toast-message">{{ toast.message }}</div>
        </div>
        <button class="toast-close" @click.stop="removeToast(toast.id)">
          ✕
        </button>
        <div
          class="toast-progress"
          :style="{ width: toast.progress + '%' }"
        ></div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script>
  import { ref, onMounted, onUnmounted } from 'vue';

  export default {
    name: 'Toast',
    setup() {
      const toasts = ref([]);
      let nextId = 1;

      const addToast = toast => {
        const id = nextId++;
        const newToast = {
          id,
          type: toast.type || 'info',
          title: toast.title || 'Notification',
          message: toast.message || '',
          duration: toast.duration || 5000,
          progress: 100,
        };

        toasts.value.push(newToast);

        // Auto-remove after duration
        if (newToast.duration > 0) {
          const startTime = Date.now();
          const progressInterval = setInterval(() => {
            const elapsed = Date.now() - startTime;
            const remaining = Math.max(
              0,
              100 - (elapsed / newToast.duration) * 100
            );

            const toastIndex = toasts.value.findIndex(t => t.id === id);
            if (toastIndex !== -1) {
              toasts.value[toastIndex].progress = remaining;
            }

            if (remaining <= 0) {
              clearInterval(progressInterval);
              removeToast(id);
            }
          }, 50);
        }

        return id;
      };

      const removeToast = id => {
        const index = toasts.value.findIndex(toast => toast.id === id);
        if (index !== -1) {
          toasts.value.splice(index, 1);
        }
      };

      const clearAll = () => {
        toasts.value = [];
      };

      // Expose methods globally
      onMounted(() => {
        window.$toast = {
          add: addToast,
          remove: removeToast,
          clear: clearAll,
          success: (title, message, duration) =>
            addToast({ type: 'success', title, message, duration }),
          error: (title, message, duration) =>
            addToast({ type: 'error', title, message, duration }),
          warning: (title, message, duration) =>
            addToast({ type: 'warning', title, message, duration }),
          info: (title, message, duration) =>
            addToast({ type: 'info', title, message, duration }),
        };
      });

      onUnmounted(() => {
        delete window.$toast;
      });

      return {
        toasts,
        addToast,
        removeToast,
        clearAll,
      };
    },
  };
</script>

<style scoped>
  .toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    pointer-events: none;
  }

  .toast-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .toast {
    display: flex;
    align-items: center;
    min-width: 300px;
    max-width: 400px;
    padding: 12px 16px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border-left: 4px solid #4caf50;
    pointer-events: auto;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .toast:hover {
    transform: translateX(-5px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  }

  .toast-success {
    border-left-color: #4caf50;
  }

  .toast-error {
    border-left-color: #f44336;
  }

  .toast-warning {
    border-left-color: #ff9800;
  }

  .toast-info {
    border-left-color: #2196f3;
  }

  .toast-icon {
    font-size: 20px;
    margin-right: 12px;
    flex-shrink: 0;
  }

  .toast-content {
    flex: 1;
    min-width: 0;
  }

  .toast-title {
    font-weight: 600;
    font-size: 14px;
    color: #333;
    margin-bottom: 2px;
  }

  .toast-message {
    font-size: 13px;
    color: #666;
    line-height: 1.4;
  }

  .toast-close {
    background: none;
    border: none;
    font-size: 16px;
    color: #999;
    cursor: pointer;
    padding: 4px;
    margin-left: 8px;
    border-radius: 4px;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .toast-close:hover {
    background: #f5f5f5;
    color: #666;
  }

  .toast-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #4caf50, #45a049);
    transition: width 0.1s linear;
  }

  .toast-error .toast-progress {
    background: linear-gradient(90deg, #f44336, #d32f2f);
  }

  .toast-warning .toast-progress {
    background: linear-gradient(90deg, #ff9800, #f57c00);
  }

  .toast-info .toast-progress {
    background: linear-gradient(90deg, #2196f3, #1976d2);
  }

  /* Animations */
  .toast-enter-active,
  .toast-leave-active {
    transition: all 0.3s ease;
  }

  .toast-enter-from {
    opacity: 0;
    transform: translateX(100%);
  }

  .toast-leave-to {
    opacity: 0;
    transform: translateX(100%);
  }

  .toast-move {
    transition: transform 0.3s ease;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .toast-container {
      top: 10px;
      right: 10px;
      left: 10px;
    }

    .toast {
      min-width: auto;
      max-width: none;
    }
  }
</style>
