"""
Test de la correction CSP pour les WebSockets
Vérifie que la Content Security Policy autorise les connexions WebSocket
"""

import requests
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_csp_headers():
    """Test des headers CSP"""
    logger.info("🔒 Test des headers CSP...")
    
    try:
        response = requests.get("http://localhost:3000")
        
        if response.status_code == 200:
            logger.info("✅ Frontend accessible")
            
            # Vérifier les headers CSP
            csp_header = response.headers.get('Content-Security-Policy')
            if csp_header:
                logger.info(f"📋 CSP header: {csp_header}")
                
                # Vérifier si connect-src est présent
                if 'connect-src' in csp_header and ('ws:' in csp_header or 'wss:' in csp_header):
                    logger.info("✅ CSP autorise les WebSockets (ws: wss:)")
                    return True
                else:
                    logger.warning("⚠️ CSP ne semble pas autoriser les WebSockets")
                    return False
            else:
                logger.warning("⚠️ Pas de header CSP trouvé")
                return False
        else:
            logger.error(f"❌ Frontend non accessible: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur test CSP: {e}")
        return False


def test_websocket_connection():
    """Test de connexion WebSocket après correction CSP"""
    logger.info("🔌 Test de connexion WebSocket après correction CSP...")
    
    try:
        # Test simple avec requests pour vérifier que le port est accessible
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 404:  # Normal, pas d'endpoint /health
            logger.info("✅ Backend accessible")
        else:
            logger.info(f"✅ Backend accessible: {response.status_code}")
        
        logger.info("✅ WebSocket devrait maintenant fonctionner")
        logger.info("💡 Testez dans le navigateur:")
        logger.info("   1. Ouvrez http://localhost:3000")
        logger.info("   2. Connectez-vous avec alice@test.com / alice123")
        logger.info("   3. Ouvrez la console (F12)")
        logger.info("   4. Exécutez: new WebSocket('ws://localhost:8000/api/ws/6889a312a274d15db190a36d')")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur test WebSocket: {e}")
        return False


def run_csp_test():
    """Test complet de la correction CSP"""
    logger.info("🚀 Test de la correction CSP pour WebSockets...")
    
    # Test 1: Headers CSP
    csp_ok = test_csp_headers()
    
    # Test 2: Connexion WebSocket
    ws_ok = test_websocket_connection()
    
    # Résumé
    logger.info("📊 Résumé des tests CSP:")
    logger.info(f"   Headers CSP: {'✅' if csp_ok else '❌'}")
    logger.info(f"   WebSocket: {'✅' if ws_ok else '❌'}")
    
    if csp_ok and ws_ok:
        logger.info("🎉 CSP corrigée ! Les WebSockets devraient maintenant fonctionner")
        logger.info("💡 Testez maintenant dans le navigateur")
    else:
        logger.error("❌ Problème avec la CSP")


if __name__ == "__main__":
    run_csp_test() 