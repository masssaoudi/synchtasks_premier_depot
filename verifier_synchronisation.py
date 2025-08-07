#!/usr/bin/env python3
"""
Vérification de la synchronisation entre formulaires de connexion et collections MongoDB
"""

from pymongo import MongoClient
import requests

# Configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "synchtasks_db"
API_URL = "http://localhost:8000"

def verifier_synchronisation():
    """Vérifier la synchronisation entre API et MongoDB"""
    
    print("VERIFICATION SYNCHRONISATION API <-> MONGODB")
    print("=" * 50)
    
    # 1. Connexion MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # 2. Récupérer tous les utilisateurs de MongoDB
    print("\n1. UTILISATEURS DANS MONGODB:")
    users_mongo = list(db.users.find({}, {"username": 1, "email": 1, "role": 1, "_id": 1}))
    print(f"   Nombre d'utilisateurs MongoDB: {len(users_mongo)}")
    
    for user in users_mongo:
        print(f"   - {user.get('username')} ({user.get('email')}) - Role: {user.get('role', 'N/A')}")
    
    # 3. Tester la connexion API pour chaque utilisateur
    print("\n2. TEST CONNEXION API:")
    
    for user in users_mongo:
        username = user.get('username')
        if not username:
            continue
            
        print(f"\n   Test connexion: {username}")
        
        # Essayer de se connecter via l'API
        try:
            # Utiliser un mot de passe simple pour tous
            login_data = {
                "username": username,
                "password": f"{username}123"  # Mot de passe simple
            }
            
            response = requests.post(f"{API_URL}/api/auth/login", json=login_data)
            
            if response.status_code == 200:
                print(f"   ✅ Connexion API réussie pour {username}")
                
                # Récupérer les tâches de cet utilisateur via l'API
                token = response.json()["data"]["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                
                tasks_response = requests.get(f"{API_URL}/api/tasks/", headers=headers)
                if tasks_response.status_code == 200:
                    tasks_api = tasks_response.json()
                    print(f"   📋 Tâches API: {len(tasks_api)} tâches")
                else:
                    print(f"   ❌ Erreur récupération tâches API: {tasks_response.status_code}")
                    
            else:
                print(f"   ❌ Échec connexion API pour {username}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur test {username}: {e}")
    
    # 4. Vérifier les tâches dans MongoDB
    print("\n3. TÂCHES DANS MONGODB:")
    tasks_mongo = list(db.tasks.find({}, {"title": 1, "created_by": 1, "status": 1, "_id": 1}))
    print(f"   Nombre total de tâches MongoDB: {len(tasks_mongo)}")
    
    # Grouper par utilisateur
    tasks_par_utilisateur = {}
    for task in tasks_mongo:
        created_by = task.get('created_by')
        if created_by not in tasks_par_utilisateur:
            tasks_par_utilisateur[created_by] = []
        tasks_par_utilisateur[created_by].append(task)
    
    for user_id, tasks in tasks_par_utilisateur.items():
        # Trouver le nom d'utilisateur
        user = db.users.find_one({"_id": user_id})
        username = user.get('username', 'Utilisateur inconnu') if user else 'Utilisateur inconnu'
        print(f"   - {username}: {len(tasks)} tâches")
    
    client.close()
    print("\n" + "=" * 50)
    print("Vérification terminée!")

if __name__ == "__main__":
    verifier_synchronisation() 