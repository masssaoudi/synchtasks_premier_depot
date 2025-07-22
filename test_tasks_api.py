import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
TASKS_URL = f"{BASE_URL}/api/tasks/"

def test_tasks_api():
    print("🧪 Test de l'API des tâches")
    print("=" * 50)
    
    # 1. Connexion
    print("1. Connexion...")
    login_data = {
        "username": "coco",
        "password": "coco123"
    }
    
    response = requests.post(LOGIN_URL, json=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Échec de la connexion")
        return
    
    login_response = response.json()
    print("✅ Connexion réussie")
    
    # Récupérer le token
    token = login_response['data']['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Récupérer les tâches existantes
    print("\n2. Récupération des tâches existantes...")
    response = requests.get(TASKS_URL, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"Nombre de tâches: {len(tasks)}")
        if tasks:
            print("Tâches trouvées:")
            for task in tasks:
                print(f"  - {task.get('title', 'Sans titre')} (ID: {task.get('id', 'N/A')})")
        else:
            print("Aucune tâche trouvée")
    else:
        print(f"❌ Erreur: {response.text}")
    
    # 3. Créer une nouvelle tâche
    print("\n3. Création d'une nouvelle tâche...")
    new_task = {
        "title": "Test tâche API avec nouvelle catégorie",
        "description": "Tâche créée via script de test avec catégorie domicile",
        "priority": "haute",
        "category": "domicile"
    }
    
    response = requests.post(TASKS_URL, json=new_task, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        created_task = response.json()
        print(f"✅ Tâche créée avec ID: {created_task.get('id', 'N/A')}")
    else:
        print(f"❌ Erreur lors de la création: {response.text}")
    
    # 4. Récupérer à nouveau les tâches
    print("\n4. Récupération des tâches après création...")
    response = requests.get(TASKS_URL, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"Nombre de tâches: {len(tasks)}")
        if tasks:
            print("Tâches trouvées:")
            for task in tasks:
                print(f"  - {task.get('title', 'Sans titre')} (ID: {task.get('id', 'N/A')})")
        else:
            print("Aucune tâche trouvée")
    else:
        print(f"❌ Erreur: {response.text}")

if __name__ == "__main__":
    test_tasks_api() 