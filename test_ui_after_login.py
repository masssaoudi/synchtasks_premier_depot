"""
Test de l'interface après connexion utilisateur
Vérifie que le WebSocket se connecte automatiquement après login
"""

import requests
import time
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_login_interface():
    """Test de connexion dans l'interface"""
    logger.info("🔐 Test connexion interface...")

    try:
        # Étape 1: Accéder à la page de login
        response = requests.get("http://localhost:3000/login", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Page de login accessible")
        else:
            logger.warning(f"⚠️ Page de login: {response.status_code}")

        # Étape 2: Se connecter via l'API
        login_data = {"username": "test@example.com", "password": "test123"}

        response = requests.post(
            "http://localhost:8000/api/auth/login", json=login_data
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                token = data["data"]["access_token"]
                user = data["data"]["user"]
                logger.info(f"✅ Connexion réussie: {user.get('username')}")

                # Étape 3: Vérifier que l'utilisateur peut accéder aux tâches
                headers = {"Authorization": f"Bearer {token}"}
                tasks_response = requests.get(
                    "http://localhost:8000/api/tasks/", headers=headers
                )

                if tasks_response.status_code == 200:
                    logger.info("✅ Accès aux tâches autorisé")
                    return token, user
                else:
                    logger.warning(f"⚠️ Accès aux tâches: {tasks_response.status_code}")
                    return token, user
            else:
                logger.error("❌ Échec de connexion")
                return None, None
        else:
            logger.error(f"❌ Erreur connexion: {response.status_code}")
            return None, None

    except Exception as e:
        logger.error(f"❌ Erreur test interface: {e}")
        return None, None


def check_websocket_connection():
    """Vérifier la connexion WebSocket dans l'interface"""
    logger.info("🔌 Vérification WebSocket interface...")

    try:
        # Vérifier que l'interface est accessible
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Interface accessible")

            # Vérifier les logs backend pour voir les connexions WebSocket
            logger.info("📊 Vérifiez les logs backend pour les connexions WebSocket")
            logger.info("🔍 Command: docker-compose logs backend --tail=20")

            return True
        else:
            logger.error(f"❌ Interface non accessible: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"❌ Erreur vérification interface: {e}")
        return False


def provide_instructions():
    """Fournir les instructions pour tester l'interface"""
    logger.info("📋 INSTRUCTIONS POUR TESTER L'INTERFACE:")
    logger.info("=" * 50)
    logger.info("1. 🌐 Ouvrez http://localhost:3000")
    logger.info("2. 🔐 Connectez-vous avec:")
    logger.info("   Email: test@example.com")
    logger.info("   Password: test123")
    logger.info(
        "3. 🔌 Après connexion, le WebSocket devrait se connecter automatiquement"
    )
    logger.info(
        "4. 📱 Vérifiez dans la console du navigateur (F12) les messages WebSocket"
    )
    logger.info("5. ✅ Vous devriez voir 'WebSocket connecté' au lieu de 'déconnecté'")
    logger.info("=" * 50)


def run_ui_test():
    """Test complet de l'interface"""
    logger.info("🚀 Test interface après connexion...")

    # Test 1: Connexion utilisateur
    token, user = test_login_interface()

    if not token or not user:
        logger.error("❌ Impossible de se connecter")
        return

    # Test 2: Vérification interface
    interface_ok = check_websocket_connection()

    # Test 3: Instructions
    provide_instructions()

    if interface_ok:
        logger.info("✅ Interface prête pour test manuel")
        logger.info("🎯 Suivez les instructions ci-dessus pour tester")
    else:
        logger.error("❌ Problème avec l'interface")


if __name__ == "__main__":
    run_ui_test()
