<template>
  <div class="google-callback">
    <div class="callback-container">
      <div class="loading-spinner"></div>
      <h2>Authentification en cours...</h2>
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import googleAuthService from '../services/googleAuth';

const router = useRouter();
const authStore = useAuthStore();
const message = ref('Connexion avec Google...');

onMounted(async () => {
  try {
    // Récupérer le code d'autorisation depuis l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const error = urlParams.get('error');

    if (error) {
      message.value = 'Erreur lors de l\'authentification Google';
      setTimeout(() => {
        window.opener?.postMessage({
          type: 'GOOGLE_AUTH_ERROR',
          error: error
        }, window.location.origin);
        window.close();
      }, 2000);
      return;
    }

    if (!code) {
      message.value = 'Code d\'autorisation manquant';
      setTimeout(() => {
        window.opener?.postMessage({
          type: 'GOOGLE_AUTH_ERROR',
          error: 'Code d\'autorisation manquant'
        }, window.location.origin);
        window.close();
      }, 2000);
      return;
    }

    message.value = 'Traitement de l\'authentification...';

    // Traiter le callback Google
    const result = await googleAuthService.handleGoogleCallback(code);

    if (result.success) {
      message.value = 'Connexion réussie ! Redirection...';
      
      // Mettre à jour le store d'authentification
      authStore.user = result.user;
      authStore.token = result.access_token;
      
      // Envoyer le message de succès à la fenêtre parente
      window.opener?.postMessage({
        type: 'GOOGLE_AUTH_SUCCESS',
        code: code,
        user: result.user
      }, window.location.origin);
      
      // Fermer la popup après un délai
      setTimeout(() => {
        window.close();
      }, 1000);
    } else {
      throw new Error('Échec de l\'authentification');
    }
  } catch (error) {
    console.error('Erreur lors du callback Google:', error);
    message.value = 'Erreur lors de l\'authentification';
    
    // Envoyer le message d'erreur à la fenêtre parente
    window.opener?.postMessage({
      type: 'GOOGLE_AUTH_ERROR',
      error: error.message
    }, window.location.origin);
    
    // Fermer la popup après un délai
    setTimeout(() => {
      window.close();
    }, 3000);
  }
});
</script>

<style scoped>
.google-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.callback-container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

h2 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

p {
  color: #666;
  font-size: 1rem;
  margin: 0;
}
</style> 