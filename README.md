# SyncTasks

Application de gestion de tâches intelligente avec IA et module d’aide à la personne.

---

## 🚀 Description
SyncTasks est une application web permettant de gérer des tâches, projets et rappels, avec intégration d’une intelligence artificielle (Gemini) et un module avancé de "personne aidante" pour l’accompagnement des utilisateurs vulnérables.

---

## 🛠️ Stack technique
- **Backend** : FastAPI (Python), MongoDB
- **Frontend** : Vue.js 3 (Vite), Pinia, Axios
- **IA** : Gemini API
- **Notifications** : WebSocket (prévu)

---

## 📦 Installation & Lancement

### 1. Cloner le dépôt
```bash
git clone https://github.com/masssaoudi/synchtasks_premier_depot.git
cd synchtasks_premier_depot
```

### 2. Backend (FastAPI)
```bash
# Activer l'environnement virtuel
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend (Vue.js)
```bash
cd frontend-vue
npm install
npm run dev
```

- Accès frontend : http://localhost:3000
- Accès backend : http://localhost:8000
- Documentation API : http://localhost:8000/docs

---

## 📈 État d’avancement
- Authentification JWT ✅
- Gestion des tâches (CRUD) ✅
- Intégration IA Gemini (chat) ✅
- Dashboard Kanban ✅
- Module personne aidante (en cours)
- Notifications temps réel (WebSocket) à venir
- Dockerisation à venir

---

## 🗺️ Roadmap & suivi
Retrouve la roadmap détaillée et l’état d’avancement dans le fichier [point_reprise.md](./point_reprise.md)

---

## 👤 Auteur
- [masssaoudi](https://github.com/masssaoudi)

---

## 📄 Licence
MIT 