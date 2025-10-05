@echo off
echo 🚀 Démarrage SynchTasks avec nettoyage automatique
echo ================================================

echo.
echo 🧹 Nettoyage du code...
python cleanup_code.py --all

echo.
echo 🐳 Démarrage Docker...
docker compose up --build

echo.
echo ✅ Application démarrée !
echo 📍 Frontend: http://localhost:80
echo 📍 Backend: http://localhost:8000
echo 📍 API Docs: http://localhost:8000/docs
echo 📍 MongoDB Express: http://localhost:8081 