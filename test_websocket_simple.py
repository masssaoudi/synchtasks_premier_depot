"""
Test simple pour vérifier le WebSocket
Version corrigée pour localhost:8000
"""

import asyncio
import websockets
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_websocket():
    """Test simple du WebSocket"""
    try:
        # Connexion WebSocket - port corrigé
        uri = "ws://localhost:8000/api/ws/test_user"
        logger.info(f"🔌 Connexion à {uri}")
        logger.info("⏳ Tentative de connexion...")

        async with websockets.connect(uri) as websocket:
            logger.info("✅ WebSocket connecté avec succès !")

            # Envoyer un ping
            ping_message = {"type": "ping", "timestamp": int(time.time())}
            await websocket.send(json.dumps(ping_message))
            logger.info("📤 Ping envoyé")

            # Recevoir la réponse
            response = await websocket.recv()
            data = json.loads(response)
            logger.info(f"📥 Réponse reçue: {data}")

            # Envoyer une mise à jour de tâche
            task_message = {
                "type": "task_update",
                "task_data": {
                    "id": "test_task_123",
                    "title": "Tâche de test WebSocket",
                    "status": "todo",
                    "timestamp": int(time.time())
                },
            }
            await websocket.send(json.dumps(task_message))
            logger.info("📤 Mise à jour tâche envoyée")

            # Attendre un peu pour voir les réponses
            await asyncio.sleep(3)

            # Envoyer un message de test
            test_message = {
                "type": "test_message",
                "content": "Test de debug WebSocket",
                "timestamp": int(time.time())
            }
            await websocket.send(json.dumps(test_message))
            logger.info("📤 Message de test envoyé")

            # Attendre encore un peu
            await asyncio.sleep(2)

            logger.info("✅ Test WebSocket réussi !")

    except websockets.exceptions.ConnectionRefusedError:
        logger.error("❌ Connexion refusée - Vérifiez que le serveur WebSocket est démarré")
    except websockets.exceptions.InvalidURI:
        logger.error("❌ URI WebSocket invalide")
    except Exception as e:
        logger.error(f"❌ Erreur test WebSocket: {e}")
        logger.error(f"Type d'erreur: {type(e).__name__}")


if __name__ == "__main__":
    logger.info("🚀 Démarrage du test WebSocket...")
    asyncio.run(test_websocket())
