"""
Script de test simplifié pour l'interface utilisateur
Sans input() pour éviter les interruptions
"""

import asyncio
import websockets
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_ui_notifications():
    """Test des notifications pour l'interface utilisateur"""
    
    try:
        uri = "ws://localhost:8001/api/ws/ui_test_user"
        logger.info(f"🔌 Connexion à {uri}")
        
        async with websockets.connect(uri) as websocket:
            logger.info("✅ WebSocket connecté pour test UI")
            
            # Attendre que l'interface se charge
            logger.info("⏳ Attente 5 secondes pour que l'interface se charge...")
            await asyncio.sleep(5)
            
            # Test 1: Création de tâches
            logger.info("📝 Test création de tâches...")
            tasks = [
                {
                    "id": "ui_task_001",
                    "title": "Tester les notifications temps réel",
                    "status": "todo",
                    "priority": "high",
                    "category": "test"
                },
                {
                    "id": "ui_task_002", 
                    "title": "Vérifier le panel de notifications",
                    "status": "in_progress",
                    "priority": "medium",
                    "category": "ui"
                },
                {
                    "id": "ui_task_003",
                    "title": "Optimiser les performances",
                    "status": "todo",
                    "priority": "low",
                    "category": "performance"
                }
            ]
            
            for i, task in enumerate(tasks):
                task_message = {
                    "type": "task_update",
                    "task_data": task
                }
                await websocket.send(json.dumps(task_message))
                logger.info(f"📤 Tâche créée: {task['title']}")
                await asyncio.sleep(3)  # Attendre 3 secondes entre chaque tâche
            
            # Test 2: Modification de tâche
            logger.info("🔄 Test modification de tâche...")
            await asyncio.sleep(2)
            
            modified_task = {
                "id": "ui_task_001",
                "title": "Tester les notifications temps réel (TERMINÉ)",
                "status": "done",
                "priority": "high",
                "category": "test"
            }
            
            task_update = {
                "type": "task_update",
                "task_data": modified_task
            }
            await websocket.send(json.dumps(task_update))
            logger.info("📤 Tâche modifiée: statut terminé")
            
            # Test 3: Connexions utilisateur
            logger.info("👤 Test connexions utilisateur...")
            await asyncio.sleep(2)
            
            users = ["alice", "bob", "charlie"]
            for user in users:
                user_connected = {
                    "type": "user_connected",
                    "user_id": user
                }
                await websocket.send(json.dumps(user_connected))
                logger.info(f"📤 Utilisateur connecté: {user}")
                await asyncio.sleep(2)
            
            # Test 4: Monitoring PA
            logger.info("👁️ Test monitoring PA...")
            await asyncio.sleep(2)
            
            pa_monitoring = {
                "type": "pa_monitoring",
                "target_user_id": "ui_test_user"
            }
            await websocket.send(json.dumps(pa_monitoring))
            logger.info("📤 Monitoring PA activé")
            
            # Test 5: Suppression de tâche
            logger.info("🗑️ Test suppression de tâche...")
            await asyncio.sleep(3)
            
            deleted_task = {
                "id": "ui_task_003",
                "title": "Optimiser les performances",
                "status": "deleted",
                "priority": "low",
                "category": "performance"
            }
            
            task_delete = {
                "type": "task_update",
                "task_data": deleted_task
            }
            await websocket.send(json.dumps(task_delete))
            logger.info("📤 Tâche supprimée")
            
            # Attendre pour observer les notifications
            logger.info("⏳ Attente 10 secondes pour observer les notifications...")
            await asyncio.sleep(10)
            
            logger.info("✅ Test terminé ! Vérifiez les notifications dans l'interface.")
            logger.info("🌐 Ouvrez http://localhost:3000 et connectez-vous pour voir les notifications")
            
    except Exception as e:
        logger.error(f"❌ Erreur test UI: {e}")


async def continuous_test():
    """Test continu pour observer les notifications"""
    
    try:
        uri = "ws://localhost:8001/api/ws/continuous_test"
        logger.info(f"🔌 Connexion continue à {uri}")
        
        async with websockets.connect(uri) as websocket:
            logger.info("✅ WebSocket connecté pour test continu")
            logger.info("🔄 Envoi de notifications toutes les 5 secondes...")
            logger.info("🌐 Ouvrez http://localhost:3000 pour observer")
            
            counter = 1
            while True:
                # Créer une tâche de test
                task = {
                    "id": f"continuous_task_{counter:03d}",
                    "title": f"Tâche automatique #{counter}",
                    "status": "todo",
                    "priority": "medium",
                    "category": "test"
                }
                
                task_message = {
                    "type": "task_update",
                    "task_data": task
                }
                
                await websocket.send(json.dumps(task_message))
                logger.info(f"📤 Notification #{counter}: {task['title']}")
                
                counter += 1
                await asyncio.sleep(5)  # Attendre 5 secondes
                
    except Exception as e:
        logger.error(f"❌ Erreur test continu: {e}")


async def main():
    """Test principal"""
    print("🧪 TEST INTERFACE UTILISATEUR - NOTIFICATIONS")
    print("=" * 50)
    print("1. Test complet (recommandé)")
    print("2. Test continu")
    print("=" * 50)
    
    # Choisir automatiquement le test complet
    choice = "1"
    
    if choice == "1":
        logger.info("🚀 Lancement du test complet...")
        await test_ui_notifications()
    elif choice == "2":
        logger.info("🔄 Lancement du test continu...")
        await continuous_test()
    else:
        logger.info("🚀 Lancement du test complet par défaut...")
        await test_ui_notifications()


if __name__ == "__main__":
    asyncio.run(main()) 