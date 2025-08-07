# 📋 CANEVAS UTILISATEURS SYNCHTASKS

## 🎯 **Utilisateurs de Test Disponibles**

---

## 👤 **UTILISATEURS NORMAUX**

| Username | Mot de passe | Email | Nom complet | Rôle |
|----------|--------------|-------|-------------|------|
| `coco` | `coco123` | `mounmas832@gmail.com` | `coco et nini` | `user` |
| `alice` | `alice123` | `alice@test.com` | `Alice Martin` | `user` |
| `bob` | `bob123` | `bob@test.com` | `Bob Dupont` | `user` |
| `charlie` | `charlie123` | `charlie@test.com` | `Charlie Bernard` | `user` |

---

## 🤝 **PERSONNES AIDANTES (PA)**

| Username | Mot de passe | Email | Nom complet | Rôle |
|----------|--------------|-------|-------------|------|
| `marie_pa` | `marie123` | `marie.pa@test.com` | `Marie Dubois` | `pa` |
| `pierre_pa` | `pierre123` | `pierre.pa@test.com` | `Pierre Martin` | `pa` |
| `sophie_pa` | `sophie123` | `sophie.pa@test.com` | `Sophie Leroy` | `pa` |

---

## 📊 **STATISTIQUES**

- **Total utilisateurs :** 7
- **Utilisateurs normaux :** 4
- **Personnes Aidantes :** 3

---

## 🚀 **UTILISATION**

### **Connexion via API :**
```bash
POST http://localhost:8000/api/auth/login
{
  "username": "alice",
  "password": "alice123"
}
```

### **Connexion via Frontend :**
- **URL :** `http://localhost:3000`
- **Page d'accueil :** `/`
- **Connexion PA :** `/personne-aidant`
- **Inscription PA :** `/pa-inscription`
- **Dashboard PA :** `/pa-dashboard`

---

## 🧪 **TESTS RÉALISÉS**

✅ **Toutes les connexions fonctionnent :**
- ✅ coco / coco123
- ✅ alice / alice123
- ✅ bob / bob123
- ✅ charlie / charlie123
- ✅ marie_pa / marie123
- ✅ pierre_pa / pierre123
- ✅ sophie_pa / sophie123

---

## 🎯 **SCÉNARIOS DE TEST RECOMMANDÉS**

### **1. Test Utilisateur Normal**
- **Utilisateur :** `alice` / `alice123`
- **Actions :** Connexion, création de tâches, délégation à PA

### **2. Test Personne Aidante**
- **Utilisateur :** `marie_pa` / `marie123`
- **Actions :** Connexion PA, demande OTP, accès Kanban, conseils IA

### **3. Test Délégation**
- **Principal :** `alice` / `alice123`
- **PA :** `marie_pa` / `marie123`
- **Actions :** Créer délégation, partager tâches

### **4. Test Système OTP**
- **PA :** `pierre_pa` / `pierre123`
- **Actions :** Demander OTP, vérifier code, accès Kanban

---

## 🔧 **MAINTENANCE**

### **Nettoyage de la base :**
```bash
python cleanup_db.py
```

### **Création d'utilisateurs :**
```bash
python create_test_users.py
```

### **Test des connexions :**
```bash
python test_users.py
```

---

## 📝 **NOTES**

- **Base de données :** MongoDB (synchtasks_db)
- **Backend :** FastAPI (port 8000)
- **Frontend :** Vue.js (port 3000)
- **Tous les mots de passe sont simples** pour faciliter les tests
- **Les rôles sont correctement définis** (user/pa)
- **Aucun conflit d'utilisateurs** après nettoyage

---

*Dernière mise à jour : 27/07/2025* 