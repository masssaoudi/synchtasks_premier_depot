<template>
  <div v-if="show" class="theme-modal-overlay" @click="close">
    <div class="theme-modal-content" @click.stop>
      <div class="theme-modal-header">
        <h2>🎨 Choisissez votre thème</h2>
        <button class="close-btn" @click="close">×</button>
      </div>

      <div class="theme-options">
        <div
          class="theme-option"
          :class="{ active: selectedTheme === 'light' }"
          @click="setTheme('light')"
        >
          <div class="theme-preview light-preview">
            <div class="preview-header"></div>
            <div class="preview-content"></div>
          </div>
          <div class="theme-info">
            <span class="theme-icon">🌞</span>
            <span class="theme-name">Mode Clair</span>
            <span class="theme-desc">Interface claire et lumineuse</span>
          </div>
        </div>

        <div
          class="theme-option"
          :class="{ active: selectedTheme === 'dark' }"
          @click="setTheme('dark')"
        >
          <div class="theme-preview dark-preview">
            <div class="preview-header"></div>
            <div class="preview-content"></div>
          </div>
          <div class="theme-info">
            <span class="theme-icon">🌙</span>
            <span class="theme-name">Mode Sombre</span>
            <span class="theme-desc">Interface sombre et reposante</span>
          </div>
        </div>

        <div
          class="theme-option"
          :class="{ active: selectedTheme === 'auto' }"
          @click="setTheme('auto')"
        >
          <div class="theme-preview auto-preview">
            <div class="preview-header"></div>
            <div class="preview-content"></div>
          </div>
          <div class="theme-info">
            <span class="theme-icon">⚙️</span>
            <span class="theme-name">Automatique</span>
            <span class="theme-desc">Suit les préférences système</span>
          </div>
        </div>
      </div>

      <div class="theme-modal-footer">
        <button class="btn-secondary" @click="close">Annuler</button>
        <button class="btn-primary" @click="applyTheme">Appliquer</button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useThemeStore } from '../stores/theme';
  import { useAuthStore } from '../stores/auth';
  import axios from 'axios';

  const props = defineProps({
    show: Boolean,
  });

  const emit = defineEmits(['close', 'themeChanged']);

  const themeStore = useThemeStore();
  const authStore = useAuthStore();

  const selectedTheme = ref('auto');

  onMounted(() => {
    // Initialiser avec le thème actuel
    selectedTheme.value = themeStore.themePreference;
    console.log('🎨 Modal initialisé avec le thème:', selectedTheme.value);
  });

  const setTheme = theme => {
    console.log('🎨 setTheme appelé avec:', theme);
    selectedTheme.value = theme;
    console.log('🎨 selectedTheme mis à jour:', selectedTheme.value);
  };

  const applyTheme = async () => {
    try {
      console.log('🎨 applyTheme appelé avec:', selectedTheme.value);

      // Appliquer le thème localement
      themeStore.setTheme(selectedTheme.value);

      // Sauvegarder sur le serveur si utilisateur connecté
      if (authStore.isAuthenticated && authStore.currentUser) {
        const userId = authStore.currentUser._id || authStore.currentUser.id;
        await axios.post(`/api/theme/${userId}`, {
          theme: selectedTheme.value,
        });
        console.log('✅ Thème sauvegardé sur le serveur');
      }

      // Émettre l'événement
      emit('themeChanged', selectedTheme.value);
      emit('close');

      // Notification
      if (window.$toast) {
        const themeNames = {
          light: 'Mode Clair',
          dark: 'Mode Sombre',
          auto: 'Mode Automatique',
        };
        window.$toast.success(
          'Thème',
          `${themeNames[selectedTheme.value]} appliqué`,
          2000
        );
      } else {
        console.log('🎨 Toast non disponible');
      }
    } catch (error) {
      console.error('❌ Erreur lors de la sauvegarde du thème:', error);
      if (window.$toast) {
        window.$toast.error(
          'Erreur',
          'Impossible de sauvegarder le thème',
          3000
        );
      }
    }
  };

  const close = () => {
    // Reset selection to current theme
    selectedTheme.value = themeStore.themePreference;
    emit('close');
  };
</script>

