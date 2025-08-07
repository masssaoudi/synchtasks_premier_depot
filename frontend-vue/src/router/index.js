import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// 🎯 IMPORT DES COMPOSANTS AVEC LAZY LOADING
const routes = [
  // 🏠 PAGE D'ACCUEIL
  {
    path: '/',
    name: 'Home',
    redirect: '/login', // Redirection vers login par défaut
  },

  // 🔐 AUTHENTIFICATION
  {
    path: '/login',
    name: 'Login',
    component: () =>
      import(/* webpackChunkName: "auth" */ '../views/LoginView.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () =>
      import(/* webpackChunkName: "auth" */ '../views/RegisterView.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/auth/google/callback',
    name: 'GoogleCallback',
    component: () =>
      import(/* webpackChunkName: "auth" */ '../views/AuthCallback.vue'),
    meta: { requiresGuest: true },
  },

  // 🎯 SÉLECTION DE SEGMENT
  {
    path: '/segment-selection',
    name: 'segmentSelection',
    component: () =>
      import(/* webpackChunkName: "segments" */ '../views/SegmentSelectionView.vue'),
    meta: { requiresAuth: true },
  },

  // 📊 DASHBOARDS PAR SEGMENT (utilisant les fichiers existants)
  {
    path: '/dashboard/particuliers',
    name: 'ParticuliersDashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/dashboards/ParticuliersDashboard.vue'),
    meta: { requiresAuth: true, segment: 'particuliers' },
  },
  {
    path: '/dashboard/professionnels',
    name: 'ProfessionnelsDashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/dashboards/ProfessionnelsDashboard.vue'),
    meta: { requiresAuth: true, segment: 'professionnels' },
  },
  {
    path: '/dashboard/etudiants',
    name: 'EtudiantsDashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/dashboards/EtudiantsDashboard.vue'),
    meta: { requiresAuth: true, segment: 'etudiants' },
  },
  {
    path: '/dashboard/entreprises',
    name: 'EntreprisesDashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/dashboards/EntreprisesDashboard.vue'),
    meta: { requiresAuth: true, segment: 'entreprises' },
  },
  {
    path: '/dashboard/medical',
    name: 'MedicalDashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/dashboards/MedicalDashboard.vue'),
    meta: { requiresAuth: true, segment: 'medical' },
  },
  {
    path: '/dashboard/memoire',
    name: 'MemoireDashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/dashboards/MemoireDashboard.vue'),
    meta: { requiresAuth: true, segment: 'memoire' },
  },

  // 📋 TÂCHES
  {
    path: '/tasks',
    name: 'tasks',
    component: () =>
      import(/* webpackChunkName: "tasks" */ '../views/TasksView.vue'),
    meta: { requiresAuth: true },
  },

  // 👥 PERSONNE AIDANTE
  {
    path: '/personne-aidant',
    name: 'personneAidant',
    component: () =>
      import(/* webpackChunkName: "pa" */ '../views/PersonneAidantView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/pa-inscription',
    name: 'paInscription',
    component: () =>
      import(/* webpackChunkName: "pa" */ '../views/PAInscriptionView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/pa-dashboard',
    name: 'paDashboard',
    component: () =>
      import(/* webpackChunkName: "pa" */ '../views/PADashboardView.vue'),
    meta: { requiresAuth: true },
  },

  // 🎯 DASHBOARD GÉNÉRIQUE
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },

  // 🎯 SEGMENT DASHBOARD
  {
    path: '/segment-dashboard',
    name: 'segmentDashboard',
    component: () =>
      import(/* webpackChunkName: "dashboard" */ '../views/SegmentDashboardView.vue'),
    meta: { requiresAuth: true },
  },

  // 🏠 LANDING PAGE
  {
    path: '/landing',
    name: 'Landing',
    component: () =>
      import(/* webpackChunkName: "landing" */ '../views/HomeView.vue'),
  },

  // 🚫 PAGE 404 - Redirection vers login
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login',
  },
];

// 🎯 CRÉATION DU ROUTER
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 🎯 GUARDS INTELLIGENTS
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // 🎯 INITIALISATION DE L'AUTH SI NÉCESSAIRE
  if (!authStore.isInitialized) {
    await authStore.initAuth();
  }

  // 🎯 GESTION DES ROUTES PROTÉGÉES
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Rediriger vers login si non connecté
      next('/login');
      return;
    }

    // 🎯 VÉRIFICATION DU SEGMENT
    if (to.meta.segment) {
      const user = authStore.currentUser;
      if (user && user.segment !== to.meta.segment) {
        // Rediriger vers le bon dashboard si segment différent
        const correctRoute = getDashboardRoute(user.segment);
        next(correctRoute);
        return;
      }
    }

    // 🎯 REDIRECTION INTELLIGENTE SI PAS DE SEGMENT
    const user = authStore.currentUser;
    if (user && !user.segment && to.path !== '/segment-selection') {
      next('/segment-selection');
      return;
    }
  }

  // 🎯 GESTION DES ROUTES GUEST
  if (to.meta.requiresGuest) {
    if (authStore.isAuthenticated) {
      // Rediriger vers le dashboard approprié si déjà connecté
      const user = authStore.currentUser;
      if (user && user.segment) {
        const dashboardRoute = getDashboardRoute(user.segment);
        next(dashboardRoute);
      } else {
        next('/segment-selection');
      }
      return;
    }
  }

  next();
});

// 🎯 FONCTION UTILITAIRE POUR DÉTERMINER LE DASHBOARD
function getDashboardRoute(segment) {
  const routes = {
    'particuliers': '/dashboard/particuliers',
    'professionnels': '/dashboard/professionnels',
    'etudiants': '/dashboard/etudiants',
    'entreprises': '/dashboard/entreprises',
    'medical': '/dashboard/medical',
    'memoire': '/dashboard/memoire'
  };
  return routes[segment] || '/segment-selection';
}

// 🎯 GESTION DES ERREURS DE NAVIGATION
router.onError((error) => {
  console.error('Erreur de navigation:', error);
  // Rediriger vers une page d'erreur ou login
  router.push('/login');
});

export default router;
