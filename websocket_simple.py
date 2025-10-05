"""
WebSocket simple et propre pour SyncTasks
Version épurée sans complexité inutile
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import logging
import time

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Gestionnaire de connexions WebSocket simple"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_rooms: Dict[str, List[str]] = {}  # user_id -> [room_ids]
        self.room_users: Dict[str, List[str]] = {}  # room_id -> [user_ids]
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Connecter un utilisateur"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"✅ Utilisateur {user_id} connecté")
        
        # Notifier les autres utilisateurs
        await self.broadcast_to_others(user_id, {
            "type": "user_connected",
            "user_id": user_id
        })
    
    def disconnect(self, user_id: str):
        """Déconnecter un utilisateur"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"🔌 Utilisateur {user_id} déconnecté")
            
            # Nettoyer les rooms
            if user_id in self.user_rooms:
                rooms = self.user_rooms[user_id].copy()
                for room_id in rooms:
                    self.leave_room(user_id, room_id)
                del self.user_rooms[user_id]
            
            # Notifier les autres utilisateurs
            self.broadcast_to_others_sync(user_id, {
                "type": "user_disconnected",
                "user_id": user_id
            })
    
    async def send_personal_message(self, message: dict, user_id: str):
        """Envoyer un message à un utilisateur spécifique"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"❌ Erreur envoi message à {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast_to_others(self, sender_id: str, message: dict):
        """Diffuser un message à tous sauf l'expéditeur"""
        for user_id, connection in self.active_connections.items():
            if user_id != sender_id:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"❌ Erreur broadcast à {user_id}: {e}")
                    self.disconnect(user_id)
    
    def broadcast_to_others_sync(self, sender_id: str, message: dict):
        """Diffuser un message de manière synchrone"""
        import asyncio
        asyncio.create_task(self.broadcast_to_others(sender_id, message))
    
    async def broadcast_to_room(self, room_id: str, message: dict, sender_id: str = None):
        """Diffuser un message à une room spécifique"""
        if room_id in self.room_users:
            for user_id in self.room_users[room_id]:
                if user_id != sender_id and user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_text(json.dumps(message))
                    except Exception as e:
                        logger.error(f"❌ Erreur broadcast room à {user_id}: {e}")
                        self.disconnect(user_id)
    
    def join_room(self, user_id: str, room_id: str):
        """Faire rejoindre une room à un utilisateur"""
        # Ajouter l'utilisateur à la room
        if room_id not in self.room_users:
            self.room_users[room_id] = []
        if user_id not in self.room_users[room_id]:
            self.room_users[room_id].append(user_id)
        
        # Ajouter la room à l'utilisateur
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = []
        if room_id not in self.user_rooms[user_id]:
            self.user_rooms[user_id].append(room_id)
        
        logger.info(f"👥 Utilisateur {user_id} rejoint room {room_id}")
    
    def leave_room(self, user_id: str, room_id: str):
        """Faire quitter une room à un utilisateur"""
        # Retirer l'utilisateur de la room
        if room_id in self.room_users and user_id in self.room_users[room_id]:
            self.room_users[room_id].remove(user_id)
            if not self.room_users[room_id]:
                del self.room_users[room_id]
        
        # Retirer la room de l'utilisateur
        if user_id in self.user_rooms and room_id in self.user_rooms[user_id]:
            self.user_rooms[user_id].remove(room_id)
            if not self.user_rooms[user_id]:
                del self.user_rooms[user_id]
        
        logger.info(f"👋 Utilisateur {user_id} quitte room {room_id}")
    
    def get_connection_status(self, user_id: str) -> bool:
        """Vérifier si un utilisateur est connecté"""
        return user_id in self.active_connections
    
    def get_connected_users(self) -> List[str]:
        """Obtenir la liste des utilisateurs connectés"""
        return list(self.active_connections.keys())


