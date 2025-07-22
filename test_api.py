#!/usr/bin/env python3
"""
Script de test rapide pour SyncTasks API
Vérifie que tous les endpoints principaux fonctionnent
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"

def test_api_connection():
    """Test de connexion à l'API"""
    try:
        response = requests.get(f"{BASE_URL}/api")
        print("✅ API connectée:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion API: {e}")
        return False

def create_test_user():
    """Créer un utilisateur de test"""
    user_data = {
        "username": "demo_user",
        "password": "demo123",
        "email": "demo@synchtasks.com",
        "full_name": "Utilisateur Démo"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📝 Création utilisateur (Status: {response.status_code}):")
        if response.status_code == 200:
            print("✅ Utilisateur créé avec succès!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print("❌ Erreur lors de la création:")
            print(json.dumps(response.json(), indent=2))
            return False
            
    except Exception as e:
        print(f"❌ Erreur de requête: {e}")
        return False

def test_login():
    """Tester la connexion"""
    login_data = {
        "username": "demo_user",
        "password": "demo123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"🔐 Test de connexion (Status: {response.status_code}):")
        if response.status_code == 200:
            print("✅ Connexion réussie!")
            result = response.json()
            print(f"Token: {result['data']['access_token'][:50]}...")
            return result['data']['access_token']
        else:
            print("❌ Erreur de connexion:")
            print(json.dumps(response.json(), indent=2))
            return None
            
    except Exception as e:
        print(f"❌ Erreur de requête: {e}")
        return None

def test_protected_endpoint(token):
    """Tester un endpoint protégé"""
    if not token:
        print("❌ Pas de token disponible")
        return False
        
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"🔒 Test endpoint protégé (Status: {response.status_code}):")
        if response.status_code == 200:
            print("✅ Endpoint protégé accessible!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print("❌ Erreur endpoint protégé:")
            print(json.dumps(response.json(), indent=2))
            return False
            
    except Exception as e:
        print(f"❌ Erreur de requête: {e}")
        return False

def main():
    print("🚀 Test de l'API SyncTasks")
    print("=" * 50)
    
    # Test de connexion
    if not test_api_connection():
        return
    
    print("\n" + "=" * 50)
    
    # Créer un utilisateur de test
    if not create_test_user():
        print("⚠️ L'utilisateur existe peut-être déjà")
    
    print("\n" + "=" * 50)
    
    # Tester la connexion
    token = test_login()
    
    if token:
        print("\n" + "=" * 50)
        # Tester un endpoint protégé
        test_protected_endpoint(token)
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés!")
    print("\n📋 Identifiants de test:")
    print("   Username: demo_user")
    print("   Password: demo123")

if __name__ == "__main__":
    main() 