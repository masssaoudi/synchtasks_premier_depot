# 🧭 CANEVAS NAVIGATION VUE.JS - SYNCTASKS

## 📁 FICHIERS DE NAVIGATION IDENTIFIÉS

### 1. 🎯 ROUTER PRINCIPAL

**Fichier :** `frontend-vue/src/router/index.js`

```javascript
// Routes principales
const routes = [
  { path: '/', name: 'Home', redirect: '/tasks' },
  { path: '/landing', name: 'Landing', component: () => import('../views/HomeView.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/WelcomeView.vue'), meta: { requiresGuest: true } },
  { path: '/welcome', name: 'Welcome', component: () => import('../views/WelcomeView.vue'), meta: { requiresAuth: true } },
  { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/tasks', name: 'tasks', component: () => import('../views/TasksView.vue'), meta: { requiresAuth: true } },
  { path: '/personne-aidant', name: 'personneAidant', component: () => import('../views/PersonneAidantView.vue'), meta: { requiresAuth: false } },
  { path: '/pa-inscription', name: 'paInscription', component: () => import('../views/PAInscriptionView.vue'), meta: { requiresAuth: false } },
  { path: '/pa-dashboard', name: 'paDashboard', component: () => import('../views/PADashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/segment-selection', name: 'segmentSelection', component: () => import('../views/SegmentSelectionView.vue'), meta: { requiresAuth: false } },
  { path: '/segment-dashboard', name: 'segmentDashboard', component: () => import('../views/SegmentDashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/dashboard/particuliers', name: 'particuliersDashboard', component: () => import('../views/dashboards/ParticuliersDashboard.vue'), meta: { requiresAuth: true } }
]

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/tasks')
    return
  }
  
  next()
})
```

### 2. 🏠 LAYOUT PRINCIPAL

**Fichier :** `frontend-vue/src/App.vue`

```vue
<template>
  <div id="app">
    <!-- Barre de navigation globale -->
    <NavigationBar />
    
    <!-- Contenu principal avec padding pour la barre de navigation -->
    <main :class="['main-content', { 'with-nav': showNav }]">
      <router-view />
    </main>
    
    <!-- Système de notifications temps réel -->
    <Toast />
  </div>
</template>

<script>
// Logique de navigation principale
const showNav = computed(() => {
  return route.path !== '/login'
})

// Vérifier l'authentification au chargement
onMounted(async () => {
  await authStore.initAuth()
  
  if (!authStore.isAuthenticated && route.path !== '/login' && route.path !== '/') {
    router.push('/login')
  }
})
</script>
```

### 3. 🧭 BARRE DE NAVIGATION

**Fichier :** `frontend-vue/src/components/NavigationBar.vue`

```vue
<template>
  <nav v-if="showNavigation" class="navigation-bar">
    <div class="nav-container">
      <!-- Logo et titre -->
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">🤖</span>
          <span class="brand-text">SyncTasks</span>
        </router-link>
      </div>

      <!-- Boutons de navigation -->
      <div class="nav-buttons">
        <button @click="goBack" class="nav-btn nav-btn-secondary" :disabled="!canGoBack">
          <span class="btn-icon">←</span>
          <span class="btn-text">Précédent</span>
        </button>
        
        <button @click="goHome" class="nav-btn nav-btn-primary">
          <span class="btn-icon">📊</span>
          <span class="btn-text">Tableau de bord</span>
        </button>
      </div>

      <!-- Menu utilisateur -->
      <div class="nav-user" v-if="authStore.isAuthenticated">
        <div class="user-info">
          <span class="user-name">{{ authStore.currentUser?.username }}</span>
          <span class="ws-badge" :class="{ connected: websocketConnected, disconnected: !websocketConnected }">
            <span class="ws-dot"></span>
            <span class="ws-text">WebSocket {{ websocketConnected ? 'actif' : 'déconnecté' }}</span>
          </span>
        </div>
        <button @click="logout" class="nav-btn nav-btn-logout">
          <span class="btn-icon">🚪</span>
          <span class="btn-text">Déconnexion</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
// Méthodes de navigation
const goBack = () => {
  if (canGoBack.value) {
    router.go(-1)
  }
}

const goHome = () => {
  if (authStore.isAuthenticated) {
    router.push('/welcome')
  } else {
    router.push('/')
  }
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

const goPersonneAidant = () => {
  router.push('/personne-aidant')
}
</script>
```

