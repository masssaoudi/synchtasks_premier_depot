import axios from 'axios';

class GoogleAuthService {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
  }

  /**
   * Récupère l'URL d'authentification Google
   */
  async getGoogleAuthUrl() {
    try {
      const response = await axios.get(`${this.baseURL}/api/auth/google/login`);
      return response.data.auth_url;
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'URL Google:', error);
      throw error;
    }
  }

  /**
   * Gère le callback Google OAuth
   */
  async handleGoogleCallback(code) {
    try {
      const response = await axios.get(`${this.baseURL}/api/auth/google/callback`, {
        params: { code }
      });
      
      if (response.data.success) {
        // Sauvegarder le token et les informations utilisateur
        const { access_token, user } = response.data.data;
        
        localStorage.setItem('authToken', access_token);
        localStorage.setItem('user', JSON.stringify(user));
        
        // Configurer axios pour les requêtes futures
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        return {
          success: true,
          user,
          access_token
        };
      } else {
        throw new Error(response.data.message || 'Erreur lors de l\'authentification Google');
      }
    } catch (error) {
      console.error('Erreur lors du callback Google:', error);
      throw error;
    }
  }

  /**
   * Lance le processus d'authentification Google
   */
  async initiateGoogleLogin() {
    try {
      // Rediriger directement vers l'endpoint Google OAuth
      window.location.href = `${this.baseURL}/api/api/auth/google/login`;
    } catch (error) {
      console.error('Erreur lors de l\'initiation de l\'authentification Google:', error);
      throw error;
    }
  }

  /**
   * Vérifie si l'utilisateur est connecté via Google
   */
  isGoogleUser() {
    const user = localStorage.getItem('user');
    if (user) {
      const userData = JSON.parse(user);
      return userData.auth_provider === 'google';
    }
    return false;
  }

  /**
   * Récupère la configuration Google OAuth
   */
  async getGoogleConfig() {
    try {
      const response = await axios.get(`${this.baseURL}/api/auth/google/config`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de la config Google:', error);
      throw error;
    }
  }
}

export default new GoogleAuthService(); 