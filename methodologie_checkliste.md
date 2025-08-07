# 🐳 Méthodologie Checklist - SynchTasks Docker

## 📋 Vue d'ensemble
Cette checklist vous guide étape par étape pour valider que votre application SynchTasks est correctement "embarquée" dans Docker.

---

## ✅ Phase 1: Test de Structure Docker

### 1.1 Vérification des conteneurs
- [ ] Exécuter `docker ps`
- [ ] Vérifier la présence de :
  - [ ] `synchtasks-backend` (port 8000)
  - [ ] `synchtasks-frontend` (port 80)
  - [ ] `synchtasks-mongo` (port 27017)
  - [ ] `synchtasks-mongo-express` (port 8081)

### 1.2 Vérification des services Docker Compose
- [ ] Exécuter `docker compose ps`
- [ ] Vérifier que tous les services sont "Up"

### 1.3 Inspection des conteneurs
- [ ] Exécuter `docker inspect synchtasks-backend`
- [ ] Vérifier les volumes, ports et réseaux

**Résultat Phase 1** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 2: Test de Persistance des Données

### 2.1 Vérification des volumes
- [ ] Exécuter `docker volume ls | grep mongo_data`
- [ ] Vérifier que le volume MongoDB est présent

### 2.2 Test de création et persistance
- [ ] Créer une tâche ou un utilisateur via l'application web
- [ ] Exécuter `docker compose down`
- [ ] Exécuter `docker compose up -d`
- [ ] Vérifier que la donnée est toujours présente

**Résultat Phase 2** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 3: Test de Connexion Interne

### 3.1 Backend → MongoDB
- [ ] Exécuter `curl http://localhost:8000/ping-db`
- [ ] Vérifier la réponse : `{"status": "ok", "message": "MongoDB connection successful"}`

### 3.2 Frontend → Backend
- [ ] Exécuter `curl http://localhost:8000/`
- [ ] Vérifier que l'API répond correctement

### 3.3 Communication inter-conteneurs
- [ ] Exécuter `docker exec -it synchtasks-backend ping -c 1 mongo`
- [ ] Vérifier que la communication fonctionne

**Résultat Phase 3** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 4: Test du Hot Reload

### 4.1 Backend Hot Reload
- [ ] Vérifier que uvicorn est lancé avec `--reload`
- [ ] Modifier un fichier Python (ex: `main.py`)
- [ ] Vérifier que le serveur se relance automatiquement

### 4.2 Frontend Hot Reload
- [ ] Modifier un composant Vue.js
- [ ] Vérifier que les changements se reflètent immédiatement dans le navigateur

**Résultat Phase 4** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 5: Test des API

### 5.1 Routes publiques
- [ ] Exécuter `curl http://localhost:8000/`
- [ ] Exécuter `curl http://localhost:8000/docs`
- [ ] Vérifier que les routes répondent avec un statut 200

### 5.2 Routes d'authentification
- [ ] Tester la création d'utilisateur via l'API
- [ ] Tester la connexion utilisateur
- [ ] Vérifier la gestion des tokens JWT

**Résultat Phase 5** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 6: Test CORS et Réseau

### 6.1 Vérification CORS
- [ ] Ouvrir les DevTools du navigateur (F12)
- [ ] Aller dans l'onglet Network
- [ ] Effectuer des requêtes vers l'API
- [ ] Vérifier qu'il n'y a pas d'erreurs CORS

### 6.2 Test de communication inter-conteneurs
- [ ] Vérifier que les conteneurs peuvent communiquer entre eux
- [ ] Tester la résolution DNS interne

**Résultat Phase 6** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 7: Test JWT et Sécurité

### 7.1 Configuration JWT
- [ ] Vérifier que `JWT_SECRET` est configuré
- [ ] Exécuter `docker exec -it synchtasks-backend env | grep JWT_SECRET`