## 📄 COMPOSANTS DE PAGES (VUES)

### 4. 🏠 PAGE D'ACCUEIL

**Fichier :** `frontend-vue/src/views/HomeView.vue`

```vue
<template>
  <div class="landing-page">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <h2>SyncTasks</h2>
        </div>
        <div class="nav-links">
          <a href="#about" class="nav-link">À propos</a>
          <div class="websocket-status">
            <span class="status-dot" :class="{ connected: websocketConnected }"></span>
            <span class="status-text">{{ websocketConnected ? 'Connecté' : 'Déconnecté' }}</span>
          </div>
          <button @click="goToLogin" class="btn btn-outline">Connexion</button>
          <button @click="goToRegister" class="btn btn-primary">S'inscrire</button>
          <button @click="startDemo" class="btn btn-demo">Demo</button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            Organisez vos tâches avec l'<span class="highlight">Intelligence Artificielle</span>
          </h1>
          <div class="hero-actions">
            <button @click="goToRegister" class="btn btn-primary btn-large">
              Commencer gratuitement
            </button>
            <button @click="startDemo" class="btn btn-secondary btn-large">
              Voir la démo
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
// Méthodes de navigation
const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/segment-selection')
}

const startDemo = () => {
  console.log('Démarrage du mode démo')
  router.push('/segment-selection')
}
</script>
```

### 5. 🔐 PAGE DE CONNEXION

**Fichier :** `frontend-vue/src/views/WelcomeView.vue`

```vue
<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>Connexion</h1>
          <p>Accédez à votre espace personnel</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required placeholder="votre@email.com" />
          </div>
          
          <div class="form-group">
            <label for="password">Mot de passe</label>
            <input type="password" id="password" v-model="password" required placeholder="Votre mot de passe" />
          </div>
          
          <button type="submit" class="btn btn-primary" :disabled="loading">
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>
        
        <div class="login-footer">
          <p>Pas encore de compte ? 
            <a @click="goToRegister" class="link">Créer un compte</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Méthodes de navigation
const handleLogin = async () => {
  if (!email.value || !password.value) {
    alert('Veuillez remplir tous les champs')
    return
  }
  
  loading.value = true
  
  try {
    await authStore.login(email.value, password.value)
    router.push('/segment-selection')
  } catch (error) {
    console.error('Erreur de connexion:', error)
    alert('Erreur de connexion. Vérifiez vos identifiants.')
  } finally {
    loading.value = false
  }
}

const goToRegister = () => {
  router.push('/segment-selection')
}
</script>
```

### 6. 📊 TABLEAU DE BORD PRINCIPAL

**Fichier :** `frontend-vue/src/views/DashboardView.vue`

### 7. 📋 VUE DES TÂCHES

**Fichier :** `frontend-vue/src/views/TasksView.vue`

