# 🐳 Guide de Test Docker - SynchTasks

## 📋 Vue d'ensemble

Ce guide vous accompagne dans la validation complète de votre application SynchTasks embarquée dans Docker. Il suit une méthodologie structurée en 10 phases pour s'assurer que votre application est prête pour le développement et la production.

## 🚀 Démarrage Rapide

### Option 1: Script Automatisé (Recommandé)
```bash
# Démarrage et test automatique
python start_and_test.py
```

### Option 2: Tests Manuels
```bash
# 1. Démarrer l'application
docker compose up -d

# 2. Lancer les tests
python test_docker_deployment.py
```

## 📚 Documentation Complète

### 📖 Méthodologie Détaillée
- **`METHODOLOGIE_DOCKER_TEST.md`** : Guide complet avec toutes les phases de test
- **`test_docker_deployment.py`** : Script automatisé de test
- **`start_and_test.py`** : Script de démarrage et test automatique

## 🧪 Phases de Test

### Phase 1: Structure Docker ✅
- Vérification des conteneurs
- Inspection des services
- Validation de la configuration

### Phase 2: Persistance des Données ✅
- Test des volumes MongoDB
- Validation de la persistance
- Vérification des données

### Phase 3: Connexions Inter-services ✅
- Backend → MongoDB
- Frontend → Backend
- Communication inter-conteneurs

### Phase 4: Hot Reload ✅
- Backend (uvicorn --reload)
- Frontend (Vue.js dev server)
- Validation des modifications

### Phase 5: API ✅
- Routes publiques
- Documentation FastAPI
- Endpoints d'authentification

### Phase 6: CORS et Réseau ✅
- Configuration CORS
- Communication inter-conteneurs
- Gestion des erreurs réseau

### Phase 7: JWT et Sécurité ✅
- Configuration JWT
- Authentification
- Gestion des tokens

### Phase 8: Tests Unitaires ✅
- Exécution pytest
- Validation des routes
- Tests d'intégration

### Phase 9: Robustesse ✅
- Healthchecks
- Gestion des pannes
- Récupération automatique

### Phase 10: Build Clean ✅
- Reconstruction complète
- Validation de la configuration
- Tests de déploiement

## 🔧 Outils Disponibles

### Scripts Automatisés
1. **`start_and_test.py`** : Démarrage + test complet
2. **`test_docker_deployment.py`** : Tests automatisés uniquement
3. **`METHODOLOGIE_DOCKER_TEST.md`** : Guide manuel détaillé

### Commandes Utiles
```bash
# Vérification rapide
docker ps
docker compose ps

# Logs en temps réel
docker compose logs -f

# Tests manuels
curl http://localhost:8000/ping-db
curl http://localhost:8000/health

# Nettoyage complet
docker compose down -v
docker system prune -f
```

## 📊 Critères de Succès

Votre application est considérée comme "embarquée" si :

✅ **Structure Docker** : Tous les conteneurs sont visibles et fonctionnels  
✅ **Persistance** : Les données survivent aux redémarrages  
✅ **Communication** : Front ↔ Back ↔ DB communiquent correctement  
✅ **Hot Reload** : Les modifications se rechargent automatiquement  
✅ **API** : Toutes les routes répondent correctement  
✅ **CORS** : Aucune erreur de cross-origin  
✅ **Sécurité** : JWT fonctionne correctement  
✅ **Tests** : Tous les tests unitaires passent  
✅ **Robustesse** : L'app gère les pannes gracieusement  
✅ **Build** : Reconstruction complète sans erreur  

## 🌐 Accès aux Services

Une fois l'application démarrée :

- **Frontend** : http://localhost
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Mongo Express** : http://localhost:8081

## 🚨 Dépannage

### Problèmes Courants

1. **Ports déjà utilisés**
   ```bash
   netstat -tulpn | grep :8000
   ```

2. **Volumes corrompus**
   ```bash
   docker volume rm synchtasks_mongo_data
   ```

3. **Images obsolètes**
   ```bash
   docker compose build --no-cache
   ```

4. **Réseau Docker**
   ```bash
   docker network prune
   ```

### Logs de Diagnostic
```bash
# Logs de tous les services
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f mongo
```

## 📝 Rapports de Test

Le script de test génère automatiquement :
- **`docker_test_report.json`** : Rapport détaillé des tests
- **Logs en temps réel** : Affichage des résultats
- **Résumé final** : Statut global de l'application

## 🔄 Workflow de Développement

1. **Démarrage** : `python start_and_test.py`
2. **Développement** : Modifications avec hot reload
3. **Test** : `python test_docker_deployment.py`
4. **Validation** : Vérification des critères de succès
5. **Déploiement** : Prêt pour la production

## 📞 Support

En cas de problème :
1. Consultez les logs : `docker compose logs -f`
2. Vérifiez la méthodologie : `METHODOLOGIE_DOCKER_TEST.md`
3. Lancez les tests : `python test_docker_deployment.py`
4. Consultez le dépannage dans ce guide

---

**🎯 Objectif** : S'assurer que votre application SynchTasks est parfaitement "embarquée" et prête pour un développement fluide et sécurisé. 