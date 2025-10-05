"""
Diagnostic et correction du WebSocket dans l'interface
Force la connexion WebSocket pour résoudre le problème d'affichage
"""

import asyncio
import websockets
import json
import logging
import time
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ID d'Alice depuis la base de données
ALICE_USER_ID = "6889a312a274d15db190a36d"
ALICE_EMAIL = "alice@test.com"
ALICE_PASSWORD = "alice123"


def login_alice_api():
    """Se connecter avec Alice via l'API"""
    logger.info("👤 Connexion API avec Alice...")
    
    try:
        login_data = {
            "username": ALICE_EMAIL,
            "password": ALICE_PASSWORD
        }
        
        response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                token = data['data']['access_token']
                user = data['data']['user']
                logger.info(f"✅ Alice connectée via API: {user.get('username', 'alice')}")
                return token, user
            else:
                logger.error("❌ Échec de connexion API Alice")
                return None, None
        else:
            logger.error(f"❌ Erreur connexion API Alice: {response.status_code}")
            return None, None
            
    except Exception as e:
        logger.error(f"❌ Erreur connexion API Alice: {e}")
        return None, None


async def force_ui_websocket_connection():
    """Force la connexion WebSocket pour l'interface"""
    logger.info("🔌 Force connexion WebSocket pour l'interface...")
    
    try:
        # URL WebSocket avec l'ID d'Alice
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        logger.info(f"🔌 Connexion à {ws_url}")
        
        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour l'interface")
            
            # Envoyer un message de connexion utilisateur
            user_connect_msg = {
                "type": "user_connected",
                "user_id": ALICE_USER_ID,
                "username": "alice",
                "timestamp": int(time.time())
            }
            await websocket.send(json.dumps(user_connect_msg))
            logger.info("📤 Message de connexion utilisateur envoyé")
            
            # Envoyer une notification de test
            notification_msg = {
                "type": "notification",
                "title": "Test WebSocket",
                "message": "Connexion WebSocket forcée pour l'interface",
                "user_id": ALICE_USER_ID,
                "timestamp": int(time.time())
            }
            await websocket.send(json.dumps(notification_msg))
            logger.info("📤 Notification de test envoyée")
            
            # Maintenir la connexion active
            logger.info("🔄 Maintien de la connexion WebSocket...")
            await asyncio.sleep(30)  # Maintenir 30 secondes
            
            logger.info("✅ Connexion WebSocket forcée réussie !")
            return True
            
    except Exception as e:
        logger.error(f"❌ Erreur connexion WebSocket forcée: {e}")
        return False


async def test_websocket_broadcast():
    """Test de broadcast WebSocket"""
    logger.info("📡 Test de broadcast WebSocket...")
    
    try:
        # Connexion WebSocket
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour broadcast")
            
            # Envoyer un message de broadcast
            broadcast_msg = {
                "type": "broadcast",
                "message": "Test de broadcast WebSocket",
                "user_id": ALICE_USER_ID,
                "timestamp": int(time.time())
            }
            await websocket.send(json.dumps(broadcast_msg))
            logger.info("📤 Message de broadcast envoyé")
            
            # Attendre un peu
            await asyncio.sleep(5)
            
            logger.info("✅ Test de broadcast terminé")
            return True
            
    except Exception as e:
        logger.error(f"❌ Erreur test broadcast: {e}")
        return False


def check_frontend_status():
    """Vérifier le statut du frontend"""
    logger.info("🌐 Vérification du statut frontend...")
    
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


async def run_ui_websocket_fix():
    """Correction complète du WebSocket pour l'interface"""
    logger.info("🚀 Correction WebSocket pour l'interface...")
    
    # Étape 1: Vérifier le frontend
    frontend_ok = check_frontend_status()
    
    # Étape 2: Se connecter avec Alice
    token, user = login_alice_api()
    
    if not token or not user:
        logger.error("❌ Impossible de se connecter avec Alice - arrêt de la correction")
        return
    
    # Étape 3: Force connexion WebSocket
    success = await force_ui_websocket_connection()
    
    if success:
        logger.info("🎉 Connexion WebSocket forcée réussie !")
        
        # Étape 4: Test de broadcast
        await test_websocket_broadcast()
        
        logger.info("💡 Instructions pour l'interface:")
        logger.info("   1. Ouvrez http://localhost:3000")
        logger.info("   2. Connectez-vous avec alice@test.com / alice123")
        logger.info("   3. Le WebSocket devrait maintenant afficher 'connecté'")
        logger.info("   4. Vérifiez les notifications temps réel")
        logger.info("   5. Si toujours 'déconnecté', rechargez la page (Ctrl+F5)")
        
    else:
        logger.error("❌ Connexion WebSocket forcée échouée")
        logger.info("🔍 Vérifiez les logs: docker-compose logs backend --tail=10")


if __name__ == "__main__":
    asyncio.run(run_ui_websocket_fix()) 