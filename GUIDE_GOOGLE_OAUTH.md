# 🔐 GUIDE CONFIGURATION GOOGLE OAUTH

## 📋 **ÉTAPES DE CONFIGURATION**

### 1. **Créer un projet Google Cloud Console**

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API Google+ API

### 2. **Configurer les identifiants OAuth**

1. Dans Google Cloud Console, allez dans **APIs & Services** > **Credentials**
2. Cliquez sur **Create Credentials** > **OAuth 2.0 Client IDs**
3. Sélectionnez **Web application**
4. Configurez les URLs autorisées :
   - **Authorized JavaScript origins** : `http://localhost:3000`
   - **Authorized redirect URIs** : `http://localhost:3000/auth/google/callback`

### 3. **Variables d'environnement**

Créez un fichier `.env` à la racine du projet avec :

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=synchtasks_db

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=True

# Security
SECRET_KEY=synchtasks-dev-secret-key-2024-change-in-production-very-long-secure-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth Configuration
GOOGLE_CLIENT_ID=votre_client_id_google
GOOGLE_CLIENT_SECRET=votre_client_secret_google
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback
```

### 4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

### 5. **Démarrer l'application**

```bash
# Backend
python main.py

# Frontend (dans un autre terminal)
cd frontend-vue
npm run dev
```

## 🧪 **TEST DE LA CONNEXION GOOGLE**

### 1. **Vérifier la configuration**

- ✅ Variables d'environnement configurées
- ✅ Backend démarré sur le port 8001
- ✅ Frontend démarré sur le port 3000
- ✅ Google Cloud Console configuré

### 2. **Tester la connexion**

1. Allez sur `http://localhost:3000/login`
2. Cliquez sur "Continuer avec Google"
3. Une popup Google s'ouvre
4. Connectez-vous avec votre compte Google
5. Vous devriez être redirigé vers la sélection de segment

## 🔧 **DÉPANNAGE**

### Erreur "Invalid redirect_uri"

- Vérifiez que l'URL de redirection dans Google Console correspond exactement à `http://localhost:3000/auth/google/callback`
- Assurez-vous qu'il n'y a pas d'espaces ou de caractères supplémentaires

### Erreur "Client ID not found"

- Vérifiez que `GOOGLE_CLIENT_ID` est correctement défini dans le fichier `.env`
- Redémarrez le serveur après modification du fichier `.env`

### Popup bloquée

- Autorisez les popups pour `localhost:3000`
- Vérifiez que le bloqueur de popups est désactivé

### Erreur CORS

- Vérifiez que le frontend est bien sur `http://localhost:3000`
- Vérifiez la configuration CORS dans `main.py`

## 📁 **FICHIERS MODIFIÉS**

### Backend
- ✅ `config.py` - Variables Google OAuth
- ✅ `google_oauth_routes.py` - Routes OAuth Google
- ✅ `main.py` - Intégration du router Google
- ✅ `requirements.txt` - Dépendances Google

### Frontend
- ✅ `frontend-vue/src/services/googleAuth.js` - Service Google OAuth
- ✅ `frontend-vue/src/views/GoogleCallbackView.vue` - Page de callback
- ✅ `frontend-vue/src/views/WelcomeView.vue` - Bouton Google fonctionnel
- ✅ `frontend-vue/src/stores/auth.js` - Méthode loginWithGoogle
- ✅ `frontend-vue/src/router/index.js` - Route callback

## 🎯 **FONCTIONNALITÉS IMPLÉMENTÉES**

### ✅ **Authentification Google OAuth**
- Connexion avec Google
- Création automatique de compte
- Gestion des utilisateurs existants
- Token JWT après OAuth

### ✅ **Interface utilisateur**
- Bouton Google fonctionnel
- Spinner de chargement
- Gestion des erreurs
- Popup d'authentification

### ✅ **Sécurité**
- Validation des tokens Google
- Gestion sécurisée des callbacks
- Intégration avec le système JWT existant

## 🚀 **PROCHAINES ÉTAPES**

1. **Tester la connexion Google** avec de vrais identifiants
2. **Implémenter Microsoft OAuth** (optionnel)
3. **Ajouter le bouton "Mot de passe oublié"**
4. **Développer le Dashboard Particulier**
5. **Implémenter le mode PA (Personne Aidante)**

---

**État :** 🟢 **Google OAuth implémenté**  
**Priorité :** 🔥 **Haute** - Test avec vrais identifiants  
**Complexité :** ⭐ **Faible** - Configuration Google Console  
**Valeur business :** 🚀 **Énorme** - UX améliorée 