### 7.2 Test d'authentification
- [ ] Créer un utilisateur
- [ ] Se connecter et récupérer le token
- [ ] Utiliser le token pour accéder aux routes protégées
- [ ] Vérifier que les routes sans token sont refusées

**Résultat Phase 7** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 8: Tests Unitaires et Intégration

### 8.1 Exécution des tests Python
- [ ] Exécuter `docker compose exec backend pytest tests/ -v`
- [ ] Vérifier que tous les tests passent

### 8.2 Tests spécifiques
- [ ] Routes publiques
- [ ] Routes protégées
- [ ] Accès à la base de données
- [ ] Connexions WebSocket
- [ ] Validations Pydantic

**Résultat Phase 8** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 9: Test de Robustesse

### 9.1 Vérification des healthchecks
- [ ] Exécuter `docker ps --format 'table {{.Names}}\t{{.Status}}' | grep synchtasks`
- [ ] Vérifier que les conteneurs sont "healthy" ou "Up"

### 9.2 Test avec backend en panne
- [ ] Arrêter le conteneur backend : `docker stop synchtasks-backend`
- [ ] Tester l'interface utilisateur
- [ ] Vérifier que les erreurs sont gérées gracieusement
- [ ] Redémarrer le backend et vérifier la reconnexion

**Résultat Phase 9** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## ✅ Phase 10: Test Docker Build Clean

### 10.1 Vérification des images
- [ ] Exécuter `docker images | grep synchtasks`
- [ ] Vérifier que les images sont présentes

### 10.2 Vérification de la configuration
- [ ] Exécuter `docker compose config`
- [ ] Vérifier que la configuration est valide

### 10.3 Reconstruction complète
- [ ] Exécuter `docker compose down -v`
- [ ] Exécuter `docker system prune -f`
- [ ] Exécuter `docker compose build --no-cache`
- [ ] Exécuter `docker compose up -d`
- [ ] Vérifier que tout fonctionne après reconstruction

**Résultat Phase 10** : [ ] ✅ Réussi / [ ] ❌ Échec

---

## 📊 Résumé Final

### Comptage des phases réussies :
- Phase 1 : [ ] ✅ / [ ] ❌
- Phase 2 : [ ] ✅ / [ ] ❌
- Phase 3 : [ ] ✅ / [ ] ❌
- Phase 4 : [ ] ✅ / [ ] ❌
- Phase 5 : [ ] ✅ / [ ] ❌
- Phase 6 : [ ] ✅ / [ ] ❌
- Phase 7 : [ ] ✅ / [ ] ❌
- Phase 8 : [ ] ✅ / [ ] ❌
- Phase 9 : [ ] ✅ / [ ] ❌
- Phase 10 : [ ] ✅ / [ ] ❌

**Total : ___/10 phases réussies**

### 🎯 Critères de Succès Final :

- [ ] **10/10 phases réussies** → 🎉 Application parfaitement embarquée !
- [ ] **8-9/10 phases réussies** → ⚠️ Quelques ajustements nécessaires
- [ ] **< 8/10 phases réussies** → ❌ Vérification de la configuration requise

---

## 🚀 Commandes Utiles

### Démarrage rapide :
```bash
# Option 1: Script automatisé
python start_and_test.py

# Option 2: Manuel
docker compose up -d
python test_docker_deployment.py
```

### Diagnostic :
```bash
# Logs en temps réel
docker compose logs -f

# Statut des conteneurs
docker ps

# Test rapide de l'API
curl http://localhost:8000/ping-db
```

### Nettoyage :
```bash
# Arrêt complet
docker compose down -v

# Nettoyage système
docker system prune -f
```

---

## 📝 Notes

- **Date du test** : _______________
- **Testeur** : _______________
- **Version Docker** : _______________
- **Observations** : _______________

---

**🎯 Objectif** : S'assurer que SynchTasks est parfaitement "embarquée" et prête pour le développement ! 