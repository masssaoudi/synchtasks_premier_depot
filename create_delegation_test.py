#!/usr/bin/env python3
"""
Script pour créer une délégation entre Alice et Marie PA pour les tests
"""

import asyncio
import httpx
import json

# Configuration
BASE_URL = "http://localhost:8000"

async def create_delegation_test():
    """Créer une délégation entre Alice et Marie PA"""
    
    async with httpx.AsyncClient() as client:
        print("🤝 Création d'une délégation pour les tests")
        print("=" * 50)
        
        # 1. Connexion Alice (utilisateur principal)
        print("\n1️⃣ Connexion Alice...")
        login_alice = await client.post(f"{BASE_URL}/api/auth/login", json={
            "username": "alice@test.com",
            "password": "alice123"
        })
        
        if login_alice.status_code != 200:
            print(f"❌ Erreur connexion Alice: {login_alice.status_code}")
            return
        
        alice_token = login_alice.json()["data"]["access_token"]
        alice_id = login_alice.json()["data"]["user"]["id"]
        print(f"✅ Alice connectée: {login_alice.json()['data']['user']['email']}")
        
        # 2. Connexion Marie PA
        print("\n2️⃣ Connexion Marie PA...")
        login_marie = await client.post(f"{BASE_URL}/api/auth/login", json={
            "username": "marie.pa@test.com",
            "password": "marie123"
        })
        
        if login_marie.status_code != 200:
            print(f"❌ Erreur connexion Marie: {login_marie.status_code}")
            return
        
        marie_id = login_marie.json()["data"]["user"]["id"]
        print(f"✅ Marie PA connectée: {login_marie.json()['data']['user']['email']}")
        
        # 3. Créer une délégation (Alice invite Marie)
        print("\n3️⃣ Création de la délégation...")
        delegation_data = {
            "nom": "Dubois",
            "prenom": "Marie",
            "email": "marie.pa@test.com",
            "telephone": "0123456789"
        }
        
        create_delegation = await client.post(
            f"{BASE_URL}/delegations/",
            json=delegation_data,
            headers={"Authorization": f"Bearer {alice_token}"}
        )
        
        print(f"Status création délégation: {create_delegation.status_code}")
        print(f"Réponse complète: {create_delegation.text}")
        if create_delegation.status_code == 200:
            delegation = create_delegation.json()
            print(f"✅ Délégation créée!")
            print(f"   - Structure: {list(delegation.keys())}")
            # Chercher l'ID dans la structure
            delegation_id = delegation.get("id") or delegation.get("_id")
            if delegation_id:
                print(f"   - ID: {delegation_id}")
                print(f"   - Status: {delegation.get('status', 'N/A')}")
            else:
                print("❌ Impossible de trouver l'ID de la délégation")
                return
        else:
            print(f"❌ Erreur création délégation: {create_delegation.text}")
            return
        
        # 4. Marie accepte la délégation
        print("\n4️⃣ Marie accepte la délégation...")
        accept_delegation = await client.post(
            f"{BASE_URL}/delegations/accept",
            params={"delegation_id": delegation_id},
            headers={"Authorization": f"Bearer {login_marie.json()['data']['access_token']}"}
        )
        
        print(f"Status acceptation: {accept_delegation.status_code}")
        if accept_delegation.status_code == 200:
            print("✅ Délégation acceptée par Marie!")
        else:
            print(f"❌ Erreur acceptation: {accept_delegation.text}")
            return
        
        # 5. Vérifier que Marie peut voir les tâches d'Alice
        print("\n5️⃣ Vérification accès aux tâches...")
        kanban_access = await client.get(
            f"{BASE_URL}/delegations/kanban",
            params={"user_id": alice_id},
            headers={"Authorization": f"Bearer {login_marie.json()['data']['access_token']}"}
        )
        
        if kanban_access.status_code == 200:
            tasks = kanban_access.json()
            print(f"✅ Marie peut voir {len(tasks)} tâches d'Alice")
        else:
            print(f"❌ Erreur accès Kanban: {kanban_access.status_code}")
            print(f"Réponse: {kanban_access.text}")
        
        print("\n" + "=" * 50)
        print("🎉 Délégation créée et testée avec succès!")

if __name__ == "__main__":
    asyncio.run(create_delegation_test()) 