import requests

def create_tasks_for_alice():
    print("📝 Création de tâches pour Alice")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # 1. Connexion d'Alice
    login_data = {
        "username": "alice",
        "password": "alice123"
    }
    
    response = requests.post(f"{base_url}/api/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        alice_token = data["data"]["access_token"]
        alice_user_id = data["data"]["user"]["id"]
        print(f"✅ Alice connectée - ID: {alice_user_id}")
    else:
        print("❌ Échec connexion Alice")
        return
    
    # 2. Créer des tâches pour Alice
    tasks = [
        {
            "title": "Faire les courses",
            "category": "course",
            "priority": "normale",
            "description": "Acheter du pain, du lait et des fruits"
        },
        {
            "title": "Rendez-vous médecin",
            "category": "sante",
            "priority": "haute",
            "description": "Contrôle annuel"
        },
        {
            "title": "Nettoyer la maison",
            "category": "domicile",
            "priority": "basse",
            "description": "Passer l'aspirateur et faire la poussière"
        },
        {
            "title": "Appeler maman",
            "category": "famille",
            "priority": "normale",
            "description": "Prendre des nouvelles"
        }
    ]
    
    headers = {"Authorization": f"Bearer {alice_token}"}
    
    for i, task_data in enumerate(tasks, 1):
        print(f"\n{i}️⃣ Création tâche: {task_data['title']}")
        response = requests.post(f"{base_url}/api/tasks/", json=task_data, headers=headers)
        
        if response.status_code == 200:
            task = response.json()
            print(f"   ✅ Tâche créée - ID: {task.get('_id', task.get('id', 'N/A'))}")
        else:
            print(f"   ❌ Échec création: {response.status_code}")
    
    # 3. Vérifier les tâches créées
    print(f"\n📊 Vérification des tâches d'Alice...")
    response = requests.get(f"{base_url}/api/tasks/", headers=headers)
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Tâches trouvées: {len(tasks)}")
        for task in tasks:
            print(f"   - {task.get('title', 'Sans titre')} ({task.get('status', 'N/A')})")
    else:
        print(f"❌ Échec récupération tâches: {response.status_code}")

if __name__ == "__main__":
    create_tasks_for_alice() 