```vue
<template>
  <div class="tasks-page">
    <div class="tasks-header">
      <h1>📋 Mes Tâches</h1>
      <div class="header-actions">
        <button @click="showHistoryModal = true" class="btn btn-secondary">
          🧠 Historique IA
        </button>
        <button @click="showNewTaskModal = true" class="btn btn-primary">
          ➕ Nouvelle tâche
        </button>
        <button @click="showChatModal = true" class="btn btn-info">
          🤖 Chat IA
        </button>
      </div>
    </div>

    <!-- Tableau de tâches simple -->
    <div class="tasks-grid">
      <!-- Section À faire -->
      <div class="tasks-section">
        <h3>📝 À faire</h3>
        <div class="tasks-list">
          <div v-for="task in todoTasks" :key="task._id" class="task-card">
            <div class="task-header">
              <h4>{{ task.title }}</h4>
              <div class="task-actions">
                <button @click="changeTaskStatus(task, 'done')" class="btn btn-success btn-sm">
                  ✅ Terminer
                </button>
                <button @click="editTask(task)" class="btn btn-secondary btn-sm">✏️</button>
                <button @click="deleteTask(task)" class="btn btn-danger btn-sm">🗑️</button>
              </div>
            </div>
            <p class="task-description">{{ task.description }}</p>
          </div>
        </div>
      </div>

      <!-- Section Terminé -->
      <div class="tasks-section">
        <h3>✅ Terminé</h3>
        <div class="tasks-list">
          <div v-for="task in completedTasks" :key="task._id" class="task-card completed">
            <div class="task-header">
              <h4>{{ task.title }}</h4>
              <div class="task-actions">
                <button @click="changeTaskStatus(task, 'todo')" class="btn btn-warning btn-sm">
                  🔄 Remettre en cours
                </button>
                <button @click="editTask(task)" class="btn btn-secondary btn-sm">✏️</button>
                <button @click="deleteTask(task)" class="btn btn-danger btn-sm">🗑️</button>
              </div>
            </div>
            <p class="task-description">{{ task.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

### 8. 👥 VUE PERSONNE AIDANT

**Fichier :** `frontend-vue/src/views/PersonneAidantView.vue`

### 9. 📊 TABLEAU DE BORD SEGMENTÉ

**Fichier :** `frontend-vue/src/views/SegmentDashboardView.vue`

```vue
<script>
// Méthodes de navigation spécifiques
const changeSegment = () => {
  router.push('/segment-selection')
}

const openChat = () => {
  showChatModal.value = false
  router.push('/tasks')
}

const openHistory = () => {
  showHistoryModal.value = false
  router.push('/tasks')
}

const openInsights = () => {
  showInsightsModal.value = false
  router.push('/tasks')
}
</script>
```

### 10. 🏠 DASHBOARD PARTICULIERS

**Fichier :** `frontend-vue/src/views/dashboards/ParticuliersDashboard.vue`

```vue
<script>
// Méthodes de navigation spécifiques aux particuliers
const changeSegment = () => {
  router.push('/segment-selection')
}

const openChat = () => {
  router.push('/tasks?module=chat')
}

const openHistory = () => {
  router.push('/tasks?module=history')
}

const openInsights = () => {
  router.push('/tasks?module=insights')
}

const openPlanning = () => {
  router.push('/tasks?feature=planning')
}

const openHouse = () => {
  router.push('/tasks?feature=house')
}

const openShopping = () => {
  router.push('/tasks?feature=shopping')
}

const openWellness = () => {
  router.push('/tasks?feature=wellness')
}
</script>
```

## 🎯 LOGIQUE DE NAVIGATION PAR BOUTONS

### Boutons de Navigation Principaux

1. **Bouton "Connexion"** (HomeView.vue)

```vue
<button @click="goToLogin" class="btn btn-outline">Connexion</button>
```

```javascript
const goToLogin = () => {
  router.push('/login')
}
```

2. **Bouton "S'inscrire"** (HomeView.vue)

```vue
<button @click="goToRegister" class="btn btn-primary">S'inscrire</button>
```

```javascript
const goToRegister = () => {
  router.push('/segment-selection')
}
```

3. **Bouton "Tableau de bord"** (NavigationBar.vue)

```vue
<button @click="goHome" class="nav-btn nav-btn-primary">
  <span class="btn-icon">📊</span>
  <span class="btn-text">Tableau de bord</span>
</button>
```

```javascript
const goHome = () => {
  if (authStore.isAuthenticated) {
    router.push('/welcome')
  } else {
    router.push('/')
  }
}
```

4. **Bouton "Déconnexion"** (NavigationBar.vue)

```vue
<button @click="logout" class="nav-btn nav-btn-logout">
  <span class="btn-icon">🚪</span>
  <span class="btn-text">Déconnexion</span>
