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
                task_id = task.get('id') or task.get('_id', 'N/A')
                print(f"  - {task.get('title', 'Sans titre')} (ID: {task_id})")
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
        created_task_id = created_task.get('id') or created_task.get('_id', 'N/A')
        print(f"✅ Tâche créée avec ID: {created_task_id}")
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
                task_id = task.get('id') or task.get('_id', 'N/A')
                print(f"  - {task.get('title', 'Sans titre')} (ID: {task_id})")
        else:
            print("Aucune tâche trouvée")
    else:
        print(f"❌ Erreur: {response.text}")

    # 5. Modification de la dernière tâche créée
    print("\n5. Modification de la dernière tâche créée...")
    # On prend l'ID de la dernière tâche créée
    response = requests.get(TASKS_URL, headers=headers)
    tasks = response.json()
    if tasks:
        last_task_id = tasks[0].get('id') or tasks[0].get('_id')
        update_data = {"title": "Tâche modifiée via API", "priority": "normale"}
        update_url = f"{TASKS_URL}{last_task_id}"
        response = requests.put(update_url, json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Tâche modifiée: {response.json().get('title')}")
        else:
            print(f"❌ Erreur lors de la modification: {response.text}")
    else:
        print("❌ Aucune tâche à modifier")

    # 6. Récupération de la tâche modifiée par ID
    print("\n6. Récupération de la tâche modifiée par ID...")
    if tasks:
        get_url = f"{TASKS_URL}{last_task_id}"
        response = requests.get(get_url, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Tâche récupérée: {response.json().get('title')}")
        else:
            print(f"❌ Erreur lors de la récupération: {response.text}")
    else:
        print("❌ Aucune tâche à récupérer")

    # 7. Suppression de la tâche modifiée
    print("\n7. Suppression de la tâche modifiée...")
    if tasks:
        delete_url = f"{TASKS_URL}{last_task_id}"
        response = requests.delete(delete_url, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Tâche supprimée")
        else:
            print(f"❌ Erreur lors de la suppression: {response.text}")
    else:
        print("❌ Aucune tâche à supprimer")

    # 8. Cas d'erreur : récupération d'une tâche inexistante
    print("\n8. Cas d'erreur : récupération d'une tâche inexistante...")
    fake_id = "000000000000000000000000"
    get_url = f"{TASKS_URL}{fake_id}"
    response = requests.get(get_url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 404:
        print("✅ Erreur 404 bien gérée pour tâche inexistante")
    else:
        print(f"❌ Problème gestion erreur: {response.text}")

    # 9. Endpoint catégories
    print("\n9. Récupération des catégories...")
    categories_url = f"{TASKS_URL}categories/"
    response = requests.get(categories_url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Catégories récupérées: {response.json().get('categories')}")
    else:
        print(f"❌ Erreur récupération catégories: {response.text}")

if __name__ == "__main__":
    test_tasks_api() 