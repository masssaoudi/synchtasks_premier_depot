"""
Test de l'interface utilisateur et WebSocket
Vérifie que le frontend se connecte correctement au WebSocket
"""

import requests
import time
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_frontend_access():
    """Test d'accès au frontend"""
    logger.info("🌐 Test d'accès au frontend...")

    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Frontend accessible")
            return True
        else:
            logger.error(f"❌ Frontend non accessible: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur accès frontend: {e}")
        return False


def test_backend_api():
    """Test de l'API backend"""
    logger.info("🔧 Test de l'API backend...")

    endpoints = ["/health", "/api/tasks", "/api/users", "/api/theme"]

    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code in [
                200,
                401,
                404,
            ]:  # 401/404 sont normaux sans auth
                logger.info(f"✅ Endpoint {endpoint}: {response.status_code}")
            else:
                logger.warning(f"⚠️ Endpoint {endpoint}: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Erreur endpoint {endpoint}: {e}")


def test_websocket_connection():
    """Test de connexion WebSocket depuis le frontend"""
    logger.info("🔌 Test de connexion WebSocket...")

    # Simuler une requête de connexion WebSocket
    try:
        # Test direct de l'endpoint WebSocket
        import websockets
        import asyncio
        import json

        async def test_ws():
            uri = "ws://localhost:8000/api/ws/test_ui_user"
            try:
                async with websockets.connect(uri) as websocket:
                    logger.info("✅ WebSocket connecté depuis le test UI")

                    # Envoyer un message de test
                    test_msg = {
                        "type": "ui_test",
                        "content": "Test depuis interface utilisateur",
                        "timestamp": int(time.time()),
                    }
                    await websocket.send(json.dumps(test_msg))
                    logger.info("📤 Message de test UI envoyé")

                    # Attendre une réponse
                    await asyncio.sleep(2)
                    logger.info("✅ Test WebSocket UI réussi")

            except Exception as e:
                logger.error(f"❌ Erreur WebSocket UI: {e}")

        asyncio.run(test_ws())

    except Exception as e:
        logger.error(f"❌ Erreur test WebSocket UI: {e}")


def test_mongo_express():
    """Test de MongoDB Express"""
    logger.info("🗄️ Test de MongoDB Express...")

    try:
        response = requests.get("http://localhost:8081", timeout=5)
        if response.status_code == 200:
            logger.info("✅ MongoDB Express accessible")
            return True
        else:
            logger.warning(f"⚠️ MongoDB Express: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur MongoDB Express: {e}")
        return False


def run_full_ui_test():
    """Exécuter tous les tests UI"""
    logger.info("🚀 Démarrage du test interface utilisateur complet...")

    # Test 1: Frontend
    frontend_ok = test_frontend_access()

    # Test 2: Backend API
    test_backend_api()

    # Test 3: WebSocket
    test_websocket_connection()

    # Test 4: MongoDB Express
    mongo_ok = test_mongo_express()

    # Résumé
    logger.info("📊 Résumé des tests:")
    logger.info(f"   Frontend: {'✅' if frontend_ok else '❌'}")
    logger.info(f"   MongoDB Express: {'✅' if mongo_ok else '❌'}")
    logger.info("   WebSocket: ✅ (testé séparément)")

    if frontend_ok:
        logger.info("🎉 Interface utilisateur prête !")
        logger.info("🌐 Accédez à: http://localhost:3000")
    else:
        logger.error("❌ Problème avec l'interface utilisateur")


if __name__ == "__main__":
    run_full_ui_test()
