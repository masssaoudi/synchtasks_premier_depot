# 🐳 CHECKLIST DOCKERISATION SYNC TASKS (MISE À JOUR JUILLET 2025)

## ✅ ÉTAPE 1 : PRÉPARATION (TERMINÉE)
- [x] Suppression de tous les anciens Dockerfile et docker-compose.yml
- [x] Nettoyage complet Docker (conteneurs, images, volumes, réseaux)
- [x] Projet versionné sur GitHub ([synchtasks_premier_depot](https://github.com/masssaoudi/synchtasks_premier_depot.git))
- [x] .gitignore et README.md à jour

## 🚧 ÉTAPE 2 : (À FAIRE) NOUVELLE DOCKERISATION
- [ ] Créer un nouveau Dockerfile pour le backend (FastAPI)
- [ ] Créer un nouveau Dockerfile pour le frontend (Vue.js) si besoin
- [ ] Créer un nouveau docker-compose.yml (orchestration backend + frontend + MongoDB)
- [ ] Créer/adapter .dockerignore (optimisation build)
- [ ] Vérifier/adapter les variables d’environnement (.env, clé Gemini, etc.)
- [ ] (Optionnel) Ajouter un script de démarrage/arrêt (start-docker.bat, stop-docker.bat)

## 🚀 ÉTAPE 3 : PREMIER LANCEMENT DOCKER
- [ ] Arrêter tous les serveurs locaux (FastAPI, npm run dev)
- [ ] Lancer docker-compose up --build
- [ ] Vérifier que tous les conteneurs sont "Up"
- [ ] Tester :
  - [ ] http://localhost:3000 (frontend)
  - [ ] http://localhost:8000 (API)
  - [ ] http://localhost:8000/docs (Swagger)
  - [ ] Authentification, tâches, chat IA, WebSocket

## 🔧 ÉTAPE 4 : OPTIMISATION ET CONFIGURATION
- [ ] Vérifier la persistance MongoDB (volume)
- [ ] Vérifier le passage des variables d’environnement (clé Gemini, etc.)
- [ ] Optimiser les images Docker (taille, cache)
- [ ] (Optionnel) Ajouter Nginx pour la prod

## 📊 ÉTAPE 5 : TESTS COMPLETS
- [ ] Tester toutes les fonctionnalités principales dans Docker
- [ ] Tester la communication frontend-backend
- [ ] Tester la persistance des données
- [ ] Tester le WebSocket temps réel

## 🎯 ÉTAPE 6 : DÉPLOIEMENT ET DOCUMENTATION
- [ ] Mettre à jour la documentation Docker dans le README.md
- [ ] Ajouter un guide de troubleshooting
- [ ] (Optionnel) Préparer la configuration pour la production

---

# Cette checklist est à jour avec la situation réelle du projet (juillet 2025) et doit être suivie pour garantir une dockerisation propre et sans conflit. 