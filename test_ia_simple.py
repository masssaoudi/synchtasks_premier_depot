#!/usr/bin/env python3
"""
Test simple de l'IA SyncTasks
"""

import requests
import json

def test_ia_chat():
    """Test du chat IA"""
    print("🤖 Test de l'IA SyncTasks...")
    
    # URL de l'API
    url = "http://localhost:8000/api/ia/chat"
    
    # Données de test
    data = {
        "message": "Salut, comment ça va ?",
        "user_id": "test_user"
    }
    
    try:
        print(f"📤 Envoi vers: {url}")
        print(f"📝 Message: {data['message']}")
        
        # Appel API
        response = requests.post(url, json=data, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Réponse IA reçue:")
            print(f"💬 Message: {result.get('response', 'Pas de réponse')}")
            print(f"💡 Suggestions: {result.get('suggestions', [])}")
            print(f"📋 Tâches suggérées: {len(result.get('task_suggestions', []))}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Contenu: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_ia_health():
    """Test de santé de l'IA"""
    print("\n🏥 Test de santé de l'IA...")
    
    url = "http://localhost:8000/api/ia/health"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ IA en bonne santé: {result.get('message', 'OK')}")
            print(f"🤖 Gemini configuré: {result.get('gemini_configured', False)}")
            return True
        else:
            print(f"❌ IA malade: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur santé: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'IA SyncTasks")
    print("=" * 40)
    
    # Test de santé
    health_ok = test_ia_health()
    
    if health_ok:
        # Test du chat
        chat_ok = test_ia_chat()
        
        if chat_ok:
            print("\n🎉 TOUS LES TESTS RÉUSSIS !")
            print("L'IA fonctionne parfaitement côté backend.")
            print("Le problème vient de l'interface frontend.")
        else:
            print("\n❌ ÉCHEC DU TEST CHAT")
    else:
        print("\n❌ ÉCHEC DU TEST SANTÉ")
    
    print("\n" + "=" * 40) 