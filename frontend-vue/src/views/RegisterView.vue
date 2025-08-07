<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h1>Créer un compte</h1>
          <p>Rejoignez SyncTasks pour organiser vos tâches</p>
        </div>

        <form class="register-form" @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="username">Nom d'utilisateur</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              placeholder="Votre nom d'utilisateur"
              :class="{ 'error': errors.username }"
            />
            <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              placeholder="votre@email.com"
              :class="{ 'error': errors.email }"
            />
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <label for="fullName">Nom complet</label>
            <input
              id="fullName"
              v-model="formData.full_name"
              type="text"
              required
              placeholder="Votre nom complet"
              :class="{ 'error': errors.full_name }"
            />
            <span v-if="errors.full_name" class="error-message">{{ errors.full_name }}</span>
          </div>

          <div class="form-group">
            <label for="password">Mot de passe</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              placeholder="Votre mot de passe"
              :class="{ 'error': errors.password }"
            />
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirmer le mot de passe</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              required
              placeholder="Confirmez votre mot de passe"
              :class="{ 'error': errors.confirmPassword }"
            />
            <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input v-model="formData.acceptTerms" type="checkbox" required />
              <span>J'accepte les <a href="#" class="link">conditions d'utilisation</a></span>
            </label>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? 'Création...' : 'Créer mon compte' }}
          </button>
        </form>

        <div class="register-divider">
          <span>ou</span>
        </div>

        <div class="social-login">
          <button 
            class="btn btn-social btn-google" 
            @click="handleGoogleRegister"
            :disabled="googleLoading"
          >
            <span v-if="googleLoading" class="loading-spinner-small"></span>
            <span v-else class="social-icon">🔍</span>
            {{ googleLoading ? 'Création...' : 'Créer avec Google' }}
          </button>
        </div>

        <div class="register-footer">
          <p>
            Déjà un compte ?
            <a class="link" @click="goToLogin">Se connecter</a>
          </p>
        </div>
      </div>

      <div class="register-info">
        <h2>Pourquoi SyncTasks ?</h2>
        <p>
          Une plateforme intelligente pour organiser vos tâches avec l'aide de l'IA
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
          <div class="feature-item">
            <span class="feature-icon">📱</span>
            <span>Interface intuitive</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const googleLoading = ref(false);
const errors = reactive({});

const formData = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false
});

const validateForm = () => {
  errors.username = '';
  errors.email = '';
  errors.full_name = '';
  errors.password = '';
  errors.confirmPassword = '';

  // Validation username
  if (formData.username.length < 3) {
    errors.username = 'Le nom d\'utilisateur doit contenir au moins 3 caractères';
  }

  // Validation email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(formData.email)) {
    errors.email = 'Veuillez entrer une adresse email valide';
  }

  // Validation nom complet
  if (formData.full_name.length < 2) {
    errors.full_name = 'Le nom complet doit contenir au moins 2 caractères';
  }

  // Validation mot de passe
  if (formData.password.length < 6) {
    errors.password = 'Le mot de passe doit contenir au moins 6 caractères';
  }

  // Validation confirmation mot de passe
  if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = 'Les mots de passe ne correspondent pas';
  }

  return Object.keys(errors).length === 0;
};

const handleRegister = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;

  try {
    const result = await authStore.register({
      username: formData.username,
      email: formData.email,
      full_name: formData.full_name,
      password: formData.password
    });

    if (result.success) {
      // Rediriger vers la sélection de segment
      router.push('/segment-selection');
    } else {
      alert(result.message || 'Erreur lors de la création du compte');
    }
  } catch (error) {
    console.error('Erreur lors de l\'inscription:', error);
    alert('Erreur lors de la création du compte. Veuillez réessayer.');
  } finally {
    loading.value = false;
  }
};

const handleGoogleRegister = async () => {
  googleLoading.value = true;
  
  try {
    const result = await authStore.loginWithGoogle();
    
    if (result.success) {
      // Rediriger vers la sélection de segment
      router.push('/segment-selection');
    } else {
      alert(result.message || 'Erreur lors de la création avec Google');
    }
  } catch (error) {
    console.error('Erreur lors de l\'inscription Google:', error);
    alert('Erreur lors de la création avec Google. Veuillez réessayer.');
  } finally {
    googleLoading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  max-width: 1200px;
  width: 100%;
  align-items: center;
}

.register-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.register-header p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
}

.register-form {
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

.form-group input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.15);
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.form-group input.error {
  border-color: #ff6b6b;
}

.error-message {
  color: #ff6b6b;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  display: block;
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
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  margin-right: 0.5rem;
  width: auto;
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
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-divider {
  text-align: center;
  margin: 2rem 0;
  position: relative;
}

.register-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.3);
}

.register-divider span {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0 1rem;
  color: white;
  font-size: 0.9rem;
}

.social-login {
  margin-bottom: 2rem;
}

.btn-social {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 1rem;
}

.btn-social:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
}

.btn-google {
  background: #4285f4;
}

.btn-google:hover:not(:disabled) {
  background: #3367d6;
}

.social-icon {
  font-size: 1.2rem;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.register-footer {
  text-align: center;
  color: white;
}

.register-footer p {
  margin: 0;
}

.link {
  color: #4CAF50;
  text-decoration: none;
  cursor: pointer;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

.register-info {
  color: white;
}

.register-info h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.register-info p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
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
  .register-container {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .register-card {
    padding: 2rem;
  }
  
  .register-header h1 {
    font-size: 2rem;
  }
}
</style> 