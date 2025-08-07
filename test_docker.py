"""
Test Docker pour SyncTasks
Vérifie que tous les services fonctionnent correctement
"""

import requests
import time
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_backend():
    """Test du backend"""
    try:
        # Test santé
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            logger.info("✅ Backend santé OK")
            return True
        else:
            logger.error(f"❌ Backend santé KO: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur backend: {e}")
        return False


def test_frontend():
    """Test du frontend"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            logger.info("✅ Frontend OK")
            return True
        else:
            logger.error(f"❌ Frontend KO: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur frontend: {e}")
        return False


def test_mongo_express():
    """Test de MongoDB Express"""
    try:
        response = requests.get('http://localhost:8081', timeout=5)
        if response.status_code == 200:
            logger.info("✅ MongoDB Express OK")
            return True
        else:
            logger.error(f"❌ MongoDB Express KO: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur MongoDB Express: {e}")
        return False


def test_websocket():
    """Test WebSocket"""
    try:
        response = requests.get('http://localhost:8000/api/ws/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logger.info("✅ WebSocket OK")
                return True
            else:
                logger.error("❌ WebSocket KO: réponse invalide")
                return False
        else:
            logger.error(f"❌ WebSocket KO: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur WebSocket: {e}")
        return False


def test_api_endpoints():
    """Test des endpoints API"""
    endpoints = [
        '/api/ws/health',
        '/api/ws/stats',
        '/api/ws/users'
    ]
    
    success_count = 0
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}', timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ {endpoint} OK")
                success_count += 1
            else:
                logger.error(f"❌ {endpoint} KO: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Erreur {endpoint}: {e}")
    
    return success_count == len(endpoints)


def main():
    """Test principal"""
    logger.info("🧪 TEST DOCKER SYNC TASKS")
    logger.info("=" * 40)
    
    # Attendre que les services démarrent
    logger.info("⏳ Attente du démarrage des services...")
    time.sleep(15)
    
    tests = [
        ("Backend", test_backend),
        ("Frontend", test_frontend),
        ("MongoDB Express", test_mongo_express),
        ("WebSocket", test_websocket),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Test {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    logger.info("\n" + "=" * 40)
    logger.info("📊 RÉSULTATS DES TESTS")
    logger.info("=" * 40)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        logger.info(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    logger.info(f"\n🎯 Score: {success_count}/{len(results)} tests réussis")
    
    if success_count == len(results):
        logger.info("🎉 TOUS LES TESTS RÉUSSIS !")
        logger.info("🌐 URLs d'accès:")
        logger.info("   - Frontend: http://localhost:3000")
        logger.info("   - Backend: http://localhost:8000")
        logger.info("   - MongoDB Express: http://localhost:8081")
    else:
        logger.warning("⚠️ Certains tests ont échoué")
        logger.info("💡 Vérifiez les logs: docker-compose logs")


if __name__ == "__main__":
    main() 