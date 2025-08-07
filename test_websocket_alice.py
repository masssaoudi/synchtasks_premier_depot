"""
Test WebSocket avec l'utilisateur alice connecté
Force la connexion WebSocket pour l'utilisateur actuel
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


def get_alice_user():
    """Récupérer les informations de l'utilisateur alice"""
    logger.info("👤 Récupération utilisateur alice...")

    try:
        # Se connecter avec alice
        login_data = {
            "username": "alice@example.com",  # ou l'email d'alice
            "password": "alice123",  # ou le mot de passe d'alice
        }

        response = requests.post(
            "http://localhost:8000/api/auth/login", json=login_data
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                token = data["data"]["access_token"]
                user = data["data"]["user"]
                logger.info(
                    f"✅ Utilisateur alice connecté: {user.get('username', 'alice')}"
                )
                return token, user
            else:
                logger.error("❌ Échec de connexion alice")
                return None, None
        else:
            logger.error(f"❌ Erreur connexion alice: {response.status_code}")
            return None, None

    except Exception as e:
        logger.error(f"❌ Erreur connexion alice: {e}")
        return None, None


async def test_websocket_alice(token, user):
    """Test WebSocket avec l'utilisateur alice"""
    logger.info("🔌 Test WebSocket avec alice...")

    try:
        # URL WebSocket avec l'ID utilisateur alice
        user_id = user.get("_id") or user.get("id") or "alice"
        ws_url = f"ws://localhost:8000/api/ws/{user_id}"
        logger.info(f"🔌 Connexion à {ws_url}")

        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté avec alice")

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
                    "id": "alice_test_task",
                    "title": "Tâche test alice",
                    "status": "todo",
                    "timestamp": int(time.time()),
                },
            }
            await websocket.send(json.dumps(task_msg))
            logger.info("📤 Tâche envoyée")

            # Attendre un peu
            await asyncio.sleep(2)

            logger.info("✅ Test WebSocket avec alice réussi !")
            return True

    except Exception as e:
        logger.error(f"❌ Erreur WebSocket avec alice: {e}")
        return False


def create_alice_user():
    """Créer l'utilisateur alice si nécessaire"""
    logger.info("👤 Création utilisateur alice...")

    try:
        user_data = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "alice123",
            "segment": "particuliers",
        }

        response = requests.post(
            "http://localhost:8000/api/auth/register", json=user_data
        )

        if response.status_code == 200:
            logger.info("✅ Utilisateur alice créé")
            return True
        elif response.status_code == 400:
            logger.info("ℹ️ Utilisateur alice existe déjà")
            return True
        else:
            logger.warning(f"⚠️ Erreur création alice: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"❌ Erreur création alice: {e}")
        return False


async def run_alice_test():
    """Test complet avec l'utilisateur alice"""
    logger.info("🚀 Test WebSocket avec utilisateur alice...")

    # Étape 1: Créer l'utilisateur alice
    create_alice_user()

    # Étape 2: Se connecter avec alice
    token, user = get_alice_user()

    if not token or not user:
        logger.error("❌ Impossible de se connecter avec alice - arrêt du test")
        return

    # Étape 3: Tester WebSocket avec alice
    success = await test_websocket_alice(token, user)

    if success:
        logger.info("🎉 Test WebSocket avec alice réussi !")
        logger.info("💡 L'interface devrait maintenant se connecter automatiquement")
        logger.info("🔍 Vérifiez les logs: docker-compose logs backend --tail=10")
    else:
        logger.error("❌ Test WebSocket avec alice échoué")


if __name__ == "__main__":
    asyncio.run(run_alice_test())
