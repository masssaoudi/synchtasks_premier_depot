import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'
import axios from 'axios'

// Configuration axios
axios.defaults.baseURL = 'http://localhost:8000'

// Intercepteur pour les requêtes
axios.interceptors.request.use(
  config => {
    console.log('🌐 Requête envoyée:', config.method?.toUpperCase(), config.url)
    return config
  },
  error => {
    console.error('❌ Erreur de requête:', error)
    return Promise.reject(error)
  }
)

// Intercepteur pour les réponses
axios.interceptors.response.use(
  response => {
    console.log('✅ Réponse reçue:', response.status, response.config.url)
    return response
  },
  error => {
    console.error('❌ Erreur de réponse:', error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app') 