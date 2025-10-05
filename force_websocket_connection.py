"""
Force la connexion WebSocket pour l'utilisateur alice
Utilise l'ID utilisateur d'alice pour forcer la connexion WebSocket
"""

import asyncio
import websockets
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def force_websocket_connection():
    """Force la connexion WebSocket pour alice"""
    logger.info("🔌 Force connexion WebSocket pour alice...")

    # ID utilisateur d'alice depuis les logs (6889a312a274d15db190a36d)
    alice_user_id = "6889a312a274d15db190a36d"

    try:
        # URL WebSocket avec l'ID utilisateur alice
        ws_url = f"ws://localhost:8000/api/ws/{alice_user_id}"
        logger.info(f"🔌 Connexion forcée à {ws_url}")

        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour alice")

            # Envoyer un ping
            ping_msg = {"type": "ping", "timestamp": int(time.time())}
            await websocket.send(json.dumps(ping_msg))
            logger.info("📤 Ping envoyé")

            # Attendre réponse
            response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
            data = json.loads(response)
            logger.info(f"📥 Pong reçu: {data}")

            # Envoyer une notification de connexion
            connect_msg = {
                "type": "user_connected",
                "user_id": alice_user_id,
                "username": "alice",
                "timestamp": int(time.time()),
            }
            await websocket.send(json.dumps(connect_msg))
            logger.info("📤 Notification de connexion envoyée")

            # Maintenir la connexion active
            logger.info("🔄 Maintien de la connexion WebSocket...")
            await asyncio.sleep(10)  # Maintenir 10 secondes

            logger.info("✅ Connexion WebSocket forcée réussie !")
            return True

    except Exception as e:
        logger.error(f"❌ Erreur connexion WebSocket forcée: {e}")
        return False


async def test_multiple_connections():
    """Test de plusieurs connexions WebSocket"""
    logger.info("🔌 Test de plusieurs connexions WebSocket...")

    # IDs utilisateurs de test
    user_ids = ["6889a312a274d15db190a36d", "test_user_1", "test_user_2"]  # alice

    connections = []

    for i, user_id in enumerate(user_ids):
        try:
            ws_url = f"ws://localhost:8000/api/ws/{user_id}"
            logger.info(f"🔌 Connexion {i+1} à {ws_url}")

            websocket = await websockets.connect(ws_url)
            connections.append(websocket)

            # Envoyer un ping
            ping_msg = {"type": "ping", "timestamp": int(time.time())}
            await websocket.send(json.dumps(ping_msg))
            logger.info(f"📤 Ping envoyé pour utilisateur {i+1}")

        except Exception as e:
            logger.error(f"❌ Erreur connexion {i+1}: {e}")

    logger.info(f"✅ {len(connections)} connexions WebSocket établies")

    # Maintenir les connexions
    await asyncio.sleep(5)

    # Fermer les connexions
    for websocket in connections:
        await websocket.close()

    logger.info("✅ Test de plusieurs connexions terminé")


async def run_force_test():
    """Test complet de force connexion"""
    logger.info("🚀 Test de force connexion WebSocket...")

    # Test 1: Force connexion pour alice
    success = await force_websocket_connection()

    if success:
        logger.info("🎉 Force connexion réussie !")
        logger.info(
            "💡 Vérifiez maintenant l'interface - le WebSocket devrait être connecté"
        )
        logger.info("🔍 Command: docker-compose logs backend --tail=10")
    else:
        logger.error("❌ Force connexion échouée")

    # Test 2: Test de plusieurs connexions
    await test_multiple_connections()


if __name__ == "__main__":
    asyncio.run(run_force_test())