<style scoped>
  .theme-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
  }

  .theme-modal-content {
    background: var(--bg-primary, #ffffff);
    border-radius: 16px;
    padding: 0;
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    border: 1px solid var(--border-color, #e1e5e9);
  }

  .theme-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color, #e1e5e9);
    background: var(--bg-secondary, #f8f9fa);
  }

  .theme-modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary, #2c3e50);
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-secondary, #6c757d);
    padding: 0.5rem;
    border-radius: 50%;
    transition: all 0.2s;
  }

  .close-btn:hover {
    background: var(--border-color, #e1e5e9);
    color: var(--text-primary, #2c3e50);
  }

  .theme-options {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .theme-option {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
    border: 2px solid transparent;
  }

  .theme-option:hover {
    background: var(--bg-secondary, #f8f9fa);
    transform: translateY(-2px);
  }

  .theme-option.active {
    border-color: var(--primary-color, #007bff);
    background: var(--bg-secondary, #f8f9fa);
  }

  .theme-preview {
    width: 60px;
    height: 40px;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border-color, #e1e5e9);
  }

  .light-preview {
    background: #ffffff;
  }

  .light-preview .preview-header {
    height: 8px;
    background: #f8f9fa;
    border-bottom: 1px solid #e1e5e9;
  }

  .light-preview .preview-content {
    height: 32px;
    background: #ffffff;
  }

  .dark-preview {
    background: #1a1a1a;
  }

  .dark-preview .preview-header {
    height: 8px;
    background: #2d2d2d;
    border-bottom: 1px solid #404040;
  }

  .dark-preview .preview-content {
    height: 32px;
    background: #1a1a1a;
  }

  .auto-preview {
    background: linear-gradient(45deg, #ffffff 50%, #1a1a1a 50%);
  }

  .auto-preview .preview-header {
    height: 8px;
    background: linear-gradient(45deg, #f8f9fa 50%, #2d2d2d 50%);
    border-bottom: 1px solid #e1e5e9;
  }

  .auto-preview .preview-content {
    height: 32px;
    background: linear-gradient(45deg, #ffffff 50%, #1a1a1a 50%);
  }

  .theme-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .theme-icon {
    font-size: 1.2rem;
  }

  .theme-name {
    font-weight: 600;
    color: var(--text-primary, #2c3e50);
    font-size: 1rem;
  }

  .theme-desc {
    font-size: 0.875rem;
    color: var(--text-secondary, #6c757d);
  }

  .theme-modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem 2rem;
    border-top: 1px solid var(--border-color, #e1e5e9);
    background: var(--bg-secondary, #f8f9fa);
  }

  .btn-primary,
  .btn-secondary {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.875rem;
  }

  .btn-primary {
    background: var(--primary-color, #007bff);
    color: white;
  }

  .btn-primary:hover {
    background: var(--primary-hover, #0056b3);
    transform: translateY(-1px);
  }

  .btn-secondary {
    background: var(--bg-primary, #ffffff);
    color: var(--text-primary, #2c3e50);
    border: 1px solid var(--border-color, #e1e5e9);
  }

  .btn-secondary:hover {
    background: var(--bg-secondary, #f8f9fa);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .theme-modal-content {
      width: 95%;
      margin: 1rem;
    }

    .theme-options {
      padding: 1rem;
    }

    .theme-modal-header,
    .theme-modal-footer {
      padding: 1rem 1.5rem;
    }
  }

  /* Dark mode styles */
  [data-theme='dark'] .theme-modal-content {
    background: #1a1a1a;
    border-color: #404040;
  }

  [data-theme='dark'] .theme-modal-header {
    background: #2d2d2d;
    border-color: #404040;
  }

  [data-theme='dark'] .theme-modal-header h2 {
    color: #ffffff;
  }

  [data-theme='dark'] .theme-option:hover {
    background: #2d2d2d;
  }

  [data-theme='dark'] .theme-option.active {
    border-color: #007bff;
    background: #2d2d2d;
  }

  [data-theme='dark'] .theme-name {
    color: #ffffff;
  }

  [data-theme='dark'] .theme-desc {
    color: #b0b0b0;
  }

  [data-theme='dark'] .theme-modal-footer {
    background: #2d2d2d;
    border-color: #404040;
  }

  [data-theme='dark'] .btn-secondary {
    background: #2d2d2d;
    color: #ffffff;
    border-color: #404040;
  }

  [data-theme='dark'] .btn-secondary:hover {
    background: #404040;
  }
</style>
