@echo off
REM Script de démarrage rapide Docker pour SyncTasks
REM Usage: start_docker.bat [deploy|stop|logs|cleanup]

setlocal enabledelayedexpansion

REM Couleurs pour Windows
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Configuration
set "APP_NAME=synchtasks"
set "VERSION=1.0.0"

REM Fonctions utilitaires
:log_info
echo %BLUE%ℹ️  %~1%NC%
goto :eof

:log_success
echo %GREEN%✅ %~1%NC%
goto :eof

:log_warning
echo %YELLOW%⚠️  %~1%NC%
goto :eof

:log_error
echo %RED%❌ %~1%NC%
goto :eof

REM Vérifier les prérequis
:check_prerequisites
call :log_info "Vérification des prérequis..."

REM Vérifier Docker
docker --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker n'est pas installé. Veuillez l'installer d'abord."
    pause
    exit /b 1
)

REM Vérifier Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    pause
    exit /b 1
)

REM Vérifier que Docker daemon fonctionne
docker info >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker daemon n'est pas en cours d'exécution."
    pause
    exit /b 1
)

call :log_success "Tous les prérequis sont satisfaits"
goto :eof

REM Créer le fichier .env
:create_env_file
if not exist ".env" (
    call :log_info "Création du fichier .env..."
    (
        echo # Configuration SyncTasks
        echo MONGODB_URL=mongodb://mongo:27017/synchtasks_db
        echo JWT_SECRET=your-super-secret-jwt-key-change-in-production
        echo ENVIRONMENT=production
        echo DEBUG=false
        echo LOG_LEVEL=INFO
        echo.
        echo # Configuration Frontend
        echo VITE_API_URL=http://localhost:8000
        echo VITE_WS_URL=ws://localhost:8000
        echo.
        echo # Configuration MongoDB
        echo MONGO_INITDB_DATABASE=synchtasks_db
        echo MONGO_INITDB_ROOT_USERNAME=admin
        echo MONGO_INITDB_ROOT_PASSWORD=admin123
        echo.
        echo # Configuration Mongo Express
        echo ME_CONFIG_MONGODB_SERVER=mongo
        echo ME_CONFIG_MONGODB_PORT=27017
        echo ME_CONFIG_BASICAUTH_USERNAME=admin
        echo ME_CONFIG_BASICAUTH_PASSWORD=admin123
    ) > .env
    call :log_success "Fichier .env créé"
) else (
    call :log_info "Fichier .env existe déjà"
)
goto :eof

REM Build des images
:build_images
call :log_info "Construction des images Docker..."

call :log_info "Construction de l'image backend..."
docker build -t %APP_NAME%-backend:%VERSION% .

call :log_info "Construction de l'image frontend..."
docker build -t %APP_NAME%-frontend:%VERSION% ./frontend-vue

call :log_success "Construction des images terminée"
goto :eof

REM Déployer l'application
:deploy
call :log_info "Déploiement de l'application..."

docker-compose up -d

call :log_info "Attente du démarrage des services..."
timeout /t 30 /nobreak >nul

call :log_success "Déploiement terminé"
goto :eof

REM Afficher les informations
:show_info
call :log_info "Informations de déploiement:"
echo.
echo 🌐 Frontend: http://localhost:80
echo 🔧 Backend API: http://localhost:8000
echo 📊 Mongo Express: http://localhost:8081
echo 🗄️  MongoDB: localhost:27017
echo.
echo 📋 Commandes utiles:
echo   - Voir les logs: docker-compose logs -f
echo   - Arrêter: docker-compose down
echo   - Redémarrer: docker-compose restart
echo   - Mettre à jour: start_docker.bat update
echo.
goto :eof

REM Arrêter l'application
:stop
call :log_info "Arrêt de l'application..."
docker-compose down
call :log_success "Application arrêtée"
goto :eof

REM Afficher les logs
:logs
call :log_info "Affichage des logs..."
docker-compose logs -f
goto :eof

REM Nettoyer
:cleanup
call :log_info "Nettoyage des ressources Docker..."

docker-compose down --remove-orphans 2>nul
docker image prune -f 2>nul

set /p "response=Voulez-vous supprimer les volumes non utilisés ? (y/N): "
if /i "!response!"=="y" (
    docker volume prune -f 2>nul
)

call :log_success "Nettoyage terminé"
goto :eof

REM Mettre à jour
:update
call :log_info "Mise à jour de l'application..."

call :build_images

docker-compose down
docker-compose up -d

call :log_success "Mise à jour terminée"
goto :eof

REM Afficher l'aide
:help
echo Script de déploiement Docker SyncTasks pour Windows
echo.
echo Usage: start_docker.bat [COMMANDE]
echo.
echo Commandes:
echo   deploy    - Déployer l'application (défaut)
echo   build     - Construire les images Docker
echo   update    - Mettre à jour l'application
echo   stop      - Arrêter l'application
echo   logs      - Afficher les logs
echo   cleanup   - Nettoyer les ressources Docker
echo   help      - Afficher cette aide
echo.
goto :eof

REM Fonction principale
:main
set "command=%~1"
if "%command%"=="" set "command=deploy"

echo 🐳 Script de déploiement Docker SyncTasks
echo ================================================

if /i "%command%"=="deploy" (
    call :check_prerequisites
    call :create_env_file
    call :build_images
    call :deploy
    call :show_info
) else if /i "%command%"=="build" (
    call :check_prerequisites
    call :build_images
) else if /i "%command%"=="update" (
    call :check_prerequisites
    call :update
    call :show_info
) else if /i "%command%"=="stop" (
    call :stop
) else if /i "%command%"=="logs" (
    call :logs
) else if /i "%command%"=="cleanup" (
    call :cleanup
) else if /i "%command%"=="help" (
    call :help
) else (
    call :log_error "Commande inconnue: %command%"
    call :help
    pause
    exit /b 1
)

echo.
echo Appuyez sur une touche pour continuer...
pause >nul
goto :eof

REM Exécuter le script
call :main %* 