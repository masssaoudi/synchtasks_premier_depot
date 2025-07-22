import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('authToken') || null)
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const currentUser = computed(() => user.value)

  // Actions
  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await axios.post('/api/auth/login', credentials)
      
      if (response.data.success) {
        token.value = response.data.data.access_token
        user.value = response.data.data.user
        
        // Sauvegarder dans localStorage
        localStorage.setItem('authToken', token.value)
        localStorage.setItem('user', JSON.stringify(user.value))
        
        // Configurer axios pour les requêtes futures
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
        
        return { success: true }
      }
    } catch (error) {
      console.error('Erreur de connexion:', error)
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Erreur de connexion' 
      }
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    loading.value = true
    try {
      const response = await axios.post('/api/auth/register', userData)
      
      if (response.data.success) {
        return { success: true, message: 'Compte créé avec succès' }
      }
    } catch (error) {
      console.error('Erreur d\'inscription:', error)
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Erreur d\'inscription' 
      }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    
    // Nettoyer localStorage
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    
    // Supprimer le header Authorization
    delete axios.defaults.headers.common['Authorization']
  }

  const checkAuth = async () => {
    if (!token.value) return false
    
    try {
      const response = await axios.get('/api/auth/me')
      
      if (response.data.success) {
        user.value = response.data.data.user
        return true
      }
    } catch (error) {
      console.error('Erreur de vérification auth:', error)
      logout()
      return false
    }
  }

  // Initialiser l'authentification au démarrage
  const initAuth = async () => {
    if (token.value) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      await checkAuth()
    }
  }

  return {
    // State
    user,
    token,
    loading,
    
    // Getters
    isAuthenticated,
    currentUser,
    
    // Actions
    login,
    register,
    logout,
    checkAuth,
    initAuth
  }
}) 