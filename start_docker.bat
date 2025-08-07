@echo off
echo 🐳 DÉMARRAGE SYNC TASKS EN DOCKER
echo ======================================

echo.
echo 🔄 Arrêt des services locaux...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
taskkill /f /im npm.exe 2>nul

echo.
echo 🧹 Nettoyage des conteneurs existants...
docker-compose down --remove-orphans

echo.
echo 🏗️ Construction des images Docker...
docker-compose build --no-cache

echo.
echo 🚀 Démarrage des services...
docker-compose up -d

echo.
echo ⏳ Attente du démarrage des services...
timeout /t 10 /nobreak >nul

echo.
echo 📊 Vérification des services...
docker-compose ps

echo.
echo 🌐 URLs d'accès :
echo   - Frontend: http://localhost:3000
echo   - Backend API: http://localhost:8000
echo   - MongoDB Express: http://localhost:8081
echo   - MongoDB: localhost:27017

echo.
echo 📋 Logs en temps réel (Ctrl+C pour arrêter) :
echo docker-compose logs -f

echo.
echo ✅ Docker démarré avec succès !
pause 