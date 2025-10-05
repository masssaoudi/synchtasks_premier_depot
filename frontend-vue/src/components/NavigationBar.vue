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

      <!-- Modal des raccourcis -->
      <ShortcutsModal
        :is-visible="showShortcutsModal"
        @close="showShortcutsModal = false"
      />

      <!-- Menu hamburger pour mobile -->
      <button
        class="mobile-menu-btn"
        :class="{ active: mobileMenuOpen }"
        @click="toggleMobileMenu"
      >
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>

      <!-- Boutons de navigation -->
      <div class="nav-buttons" :class="{ 'mobile-open': mobileMenuOpen }">
        <button
          class="nav-btn nav-btn-secondary"
          :disabled="!canGoBack"
          @click="goBack"
        >
          <span class="btn-icon">←</span>
          <span class="btn-text">Précédent</span>
        </button>

        <button class="nav-btn nav-btn-primary" @click="goHome">
          <span class="btn-icon">📊</span>
          <span class="btn-text">Tableau de bord</span>
        </button>
      </div>

      <!-- Menu utilisateur -->
      <div
        v-if="authStore.isAuthenticated"
        class="nav-user"
        :class="{ 'mobile-open': mobileMenuOpen }"
      >
        <div class="user-info">
          <span class="user-name">{{ authStore.currentUser?.username }}</span>
          <span
            class="ws-badge"
            :class="{
              connected: websocketConnected,
              disconnected: !websocketConnected,
            }"
          >
            <span class="ws-dot"></span>
            <span class="ws-text"
              >WebSocket {{ websocketConnected ? 'actif' : 'déconnecté' }}</span
            >
          </span>
        </div>

        <!-- Bouton de basculement du thème -->
        <button
          class="nav-btn nav-btn-theme"
          :title="
            themeStore.isDarkMode
              ? 'Passer en mode clair'
              : 'Passer en mode sombre'
          "
          @click="themeStore.toggleTheme()"
        >
          <span class="btn-icon">{{
            themeStore.isDarkMode ? '🌞' : '🌙'
          }}</span>
          <span class="btn-text">{{
            themeStore.isDarkMode ? 'Clair' : 'Sombre'
          }}</span>
        </button>

        <!-- Panel des notifications -->
        <NotificationsPanel />

        <!-- Bouton des raccourcis clavier -->
        <button
          class="nav-btn nav-btn-shortcuts"
          title="Raccourcis clavier"
          @click="showShortcutsModal = true"
        >
          <span class="btn-icon">⌨️</span>
          <span class="btn-text">Raccourcis</span>
        </button>

        <button class="nav-btn nav-btn-logout" @click="logout">
          <span class="btn-icon">🚪</span>
          <span class="btn-text">Déconnexion</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
  import { computed, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../stores/auth';
  import { useTasksStore } from '../stores/tasks';
  import { useThemeStore } from '../stores/theme';
  import ShortcutsModal from './ShortcutsModal.vue';
import NotificationsPanel from './NotificationsPanel.vue';

  export default {
    name: 'NavigationBar',
    components: {
      ShortcutsModal,
      NotificationsPanel,
    },
    setup() {
      const router = useRouter();
      const authStore = useAuthStore();
      const tasksStore = useTasksStore();
      const themeStore = useThemeStore();
      const mobileMenuOpen = ref(false);
      const showShortcutsModal = ref(false);

      const showNavigation = computed(() => {
        // Ne pas afficher sur la page de login
        return router.currentRoute.value.path !== '/login';
      });

      const canGoBack = computed(() => {
        return window.history.length > 1;
      });

      const toggleMobileMenu = () => {
        mobileMenuOpen.value = !mobileMenuOpen.value;
      };

      const goBack = () => {
        if (canGoBack.value) {
          mobileMenuOpen.value = false;
          router.go(-1);
        }
      };

      const goHome = () => {
        mobileMenuOpen.value = false;
        if (authStore.isAuthenticated) {
          router.push('/welcome');
        } else {
          router.push('/');
        }
      };

      const logout = () => {
        mobileMenuOpen.value = false;
        authStore.logout();
        router.push('/login');
      };

      const goPersonneAidant = () => {
        mobileMenuOpen.value = false;
        router.push('/personne-aidant');
      };

      // Basculement du thème
      const toggleTheme = () => {
        mobileMenuOpen.value = false;

        console.log(
          '🎨 Avant toggle - isDarkMode:',
          themeStore.isDarkMode.value
        );

        // Test du store theme
        try {
          themeStore.toggleTheme();
          console.log(
            '🎨 Après toggle - isDarkMode:',
            themeStore.isDarkMode.value
          );

          // Vérifier si la classe est appliquée
          const html = document.documentElement;
          console.log('🎨 Classes HTML:', html.className);
          console.log('🎨 data-theme:', html.getAttribute('data-theme'));

          // Test simple du toast
          if (window.$toast) {
            const message = themeStore.isDarkMode.value
              ? 'Mode sombre activé'
              : 'Mode clair activé';
            window.$toast.success('Thème', message, 3000);
          } else {
            console.log('Toast non disponible');
            alert(
              `Test du thème - ${themeStore.isDarkMode.value ? 'Mode sombre' : 'Mode clair'} activé`
            );
          }
        } catch (error) {
          console.error('Erreur theme store:', error);
          alert(`Erreur dans le store theme: ${error.message}`);
        }
      };

      // Badge WebSocket actif
      const websocketConnected = computed(() => tasksStore.websocketConnected);

      const handleShortcutsClose = () => {
        showShortcutsModal.value = false;
      };

      return {
        authStore,
        tasksStore,
        themeStore,
        showNavigation,
        canGoBack,
        websocketConnected,
        mobileMenuOpen,
        showShortcutsModal,
        toggleMobileMenu,
        goBack,
        goHome,
        logout,
        handleShortcutsClose,
      };
    },
  };
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

  /* Menu hamburger */
  .mobile-menu-btn {
    display: none;
    flex-direction: column;
    justify-content: space-around;
    width: 30px;
    height: 30px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
    z-index: 10;
  }

  .hamburger-line {
    width: 25px;
    height: 3px;
    background: white;
    border-radius: 10px;
    transition: all 0.3s linear;
    position: relative;
    transform-origin: 1px;
  }

  .mobile-menu-btn.active .hamburger-line:first-child {
    transform: rotate(45deg);
  }

  .mobile-menu-btn.active .hamburger-line:nth-child(2) {
    opacity: 0;
  }

  .mobile-menu-btn.active .hamburger-line:nth-child(3) {
    transform: rotate(-45deg);
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
    min-height: 44px; /* Accessibilité mobile */
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

  .nav-btn-theme {
    background: rgba(255, 193, 7, 0.9);
    color: #2c3e50;
    border: 1px solid rgba(255, 193, 7, 0.3);
  }

  .nav-btn-theme:hover {
    background: #ffc107;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
  }

  .nav-btn-shortcuts {
    background: rgba(156, 39, 176, 0.9);
    color: white;
    border: 1px solid rgba(156, 39, 176, 0.3);
  }

  .nav-btn-shortcuts:hover {
    background: #9c27b0;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(156, 39, 176, 0.3);
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
    background: rgba(255, 255, 255, 0.18);
    color: #fff;
    border: 1.5px solid #bbb;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
    transition:
      background 0.2s,
      color 0.2s,
      border 0.2s;
  }
  .ws-badge.connected {
    background: rgba(76, 175, 80, 0.18);
    color: #4caf50;
    border-color: #4caf50;
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
    background: #4caf50;
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
    .mobile-menu-btn {
      display: flex;
    }

    .nav-container {
      padding: 0 0.5rem;
    }

    .nav-buttons {
      position: fixed;
      top: 60px;
      left: 0;
      right: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      flex-direction: column;
      padding: 1rem;
      gap: 0.5rem;
      transform: translateY(-100%);
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .nav-buttons.mobile-open {
      transform: translateY(0);
      opacity: 1;
      visibility: visible;
    }

    .nav-user {
      position: fixed;
      top: 60px;
      left: 0;
      right: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      flex-direction: column;
      padding: 1rem;
      gap: 0.5rem;
      transform: translateY(-100%);
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .nav-user.mobile-open {
      transform: translateY(0);
      opacity: 1;
      visibility: visible;
    }

    .btn-text {
      display: block;
    }

    .nav-btn {
      padding: 0.75rem 1rem;
      width: 100%;
      justify-content: center;
    }

    .user-name {
      display: block;
      text-align: center;
    }

    .ws-badge {
      font-size: 0.8em;
      padding: 0.12em 0.5em 0.12em 0.3em;
      justify-content: center;
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
      top: 50px;
    }

    .nav-user {
      top: 50px;
    }

    .btn-text {
      font-size: 0.85rem;
    }

    .user-name {
      font-size: 0.85rem;
    }
  }

  /* Animation pour le menu mobile */
  @keyframes slideDown {
    from {
      transform: translateY(-100%);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  .nav-buttons.mobile-open,
  .nav-user.mobile-open {
    animation: slideDown 0.3s ease-out;
  }
</style>
