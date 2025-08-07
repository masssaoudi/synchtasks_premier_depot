# 🐳 Méthodologie de Test Docker - SynchTasks

## 📋 Vue d'ensemble
Cette méthodologie suit une approche systématique pour valider que votre application SynchTasks est correctement "embarquée" dans Docker et prête pour le développement.

## 🎯 Objectifs
- ✅ Vérifier la structure et la santé des conteneurs
- ✅ Valider la persistance des données
- ✅ Tester les communications inter-services
- ✅ S'assurer du bon fonctionnement du hot reload
- ✅ Valider les API et l'authentification
- ✅ Vérifier la robustesse de l'application

---

## 🧪 Phase 1: Test de Structure Docker

### 1.1 Vérification des conteneurs
```bash
# Vérifier que tous les conteneurs tournent
docker ps

# Résultat attendu :
# synchtasks-backend    (port 8000)
# synchtasks-frontend   (port 80)
# synchtasks-mongo      (port 27017)
# synchtasks-mongo-express (port 8081)
```

### 1.2 Vérification des services Docker Compose
```bash
docker compose ps
```

### 1.3 Inspection des conteneurs
```bash
# Vérifier les volumes, ports et réseaux
docker inspect synchtasks-backend
docker inspect synchtasks-mongo
```

---

## 🧪 Phase 2: Test de Persistance des Données

### 2.1 Test de création et persistance
1. **Créer une donnée** via l'application web
2. **Redémarrer les conteneurs** :
```bash
docker compose down
docker compose up -d
```
3. **Vérifier** que la donnée est toujours présente

### 2.2 Vérification des volumes
```bash
# Vérifier que le volume MongoDB est bien monté
docker volume ls | grep mongo_data
```

---

## 🧪 Phase 3: Test de Connexion Interne

### 3.1 Backend → MongoDB
Ajouter temporairement cette route dans `main.py` :

```python
@app.get("/ping-db")
async def ping_db():
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        await client.admin.command('ping')
        return {"status": "ok", "message": "MongoDB connection successful"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}
```

Tester avec :
```bash
curl http://localhost:8000/ping-db
```

### 3.2 Frontend → Backend
Dans le frontend Vue.js, ajouter un test de connexion :

```javascript
// Dans un composant ou service
axios.get("http://localhost:8000/ping-db")
  .then(res => console.log("✅ Backend API OK:", res.data))
  .catch(err => console.error("❌ Backend API KO:", err))
```

---

## 🧪 Phase 4: Test du Hot Reload

### 4.1 Backend Hot Reload
1. Modifier un fichier Python (ex: `main.py`)
2. Vérifier que uvicorn se relance automatiquement
3. Tester que les changements sont pris en compte

### 4.2 Frontend Hot Reload
1. Modifier un composant Vue.js
2. Vérifier que les changements se reflètent immédiatement dans le navigateur

---

## 🧪 Phase 5: Test des API

### 5.1 Tests des routes publiques
```bash
# Test de santé
curl http://localhost:8000/

# Test des tâches (si route publique)
curl http://localhost:8000/api/tasks

# Test de création d'utilisateur
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'
```

### 5.2 Tests d'authentification
```bash
# Test de login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'

# Extraire le token JWT de la réponse et tester une route protégée
curl -H "Authorization: Bearer <TOKEN_JWT>" \
  http://localhost:8000/api/tasks
```

---

## 🧪 Phase 6: Test CORS et Réseau

### 6.1 Vérification CORS
1. Ouvrir les DevTools du navigateur (F12)
2. Aller dans l'onglet Network
3. Effectuer des requêtes vers l'API
4. Vérifier qu'il n'y a pas d'erreurs CORS

### 6.2 Test de communication inter-conteneurs
```bash
# Tester depuis l'intérieur du conteneur backend
docker exec -it synchtasks-backend curl http://mongo:27017
```

---

## 🧪 Phase 7: Test JWT et Sécurité

