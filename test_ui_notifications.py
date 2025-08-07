"""
Test des notifications dans l'interface utilisateur
Envoie des notifications et vérifie qu'elles apparaissent dans l'UI
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

# ID d'Alice depuis la base de données
ALICE_USER_ID = "6889a312a274d15db190a36d"


async def send_ui_notifications():
    """Envoyer des notifications pour tester l'interface"""
    logger.info("🔔 Test des notifications dans l'interface...")

    try:
        # URL WebSocket avec l'ID d'Alice
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        logger.info(f"🔌 Connexion à {ws_url}")

        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour notifications UI")

            # Notification 1: Nouvelle tâche
            notification_1 = {
                "type": "notification",
                "title": "🎯 Nouvelle tâche créée",
                "message": "La tâche 'Réviser les mathématiques' a été ajoutée à votre liste",
                "category": "task_created",
                "priority": "normal",
                "timestamp": int(time.time()),
            }
            await websocket.send(json.dumps(notification_1))
            logger.info("📤 Notification 1 envoyée: Nouvelle tâche")

            await asyncio.sleep(3)

            # Notification 2: Tâche terminée
            notification_2 = {
                "type": "notification",
                "title": "✅ Tâche terminée",
                "message": "Félicitations ! Vous avez terminé 'Rendez-vous médecin'",
                "category": "task_completed",
                "priority": "high",
                "timestamp": int(time.time()),
            }
            await websocket.send(json.dumps(notification_2))
            logger.info("📤 Notification 2 envoyée: Tâche terminée")

            await asyncio.sleep(3)

            # Notification 3: Rappel urgent
            notification_3 = {
                "type": "notification",
                "title": "⏰ Rappel urgent",
                "message": "Votre rendez-vous médical est dans 15 minutes !",
                "category": "reminder",
                "priority": "urgent",
                "timestamp": int(time.time()),
            }
            await websocket.send(json.dumps(notification_3))
            logger.info("📤 Notification 3 envoyée: Rappel urgent")

            await asyncio.sleep(3)

            # Notification 4: Message système
            notification_4 = {
                "type": "notification",
                "title": "🔧 Système",
                "message": "WebSocket temps réel opérationnel - notifications actives",
                "category": "system",
                "priority": "info",
                "timestamp": int(time.time()),
            }
            await websocket.send(json.dumps(notification_4))
            logger.info("📤 Notification 4 envoyée: Message système")

            logger.info("✅ Toutes les notifications envoyées")
            logger.info("💡 Vérifiez l'interface pour voir les notifications")

    except Exception as e:
        logger.error(f"❌ Erreur envoi notifications UI: {e}")


async def test_task_realtime_updates():
    """Test des mises à jour de tâches en temps réel"""
    logger.info("📋 Test des mises à jour de tâches en temps réel...")

    try:
        ws_url = f"ws://localhost:8000/api/ws/{ALICE_USER_ID}"
        async with websockets.connect(ws_url) as websocket:
            logger.info("✅ WebSocket connecté pour mises à jour temps réel")

            # Mise à jour 1: Tâche en cours
            task_update_1 = {
                "type": "task_update",
                "task_data": {
                    "id": "task_math_001",
                    "title": "Réviser les mathématiques",
                    "status": "en_cours",
                    "priority": "high",
                    "category": "académique",
                    "timestamp": int(time.time()),
                },
            }
            await websocket.send(json.dumps(task_update_1))
            logger.info("📤 Mise à jour 1: Tâche en cours")

            await asyncio.sleep(3)

            # Mise à jour 2: Tâche terminée
            task_update_2 = {
                "type": "task_update",
                "task_data": {
                    "id": "task_med_002",
                    "title": "Rendez-vous médecin",
                    "status": "terminé",
                    "priority": "urgent",
                    "category": "santé",
                    "timestamp": int(time.time()),
                },
            }
            await websocket.send(json.dumps(task_update_2))
            logger.info("📤 Mise à jour 2: Tâche terminée")

            await asyncio.sleep(3)

            # Mise à jour 3: Nouvelle tâche
            task_update_3 = {
                "type": "task_update",
                "task_data": {
                    "id": "task_sport_003",
                    "title": "Faire du sport",
                    "status": "todo",
                    "priority": "normal",
                    "category": "santé",
                    "timestamp": int(time.time()),
                },
            }
            await websocket.send(json.dumps(task_update_3))
            logger.info("📤 Mise à jour 3: Nouvelle tâche")

            logger.info("✅ Mises à jour de tâches envoyées")

    except Exception as e:
        logger.error(f"❌ Erreur mises à jour temps réel: {e}")


async def run_ui_notification_tests():
    """Tests complets des notifications dans l'interface"""
    logger.info("🚀 Tests des notifications dans l'interface...")

    # Étape 1: Test des notifications
    await send_ui_notifications()

    # Étape 2: Test des mises à jour de tâches
    await test_task_realtime_updates()

    logger.info("🎉 Tests des notifications dans l'interface terminés !")
    logger.info("💡 Instructions pour vérifier:")
    logger.info("   1. Ouvrez http://localhost:3000")
    logger.info("   2. Connectez-vous avec alice@test.com / alice123")
    logger.info("   3. Cliquez sur l'icône de cloche (🔔) pour voir les notifications")
    logger.info("   4. Vérifiez que les notifications apparaissent en temps réel")
    logger.info("   5. Les tâches devraient se mettre à jour automatiquement")


if __name__ == "__main__":
    asyncio.run(run_ui_notification_tests())
