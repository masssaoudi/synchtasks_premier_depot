import json
import logging
import os
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from datetime import datetime

logger = logging.getLogger(__name__)

# Variable d'environnement pour désactiver les WebSockets en mode test
DISABLE_WEBSOCKETS = os.getenv("DISABLE_WEBSOCKETS", "false").lower() == "true"

class ConnectionManager:
    """Gestionnaire des connexions WebSocket pour la synchronisation temps réel"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str = None):
        """Connecte un nouveau client WebSocket"""
        if DISABLE_WEBSOCKETS:
            logger.info("🔌 WebSockets désactivés - connexion ignorée")
            return
            
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
        
        logger.info(f"🔌 WebSocket connecté - Total: {len(self.active_connections)}")
        
        # Envoyer un message de bienvenue
        await self.send_personal_message({
            "type": "connection",
            "message": "Connecté au serveur temps réel",
            "user_id": user_id
        }, websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str = None):
        """Déconnecte un client WebSocket"""
        if DISABLE_WEBSOCKETS:
            return
            
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        logger.info(f"🔌 WebSocket déconnecté - Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Envoie un message à un client spécifique"""
        if DISABLE_WEBSOCKETS:
            return
            
        if websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"❌ Erreur envoi message personnel: {e}")
                self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any], exclude_user: str = None):
        """Diffuse un message à tous les clients connectés"""
        if DISABLE_WEBSOCKETS:
            logger.info("📡 Broadcast ignoré - WebSockets désactivés")
            return
            
        disconnected = []
        
        for connection in self.active_connections:
            if connection.client_state == WebSocketState.CONNECTED:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"❌ Erreur broadcast: {e}")
                    disconnected.append(connection)
        
        # Nettoyer les connexions défaillantes
        for connection in disconnected:
            self.disconnect(connection)
        
        logger.info(f"📡 Broadcast envoyé à {len(self.active_connections)} clients")
    
    async def broadcast_to_user(self, message: Dict[str, Any], user_id: str):
        """Diffuse un message à un utilisateur spécifique"""
        if DISABLE_WEBSOCKETS:
            return
            
        if user_id in self.user_connections:
            disconnected = []
            
            for connection in self.user_connections[user_id]:
                if connection.client_state == WebSocketState.CONNECTED:
                    try:
                        await connection.send_text(json.dumps(message))
                    except Exception as e:
                        logger.error(f"❌ Erreur broadcast utilisateur: {e}")
                        disconnected.append(connection)
            
            # Nettoyer les connexions défaillantes
            for connection in disconnected:
                self.disconnect(connection, user_id)
            
            logger.info(f"📡 Broadcast utilisateur {user_id}: {len(self.user_connections.get(user_id, []))} clients")

def serialize_task_data(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Sérialise les données de tâche pour JSON (convertit les datetime)"""
    serialized = {}
    for key, value in task_data.items():
        if isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, dict):
            serialized[key] = serialize_task_data(value)
        elif isinstance(value, list):
            serialized[key] = [
                serialize_task_data(item) if isinstance(item, dict) else item 
                for item in value
            ]
        else:
            serialized[key] = value
    return serialized

# Instance globale du gestionnaire de connexions
manager = ConnectionManager()

# Messages de synchronisation des tâches
async def broadcast_task_update(task_data: Dict[str, Any], action: str = "update"):
    """Diffuse une mise à jour de tâche à tous les clients"""
    if DISABLE_WEBSOCKETS:
        return
        
    # Sérialiser les données pour JSON
    serialized_task = serialize_task_data(task_data)
    
    message = {
        "type": "task_update",
        "action": action,  # "create", "update", "delete", "complete"
        "task": serialized_task,
        "timestamp": serialized_task.get("updated_at")
    }
    await manager.broadcast(message)

async def broadcast_task_created(task_data: Dict[str, Any]):
    """Diffuse la création d'une nouvelle tâche"""
    if DISABLE_WEBSOCKETS:
        return
    await broadcast_task_update(task_data, "create")

async def broadcast_task_updated(task_data: Dict[str, Any]):
    """Diffuse la mise à jour d'une tâche"""
    if DISABLE_WEBSOCKETS:
        return
    await broadcast_task_update(task_data, "update")

async def broadcast_task_deleted(task_id: str):
    """Diffuse la suppression d'une tâche"""
    if DISABLE_WEBSOCKETS:
        return
    message = {
        "type": "task_update",
        "action": "delete",
        "task_id": task_id,
        "timestamp": None
    }
    await manager.broadcast(message)

async def broadcast_task_completed(task_data: Dict[str, Any]):
    """Diffuse la completion d'une tâche"""
    if DISABLE_WEBSOCKETS:
        return
    await broadcast_task_update(task_data, "complete") 