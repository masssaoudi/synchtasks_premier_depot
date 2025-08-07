"""
Script de debug complet pour WebSocket SyncTasks
Teste tous les aspects : connexion, authentification, messages, rooms
"""

import asyncio
import websockets
import json
import logging
import time
import requests
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WebSocketDebugger:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.ws_url = "ws://localhost:8000/api/ws"
        self.test_user_id = "debug_user_123"
        self.test_token = None

    async def test_backend_health(self):
        """Test de santé du backend"""
        logger.info("🔍 Test de santé du backend...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Backend en bonne santé")
                return True
            else:
                logger.error(f"❌ Backend non disponible: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Erreur connexion backend: {e}")
            return False

    async def test_websocket_endpoint(self):
        """Test de l'endpoint WebSocket"""
        logger.info("🔍 Test de l'endpoint WebSocket...")
        try:
            # Test sans authentification
            uri = f"{self.ws_url}/{self.test_user_id}"
            logger.info(f"🔌 Tentative de connexion à {uri}")

            async with websockets.connect(uri) as websocket:
                logger.info("✅ Connexion WebSocket réussie !")

                # Test ping
                await self.test_ping(websocket)

                # Test messages
                await self.test_messages(websocket)

                # Test rooms
                await self.test_rooms(websocket)

                return True

        except websockets.exceptions.ConnectionRefusedError:
            logger.error("❌ Connexion refusée - WebSocket non disponible")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur WebSocket: {e}")
            return False

    async def test_ping(self, websocket):
        """Test du ping/pong"""
        logger.info("🏓 Test ping/pong...")
        try:
            ping_msg = {"type": "ping", "timestamp": int(time.time())}
            await websocket.send(json.dumps(ping_msg))
            logger.info("📤 Ping envoyé")

            # Attendre réponse
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            logger.info(f"📥 Pong reçu: {data}")

        except asyncio.TimeoutError:
            logger.warning("⚠️ Pas de réponse ping/pong (timeout)")
        except Exception as e:
            logger.error(f"❌ Erreur ping/pong: {e}")

    async def test_messages(self, websocket):
        """Test des messages"""
        logger.info("💬 Test des messages...")

        test_messages = [
            {
                "type": "task_update",
                "task_data": {
                    "id": "debug_task_1",
                    "title": "Tâche de debug",
                    "status": "in_progress",
                    "timestamp": int(time.time()),
                },
            },
            {
                "type": "notification",
                "content": "Test notification",
                "level": "info",
                "timestamp": int(time.time()),
            },
            {
                "type": "user_status",
                "user_id": self.test_user_id,
                "status": "online",
                "timestamp": int(time.time()),
            },
        ]

        for i, msg in enumerate(test_messages):
            try:
                await websocket.send(json.dumps(msg))
                logger.info(f"📤 Message {i+1} envoyé: {msg['type']}")

                # Attendre un peu
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"❌ Erreur envoi message {i+1}: {e}")

    async def test_rooms(self, websocket):
        """Test des rooms"""
        logger.info("🏠 Test des rooms...")

        room_tests = [
            {"type": "join_room", "room_id": "debug_room_1"},
            {"type": "leave_room", "room_id": "debug_room_1"},
            {"type": "join_room", "room_id": "debug_room_2"},
        ]

        for i, room_msg in enumerate(room_tests):
            try:
                await websocket.send(json.dumps(room_msg))
                logger.info(f"📤 Room message {i+1} envoyé: {room_msg['type']}")
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"❌ Erreur room message {i+1}: {e}")

    async def test_connection_stability(self):
        """Test de stabilité de connexion"""
        logger.info("🔗 Test de stabilité de connexion...")

        try:
            uri = f"{self.ws_url}/{self.test_user_id}"
            async with websockets.connect(uri) as websocket:
                logger.info("✅ Connexion établie")

                # Envoyer des messages pendant 10 secondes
                start_time = time.time()
                message_count = 0

                while time.time() - start_time < 10:
                    try:
                        msg = {
                            "type": "stability_test",
                            "message_id": message_count,
                            "timestamp": int(time.time()),
                        }
                        await websocket.send(json.dumps(msg))
                        message_count += 1
                        await asyncio.sleep(0.5)

                    except Exception as e:
                        logger.error(
                            f"❌ Erreur stabilité message {message_count}: {e}"
                        )
                        break

                logger.info(
                    f"✅ Test stabilité terminé: {message_count} messages envoyés"
                )

        except Exception as e:
            logger.error(f"❌ Erreur test stabilité: {e}")

    async def run_full_debug(self):
        """Exécuter tous les tests de debug"""
        logger.info("🚀 Démarrage du debug WebSocket complet...")

        # Test 1: Santé du backend
        backend_ok = await self.test_backend_health()
        if not backend_ok:
            logger.error("❌ Backend non disponible - arrêt du debug")
            return

        # Test 2: Endpoint WebSocket
        ws_ok = await self.test_websocket_endpoint()
        if not ws_ok:
            logger.error("❌ WebSocket non fonctionnel")
            return

        # Test 3: Stabilité
        await self.test_connection_stability()

        logger.info("✅ Debug WebSocket terminé !")


async def main():
    debugger = WebSocketDebugger()
    await debugger.run_full_debug()


if __name__ == "__main__":
    asyncio.run(main())
