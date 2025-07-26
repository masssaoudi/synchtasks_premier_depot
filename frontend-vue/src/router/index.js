import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Import des composants
import HomeView from '../views/HomeView.vue'
import TasksView from '../views/TasksView.vue'
import DashboardView from '../views/DashboardView.vue'
import PersonneAidantView from '../views/PersonneAidantView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/welcome',
    name: 'Welcome',
    component: () => import('../views/WelcomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: () => import('../views/TasksView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/personne-aidant',
    name: 'personneAidant',
    component: () => import('../views/PersonneAidantView.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Si la route nécessite une authentification
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/') // Redirection vers la page d'accueil au lieu de /login
    return
  }
  
  // Si la route nécessite d'être invité (non connecté)
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
    return
  }
  
  next()
})

export default router 