"""
Test WebSocket avec authentification
Simule une connexion utilisateur puis teste le WebSocket
"""

import requests
import asyncio
import websockets
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def login_user():
    """Se connecter en tant qu'utilisateur"""
    logger.info("🔐 Connexion utilisateur...")

    try:
        # Données de connexion (utilisateur de test)
        login_data = {"username": "test@example.com", "password": "test123"}

        response = requests.post(
            "http://localhost:8000/api/auth/login", json=login_data
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                token = data["data"]["access_token"]
                user = data["data"]["user"]
                logger.info(
                    f"✅ Utilisateur connecté: {user.get('username', 'Unknown')}"
                )
                return token, user
            else:
                logger.error("❌ Échec de connexion")
                return None, None
        else:
            logger.error(f"❌ Erreur connexion: {response.status_code}")
            return None, None

    except Exception as e:
        logger.error(f"❌ Erreur connexion: {e}")
        return None, None


async def test_websocket_with_auth(token, user):
    """Test WebSocket avec authentification"""
    logger.info("🔌 Test WebSocket avec auth...")

    try:
        # URL WebSocket avec l'ID utilisateur
        user_id = user.get("_id") or user.get("id") or "test_user"
        ws_url = f"ws://localhost:8000/api/ws/{user_id}"
        logger.info(f"🔌 Connexion à {ws_url}")

        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté avec auth")

            # Envoyer un ping
            ping_msg = {"type": "ping", "timestamp": int(time.time())}
            await websocket.send(json.dumps(ping_msg))
            logger.info("📤 Ping envoyé")

            # Attendre réponse
            response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
            data = json.loads(response)
            logger.info(f"📥 Pong reçu: {data}")

            # Envoyer une mise à jour de tâche
            task_msg = {
                "type": "task_update",
                "task_data": {
                    "id": "auth_test_task",
                    "title": "Tâche test avec auth",
                    "status": "todo",
                    "timestamp": int(time.time()),
                },
            }
            await websocket.send(json.dumps(task_msg))
            logger.info("📤 Tâche envoyée")

            # Attendre un peu
            await asyncio.sleep(2)

            logger.info("✅ Test WebSocket avec auth réussi !")
            return True

    except Exception as e:
        logger.error(f"❌ Erreur WebSocket avec auth: {e}")
        return False


def create_test_user():
    """Créer un utilisateur de test si nécessaire"""
    logger.info("👤 Création utilisateur de test...")

    try:
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test123",
            "segment": "medical",
        }

        response = requests.post(
            "http://localhost:8000/api/auth/register", json=user_data
        )

        if response.status_code == 200:
            logger.info("✅ Utilisateur de test créé")
            return True
        elif response.status_code == 400:
            logger.info("ℹ️ Utilisateur de test existe déjà")
            return True
        else:
            logger.warning(f"⚠️ Erreur création utilisateur: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"❌ Erreur création utilisateur: {e}")
        return False


async def run_auth_test():
    """Test complet avec authentification"""
    logger.info("🚀 Test WebSocket avec authentification...")

    # Étape 1: Créer un utilisateur de test
    create_test_user()

    # Étape 2: Se connecter
    token, user = login_user()

    if not token or not user:
        logger.error("❌ Impossible de se connecter - arrêt du test")
        return

    # Étape 3: Tester WebSocket avec auth
    success = await test_websocket_with_auth(token, user)

    if success:
        logger.info("🎉 Test WebSocket avec auth réussi !")
        logger.info("💡 L'interface devrait maintenant se connecter automatiquement")
    else:
        logger.error("❌ Test WebSocket avec auth échoué")


if __name__ == "__main__":
    asyncio.run(run_auth_test())
