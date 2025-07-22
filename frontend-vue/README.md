# SyncTasks Frontend Vue.js

Frontend moderne pour l'application SyncTasks, développé avec Vue.js 3, Vite et Pinia.

## 🚀 Fonctionnalités

- **Interface moderne** : Design responsive et intuitif
- **Authentification** : Système de connexion/inscription complet
- **Gestion des tâches** : Tableau Kanban interactif
- **Dashboard** : Statistiques et métriques de productivité
- **Navigation fluide** : Routing avec Vue Router
- **État global** : Gestion d'état avec Pinia

## 📁 Structure du projet

```
frontend-vue/
├── src/
│   ├── views/           # Pages principales
│   │   ├── HomeView.vue
│   │   ├── LoginView.vue
│   │   ├── TasksView.vue
│   │   └── DashboardView.vue
│   ├── stores/          # Stores Pinia
│   │   └── auth.js
│   ├── router/          # Configuration des routes
│   │   └── index.js
│   ├── App.vue          # Composant racine
│   ├── main.js          # Point d'entrée
│   └── style.css        # Styles globaux
├── index.html
├── package.json
├── vite.config.js
└── tsconfig.json
```

## 🛠️ Installation et démarrage

### Prérequis
- Node.js 16+ 
- npm ou yarn

### Installation des dépendances
```bash
cd frontend-vue
npm install
```

### Démarrage en mode développement
```bash
npm run dev
```

L'application sera accessible sur `http://localhost:3000`

### Build pour la production
```bash
npm run build
```

### Prévisualisation du build
```bash
npm run preview
```

## 🔧 Configuration

### Proxy API
Le frontend est configuré pour rediriger les appels API vers le backend Flask sur `http://localhost:8000` via le proxy Vite.

### Variables d'environnement
Créez un fichier `.env` à la racine du projet frontend-vue :

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📱 Pages disponibles

### 🏠 Accueil (`/`)
- Vue d'ensemble de l'application
- Statistiques rapides
- Accès aux fonctionnalités principales

### 🔐 Connexion (`/login`)
- Formulaire de connexion
- Formulaire d'inscription
- Mode démo pour tester l'application

### 📋 Tâches (`/tasks`)
- Tableau Kanban avec 3 colonnes : À faire, En cours, Terminé
- Création de nouvelles tâches
- Gestion des priorités et dates d'échéance
- Interface drag & drop (à implémenter)

### 📊 Dashboard (`/dashboard`)
- Statistiques détaillées
- Graphiques de progression
- Activité récente
- Conseils IA et objectifs

## 🎨 Design System

### Couleurs principales
- **Primaire** : `#667eea` (Bleu-violet)
- **Secondaire** : `#764ba2` (Violet)
- **Succès** : `#28a745` (Vert)
- **Avertissement** : `#ffc107` (Jaune)
- **Danger** : `#dc3545` (Rouge)

### Composants réutilisables
- Boutons (`.btn`, `.btn-primary`, `.btn-secondary`)
- Cartes (`.card`)
- Formulaires (`.form-group`)
- Alertes (`.alert`, `.alert-success`, `.alert-error`)

## 🔌 Intégration API

### Endpoints utilisés
- `POST /api/auth/login` - Connexion
- `POST /api/auth/register` - Inscription
- `GET /api/auth/me` - Informations utilisateur
- `GET /api/tasks` - Liste des tâches
- `POST /api/tasks` - Création de tâche
- `PUT /api/tasks/:id` - Modification de tâche
- `DELETE /api/tasks/:id` - Suppression de tâche

### Gestion des erreurs
- Interception automatique des erreurs 401 (redirection vers login)
- Affichage des messages d'erreur utilisateur
- Gestion des timeouts et erreurs réseau

## 🧪 Tests

### Tests unitaires
```bash
npm run test:unit
```

### Tests d'intégration
```bash
npm run test:integration
```

## 📦 Déploiement

### Build de production
```bash
npm run build
```

Les fichiers de production seront générés dans le dossier `dist/`.

### Variables d'environnement de production
```env
VITE_API_BASE_URL=https://api.synchtasks.com
```

## 🔄 Développement

### Ajout d'une nouvelle page
1. Créer le composant Vue dans `src/views/`
2. Ajouter la route dans `src/router/index.js`
3. Ajouter le lien dans la navigation si nécessaire

### Ajout d'un nouveau store Pinia
1. Créer le fichier dans `src/stores/`
2. Utiliser `defineStore` avec la Composition API
3. Importer et utiliser dans les composants

### Styles
- Utiliser les classes CSS globales définies dans `src/style.css`
- Ajouter des styles scoped dans chaque composant
- Respecter la palette de couleurs du design system

## 🐛 Dépannage

### Erreur de proxy API
- Vérifier que le backend Flask est démarré sur le port 8000
- Vérifier la configuration dans `vite.config.js`

### Erreurs de build
- Vérifier les dépendances : `npm install`
- Nettoyer le cache : `npm run clean`
- Vérifier la configuration TypeScript

### Problèmes de routing
- Vérifier la configuration dans `src/router/index.js`
- S'assurer que les composants sont correctement importés

## 📚 Ressources

- [Vue.js 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vue Router Documentation](https://router.vuejs.org/) 