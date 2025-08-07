# 🧪 GUIDE DE TEST - NOTIFICATIONS TEMPS RÉEL

## 🎯 **OBJECTIF**
Tester l'intégration complète des notifications temps réel avec optimisations de performance.

## 🚀 **PRÉREQUIS**
- Serveur backend démarré sur le port 8001
- Frontend Vue.js accessible
- WebSocket fonctionnel

## 📋 **ÉTAPES DE TEST**

### **1. 🔧 Vérification du Backend**

```bash
# Vérifier que le serveur répond
curl http://localhost:8001/api/ws/health

# Vérifier les stats WebSocket
curl http://localhost:8001/api/ws/stats

# Vérifier la santé générale
curl http://localhost:8001/health
```

**Résultat attendu :**
```json
{
  "success": true,
  "status": "healthy",
  "connected_users": 0,
  "active_rooms": 0
}
```

### **2. 🔌 Test WebSocket Simple**

```bash
# Lancer le test WebSocket
python test_websocket_simple.py
```

**Résultat attendu :**
```
✅ WebSocket connecté
📤 Ping envoyé
📥 Pong reçu: {'type': 'pong', 'timestamp': 123456789}
✅ Test WebSocket réussi !
```

### **3. 🔔 Test Notifications Temps Réel**

```bash
# Lancer le test complet des notifications
python test_notifications_realtime.py
```

**Résultat attendu :**
```
✅ Serveur WebSocket accessible
✅ WebSocket connecté
📤 Ping envoyé
📥 Pong reçu: {'type': 'pong', 'timestamp': 1754468148431}
📤 Notification création tâche envoyée
📤 Notification mise à jour tâche envoyée
📤 Notification utilisateur connecté envoyée
📤 Notification monitoring PA envoyée
✅ Test notifications temps réel réussi !
```

### **4. 🌐 Test Interface Utilisateur**

#### **4.1 Démarrer le Frontend**
```bash
cd frontend-vue
npm run dev
```

#### **4.2 Tester les Notifications**
1. **Ouvrir l'application** : `http://localhost:3000`
2. **Se connecter** avec un utilisateur test
3. **Vérifier le panel notifications** :
   - Cliquer sur l'icône 🔔 dans la barre de navigation
   - Vérifier que le panel s'ouvre
   - Vérifier le statut WebSocket (connecté/déconnecté)

#### **4.3 Tester les Actions Temps Réel**
1. **Créer une tâche** :
   - Créer une nouvelle tâche
   - Vérifier qu'une notification apparaît
   - Vérifier que la tâche apparaît dans la liste

2. **Modifier une tâche** :
   - Modifier le titre ou le statut d'une tâche
   - Vérifier qu'une notification de mise à jour apparaît

3. **Supprimer une tâche** :
   - Supprimer une tâche
   - Vérifier qu'une notification de suppression apparaît

#### **4.4 Tester les Notifications Multi-utilisateurs**
1. **Ouvrir un second onglet** avec l'application
2. **Se connecter avec un autre utilisateur**
3. **Créer/modifier des tâches** dans le second onglet
4. **Vérifier** que les notifications apparaissent dans le premier onglet

### **5. ⚡ Test des Optimisations de Performance**

#### **5.1 Vérifier les Métriques**
- Ouvrir les DevTools (F12)
- Aller dans l'onglet Performance
- Enregistrer une session d'utilisation
- Vérifier les temps de chargement et l'utilisation mémoire

#### **5.2 Tester le Mode Économie d'Énergie**
```javascript
// Dans la console du navigateur
// Simuler un appareil en mode économie d'énergie
navigator.getBattery().then(battery => {
  console.log('Niveau batterie:', battery.level);
  console.log('En charge:', battery.charging);
});
```

#### **5.3 Tester le Lazy Loading**
- Vérifier que les images se chargent progressivement
- Vérifier que les composants se chargent à la demande

## 🎯 **CRITÈRES DE SUCCÈS**

### ✅ **Backend**
- [ ] Serveur répond sur le port 8001
- [ ] WebSocket accepte les connexions
- [ ] Messages ping/pong fonctionnent
- [ ] Notifications sont diffusées correctement

### ✅ **Frontend**
- [ ] Panel de notifications s'ouvre/ferme
- [ ] Notifications apparaissent en temps réel
- [ ] Badge de notifications fonctionne
- [ ] Statut WebSocket affiché correctement

### ✅ **Performance**
- [ ] Temps de chargement < 2 secondes
- [ ] Utilisation mémoire stable
- [ ] Animations fluides
- [ ] Mode économie d'énergie détecté

### ✅ **Notifications**
- [ ] Notifications de création de tâches
- [ ] Notifications de modification de tâches
- [ ] Notifications de suppression de tâches
- [ ] Notifications de connexion utilisateur
- [ ] Notifications de monitoring PA

## 🐛 **DÉPANNAGE**

### **Problème : WebSocket ne se connecte pas**
```bash
# Vérifier que le serveur tourne
curl http://localhost:8001/health

# Vérifier les logs du serveur
# Redémarrer le serveur si nécessaire
python main.py
```

### **Problème : Notifications n'apparaissent pas**
1. Vérifier la console du navigateur pour les erreurs
2. Vérifier que le WebSocket est connecté
3. Vérifier que le store de notifications est initialisé

### **Problème : Performance lente**
1. Vérifier les métriques dans DevTools
2. Activer le mode économie d'énergie
3. Vérifier la connexion réseau

## 📊 **MÉTRIQUES À SURVEILLER**

- **Temps de réponse WebSocket** : < 100ms
- **Temps de chargement initial** : < 2s
- **Utilisation mémoire** : < 100MB
- **FPS** : > 60fps
- **Notifications par minute** : < 10

## 🎉 **SUCCÈS**
Si tous les critères sont validés, le système de notifications temps réel est opérationnel avec des performances optimisées ! 