<template>
  <div class="home-container">
    <div class="welcome-card">
      <h1>Bienvenue sur SyncTasks</h1>
      <p>Connectez-vous pour accéder à vos tâches :</p>
      
      <form @submit.prevent="loginUser" class="login-form">
        <input 
          v-model="userUsername" 
          type="text" 
          placeholder="Nom d'utilisateur" 
          class="input" 
          required 
        />
        <input 
          v-model="userPassword" 
          type="password" 
          placeholder="Mot de passe" 
          class="input" 
          required 
        />
        <button type="submit" class="btn btn-primary">Se connecter</button>
        <div v-if="userError" class="error-message">{{ userError }}</div>
      </form>
      
      <div class="register-section">
        <p class="register-text">Pas encore de compte ?</p>
        <button @click="showRegisterModal = true" class="btn btn-secondary">
          S'inscrire
        </button>
      </div>
    </div>
    
    <!-- Modal d'inscription -->
    <div v-if="showRegisterModal" class="modal-overlay" @click="showRegisterModal = false">
      <div class="modal-content" @click.stop>
        <h2>Créer un compte</h2>
        <form @submit.prevent="registerUser" class="register-form">
          <input 
            v-model="registerData.username" 
            type="text" 
            placeholder="Nom d'utilisateur" 
            class="input" 
            required 
          />
          <input 
            v-model="registerData.email" 
            type="email" 
            placeholder="Email" 
            class="input" 
            required 
          />
          <input 
            v-model="registerData.password" 
            type="password" 
            placeholder="Mot de passe" 
            class="input" 
            required 
          />
          <input 
            v-model="registerData.confirmPassword" 
            type="password" 
            placeholder="Confirmer le mot de passe" 
            class="input" 
            required 
          />
          <button type="submit" class="btn btn-primary">Créer le compte</button>
          <div v-if="registerError" class="error-message">{{ registerError }}</div>
          <div v-if="registerSuccess" class="success-message">{{ registerSuccess }}</div>
        </form>
        <button @click="showRegisterModal = false" class="btn btn-secondary close-btn">
          Fermer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const userUsername = ref('')
const userPassword = ref('')
const userError = ref('')
const showRegisterModal = ref(false)
const registerError = ref('')
const registerSuccess = ref('')
const registerData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const router = useRouter()
const authStore = useAuthStore()

async function loginUser() {
  userError.value = ''
  
  const result = await authStore.login({
    username: userUsername.value.trim().toLowerCase(),
    password: userPassword.value
  })
  
  if (result.success) {
    router.push('/welcome')
  } else {
    userError.value = result.message || "Nom d'utilisateur ou mot de passe incorrect."
  }
}

async function registerUser() {
  registerError.value = ''
  registerSuccess.value = ''
  
  // Validation des mots de passe
  if (registerData.value.password !== registerData.value.confirmPassword) {
    registerError.value = "Les mots de passe ne correspondent pas."
    return
  }
  
  if (registerData.value.password.length < 6) {
    registerError.value = "Le mot de passe doit contenir au moins 6 caractères."
    return
  }
  
  const result = await authStore.register({
    username: registerData.value.username.trim().toLowerCase(),
    email: registerData.value.email.trim().toLowerCase(),
    password: registerData.value.password
  })
  
  if (result.success) {
    registerSuccess.value = "Compte créé avec succès ! Vous pouvez maintenant vous connecter."
    // Vider le formulaire
    registerData.value = {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
    // Fermer le modal après 2 secondes
    setTimeout(() => {
      showRegisterModal.value = false
      registerSuccess.value = ''
    }, 2000)
  } else {
    registerError.value = result.message || "Erreur lors de la création du compte."
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.welcome-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08);
  padding: 3rem 2.5rem;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.login-form {
  margin-top: 2rem;
}

.input {
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.7rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 0.7rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.error-message {
  color: #d32f2f;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.success-message {
  color: #2e7d32;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.register-section {
  margin-top: 2rem;
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.register-text {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-content h2 {
  color: #667eea;
  margin-bottom: 1.5rem;
  text-align: center;
}

.register-form {
  margin-bottom: 1.5rem;
}

.close-btn {
  width: 100%;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 1.5rem;
  }
}
</style> 