# Instance globale du gestionnaire
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Endpoint WebSocket principal"""
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Recevoir le message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.info(f"📥 Message reçu de {user_id}: {message.get('type', 'unknown')}")
            
            # Traiter le message selon son type
            await handle_message(user_id, message)
            
    except WebSocketDisconnect:
        logger.info(f"🔌 WebSocket déconnecté: {user_id}")
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"❌ Erreur WebSocket pour {user_id}: {e}")
        manager.disconnect(user_id)


async def handle_message(user_id: str, message: dict):
    """Traiter les messages WebSocket"""
    message_type = message.get('type')
    
    if message_type == 'ping':
        # Heartbeat
        await manager.send_personal_message({
            "type": "pong",
            "timestamp": message.get('timestamp')
        }, user_id)
    
    elif message_type == 'join_room':
        # Rejoindre une room
        room_id = message.get('room_id')
        if room_id:
            manager.join_room(user_id, room_id)
            await manager.send_personal_message({
                "type": "room_joined",
                "room_id": room_id
            }, user_id)
    
    elif message_type == 'leave_room':
        # Quitter une room
        room_id = message.get('room_id')
        if room_id:
            manager.leave_room(user_id, room_id)
            await manager.send_personal_message({
                "type": "room_left",
                "room_id": room_id
            }, user_id)
    
    elif message_type == 'task_update':
        # Mise à jour de tâche
        task_data = message.get('task_data')
        room_id = message.get('room_id')
        
        if room_id:
            # Diffuser à la room
            await manager.broadcast_to_room(room_id, {
                "type": "task_updated",
                "task_data": task_data,
                "user_id": user_id
            }, user_id)
        else:
            # Diffuser à tous les autres utilisateurs
            await manager.broadcast_to_others(user_id, {
                "type": "task_updated",
                "task_data": task_data,
                "user_id": user_id
            })
    
    elif message_type == 'notification':
        # Notification temps réel
        notification_data = {
            "type": "notification",
            "title": message.get('title', 'Notification'),
            "message": message.get('message', ''),
            "category": message.get('category', 'info'),
            "priority": message.get('priority', 'normal'),
            "timestamp": message.get('timestamp', int(time.time())),
            "user_id": user_id
        }
        
        # Envoyer la notification à l'utilisateur
        await manager.send_personal_message(notification_data, user_id)
        logger.info(f"🔔 Notification envoyée à {user_id}: {notification_data['title']}")
    
    elif message_type == 'user_connected':
        # Utilisateur connecté
        await manager.broadcast_to_others(user_id, {
            "type": "user_connected",
            "user_id": user_id,
            "username": message.get('username', 'Utilisateur'),
            "timestamp": message.get('timestamp', int(time.time()))
        })
        logger.info(f"👤 Utilisateur {user_id} connecté")
    
    elif message_type == 'broadcast':
        # Message de broadcast
        broadcast_data = {
            "type": "broadcast",
            "message": message.get('message', ''),
            "user_id": user_id,
            "timestamp": message.get('timestamp', int(time.time()))
        }
        
        # Diffuser à tous les autres utilisateurs
        await manager.broadcast_to_others(user_id, broadcast_data)
        logger.info(f"📡 Broadcast envoyé par {user_id}")
    
    elif message_type == 'kanban_update':
        # Mise à jour du Kanban
        kanban_data = message.get('kanban_data')
        room_id = message.get('room_id')
        
        if room_id:
            await manager.broadcast_to_room(room_id, {
                "type": "kanban_updated",
                "kanban_data": kanban_data,
                "user_id": user_id
            }, user_id)
        else:
            await manager.broadcast_to_others(user_id, {
                "type": "kanban_updated",
                "kanban_data": kanban_data,
                "user_id": user_id
            })
    
    elif message_type == 'pa_monitoring':
        # Monitoring PA
        target_user_id = message.get('target_user_id')
        if target_user_id and manager.get_connection_status(target_user_id):
            await manager.send_personal_message({
                "type": "pa_monitoring_started",
                "monitor_user_id": user_id
            }, target_user_id)
    
    else:
        # Message non reconnu
        logger.warning(f"⚠️ Type de message non reconnu: {message_type}")
        await manager.send_personal_message({
            "type": "error",
            "message": f"Type de message non reconnu: {message_type}"
        }, user_id)


# Fonctions utilitaires pour l'API

async def send_task_update(task_data: dict, user_id: str = None, room_id: str = None):
    """Envoyer une mise à jour de tâche via WebSocket"""
    message = {
        "type": "task_updated",
        "task_data": task_data,
        "user_id": user_id or "system"
    }
    
    if room_id:
        await manager.broadcast_to_room(room_id, message)
    else:
        # Diffuser à tous les utilisateurs connectés
        for connected_user_id in manager.get_connected_users():
            if connected_user_id != user_id:
                await manager.send_personal_message(message, connected_user_id)


async def send_kanban_update(kanban_data: dict, user_id: str = None, room_id: str = None):
    """Envoyer une mise à jour de Kanban via WebSocket"""
    message = {
        "type": "kanban_updated",
        "kanban_data": kanban_data,
        "user_id": user_id or "system"
    }
    
    if room_id:
        await manager.broadcast_to_room(room_id, message)
    else:
        for connected_user_id in manager.get_connected_users():
            if connected_user_id != user_id:
                await manager.send_personal_message(message, connected_user_id)


def get_connection_stats():
    """Obtenir les statistiques de connexion"""
    return {
        "connected_users": len(manager.active_connections),
        "active_rooms": len(manager.room_users),
        "users": manager.get_connected_users()
    } 