"""
Force la connexion WebSocket pour Alice et diagnostique le problème
Utilise l'ID d'Alice depuis la base de données
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


def login_alice():
    """Se connecter avec Alice"""
    logger.info("👤 Connexion avec Alice...")
    
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
                logger.info(f"✅ Alice connectée: {user.get('username', 'alice')}")
                return token, user
            else:
                logger.error("❌ Échec de connexion Alice")
                return None, None
        else:
            logger.error(f"❌ Erreur connexion Alice: {response.status_code}")
            return None, None
            
    except Exception as e:
        logger.error(f"❌ Erreur connexion Alice: {e}")
        return None, None


async def force_alice_websocket():
    """Force la connexion WebSocket pour Alice"""
    logger.info("🔌 Force connexion WebSocket pour Alice...")
    
    try:
        # URL WebSocket avec l'ID d'Alice
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        logger.info(f"🔌 Connexion à {ws_url}")
        
        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour Alice")
            
            # Envoyer un ping
            ping_msg = {"type": "ping", "timestamp": int(time.time())}
            await websocket.send(json.dumps(ping_msg))
            logger.info("📤 Ping envoyé")
            
            # Attendre réponse
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                data = json.loads(response)
                logger.info(f"📥 Pong reçu: {data}")
            except asyncio.TimeoutError:
                logger.warning("⚠️ Pas de réponse au ping (timeout)")
            
            # Envoyer une notification de connexion
            connect_msg = {
                "type": "user_connected",
                "user_id": ALICE_USER_ID,
                "username": "alice",
                "timestamp": int(time.time())
            }
            await websocket.send(json.dumps(connect_msg))
            logger.info("📤 Notification de connexion envoyée")
            
            # Maintenir la connexion active
            logger.info("🔄 Maintien de la connexion WebSocket...")
            await asyncio.sleep(15)  # Maintenir 15 secondes
            
            logger.info("✅ Connexion WebSocket forcée réussie !")
            return True
            
    except Exception as e:
        logger.error(f"❌ Erreur connexion WebSocket forcée: {e}")
        return False


async def test_multiple_alice_connections():
    """Test de plusieurs connexions WebSocket pour Alice"""
    logger.info("🔌 Test de plusieurs connexions WebSocket pour Alice...")
    
    connections = []
    
    for i in range(3):
        try:
            ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
            logger.info(f"🔌 Connexion {i+1} à {ws_url}")
            
            websocket = await websockets.connect(ws_url)
            connections.append(websocket)
            
            # Envoyer un ping
            ping_msg = {"type": "ping", "timestamp": int(time.time())}
            await websocket.send(json.dumps(ping_msg))
            logger.info(f"📤 Ping envoyé pour connexion {i+1}")
            
        except Exception as e:
            logger.error(f"❌ Erreur connexion {i+1}: {e}")
    
    logger.info(f"✅ {len(connections)} connexions WebSocket établies")
    
    # Maintenir les connexions
    await asyncio.sleep(10)
    
    # Fermer les connexions
    for websocket in connections:
        await websocket.close()
    
    logger.info("✅ Test de plusieurs connexions terminé")


async def check_backend_websocket_logs():
    """Vérifier les logs du backend pour les connexions WebSocket"""
    logger.info("📋 Vérification des logs backend...")
    
    try:
        # Simuler une connexion pour déclencher des logs
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        async with websockets.connect(ws_url) as websocket:
            logger.info("🔌 Connexion de test établie")
            await asyncio.sleep(2)
        
        logger.info("✅ Connexion de test terminée")
        logger.info("🔍 Vérifiez les logs: docker-compose logs backend --tail=20")
        
    except Exception as e:
        logger.error(f"❌ Erreur connexion de test: {e}")


async def run_alice_diagnostic():
    """Diagnostic complet pour Alice"""
    logger.info("🚀 Diagnostic complet WebSocket pour Alice...")
    
    # Étape 1: Se connecter avec Alice
    token, user = login_alice()
    
    if not token or not user:
        logger.error("❌ Impossible de se connecter avec Alice - arrêt du diagnostic")
        return
    
    # Étape 2: Force connexion WebSocket
    success = await force_alice_websocket()
    
    if success:
        logger.info("🎉 Connexion WebSocket forcée réussie !")
        
        # Étape 3: Test de plusieurs connexions
        await test_multiple_alice_connections()
        
        # Étape 4: Vérifier les logs
        await check_backend_websocket_logs()
        
        logger.info("💡 Instructions pour l'interface:")
        logger.info("   1. Rechargez la page (Ctrl+F5)")
        logger.info("   2. Connectez-vous avec alice@test.com / alice123")
        logger.info("   3. Le WebSocket devrait se connecter automatiquement")
        logger.info("   4. Vérifiez le statut 'WebSocket connecté'")
        
    else:
        logger.error("❌ Connexion WebSocket forcée échouée")
        logger.info("🔍 Vérifiez les logs: docker-compose logs backend --tail=20")


if __name__ == "__main__":
    asyncio.run(run_alice_diagnostic()) 