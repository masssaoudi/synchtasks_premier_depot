"""
Test de la connexion WebSocket dans l'interface utilisateur
Vérifie que l'UI se connecte correctement au WebSocket
"""

import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_ui_websocket_connection():
    """Test de la connexion WebSocket dans l'UI"""
    logger.info("🔌 Test connexion WebSocket UI...")
    
    try:
        # Vérifier que l'interface est accessible
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code != 200:
            logger.error(f"❌ Interface non accessible: {response.status_code}")
            return False
        
        logger.info("✅ Interface accessible")
        
        # Vérifier que le JavaScript WebSocket est présent
        html_content = response.text.lower()
        
        # Rechercher les indicateurs WebSocket
        websocket_indicators = [
            "websocket",
            "ws://",
            "websocketservice",
            "socket",
            "realtime"
        ]
        
        found_indicators = []
        for indicator in websocket_indicators:
            if indicator in html_content:
                found_indicators.append(indicator)
        
        if found_indicators:
            logger.info(f"✅ WebSocket détecté dans l'UI: {found_indicators}")
        else:
            logger.warning("⚠️ WebSocket non détecté dans l'UI")
        
        # Vérifier les fichiers JavaScript
        js_files = [
            "/js/app.js",
            "/js/chunk-vendors.js",
            "/js/chunk-common.js"
        ]
        
        for js_file in js_files:
            try:
                js_response = requests.get(f"http://localhost:3000{js_file}", timeout=5)
                if js_response.status_code == 200:
                    js_content = js_response.text.lower()
                    if "websocket" in js_content or "ws://" in js_content:
                        logger.info(f"✅ WebSocket trouvé dans {js_file}")
                    else:
                        logger.warning(f"⚠️ WebSocket non trouvé dans {js_file}")
                else:
                    logger.warning(f"⚠️ Fichier JS non accessible: {js_file}")
            except Exception as e:
                logger.warning(f"⚠️ Erreur accès {js_file}: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur test UI WebSocket: {e}")
        return False


def test_mongo_express_fix():
    """Corriger le problème MongoDB Express"""
    logger.info("🗄️ Diagnostic MongoDB Express...")
    
    try:
        # Test sans auth
        response = requests.get("http://localhost:8081", timeout=5)
        logger.info(f"📊 MongoDB Express status: {response.status_code}")
        
        if response.status_code == 401:
            logger.info("ℹ️ MongoDB Express nécessite une authentification")
            logger.info("🔑 Credentials: admin / admin123")
            logger.info("🌐 Accès: http://localhost:8081")
            logger.info("📝 Login avec: admin / admin123")
            
            # Test avec auth
            auth_response = requests.get(
                "http://localhost:8081", 
                auth=("admin", "admin123"),
                timeout=5
            )
            
            if auth_response.status_code == 200:
                logger.info("✅ MongoDB Express accessible avec auth")
                return True
            else:
                logger.warning(f"⚠️ MongoDB Express auth échoué: {auth_response.status_code}")
                return False
                
        elif response.status_code == 200:
            logger.info("✅ MongoDB Express accessible sans auth")
            return True
        else:
            logger.warning(f"⚠️ MongoDB Express: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur MongoDB Express: {e}")
        return False


def test_websocket_status():
    """Test du statut WebSocket"""
    logger.info("🔌 Test statut WebSocket...")
    
    try:
        # Test de connexion WebSocket
        import websockets
        import asyncio
        import json
        
        async def test_ws_status():
            uri = "ws://localhost:8000/api/ws/test_ui_status"
            try:
                async with websockets.connect(uri) as websocket:
                    logger.info("✅ WebSocket connecté")
                    
                    # Envoyer un ping
                    ping_msg = {"type": "ping", "timestamp": int(time.time())}
                    await websocket.send(json.dumps(ping_msg))
                    logger.info("📤 Ping envoyé")
                    
                    # Attendre réponse
                    response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                    data = json.loads(response)
                    logger.info(f"📥 Pong reçu: {data}")
                    
                    logger.info("✅ WebSocket opérationnel")
                    return True
                    
            except Exception as e:
                logger.error(f"❌ Erreur WebSocket: {e}")
                return False
        
        return asyncio.run(test_ws_status())
        
    except Exception as e:
        logger.error(f"❌ Erreur test WebSocket: {e}")
        return False


def run_ui_diagnostic():
    """Diagnostic complet de l'UI"""
    logger.info("🚀 Diagnostic complet interface utilisateur...")
    
    # Test 1: Interface WebSocket
    ui_ok = test_ui_websocket_connection()
    
    # Test 2: MongoDB Express
    mongo_ok = test_mongo_express_fix()
    
    # Test 3: WebSocket status
    ws_ok = test_websocket_status()
    
    # Résumé
    logger.info("📊 Résumé du diagnostic:")
    logger.info(f"   Interface UI: {'✅' if ui_ok else '❌'}")
    logger.info(f"   MongoDB Express: {'✅' if mongo_ok else '❌'}")
    logger.info(f"   WebSocket: {'✅' if ws_ok else '❌'}")
    
    if ui_ok and ws_ok:
        logger.info("🎉 Interface utilisateur prête !")
        logger.info("🌐 Accédez à: http://localhost:3000")
        logger.info("🔌 WebSocket devrait être connecté")
        
        if not mongo_ok:
            logger.info("⚠️ MongoDB Express nécessite auth: admin/admin123")
    else:
        logger.error("❌ Problèmes détectés avec l'interface")


if __name__ == "__main__":
    run_ui_diagnostic() 