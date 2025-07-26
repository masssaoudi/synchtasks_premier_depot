# Script de déploiement SyncTasks pour Windows
# Automatise la dockerisation et le déploiement de l'application

param(
    [Parameter(Position=0)]
    [string]$Command = "deploy"
)

# Configuration
$APP_NAME = "synchtasks"
$VERSION = "1.0.0"
$DOCKER_REGISTRY = ""  # Laissez vide pour build local

# Fonctions utilitaires
function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Vérifier les prérequis
function Test-Prerequisites {
    Write-Info "Vérification des prérequis..."
    
    # Vérifier Docker
    try {
        $null = Get-Command docker -ErrorAction Stop
    }
    catch {
        Write-Error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    }
    
    # Vérifier Docker Compose
    try {
        $null = Get-Command docker-compose -ErrorAction Stop
    }
    catch {
        Write-Error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    }
    
    # Vérifier que Docker daemon fonctionne
    try {
        $null = docker info 2>$null
    }
    catch {
        Write-Error "Docker daemon n'est pas en cours d'exécution."
        exit 1
    }
    
    Write-Success "Tous les prérequis sont satisfaits"
}

# Nettoyer les ressources Docker
function Remove-DockerResources {
    Write-Info "Nettoyage des ressources Docker..."
    
    # Arrêter et supprimer les conteneurs existants
    try {
        docker-compose down --remove-orphans 2>$null
    }
    catch {
        # Ignorer les erreurs si aucun conteneur n'existe
    }
    
    # Supprimer les images non utilisées
    try {
        docker image prune -f 2>$null
    }
    catch {
        # Ignorer les erreurs
    }
    
    # Supprimer les volumes non utilisés (optionnel)
    $response = Read-Host "Voulez-vous supprimer les volumes non utilisés ? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        try {
            docker volume prune -f 2>$null
        }
        catch {
            # Ignorer les erreurs
        }
    }
    
    Write-Success "Nettoyage terminé"
}

# Créer le fichier .env s'il n'existe pas
function New-EnvFile {
    if (-not (Test-Path ".env")) {
        Write-Info "Création du fichier .env..."
        @"
# Configuration SyncTasks
MONGODB_URL=mongodb://mongo:27017/synchtasks_db
JWT_SECRET=your-super-secret-jwt-key-change-in-production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Configuration Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Configuration MongoDB
MONGO_INITDB_DATABASE=synchtasks_db
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123

# Configuration Mongo Express
ME_CONFIG_MONGODB_SERVER=mongo
ME_CONFIG_MONGODB_PORT=27017
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=admin123
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Success "Fichier .env créé"
    }
    else {
        Write-Info "Fichier .env existe déjà"
    }
}

# Build des images Docker
function Build-DockerImages {
    Write-Info "Construction des images Docker..."
    
    # Build du backend
    Write-Info "Construction de l'image backend..."
    docker build -t "${APP_NAME}-backend:${VERSION}" .
    
    # Build du frontend
    Write-Info "Construction de l'image frontend..."
    docker build -t "${APP_NAME}-frontend:${VERSION}" ./frontend-vue
    
    Write-Success "Construction des images terminée"
}

# Déployer l'application
function Start-Deployment {
    Write-Info "Déploiement de l'application..."
    
    # Démarrer les services
    docker-compose up -d
    
    # Attendre que les services soient prêts
    Write-Info "Attente du démarrage des services..."
    Start-Sleep -Seconds 30
    
    # Vérifier l'état des services
    Test-ServicesHealth
    
    Write-Success "Déploiement terminé"
}

# Vérifier la santé des services
function Test-ServicesHealth {
    Write-Info "Vérification de la santé des services..."
    
    # Vérifier MongoDB
    try {
        $null = docker-compose exec -T mongo mongosh --eval "db.adminCommand('ping')" 2>$null
        Write-Success "MongoDB est opérationnel"
    }
    catch {
        Write-Warning "MongoDB n'est pas encore prêt"
    }
    
    # Vérifier le backend
    try {
        $null = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        Write-Success "Backend est opérationnel"
    }
    catch {
        Write-Warning "Backend n'est pas encore prêt"
    }
    
    # Vérifier le frontend
    try {
        $null = Invoke-WebRequest -Uri "http://localhost:80" -UseBasicParsing -TimeoutSec 5
        Write-Success "Frontend est opérationnel"
    }
    catch {
        Write-Warning "Frontend n'est pas encore prêt"
    }
}

# Afficher les informations de déploiement
function Show-DeploymentInfo {
    Write-Info "Informations de déploiement:"
    Write-Host ""
    Write-Host "🌐 Frontend: http://localhost:80"
    Write-Host "🔧 Backend API: http://localhost:8000"
    Write-Host "📊 Mongo Express: http://localhost:8081"
    Write-Host "🗄️  MongoDB: localhost:27017"
    Write-Host ""
    Write-Host "📋 Commandes utiles:"
    Write-Host "  - Voir les logs: docker-compose logs -f"
    Write-Host "  - Arrêter: docker-compose down"
    Write-Host "  - Redémarrer: docker-compose restart"
    Write-Host "  - Mettre à jour: .\deploy.ps1 update"
    Write-Host ""
}

# Mettre à jour l'application
function Update-Application {
    Write-Info "Mise à jour de l'application..."
    
    # Pull des dernières images (si registry configuré)
    if ($DOCKER_REGISTRY) {
        docker-compose pull
    }
    
    # Rebuild des images
    Build-DockerImages
    
    # Redéployer
    docker-compose down
    docker-compose up -d
    
    Write-Success "Mise à jour terminée"
}

# Arrêter l'application
function Stop-Application {
    Write-Info "Arrêt de l'application..."
    docker-compose down
    Write-Success "Application arrêtée"
}

# Afficher les logs
function Show-Logs {
    Write-Info "Affichage des logs..."
    docker-compose logs -f
}

# Afficher l'aide
function Show-Help {
    Write-Host "Script de déploiement SyncTasks pour Windows"
    Write-Host ""
    Write-Host "Usage: .\deploy.ps1 [COMMANDE]"
    Write-Host ""
    Write-Host "Commandes:"
    Write-Host "  deploy    - Déployer l'application (défaut)"
    Write-Host "  build     - Construire les images Docker"
    Write-Host "  update    - Mettre à jour l'application"
    Write-Host "  stop      - Arrêter l'application"
    Write-Host "  logs      - Afficher les logs"
    Write-Host "  cleanup   - Nettoyer les ressources Docker"
    Write-Host "  health    - Vérifier la santé des services"
    Write-Host "  help      - Afficher cette aide"
    Write-Host ""
}

# Fonction principale
function Main {
    switch ($Command.ToLower()) {
        "deploy" {
            Test-Prerequisites
            New-EnvFile
            Build-DockerImages
            Start-Deployment
            Show-DeploymentInfo
        }
        "build" {
            Test-Prerequisites
            Build-DockerImages
        }
        "update" {
            Test-Prerequisites
            Update-Application
            Show-DeploymentInfo
        }
        "stop" {
            Stop-Application
        }
        "logs" {
            Show-Logs
        }
        "cleanup" {
            Remove-DockerResources
        }
        "health" {
            Test-ServicesHealth
        }
        "help" {
            Show-Help
        }
        default {
            Write-Error "Commande inconnue: $Command"
            Show-Help
            exit 1
        }
    }
}

# Exécuter le script
Main 