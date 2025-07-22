#!/usr/bin/env python3
"""
Test direct de l'API chat IA
"""

import requests
import json

def test_chat_api():
    """Test direct de l'API chat"""
    print("🤖 Test direct de l'API chat IA...")
    
    url = "http://localhost:8000/api/ia/chat"
    data = {
        "message": "Salut, comment ça va ?",
        "user_id": "test_user"
    }
    
    try:
        print(f"📤 Envoi vers: {url}")
        print(f"📝 Message: {data['message']}")
        
        response = requests.post(url, json=data, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Réponse IA reçue:")
            print(f"💬 Message: {result.get('response', 'Pas de réponse')}")
            print(f"💡 Suggestions: {result.get('suggestions', [])}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

if __name__ == "__main__":
    test_chat_api() 