### 7.1 Test complet du flow d'authentification
1. Créer un utilisateur
2. Se connecter et récupérer le token
3. Utiliser le token pour accéder aux routes protégées
4. Vérifier que les routes sans token sont refusées

### 7.2 Vérification du stockage des tokens
- Vérifier dans le localStorage du navigateur
- Tester la déconnexion et la suppression du token

---

## 🧪 Phase 8: Tests Unitaires et Intégration

### 8.1 Exécution des tests Python
```bash
# Depuis le conteneur backend
docker exec -it synchtasks-backend pytest tests/

# Ou depuis l'extérieur
docker compose exec backend pytest tests/
```

### 8.2 Tests spécifiques à vérifier
- Routes publiques
- Routes protégées
- Accès à la base de données
- Connexions WebSocket
- Validations Pydantic

---

## 🧪 Phase 9: Test de Robustesse Frontend

### 9.1 Test avec backend en panne
1. Arrêter le conteneur backend : `docker stop synchtasks-backend`
2. Tester l'interface utilisateur
3. Vérifier que les erreurs sont gérées gracieusement
4. Redémarrer le backend et vérifier la reconnexion

---

## 🧪 Phase 10: Test Docker Build Clean

### 10.1 Reconstruction complète
```bash
# Nettoyer complètement
docker compose down -v
docker system prune -f

# Reconstruire sans cache
docker compose build --no-cache

# Redémarrer
docker compose up -d
```

### 10.2 Vérification post-reconstruction
- Tous les services démarrent sans erreur
- Les données sont correctement initialisées
- L'application fonctionne normalement

---

## ✅ Critères de Succès

Votre application est considérée comme "embarquée" si :

1. **✅ Structure Docker** : Tous les conteneurs sont visibles et fonctionnels
2. **✅ Persistance** : Les données survivent aux redémarrages
3. **✅ Communication** : Front ↔ Back ↔ DB communiquent correctement
4. **✅ Hot Reload** : Les modifications se rechargent automatiquement
5. **✅ API** : Toutes les routes répondent correctement
6. **✅ CORS** : Aucune erreur de cross-origin
7. **✅ Sécurité** : JWT fonctionne correctement
8. **✅ Tests** : Tous les tests unitaires passent
9. **✅ Robustesse** : L'app gère les pannes gracieusement
10. **✅ Build** : Reconstruction complète sans erreur

---

## 🚀 Scripts d'Automatisation

### Script de test complet
```bash
#!/bin/bash
echo "🧪 Démarrage des tests Docker..."

# Phase 1: Structure
echo "1. Vérification de la structure Docker..."
docker ps
docker compose ps

# Phase 2: Persistance
echo "2. Test de persistance..."
# [Logique de test]

# Phase 3: Connexions
echo "3. Test des connexions..."
curl -f http://localhost:8000/ping-db || echo "❌ Backend → MongoDB KO"

# Phase 4: API
echo "4. Test des API..."
curl -f http://localhost:8000/ || echo "❌ API principale KO"

echo "✅ Tests terminés"
```

---

## 📝 Notes Importantes

- **Environnement** : Assurez-vous d'avoir un fichier `.env` correctement configuré
- **Ports** : Vérifiez que les ports 80, 8000, 27017, 8081 ne sont pas utilisés
- **Volumes** : Les données MongoDB sont persistées dans le volume `mongo_data`
- **Réseau** : Tous les services utilisent le réseau `synchtasks-network`

---

## 🔧 Dépannage Rapide

### Problèmes courants :
1. **Ports déjà utilisés** : `netstat -tulpn | grep :8000`
2. **Volumes corrompus** : `docker volume rm synchtasks_mongo_data`
3. **Images obsolètes** : `docker compose build --no-cache`
4. **Réseau Docker** : `docker network prune`

### Commandes utiles :
```bash
# Logs en temps réel
docker compose logs -f

# Accès au shell d'un conteneur
docker exec -it synchtasks-backend bash

# Nettoyage complet
docker compose down -v && docker system prune -f
``` 