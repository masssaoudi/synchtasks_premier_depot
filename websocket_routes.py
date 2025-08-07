"""
Routes WebSocket simples pour SyncTasks
Version épurée sans complexité inutile
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from websocket_simple import websocket_endpoint, manager, get_connection_stats

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_route(websocket: WebSocket, user_id: str):
    """Route WebSocket principale"""
    await websocket_endpoint(websocket, user_id)


@router.get("/ws/stats")
async def get_websocket_stats():
    """Obtenir les statistiques WebSocket"""
    try:
        stats = get_connection_stats()
        return JSONResponse({
            "success": True,
            "data": stats
        })
    except Exception as e:
        logger.error(f"❌ Erreur stats WebSocket: {e}")
        return JSONResponse({
            "success": False,
            "message": "Erreur lors de la récupération des stats"
        }, status_code=500)


@router.get("/ws/health")
async def websocket_health():
    """Health check WebSocket"""
    try:
        stats = get_connection_stats()
        return JSONResponse({
            "success": True,
            "status": "healthy",
            "connected_users": stats["connected_users"],
            "active_rooms": stats["active_rooms"]
        })
    except Exception as e:
        logger.error(f"❌ Erreur health check WebSocket: {e}")
        return JSONResponse({
            "success": False,
            "status": "unhealthy",
            "message": str(e)
        }, status_code=500)


@router.get("/ws/users")
async def get_connected_users():
    """Obtenir la liste des utilisateurs connectés"""
    try:
        users = manager.get_connected_users()
        return JSONResponse({
            "success": True,
            "data": {
                "users": users,
                "count": len(users)
            }
        })
    except Exception as e:
        logger.error(f"❌ Erreur liste utilisateurs: {e}")
        return JSONResponse({
            "success": False,
            "message": "Erreur lors de la récupération des utilisateurs"
        }, status_code=500)


@router.get("/ws/rooms")
async def get_active_rooms():
    """Obtenir la liste des rooms actives"""
    try:
        rooms = list(manager.room_users.keys())
        return JSONResponse({
            "success": True,
            "data": {
                "rooms": rooms,
                "count": len(rooms)
            }
        })
    except Exception as e:
        logger.error(f"❌ Erreur liste rooms: {e}")
        return JSONResponse({
            "success": False,
            "message": "Erreur lors de la récupération des rooms"
        }, status_code=500)


@router.get("/ws/user/{user_id}/status")
async def get_user_status(user_id: str):
    """Vérifier le statut de connexion d'un utilisateur"""
    try:
        is_connected = manager.get_connection_status(user_id)
        return JSONResponse({
            "success": True,
            "data": {
                "user_id": user_id,
                "connected": is_connected
            }
        })
    except Exception as e:
        logger.error(f"❌ Erreur statut utilisateur {user_id}: {e}")
        return JSONResponse({
            "success": False,
            "message": "Erreur lors de la vérification du statut"
        }, status_code=500)


@router.get("/ws/room/{room_id}/users")
async def get_room_users(room_id: str):
    """Obtenir les utilisateurs d'une room"""
    try:
        users = manager.room_users.get(room_id, [])
        return JSONResponse({
            "success": True,
            "data": {
                "room_id": room_id,
                "users": users,
                "count": len(users)
            }
        })
    except Exception as e:
        logger.error(f"❌ Erreur utilisateurs room {room_id}: {e}")
        return JSONResponse({
            "success": False,
            "message": "Erreur lors de la récupération des utilisateurs de la room"
        }, status_code=500) 