</button>
```

```javascript
const logout = () => {
  authStore.logout()
  router.push('/login')
}
```

5. **Bouton "Précédent"** (NavigationBar.vue)

```vue
<button @click="goBack" class="nav-btn nav-btn-secondary" :disabled="!canGoBack">
  <span class="btn-icon">←</span>
  <span class="btn-text">Précédent</span>
</button>
```

```javascript
const goBack = () => {
  if (canGoBack.value) {
    router.go(-1)
  }
}
```

### Boutons de Navigation Spécialisés

6. **Boutons de modules IA** (ParticuliersDashboard.vue)

```vue
<button @click="openChat" class="module-btn">
  <span class="module-icon">💬</span>
  <span class="module-text">Chat IA</span>
</button>
```

```javascript
const openChat = () => {
  router.push('/tasks?module=chat')
}
```

7. **Boutons de fonctionnalités** (ParticuliersDashboard.vue)

```vue
<button @click="openPlanning" class="feature-btn">
  <span class="feature-icon">📅</span>
  <span class="feature-text">Planning</span>
</button>
```

```javascript
const openPlanning = () => {
  router.push('/tasks?feature=planning')
}
```

## 🔄 FLUX DE NAVIGATION

### Parcours Utilisateur Non Authentifié

1. **Accueil** (`/`) → Redirection vers `/tasks`
2. **Landing** (`/landing`) → Page d'accueil avec boutons Connexion/Inscription
3. **Login** (`/login`) → Formulaire de connexion
4. **Segment Selection** (`/segment-selection`) → Choix du profil utilisateur

### Parcours Utilisateur Authentifié

1. **Welcome** (`/welcome`) → Page de bienvenue après connexion
2. **Dashboard** (`/dashboard`) → Tableau de bord principal
3. **Tasks** (`/tasks`) → Gestion des tâches (page principale)
4. **Segment Dashboard** (`/segment-dashboard`) → Dashboard spécialisé par segment
5. **Particuliers Dashboard** (`/dashboard/particuliers`) → Dashboard spécifique aux particuliers

### Parcours Personne Aidant

1. **Personne Aidant** (`/personne-aidant`) → Page d'accueil PA
2. **PA Inscription** (`/pa-inscription`) → Inscription PA
3. **PA Dashboard** (`/pa-dashboard`) → Dashboard PA

## 🛡️ GUARDS DE NAVIGATION

### Protection des Routes

- **requiresAuth: true** → Nécessite une authentification
- **requiresGuest: true** → Nécessite d'être non connecté

### Redirections Automatiques

- Utilisateur non connecté sur route protégée → `/login`
- Utilisateur connecté sur route invité → `/tasks`

## 📱 RESPONSIVE DESIGN

### Navigation Mobile

- Boutons avec icônes seulement sur mobile
- Menu utilisateur adaptatif
- Barre de navigation fixe avec padding adaptatif

---

## 🎯 RÉSUMÉ DES FICHIERS DE NAVIGATION

✅ **Fichiers identifiés et analysés :**

1. `frontend-vue/src/router/index.js` - Configuration des routes
2. `frontend-vue/src/App.vue` - Layout principal avec router-view
3. `frontend-vue/src/components/NavigationBar.vue` - Barre de navigation
4. `frontend-vue/src/views/HomeView.vue` - Page d'accueil
5. `frontend-vue/src/views/WelcomeView.vue` - Page de connexion
6. `frontend-vue/src/views/DashboardView.vue` - Tableau de bord principal
7. `frontend-vue/src/views/TasksView.vue` - Gestion des tâches
8. `frontend-vue/src/views/PersonneAidantView.vue` - Vue PA
9. `frontend-vue/src/views/SegmentDashboardView.vue` - Dashboard segmenté
10. `frontend-vue/src/views/dashboards/ParticuliersDashboard.vue` - Dashboard particuliers

🎁 **Bonus : Logique de navigation par boutons** ✅

- Boutons de navigation principaux (Connexion, Inscription, Dashboard)
- Boutons de navigation spécialisés (Chat IA, Planning, etc.)
- Méthodes de navigation avec `router.push()` et `router.go()`

**Voilà ton canevas complet pour organiser la logique de navigation Vue.js ! 🚀**
