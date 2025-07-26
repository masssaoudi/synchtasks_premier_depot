#!/usr/bin/env python3
"""
Test simple pour vérifier les WebSockets
"""

import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_websocket():
    """Test de connexion WebSocket"""
    uri = "ws://localhost:8000/ws"
    
    try:
        logger.info(f"🔌 Connexion à {uri}")
        async with websockets.connect(uri) as websocket:
            logger.info("✅ WebSocket connecté")
            
            # Envoyer un message de test
            test_message = {
                "type": "test",
                "message": "Test WebSocket"
            }
            
            await websocket.send(json.dumps(test_message))
            logger.info("📤 Message envoyé")
            
            # Attendre une réponse
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                logger.info(f"📨 Réponse reçue: {response}")
            except asyncio.TimeoutError:
                logger.warning("⏰ Timeout - pas de réponse")
            
            logger.info("✅ Test WebSocket terminé")
            
    except Exception as e:
        logger.error(f"❌ Erreur WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket()) 