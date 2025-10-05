"""
Test WebSocket depuis le point de vue du frontend
Simule la connexion WebSocket comme le fait l'interface utilisateur
"""

import asyncio
import websockets
import json
import logging
import time
import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_frontend_websocket():
    """Test WebSocket comme le fait le frontend"""
    logger.info("🔌 Test WebSocket frontend...")

    # Simuler un utilisateur connecté
    user_id = "test_frontend_user"

    try:
        # URL comme dans le service WebSocket frontend
        ws_url = f"ws://localhost:8000/api/ws/{user_id}"
        logger.info(f"🔌 Connexion à {ws_url}")

        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté (comme frontend)")

            # Simuler les messages du frontend
            frontend_messages = [
                {"type": "ping", "timestamp": int(time.time())},
                {
                    "type": "task_update",
                    "task_data": {
                        "id": "frontend_task_1",
                        "title": "Tâche depuis frontend",
                        "status": "todo",
                        "timestamp": int(time.time()),
                    },
                },
                {"type": "join_room", "room_id": "frontend_room"},
            ]

            for i, msg in enumerate(frontend_messages):
                try:
                    await websocket.send(json.dumps(msg))
                    logger.info(f"📤 Message frontend {i+1} envoyé: {msg['type']}")

                    # Attendre une réponse
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        data = json.loads(response)
                        logger.info(f"📥 Réponse reçue: {data}")
                    except asyncio.TimeoutError:
                        logger.warning(f"⚠️ Pas de réponse pour message {i+1}")

                    await asyncio.sleep(1)

                except Exception as e:
                    logger.error(f"❌ Erreur message {i+1}: {e}")

            logger.info("✅ Test WebSocket frontend réussi !")

    except websockets.exceptions.ConnectionRefusedError:
        logger.error("❌ Connexion refusée - WebSocket non disponible")
    except Exception as e:
        logger.error(f"❌ Erreur WebSocket frontend: {e}")


def test_frontend_interface():
    """Test de l'interface frontend"""
    logger.info("🌐 Test interface frontend...")

    try:
        # Test d'accès au frontend
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Frontend accessible")

            # Vérifier si le JavaScript WebSocket est chargé
            if "websocket" in response.text.lower() or "ws://" in response.text:
                logger.info("✅ JavaScript WebSocket détecté")
            else:
                logger.warning("⚠️ JavaScript WebSocket non détecté")

        else:
            logger.error(f"❌ Frontend non accessible: {response.status_code}")

    except Exception as e:
        logger.error(f"❌ Erreur test frontend: {e}")


def test_mongo_express_auth():
    """Test de l'authentification MongoDB Express"""
    logger.info("🗄️ Test MongoDB Express auth...")

    try:
        # Test sans authentification
        response = requests.get("http://localhost:8081", timeout=5)
        logger.info(f"📊 MongoDB Express status: {response.status_code}")

        if response.status_code == 401:
            logger.info("ℹ️ MongoDB Express nécessite une authentification")
            logger.info("🔑 Login: admin / admin123")

            # Test avec authentification
            auth_response = requests.get(
                "http://localhost:8081", auth=("admin", "admin123"), timeout=5
            )

            if auth_response.status_code == 200:
                logger.info("✅ MongoDB Express accessible avec auth")
            else:
                logger.warning(f"⚠️ MongoDB Express auth: {auth_response.status_code}")

        elif response.status_code == 200:
            logger.info("✅ MongoDB Express accessible sans auth")
        else:
            logger.warning(f"⚠️ MongoDB Express: {response.status_code}")

    except Exception as e:
        logger.error(f"❌ Erreur MongoDB Express: {e}")


async def run_full_frontend_test():
    """Test complet frontend + WebSocket"""
    logger.info("🚀 Test complet frontend + WebSocket...")

    # Test 1: Interface frontend
    test_frontend_interface()

    # Test 2: MongoDB Express
    test_mongo_express_auth()

    # Test 3: WebSocket frontend
    await test_frontend_websocket()

    logger.info("✅ Test complet terminé !")


if __name__ == "__main__":
    asyncio.run(run_full_frontend_test())
