<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">🤖 SyncTasks</h1>
        <p class="login-subtitle">Gestion de Tâches Intelligente</p>
      </div>

      <!-- Messages d'alerte -->
      <div v-if="alert" :class="['alert', alert.type === 'success' ? 'alert-success' : 'alert-error']">
        {{ alert.message }}
      </div>

      <!-- Formulaire de connexion -->
      <form v-if="!showRegister" @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input 
            type="text" 
            id="username" 
            v-model="loginForm.username" 
            required
            placeholder="Votre nom d'utilisateur"
          >
        </div>

        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input 
            type="password" 
            id="password" 
            v-model="loginForm.password" 
            required
            placeholder="Votre mot de passe"
          >
        </div>

        <button type="submit" class="btn btn-primary" :disabled="authStore.loading">
          <span v-if="authStore.loading" class="loading"></span>
          <span v-else>Se connecter</span>
        </button>
      </form>

      <!-- Formulaire d'inscription -->
      <form v-else @submit.prevent="handleRegister" class="login-form">
        <div class="form-group">
          <label for="fullName">Nom complet</label>
          <input 
            type="text" 
            id="fullName" 
            v-model="registerForm.full_name" 
            required
            placeholder="Votre nom complet"
          >
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="registerForm.email" 
            required
            placeholder="votre@email.com"
          >
        </div>

        <div class="form-group">
          <label for="regUsername">Nom d'utilisateur</label>
          <input 
            type="text" 
            id="regUsername" 
            v-model="registerForm.username" 
            required
            placeholder="Choisissez un nom d'utilisateur"
          >
        </div>

        <div class="form-group">
          <label for="regPassword">Mot de passe</label>
          <input 
            type="password" 
            id="regPassword" 
            v-model="registerForm.password" 
            required
            placeholder="Créez un mot de passe"
          >
        </div>

        <button type="submit" class="btn btn-primary" :disabled="authStore.loading">
          <span v-if="authStore.loading" class="loading"></span>
          <span v-else>Créer mon compte</span>
        </button>
      </form>

      <!-- Liens de navigation -->
      <div class="login-links">
        <button v-if="!showRegister" @click="showRegister = true" class="btn btn-secondary">
          Créer un compte
        </button>
        <button v-else @click="showRegister = false" class="btn btn-secondary">
          Déjà un compte ? Se connecter
        </button>
      </div>


    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const showRegister = ref(false)
    const alert = ref(null)
    
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    const registerForm = reactive({
      full_name: '',
      email: '',
      username: '',
      password: ''
    })
    
    const showAlert = (message, type = 'error') => {
      alert.value = { message, type }
      setTimeout(() => {
        alert.value = null
      }, 5000)
    }
    
    const handleLogin = async () => {
      const result = await authStore.login(loginForm)
      
      if (result.success) {
        showAlert('Connexion réussie !', 'success')
        setTimeout(() => {
          router.push('/')
        }, 1000)
      } else {
        showAlert(result.message)
      }
    }
    
    const handleRegister = async () => {
      const result = await authStore.register(registerForm)
      
      if (result.success) {
        showAlert(result.message, 'success')
        showRegister.value = false
        // Réinitialiser le formulaire
        Object.keys(registerForm).forEach(key => {
          registerForm[key] = ''
        })
      } else {
        showAlert(result.message)
      }
    }
    

    
    return {
      authStore,
      showRegister,
      alert,
      loginForm,
      registerForm,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-header {
  margin-bottom: 30px;
}

.login-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.login-subtitle {
  color: #666;
  font-size: 1.1rem;
}

.login-form {
  text-align: left;
  margin-bottom: 20px;
}

.login-links {
  margin: 20px 0;
}



.btn {
  width: 100%;
  margin-bottom: 10px;
}
</style> 