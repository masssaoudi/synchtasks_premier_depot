"""
Test des notifications temps réel via WebSocket
Envoie des notifications à Alice et vérifie qu'elles apparaissent dans l'interface
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


def login_alice():
    """Se connecter avec Alice"""
    logger.info("👤 Connexion avec Alice...")
    
    try:
        login_data = {
            "username": "alice@test.com",
            "password": "alice123"
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


async def send_notification_test():
    """Envoyer une notification de test via WebSocket"""
    logger.info("🔔 Test de notification temps réel...")
    
    try:
        # URL WebSocket avec l'ID d'Alice
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        logger.info(f"🔌 Connexion à {ws_url}")
        
        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour notifications")
            
            # Notification 1: Tâche créée
            notification_1 = {
                "type": "notification",
                "title": "Nouvelle tâche créée",
                "message": "Une nouvelle tâche 'Réviser les maths' a été créée",
                "user_id": ALICE_USER_ID,
                "timestamp": int(time.time()),
                "category": "task_created",
                "priority": "normal"
            }
            await websocket.send(json.dumps(notification_1))
            logger.info("📤 Notification 1 envoyée: Tâche créée")
            
            await asyncio.sleep(2)
            
            # Notification 2: Tâche mise à jour
            notification_2 = {
                "type": "notification",
                "title": "Tâche mise à jour",
                "message": "La tâche 'Rendez-vous médecin' a été marquée comme terminée",
                "user_id": ALICE_USER_ID,
                "timestamp": int(time.time()),
                "category": "task_updated",
                "priority": "high"
            }
            await websocket.send(json.dumps(notification_2))
            logger.info("📤 Notification 2 envoyée: Tâche mise à jour")
            
            await asyncio.sleep(2)
            
            # Notification 3: Rappel
            notification_3 = {
                "type": "notification",
                "title": "Rappel important",
                "message": "N'oubliez pas votre rendez-vous médical dans 30 minutes",
                "user_id": ALICE_USER_ID,
                "timestamp": int(time.time()),
                "category": "reminder",
                "priority": "urgent"
            }
            await websocket.send(json.dumps(notification_3))
            logger.info("📤 Notification 3 envoyée: Rappel urgent")
            
            await asyncio.sleep(2)
            
            # Notification 4: Message système
            notification_4 = {
                "type": "notification",
                "title": "Système",
                "message": "WebSocket temps réel opérationnel - notifications actives",
                "user_id": ALICE_USER_ID,
                "timestamp": int(time.time()),
                "category": "system",
                "priority": "info"
            }
            await websocket.send(json.dumps(notification_4))
            logger.info("📤 Notification 4 envoyée: Message système")
            
            logger.info("✅ Toutes les notifications envoyées")
            logger.info("💡 Vérifiez l'interface pour voir les notifications")
            
    except Exception as e:
        logger.error(f"❌ Erreur envoi notifications: {e}")


async def test_task_updates():
    """Test des mises à jour de tâches temps réel"""
    logger.info("📋 Test des mises à jour de tâches temps réel...")
    
    try:
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour mises à jour tâches")
            
            # Mise à jour tâche 1
            task_update_1 = {
                "type": "task_update",
                "task_data": {
                    "id": "task_123",
                    "title": "Réviser les maths",
                    "status": "en_cours",
                    "priority": "high",
                    "timestamp": int(time.time())
                },
                "user_id": ALICE_USER_ID
            }
            await websocket.send(json.dumps(task_update_1))
            logger.info("📤 Mise à jour tâche 1 envoyée")
            
            await asyncio.sleep(2)
            
            # Mise à jour tâche 2
            task_update_2 = {
                "type": "task_update",
                "task_data": {
                    "id": "task_456",
                    "title": "Faire du sport",
                    "status": "terminé",
                    "priority": "normal",
                    "timestamp": int(time.time())
                },
                "user_id": ALICE_USER_ID
            }
            await websocket.send(json.dumps(task_update_2))
            logger.info("📤 Mise à jour tâche 2 envoyée")
            
            logger.info("✅ Mises à jour de tâches envoyées")
            
    except Exception as e:
        logger.error(f"❌ Erreur mises à jour tâches: {e}")


async def run_notification_tests():
    """Tests complets des notifications temps réel"""
    logger.info("🚀 Tests des notifications temps réel...")
    
    # Étape 1: Se connecter avec Alice
    token, user = login_alice()
    
    if not token or not user:
        logger.error("❌ Impossible de se connecter avec Alice - arrêt des tests")
        return
    
    # Étape 2: Test des notifications
    await send_notification_test()
    
    # Étape 3: Test des mises à jour de tâches
    await test_task_updates()
    
    logger.info("🎉 Tests des notifications temps réel terminés !")
    logger.info("💡 Instructions:")
    logger.info("   1. Vérifiez l'interface pour voir les notifications")
    logger.info("   2. Cliquez sur l'icône de cloche pour voir les notifications")
    logger.info("   3. Les tâches devraient se mettre à jour en temps réel")


if __name__ == "__main__":
    asyncio.run(run_notification_tests()) 