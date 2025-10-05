<template>
  <div class="auth-callback">
    <div class="callback-container">
      <div class="loading-spinner"></div>
      <h2>Authentification en cours...</h2>
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const message = ref('Traitement de l\'authentification...');

onMounted(async () => {
  try {
    const token = route.query.token;
    const user = route.query.user;

    if (!token) {
      message.value = 'Token d\'authentification manquant';
      setTimeout(() => {
        router.push('/login');
      }, 2000);
      return;
    }

    message.value = 'Connexion réussie ! Redirection...';

    // Sauvegarder le token
    authStore.setToken(token);
    
    // Récupérer les informations utilisateur depuis le backend
    try {
      const response = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const userData = await response.json();
        authStore.setUser(userData.data.user);
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des données utilisateur:', error);
    }

    // Rediriger vers le dashboard
    setTimeout(() => {
      router.push('/segment-selection');
    }, 1000);

  } catch (error) {
    console.error('Erreur lors du callback:', error);
    message.value = 'Erreur lors de l\'authentification';
    setTimeout(() => {
      router.push('/login');
    }, 3000);
  }
});
</script>

<style scoped>
.auth-callback {
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