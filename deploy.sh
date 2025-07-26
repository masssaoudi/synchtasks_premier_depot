#!/bin/bash

# Script de déploiement SyncTasks
# Automatise la dockerisation et le déploiement de l'application

set -e  # Arrêter le script en cas d'erreur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="synchtasks"
VERSION="1.0.0"
DOCKER_REGISTRY=""  # Laissez vide pour build local

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier les prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    # Vérifier que Docker daemon fonctionne
    if ! docker info &> /dev/null; then
        log_error "Docker daemon n'est pas en cours d'exécution."
        exit 1
    fi
    
    log_success "Tous les prérequis sont satisfaits"
}

# Nettoyer les ressources Docker
cleanup() {
    log_info "Nettoyage des ressources Docker..."
    
    # Arrêter et supprimer les conteneurs existants
    docker-compose down --remove-orphans 2>/dev/null || true
    
    # Supprimer les images non utilisées
    docker image prune -f 2>/dev/null || true
    
    # Supprimer les volumes non utilisés (optionnel)
    read -p "Voulez-vous supprimer les volumes non utilisés ? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f 2>/dev/null || true
    fi
    
    log_success "Nettoyage terminé"
}

# Créer le fichier .env s'il n'existe pas
create_env_file() {
    if [ ! -f .env ]; then
        log_info "Création du fichier .env..."
        cat > .env << EOF
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
EOF
        log_success "Fichier .env créé"
    else
        log_info "Fichier .env existe déjà"
    fi
}

# Build des images Docker
build_images() {
    log_info "Construction des images Docker..."
    
    # Build du backend
    log_info "Construction de l'image backend..."
    docker build -t ${APP_NAME}-backend:${VERSION} .
    
    # Build du frontend
    log_info "Construction de l'image frontend..."
    docker build -t ${APP_NAME}-frontend:${VERSION} ./frontend-vue
    
    log_success "Construction des images terminée"
}

# Déployer l'application
deploy() {
    log_info "Déploiement de l'application..."
    
    # Démarrer les services
    docker-compose up -d
    
    # Attendre que les services soient prêts
    log_info "Attente du démarrage des services..."
    sleep 30
    
    # Vérifier l'état des services
    check_services_health
    
    log_success "Déploiement terminé"
}

# Vérifier la santé des services
check_services_health() {
    log_info "Vérification de la santé des services..."
    
    # Vérifier MongoDB
    if docker-compose exec -T mongo mongosh --eval "db.adminCommand('ping')" &> /dev/null; then
        log_success "MongoDB est opérationnel"
    else
        log_warning "MongoDB n'est pas encore prêt"
    fi
    
    # Vérifier le backend
    if curl -f http://localhost:8000/health &> /dev/null; then
        log_success "Backend est opérationnel"
    else
        log_warning "Backend n'est pas encore prêt"
    fi
    
    # Vérifier le frontend
    if curl -f http://localhost:80 &> /dev/null; then
        log_success "Frontend est opérationnel"
    else
        log_warning "Frontend n'est pas encore prêt"
    fi
}

# Afficher les informations de déploiement
show_deployment_info() {
    log_info "Informations de déploiement:"
    echo
    echo "🌐 Frontend: http://localhost:80"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📊 Mongo Express: http://localhost:8081"
    echo "🗄️  MongoDB: localhost:27017"
    echo
    echo "📋 Commandes utiles:"
    echo "  - Voir les logs: docker-compose logs -f"
    echo "  - Arrêter: docker-compose down"
    echo "  - Redémarrer: docker-compose restart"
    echo "  - Mettre à jour: ./deploy.sh update"
    echo
}

# Mettre à jour l'application
update() {
    log_info "Mise à jour de l'application..."
    
    # Pull des dernières images (si registry configuré)
    if [ ! -z "$DOCKER_REGISTRY" ]; then
        docker-compose pull
    fi
    
    # Rebuild des images
    build_images
    
    # Redéployer
    docker-compose down
    docker-compose up -d
    
    log_success "Mise à jour terminée"
}

# Arrêter l'application
stop() {
    log_info "Arrêt de l'application..."
    docker-compose down
    log_success "Application arrêtée"
}

# Afficher les logs
logs() {
    log_info "Affichage des logs..."
    docker-compose logs -f
}

# Afficher l'aide
show_help() {
    echo "Script de déploiement SyncTasks"
    echo
    echo "Usage: $0 [COMMANDE]"
    echo
    echo "Commandes:"
    echo "  deploy    - Déployer l'application (défaut)"
    echo "  build     - Construire les images Docker"
    echo "  update    - Mettre à jour l'application"
    echo "  stop      - Arrêter l'application"
    echo "  logs      - Afficher les logs"
    echo "  cleanup   - Nettoyer les ressources Docker"
    echo "  health    - Vérifier la santé des services"
    echo "  help      - Afficher cette aide"
    echo
}

# Fonction principale
main() {
    local command=${1:-deploy}
    
    case $command in
        "deploy")
            check_prerequisites
            create_env_file
            build_images
            deploy
            show_deployment_info
            ;;
        "build")
            check_prerequisites
            build_images
            ;;
        "update")
            check_prerequisites
            update
            show_deployment_info
            ;;
        "stop")
            stop
            ;;
        "logs")
            logs
            ;;
        "cleanup")
            cleanup
            ;;
        "health")
            check_services_health
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "Commande inconnue: $command"
            show_help
            exit 1
            ;;
    esac
}

# Exécuter le script
main "$@" 