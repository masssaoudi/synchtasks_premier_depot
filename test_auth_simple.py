#!/usr/bin/env python3
"""
Script simple pour tester l'authentification
"""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8000"
TEST_USER_EMAIL = "alice@test.com"
TEST_USER_PASSWORD = "alice123"


def test_auth():
    """Tester l'authentification"""
    print("🔐 Test d'authentification...")

    try:
        # Données de connexion
        login_data = {
            "username": TEST_USER_EMAIL,  # L'API accepte email comme username
            "password": TEST_USER_PASSWORD,
        }

        print(f"📤 Envoi de la requête à {BACKEND_URL}/api/auth/login")
        print(f"📋 Données: {login_data}")

        # Requête POST
        response = requests.post(
            f"{BACKEND_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
        )

        print(f"📥 Status: {response.status_code}")
        print(f"📥 Headers: {dict(response.headers)}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Réponse: {json.dumps(data, indent=2)}")

            if data.get("success"):
                token = data["data"]["access_token"]
                user_id = data["data"]["user"]["_id"]
                print(f"🎉 Authentification réussie!")
                print(f"   Token: {token[:50]}...")
                print(f"   User ID: {user_id}")
                return True, token, user_id
            else:
                print(f"❌ Réponse non réussie: {data}")
                return False, None, None
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"📥 Contenu: {response.text}")
            return False, None, None

    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, None, None


if __name__ == "__main__":
    success, token, user_id = test_auth()
    if success:
        print("\n✅ Test d'authentification réussi!")
    else:
        print("\n❌ Test d'authentification échoué!")
