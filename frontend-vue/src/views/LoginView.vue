<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>Connexion</h1>
          <p>Accédez à votre espace personnel</p>
        </div>

        <!-- Formulaire de connexion -->
        <form class="login-form" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              placeholder="votre@email.com"
              :disabled="loading"
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
              :disabled="loading"
            />
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input v-model="rememberMe" type="checkbox" />
              <span>Se souvenir de moi</span>
            </label>
            <a href="#" class="forgot-password" @click="handleForgotPassword">
              Mot de passe oublié ?
            </a>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>

        <div class="login-divider">
          <span>ou</span>
        </div>

        <!-- Connexion sociale -->
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
        </div>

        <!-- Lien vers l'inscription -->
        <div class="login-footer">
          <p>
            Pas encore de compte ?
            <a class="link" @click="goToRegister">Créer un compte</a>
          </p>
        </div>
      </div>

      <!-- Informations sur l'application -->
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

// 🎯 ROUTER ET STORES
const router = useRouter();
const authStore = useAuthStore();

// 🎯 ÉTAT RÉACTIF
const email = ref('');
const password = ref('');
const rememberMe = ref(false);
const loading = ref(false);
const googleLoading = ref(false);

// 🎯 GESTION DE LA CONNEXION
const handleLogin = async () => {
  if (!email.value || !password.value) {
    alert('Veuillez remplir tous les champs');
    return;
  }

  loading.value = true;
  
  try {
    const result = await authStore.login({
      email: email.value,
      password: password.value
    });

    if (result.success) {
      // 🎯 REDIRECTION INTELLIGENTE
      await redirectAfterLogin();
    } else {
      alert(result.message || 'Erreur de connexion');
    }
  } catch (error) {
    console.error('Erreur de connexion:', error);
    alert('Erreur de connexion');
  } finally {
    loading.value = false;
  }
};

// 🎯 GESTION GOOGLE OAUTH
const handleGoogleLogin = async () => {
  googleLoading.value = true;
  
  try {
    const result = await authStore.loginWithGoogle();
    
    if (result.success) {
      // 🎯 REDIRECTION INTELLIGENTE
      await redirectAfterLogin();
    } else {
      alert(result.message || 'Erreur de connexion Google');
    }
  } catch (error) {
    console.error('Erreur Google OAuth:', error);
    alert('Erreur de connexion Google');
  } finally {
    googleLoading.value = false;
  }
};

// 🎯 REDIRECTION INTELLIGENTE APRÈS CONNEXION
const redirectAfterLogin = async () => {
  const user = authStore.currentUser;
  
  // Vérifier si l'utilisateur a déjà un segment
  if (user && user.segment) {
    // Rediriger vers le dashboard approprié
    const dashboardRoute = getDashboardRoute(user.segment);
    router.push(dashboardRoute);
  } else {
    // Rediriger vers la sélection de segment
    router.push('/segment-selection');
  }
};

// 🎯 DÉTERMINER LE DASHBOARD SELON LE SEGMENT
const getDashboardRoute = (segment) => {
  const routes = {
    'particuliers': '/dashboard/particuliers',
    'professionnels': '/dashboard/professionnels',
    'etudiants': '/dashboard/etudiants',
    'entreprises': '/dashboard/entreprises',
    'medical': '/dashboard/medical',
    'memoire': '/dashboard/memoire'
  };
  return routes[segment] || '/segment-selection';
};

// 🎯 NAVIGATION VERS L'INSCRIPTION
const goToRegister = () => {
  router.push('/register');
};

// 🎯 GESTION MOT DE PASSE OUBLIÉ
const handleForgotPassword = () => {
  // TODO: Implémenter la récupération de mot de passe
  alert('Fonctionnalité à venir');
};

// 🎯 INITIALISATION
// Vérifier si l'utilisateur est déjà connecté
if (authStore.isAuthenticated) {
  redirectAfterLogin();
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  display: flex;
  max-width: 1200px;
  width: 100%;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.login-card {
  flex: 1;
  padding: 40px;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2rem;
}

.login-header p {
  color: #7f8c8d;
  font-size: 1rem;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.forgot-password {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
}

.forgot-password:hover {
  text-decoration: underline;
}

.btn {
  width: 100%;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-divider {
  text-align: center;
  margin: 20px 0;
  position: relative;
}

.login-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e1e8ed;
}

.login-divider span {
  background: white;
  padding: 0 20px;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.social-login {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.btn-social {
  background: white;
  border: 2px solid #e1e8ed;
  color: #2c3e50;
}

.btn-social:hover:not(:disabled) {
  border-color: #667eea;
  transform: translateY(-1px);
}

.btn-google {
  background: #4285f4;
  color: white;
  border-color: #4285f4;
}

.btn-google:hover:not(:disabled) {
  background: #3367d6;
  border-color: #3367d6;
}

.social-icon {
  font-size: 1.2rem;
}

.loading-spinner,
.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner-small {
  width: 12px;
  height: 12px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.login-footer {
  text-align: center;
  margin-top: 20px;
}

.link {
  color: #667eea;
  cursor: pointer;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.login-info {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-info h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.login-info p {
  font-size: 1.1rem;
  margin-bottom: 30px;
  opacity: 0.9;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 1.1rem;
}

.feature-icon {
  font-size: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }
  
  .login-info {
    display: none;
  }
  
  .login-card {
    max-width: none;
  }
}
</style> 