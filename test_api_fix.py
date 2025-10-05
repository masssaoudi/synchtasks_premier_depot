"""
Test de l'API après correction CORS
Vérifie que les requêtes API fonctionnent correctement
"""

import requests
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_backend_health():
    """Test de santé du backend"""
    logger.info("🏥 Test de santé du backend...")

    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            logger.info("✅ Backend en bonne santé")
            return True
        else:
            logger.error(f"❌ Backend non disponible: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur connexion backend: {e}")
        return False


def test_api_tasks():
    """Test de l'API des tâches"""
    logger.info("📋 Test de l'API des tâches...")

    try:
        # Test GET /api/tasks
        response = requests.get("http://localhost:8000/api/tasks")
        logger.info(f"📥 GET /api/tasks: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Tâches récupérées: {len(data.get('data', []))} tâches")
            return True
        else:
            logger.error(f"❌ Erreur API tâches: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"❌ Erreur API tâches: {e}")
        return False


def test_frontend_access():
    """Test d'accès au frontend"""
    logger.info("🌐 Test d'accès au frontend...")

    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            logger.info("✅ Frontend accessible")
            return True
        else:
            logger.error(f"❌ Frontend non accessible: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur accès frontend: {e}")
        return False


def test_cors_headers():
    """Test des headers CORS"""
    logger.info("🔒 Test des headers CORS...")

    try:
        # Test avec une requête OPTIONS (preflight)
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        }

        response = requests.options("http://localhost:8000/api/tasks", headers=headers)
        logger.info(f"📥 OPTIONS /api/tasks: {response.status_code}")

        # Vérifier les headers CORS
        cors_headers = response.headers.get("Access-Control-Allow-Origin")
        if cors_headers:
            logger.info(f"✅ CORS configuré: {cors_headers}")
            return True
        else:
            logger.warning("⚠️ Headers CORS non trouvés")
            return False

    except Exception as e:
        logger.error(f"❌ Erreur test CORS: {e}")
        return False


def run_api_test():
    """Test complet de l'API"""
    logger.info("🚀 Test complet de l'API après correction CORS...")

    # Test 1: Backend health
    backend_ok = test_backend_health()

    # Test 2: API tâches
    api_ok = test_api_tasks()

    # Test 3: Frontend access
    frontend_ok = test_frontend_access()

    # Test 4: CORS headers
    cors_ok = test_cors_headers()

    # Résumé
    logger.info("📊 Résumé des tests:")
    logger.info(f"   Backend: {'✅' if backend_ok else '❌'}")
    logger.info(f"   API Tâches: {'✅' if api_ok else '❌'}")
    logger.info(f"   Frontend: {'✅' if frontend_ok else '❌'}")
    logger.info(f"   CORS: {'✅' if cors_ok else '❌'}")

    if all([backend_ok, api_ok, frontend_ok]):
        logger.info("🎉 Tous les tests API sont passés !")
        logger.info("💡 L'interface devrait maintenant fonctionner correctement")
    else:
        logger.error("❌ Certains tests ont échoué")


if __name__ == "__main__":
    run_api_test()
