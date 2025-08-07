import axios from 'axios';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  // State - CORRECTION 1: Restaurer l'utilisateur depuis localStorage
  const user = ref(JSON.parse(localStorage.getItem('user')) || null);
  const token = ref(localStorage.getItem('authToken') || null);
  const loading = ref(false);
  const isInitialized = ref(false); // 🎯 NOUVEAU: État d'initialisation

  // Getters
  const isAuthenticated = computed(() => !!token.value);
  const currentUser = computed(() => user.value);

  // CORRECTION 2: Factoriser la logique d'auth
  const setAuth = (data) => {
    token.value = data.access_token;
    user.value = data.user;
    localStorage.setItem('authToken', token.value);
    localStorage.setItem('user', JSON.stringify(user.value));
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;
  };

  // Actions
  const login = async credentials => {
    loading.value = true;
    try {
      const response = await axios.post('/api/auth/login', credentials);

      if (response.data.success) {
        setAuth(response.data.data);
        return { success: true, message: 'Connexion réussie' };
      }
    } catch (error) {
      console.error('Erreur de connexion:', error);
      return {
        success: false,
        message: error.response?.data?.detail || 'Erreur de connexion',
      };
    } finally {
      loading.value = false;
    }
  };

  // CORRECTION 3: Auto-login après inscription
  const register = async userData => {
    loading.value = true;
    try {
      const response = await axios.post('/api/auth/register', userData);

      if (response.data.success) {
        // Auto-login avec les données reçues
        setAuth(response.data.data);
        return { success: true, message: 'Compte créé et connecté avec succès' };
      }
    } catch (error) {
      console.error("Erreur d'inscription:", error);
      return {
        success: false,
        message: error.response?.data?.detail || "Erreur d'inscription",
      };
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    token.value = null;
    user.value = null;

    // Nettoyer localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');

    // Supprimer le header Authorization
    delete axios.defaults.headers.common['Authorization'];
  };

  const checkAuth = async () => {
    if (!token.value) {
      return false;
    }

    try {
      const response = await axios.get('/api/auth/me');

      if (response.data.success) {
        user.value = response.data.data.user;
        return true;
      }
    } catch (error) {
      console.error('Erreur de vérification auth:', error);
      logout();
      return false;
    }
  };

  // Initialiser l'authentification au démarrage - 🎯 AMÉLIORÉ
  const initAuth = async () => {
    try {
      if (token.value) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;
        await checkAuth();
      }
    } catch (error) {
      console.error('Erreur lors de l\'initialisation auth:', error);
      logout();
    } finally {
      isInitialized.value = true; // 🎯 MARQUER COMME INITIALISÉ
    }
  };

  // Méthodes pour définir manuellement le token et l'utilisateur
  const setToken = newToken => {
    token.value = newToken;
    localStorage.setItem('authToken', newToken);
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
  };

  const setUser = newUser => {
    user.value = newUser;
    localStorage.setItem('user', JSON.stringify(newUser));
  };

  // Méthode pour l'authentification Google - CORRECTION 2: Utiliser setAuth
  const loginWithGoogle = async () => {
    loading.value = true;
    try {
      const googleAuthService = await import('../services/googleAuth');
      const result = await googleAuthService.default.initiateGoogleLogin();
      
      if (result.success) {
        setAuth({ access_token: result.access_token, user: result.user });
        return { success: true, message: 'Connexion Google réussie' };
      } else {
        return { success: false, message: 'Échec de la connexion Google' };
      }
    } catch (error) {
      console.error('Erreur lors de la connexion Google:', error);
      return {
        success: false,
        message: error.message || 'Erreur lors de la connexion Google',
      };
    } finally {
      loading.value = false;
    }
  };

  return {
    // State
    user,
    token,
    loading,
    isInitialized, // 🎯 NOUVEAU: Exposer l'état d'initialisation

    // Getters
    isAuthenticated,
    currentUser,

    // Actions
    login,
    register,
    logout,
    checkAuth,
    initAuth,
    setToken,
    setUser,
    loginWithGoogle,
    setAuth, // Exposer setAuth pour usage externe
  };
});
