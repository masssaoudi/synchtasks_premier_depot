# 🏗️ STRUCTURE LOGIQUE SYNC TASKS

## 🎯 **FLUX UTILISATEUR LOGIQUE**

### 1. **ARRIVÉE SUR L'APPLICATION**
```
Page d'accueil (/)
├── Découverte de l'application
├── Présentation des fonctionnalités
└── Choix : Se connecter OU Créer un compte
```

### 2. **AUTHENTIFICATION**
```
Login (/login)
├── Formulaire de connexion classique
├── Connexion Google OAuth
└── Lien vers inscription

Inscription (/register)
├── Formulaire d'inscription complet
├── Inscription Google OAuth
└── Lien vers connexion
```

### 3. **PREMIÈRE CONNEXION**
```
Sélection de profil (/segment-selection)
├── Choix du segment (Particuliers, Étudiants, etc.)
├── Configuration initiale
└── Redirection vers dashboard spécialisé
```

### 4. **UTILISATION NORMALE**
```
Dashboard spécialisé (/dashboard/[segment])
├── Interface adaptée au segment
├── Gestion des tâches
├── IA spécialisée
└── Navigation vers autres fonctionnalités
```

## 📁 **STRUCTURE DES DOSSIERS**

```
frontend-vue/
├── src/
│   ├── views/
│   │   ├── auth/
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   └── AuthCallback.vue
│   │   ├── onboarding/
│   │   │   ├── WelcomeView.vue
│   │   │   └── SegmentSelectionView.vue
│   │   ├── dashboard/
│   │   │   ├── DashboardView.vue
│   │   │   └── segments/
│   │   │       ├── ParticuliersDashboard.vue
│   │   │       ├── EtudiantsDashboard.vue
│   │   │       └── ...
│   │   └── tasks/
│   │       └── TasksView.vue
│   ├── components/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   └── tasks/
│   ├── stores/
│   │   ├── auth.js
│   │   ├── segments.js
│   │   └── tasks.js
│   └── services/
│       ├── auth.js
│       ├── api.js
│       └── googleAuth.js
```

## 🛣️ **ROUTES LOGIQUES**

```javascript
const routes = [
  // 1. ACCUEIL
  { path: '/', component: HomeView },
  
  // 2. AUTHENTIFICATION
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/auth/callback', component: AuthCallback },
  
  // 3. ONBOARDING
  { path: '/welcome', component: WelcomeView },
  { path: '/segment-selection', component: SegmentSelectionView },
  
  // 4. DASHBOARDS SPÉCIALISÉS
  { path: '/dashboard/particuliers', component: ParticuliersDashboard },
  { path: '/dashboard/etudiants', component: EtudiantsDashboard },
  { path: '/dashboard/medical', component: MedicalDashboard },
  { path: '/dashboard/memoire', component: MemoireDashboard },
  { path: '/dashboard/professionnels', component: ProfessionnelsDashboard },
  { path: '/dashboard/entreprises', component: EntreprisesDashboard },
  
  // 5. FONCTIONNALITÉS
  { path: '/tasks', component: TasksView },
  { path: '/pa-dashboard', component: PADashboardView },
]
```

## 🔄 **FLUX D'ÉTATS**

### **ÉTAT 1 : Visiteur**
- Peut voir la page d'accueil
- Peut se connecter ou s'inscrire

### **ÉTAT 2 : Utilisateur connecté sans profil**
- Redirigé vers sélection de segment
- Doit choisir un profil

### **ÉTAT 3 : Utilisateur avec profil**
- Accès au dashboard spécialisé
- Navigation complète

## 🎨 **PRINCIPES DE DESIGN**

### **1. Cohérence visuelle**
- Design system unifié
- Couleurs par segment
- Composants réutilisables

### **2. Expérience utilisateur**
- Navigation intuitive
- Feedback immédiat
- États de chargement

### **3. Responsive design**
- Mobile-first
- Adaptatif par segment
- Accessibilité

## 🚀 **PLAN DE MIGRATION**

### **Phase 1 : Nettoyage**
1. Réorganiser les fichiers
2. Supprimer les doublons
3. Standardiser les noms

### **Phase 2 : Restructuration**
1. Créer la nouvelle structure
2. Migrer les composants
3. Mettre à jour les routes

### **Phase 3 : Amélioration**
1. Optimiser les performances
2. Améliorer l'UX
3. Tests complets 