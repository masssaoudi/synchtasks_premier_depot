@echo off
echo ========================================
echo    SyncTasks API - Demarrage
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Environnement virtuel non trouvé!
    echo Veuillez créer l'environnement virtuel d'abord:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Vérifier les dépendances
echo 📦 Vérification des dépendances...
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo ❌ Dépendances manquantes! Installation...
    pip install -r requirements.txt
)

REM Démarrer le serveur
echo 🚀 Démarrage du serveur...
echo.
echo 📡 API: http://localhost:8000
echo 📚 Docs: http://localhost:8000/docs
echo 🛑 Ctrl+C pour arrêter
echo.

python start_server.py

pause 