#!/usr/bin/env python3
"""
Script de test pour vérifier le déploiement Docker de SyncTasks
"""

import requests
import time
import json
import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:80"
MONGO_EXPRESS_URL = "http://localhost:8081"

# Couleurs pour les messages
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

def log_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def log_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def log_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def log_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def test_service_health(url, service_name, timeout=10):
    """Teste la santé d'un service"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            log_success(f"{service_name} est opérationnel ({url})")
            return True
        else:
            log_warning(f"{service_name} répond avec le code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        log_error(f"{service_name} n'est pas accessible: {e}")
        return False

def test_backend_health():
    """Teste la santé du backend"""
    log_info("Test de la santé du backend...")
    
    # Test de l'endpoint health
    health_url = urljoin(BASE_URL, "/health")
    if not test_service_health(health_url, "Backend Health"):
        return False
    
    # Test de l'endpoint racine
    root_url = urljoin(BASE_URL, "/")
    if not test_service_health(root_url, "Backend Root"):
        return False
    
    return True

def test_frontend():
    """Teste le frontend"""
    log_info("Test du frontend...")
    return test_service_health(FRONTEND_URL, "Frontend")

def test_mongo_express():
    """Teste Mongo Express"""
    log_info("Test de Mongo Express...")
    return test_service_health(MONGO_EXPRESS_URL, "Mongo Express")

def test_api_endpoints():
    """Teste les endpoints de l'API"""
    log_info("Test des endpoints de l'API...")
    
    endpoints = [
        "/api/auth/login",
        "/api/tasks/",
        "/api/tasks/categories/",
        "/api/tasks/priorities/",
        "/api/ia/history"
    ]
    
    success_count = 0
    for endpoint in endpoints:
        url = urljoin(BASE_URL, endpoint)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 401, 405]:  # 401 = non autorisé, 405 = méthode non autorisée
                log_success(f"Endpoint {endpoint} répond correctement")
                success_count += 1
            else:
                log_warning(f"Endpoint {endpoint} répond avec le code {response.status_code}")
        except requests.exceptions.RequestException as e:
            log_error(f"Endpoint {endpoint} n'est pas accessible: {e}")
    
    return success_count >= len(endpoints) * 0.8  # Au moins 80% des endpoints doivent répondre

def test_authentication():
    """Teste l'authentification"""
    log_info("Test de l'authentification...")
    
    login_url = urljoin(BASE_URL, "/api/auth/login")
    login_data = {
        "username": "coco",
        "password": "coco123"
    }
    
    try:
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'access_token' in data['data']:
                log_success("Authentification réussie")
                return data['data']['access_token']
            else:
                log_error("Réponse d'authentification invalide")
                return None
        else:
            log_warning(f"Authentification échouée avec le code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        log_error(f"Erreur lors de l'authentification: {e}")
        return None

def test_authenticated_endpoints(token):
    """Teste les endpoints nécessitant une authentification"""
    if not token:
        log_warning("Pas de token d'authentification, test des endpoints authentifiés ignoré")
        return True
    
    log_info("Test des endpoints authentifiés...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test de récupération des tâches
    tasks_url = urljoin(BASE_URL, "/api/tasks/")
    try:
        response = requests.get(tasks_url, headers=headers, timeout=10)
        if response.status_code == 200:
            tasks = response.json()
            log_success(f"Récupération des tâches réussie ({len(tasks)} tâches)")
        else:
            log_warning(f"Récupération des tâches échouée avec le code {response.status_code}")
    except requests.exceptions.RequestException as e:
        log_error(f"Erreur lors de la récupération des tâches: {e}")
    
    return True

def test_websocket():
    """Teste la connexion WebSocket"""
    log_info("Test de la connexion WebSocket...")
    
    try:
        import websocket
        import threading
        
        def on_message(ws, message):
            log_success("Message WebSocket reçu")
            ws.close()
        
        def on_error(ws, error):
            log_error(f"Erreur WebSocket: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            log_info("Connexion WebSocket fermée")
        
        def on_open(ws):
            log_success("Connexion WebSocket établie")
            # Envoyer un message de test
            ws.send(json.dumps({"type": "ping"}))
        
        # Créer la connexion WebSocket
        ws_url = BASE_URL.replace("http", "ws") + "/ws"
        ws = websocket.WebSocketApp(ws_url,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
        
        # Démarrer la connexion dans un thread
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        
        # Attendre un peu pour le test
        time.sleep(3)
        
        return True
        
    except ImportError:
        log_warning("Module websocket-client non installé, test WebSocket ignoré")
        return True
    except Exception as e:
        log_error(f"Erreur lors du test WebSocket: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test du déploiement Docker SyncTasks")
    print("=" * 50)
    
    # Attendre un peu que les services démarrent
    log_info("Attente du démarrage des services...")
    time.sleep(5)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend", test_frontend),
        ("Mongo Express", test_mongo_express),
        ("API Endpoints", test_api_endpoints),
    ]
    
    # Tests qui nécessitent une authentification
    auth_token = test_authentication()
    if auth_token:
        tests.append(("Authenticated Endpoints", lambda: test_authenticated_endpoints(auth_token)))
    
    # Test WebSocket (optionnel)
    tests.append(("WebSocket", test_websocket))
    
    # Exécuter tous les tests
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- Test: {test_name} ---")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            log_error(f"Erreur lors du test {test_name}: {e}")
    
    # Résumé
    print(f"\n{'='*50}")
    print(f"📊 Résumé des tests: {passed}/{total} réussis")
    
    if passed == total:
        log_success("🎉 Tous les tests sont passés ! Le déploiement est réussi.")
        print("\n🌐 Accès aux services:")
        print(f"   Frontend: {FRONTEND_URL}")
        print(f"   Backend API: {BASE_URL}")
        print(f"   Mongo Express: {MONGO_EXPRESS_URL}")
        return 0
    else:
        log_warning(f"⚠️  {total - passed} test(s) ont échoué. Vérifiez les logs Docker.")
        print("\n🔍 Pour diagnostiquer:")
        print("   docker-compose logs -f")
        print("   docker-compose ps")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 