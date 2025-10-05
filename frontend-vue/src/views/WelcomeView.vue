<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>Connexion</h1>
          <p>Accédez à votre espace personnel</p>
        </div>

        <form class="login-form" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              placeholder="votre@email.com"
            />
          </div>

          <div class="form-group">
            <label for="password">Mot de passe</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              placeholder="Votre mot de passe"
            />
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input v-model="rememberMe" type="checkbox" />
              <span>Se souvenir de moi</span>
            </label>
            <a href="#" class="forgot-password">Mot de passe oublié ?</a>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>

        <div class="login-divider">
          <span>ou</span>
        </div>

        <div class="social-login">
          <button 
            class="btn btn-social btn-google" 
            @click="handleGoogleLogin"
            :disabled="googleLoading"
          >
            <span v-if="googleLoading" class="loading-spinner-small"></span>
            <span v-else class="social-icon">🔍</span>
            {{ googleLoading ? 'Connexion...' : 'Continuer avec Google' }}
          </button>
          <button class="btn btn-social btn-microsoft" disabled>
            <span class="social-icon">🪟</span>
            Continuer avec Microsoft
          </button>
        </div>

        <div class="login-footer">
          <p>
            Pas encore de compte ?
            <a class="link" @click="goToRegister">Créer un compte</a>
          </p>
        </div>
      </div>

      <div class="login-info">
        <h2>Bienvenue sur SyncTasks</h2>
        <p>
          Une plateforme intelligente pour organiser vos tâches avec l'aide de
          l'IA
        </p>
        <div class="features-list">
          <div class="feature-item">
            <span class="feature-icon">🤖</span>
            <span>Assistant IA personnalisé</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">⚡</span>
            <span>Synchronisation temps réel</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">🔒</span>
            <span>Données sécurisées</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

  const router = useRouter();
  const authStore = useAuthStore();

  const email = ref('');
  const password = ref('');
  const rememberMe = ref(false);
  const loading = ref(false);
  const googleLoading = ref(false);

  const handleLogin = async () => {
    if (!email.value || !password.value) {
      alert('Veuillez remplir tous les champs');
      return;
    }

    loading.value = true;

    try {
      const result = await authStore.login({
        username: email.value,
        password: password.value,
      });

      if (result.success) {
        router.push('/segment-selection');
      } else {
        alert(
          result.message || 'Erreur de connexion. Vérifiez vos identifiants.'
        );
      }
    } catch (error) {
      console.error('Erreur de connexion:', error);
      alert('Erreur de connexion. Vérifiez vos identifiants.');
    } finally {
      loading.value = false;
    }
  };

  const goToRegister = () => {
    router.push('/register');
  };

  const handleGoogleLogin = async () => {
    googleLoading.value = true;
    
    try {
      const result = await authStore.loginWithGoogle();
      
      if (result.success) {
        router.push('/segment-selection');
      } else {
        alert(result.message || 'Erreur lors de la connexion Google');
      }
    } catch (error) {
      console.error('Erreur de connexion Google:', error);
      alert('Erreur lors de la connexion Google. Veuillez réessayer.');
    } finally {
      googleLoading.value = false;
    }
  };
</script>

<style scoped>
  .login-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .login-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    max-width: 1200px;
    width: 100%;
    align-items: center;
  }

  .login-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  }

  .login-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .login-header h1 {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }

  .login-header p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.1rem;
  }

  .login-form {
    margin-bottom: 2rem;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  .form-group label {
    display: block;
    color: white;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .form-group input {
    width: 100%;
    padding: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  .form-group input::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  .form-group input:focus {
    outline: none;
    border-color: #2ed573;
    background: rgba(255, 255, 255, 0.15);
  }

  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: white;
    font-size: 0.9rem;
    cursor: pointer;
  }

  .checkbox-label input[type='checkbox'] {
    width: auto;
    margin: 0;
  }

  .forgot-password {
    color: #2ed573;
    text-decoration: none;
    font-size: 0.9rem;
    transition: opacity 0.3s;
  }

  .forgot-password:hover {
    opacity: 0.8;
  }

  .btn {
    width: 100%;
    padding: 1rem;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .btn-primary {
    background: #2ed573;
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    background: #26d066;
    transform: translateY(-2px);
  }

  .btn-primary:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .loading-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .login-divider {
    text-align: center;
    margin: 2rem 0;
    position: relative;
  }

  .login-divider::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: rgba(255, 255, 255, 0.3);
  }

  .login-divider span {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    padding: 0 1rem;
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
  }

  .social-login {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .btn-social {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.2);
  }

  .btn-social:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .social-icon {
    font-size: 1.2rem;
  }

  .loading-spinner-small {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    display: inline-block;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .login-footer {
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
  }

  .link {
    color: #2ed573;
    text-decoration: none;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.3s;
  }

  .link:hover {
    opacity: 0.8;
  }

  /* Info Section */
  .login-info {
    color: white;
    text-align: center;
  }

  .login-info h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }

  .login-info p {
    font-size: 1.2rem;
    margin-bottom: 3rem;
    opacity: 0.9;
    line-height: 1.6;
  }

  .features-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .feature-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1.1rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    backdrop-filter: blur(10px);
  }

  .feature-icon {
    font-size: 1.5rem;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .login-container {
      grid-template-columns: 1fr;
      gap: 2rem;
    }

    .login-info {
      order: -1;
    }

    .login-info h2 {
      font-size: 2rem;
    }

    .login-card {
      padding: 2rem;
    }
  }
</style>
