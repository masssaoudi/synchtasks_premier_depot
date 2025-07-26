# 🐳 Dockerisation et Déploiement SyncTasks

Ce guide explique comment dockeriser et déployer l'application SyncTasks en utilisant Docker et Docker Compose.

## 📋 Prérequis

- Docker Desktop installé et en cours d'exécution
- Docker Compose installé
- Git (pour cloner le projet)

## 🚀 Déploiement Rapide

### Windows (PowerShell)
```powershell
# Déployer l'application
.\deploy.ps1

# Ou avec une commande spécifique
.\deploy.ps1 deploy
```

### Linux/macOS (Bash)
```bash
# Rendre le script exécutable
chmod +x deploy.sh

# Déployer l'application
./deploy.sh

# Ou avec une commande spécifique
./deploy.sh deploy
```

## 📦 Architecture Docker

L'application est composée de 4 services :

1. **Backend** (FastAPI) - Port 8000
2. **Frontend** (Vue.js) - Port 80
3. **MongoDB** - Port 27017
4. **Mongo Express** (Interface web MongoDB) - Port 8081

## 🔧 Commandes Disponibles

### Déploiement
```bash
# Déployer l'application complète
./deploy.sh deploy

# Construire uniquement les images
./deploy.sh build

# Mettre à jour l'application
./deploy.sh update
```

### Gestion
```bash
# Arrêter l'application
./deploy.sh stop

# Voir les logs en temps réel
./deploy.sh logs

# Vérifier la santé des services
./deploy.sh health

# Nettoyer les ressources Docker
./deploy.sh cleanup
```

### Aide
```bash
# Afficher l'aide
./deploy.sh help
```

## 🌐 Accès aux Services

Une fois déployée, l'application sera accessible aux adresses suivantes :

- **Frontend** : http://localhost:80
- **Backend API** : http://localhost:8000
- **Mongo Express** : http://localhost:8081
- **MongoDB** : localhost:27017

## 📁 Structure des Fichiers

```
SynchTasks/
├── Dockerfile                 # Backend Dockerfile
├── docker-compose.yml         # Configuration multi-services
├── deploy.sh                  # Script de déploiement (Linux/macOS)
├── deploy.ps1                 # Script de déploiement (Windows)
├── .env                       # Variables d'environnement (créé automatiquement)
├── frontend-vue/
│   ├── Dockerfile            # Frontend Dockerfile
│   └── nginx.conf            # Configuration Nginx
└── mongo-init/               # Scripts d'initialisation MongoDB
```

## ⚙️ Configuration

### Variables d'Environnement

Le script crée automatiquement un fichier `.env` avec les configurations suivantes :

```env
# Configuration SyncTasks
MONGODB_URL=mongodb://mongo:27017/synchtasks_db
JWT_SECRET=your-super-secret-jwt-key-change-in-production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Configuration Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Configuration MongoDB
MONGO_INITDB_DATABASE=synchtasks_db
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123

# Configuration Mongo Express
ME_CONFIG_MONGODB_SERVER=mongo
ME_CONFIG_MONGODB_PORT=27017
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=admin123
```

### Personnalisation

Pour personnaliser le déploiement, modifiez les variables dans les scripts :

```bash
# Dans deploy.sh ou deploy.ps1
APP_NAME="synchtasks"
VERSION="1.0.0"
DOCKER_REGISTRY=""  # Ajoutez votre registry Docker
```

## 🔍 Monitoring et Debugging

### Vérifier l'état des services
```bash
# Vérifier tous les services
./deploy.sh health

# Voir les logs en temps réel
./deploy.sh logs

# Voir les logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongo
```

### Accéder aux conteneurs
```bash
# Accéder au backend
docker-compose exec backend bash

# Accéder à MongoDB
docker-compose exec mongo mongosh

# Accéder au frontend
docker-compose exec frontend sh
```

## 🛠️ Déploiement Manuel

Si vous préférez déployer manuellement :

```bash
# 1. Créer le fichier .env
cp .env.example .env

# 2. Construire les images
docker build -t synchtasks-backend:1.0.0 .
docker build -t synchtasks-frontend:1.0.0 ./frontend-vue

# 3. Démarrer les services
docker-compose up -d

# 4. Vérifier l'état
docker-compose ps
```

## 🔄 Mise à Jour

Pour mettre à jour l'application :

```bash
# Mise à jour automatique
./deploy.sh update

# Ou manuellement
docker-compose down
docker-compose pull  # Si vous utilisez un registry
docker-compose up -d --build
```

## 🧹 Nettoyage

Pour nettoyer les ressources Docker :

```bash
# Nettoyage complet
./deploy.sh cleanup

# Ou manuellement
docker-compose down --volumes --remove-orphans
docker system prune -f
```

## 🚨 Dépannage

### Problèmes Courants

1. **Ports déjà utilisés**
   ```bash
   # Vérifier les ports utilisés
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :80
   
   # Arrêter les services qui utilisent ces ports
   sudo systemctl stop apache2  # Si Apache utilise le port 80
   ```

2. **MongoDB ne démarre pas**
   ```bash
   # Vérifier les logs MongoDB
   docker-compose logs mongo
   
   # Supprimer le volume et redémarrer
   docker-compose down -v
   docker-compose up -d
   ```

3. **Frontend ne se connecte pas au backend**
   ```bash
   # Vérifier la configuration VITE_API_URL dans .env
   # Vérifier que le backend répond
   curl http://localhost:8000/health
   ```

### Logs Détaillés

```bash
# Logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongo

# Logs en temps réel
docker-compose logs -f
```

## 🔒 Sécurité

### Production

Pour un déploiement en production :

1. **Changer les mots de passe par défaut**
   ```env
   JWT_SECRET=votre-super-secret-jwt-key-tres-long-et-complexe
   MONGO_INITDB_ROOT_PASSWORD=votre-mot-de-passe-mongo-complexe
   ME_CONFIG_BASICAUTH_PASSWORD=votre-mot-de-passe-mongo-express
   ```

2. **Utiliser HTTPS**
   - Configurer un reverse proxy (Nginx/Traefik)
   - Ajouter des certificats SSL

3. **Restreindre l'accès réseau**
   - Ne pas exposer MongoDB directement
   - Utiliser des réseaux Docker internes

4. **Backup automatique**
   ```bash
   # Script de backup MongoDB
   docker-compose exec mongo mongodump --out /backup/$(date +%Y%m%d)
   ```

## 📊 Monitoring

### Health Checks

L'application inclut des health checks automatiques :

- **Backend** : `http://localhost:8000/health`
- **Frontend** : `http://localhost:80/`
- **MongoDB** : Ping MongoDB

### Métriques

Pour ajouter du monitoring :

```yaml
# Dans docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

## 🎯 Prochaines Étapes

1. **CI/CD Pipeline** : Automatiser le déploiement
2. **Monitoring** : Ajouter Prometheus/Grafana
3. **Backup** : Automatiser les sauvegardes
4. **Scaling** : Configurer le load balancing
5. **Security** : Audit de sécurité complet

---

## 📞 Support

Pour toute question ou problème :

1. Vérifiez les logs : `./deploy.sh logs`
2. Consultez ce guide de dépannage
3. Ouvrez une issue sur le repository

**Happy Deploying! 🚀** 