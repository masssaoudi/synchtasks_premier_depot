# 🔧 Guide de Résolution des Problèmes - SynchTasks

## 🚨 Problèmes Courants et Solutions

### 1. Erreur d'Encodage Windows (cp1252)

**Symptômes :**
```
File "C:\Users\...\lib\encodings\cp1252.py", line 22, in decode
    def decode(self, input, final=False):
KeyboardInterrupt
```

**Solution :**
```bash
# Exécuter le script de correction
python fix_encoding_issues.py

# Ou utiliser le script de démarrage sécurisé
python start_safe.py
```

### 2. Conflit de Versions MongoDB

**Symptômes :**
```
ImportError: cannot import name 'AsyncIOMotorClient' from 'motor'
```

**Solution :**
```bash
# Désinstaller et réinstaller les packages MongoDB
pip uninstall motor pymongo -y
pip install pymongo==4.6.0
pip install motor==3.3.2
```

### 3. MongoDB Non Accessible

**Symptômes :**
```
ConnectionRefusedError: [Errno 10061] No connection could be made
```

**Solutions :**

#### Option A : Installer MongoDB Localement
1. Télécharger MongoDB Community Server
2. Installer et démarrer le service
3. Vérifier que MongoDB écoute sur `localhost:27017`

#### Option B : Utiliser MongoDB Atlas (Cloud)
1. Créer un compte sur MongoDB Atlas
2. Créer un cluster gratuit
3. Modifier le fichier `.env` :
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

### 4. Port 8000 Déjà Utilisé

**Symptômes :**
```
OSError: [Errno 10048] Only one usage of each socket address is normally permitted
```

**Solution :**
```bash
# Changer le port dans le fichier .env
API_PORT=8001

# Ou utiliser un autre port directement
python -m uvicorn main:app --port 8001
```

### 5. Dépendances Manquantes

**Symptômes :**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution :**
```bash
# Installer toutes les dépendances
pip install -r requirements.txt

# Ou installer individuellement
pip install fastapi uvicorn motor pymongo
```

## 🚀 Méthodes de Démarrage

### Méthode 1 : Script de Correction (Recommandé)
```bash
cd SynchTasks
python fix_encoding_issues.py
python start_safe.py
```

### Méthode 2 : Fichier Batch Windows
```bash
# Double-cliquer sur start_api.bat
# Ou exécuter en ligne de commande
start_api.bat
```

### Méthode 3 : Commande Directe
```bash
# Configuration manuelle de l'encodage
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔍 Diagnostic

### Vérifier l'État de l'API
```bash
# Test de santé
curl http://localhost:8000/health

# Documentation interactive
# Ouvrir http://localhost:8000/docs dans le navigateur
```

### Vérifier MongoDB
```bash
# Test de connexion MongoDB
python -c "
import asyncio
import motor.motor_asyncio
from config import settings

async def test():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    await client.admin.command('ping')
    print('✅ MongoDB OK')
    client.close()

asyncio.run(test())
"
```

### Vérifier les Logs
```bash
# Les logs apparaissent dans la console
# Rechercher les messages d'erreur commençant par ❌
```

## 📋 Checklist de Démarrage

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` créé
- [ ] MongoDB accessible (local ou cloud)
- [ ] Port 8000 libre
- [ ] Encodage UTF-8 configuré
- [ ] Variables d'environnement définies

## 🆘 Support

Si les problèmes persistent :

1. **Vérifier les logs** : Regarder les messages d'erreur dans la console
2. **Tester MongoDB** : S'assurer que la base de données est accessible
3. **Vérifier les ports** : S'assurer qu'aucun autre service n'utilise le port 8000
4. **Redémarrer** : Fermer tous les processus Python et redémarrer
5. **Réinstaller** : Supprimer le dossier `__pycache__` et réinstaller les dépendances

## 🔄 Mise à Jour

Pour mettre à jour l'application :

```bash
# Sauvegarder les données importantes
# Puis mettre à jour le code

# Réinstaller les dépendances
pip install -r requirements.txt --upgrade

# Redémarrer l'API
python start_safe.py
``` 