#!/usr/bin/env python3
"""
Script simple pour examiner la base de données MongoDB
"""

from pymongo import MongoClient

# Connexion MongoDB directe
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "synchtasks_db"

def debug_database():
    """Examiner directement la base de données"""
    
    print("EXAMEN DIRECT DE LA BASE DE DONNEES MONGODB")
    print("=" * 60)
    
    # 1. Connexion directe à MongoDB
    print("\n1. Connexion directe a MongoDB...")
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print("OK - Connexion MongoDB reussie")
    except Exception as e:
        print(f"ERREUR connexion MongoDB: {e}")
        return
    
    # 2. Examiner la collection users
    print("\n2. Collection 'users':")
    users = list(db.users.find({}, {"username": 1, "email": 1, "role": 1, "_id": 1}))
    print(f"   Nombre d'utilisateurs: {len(users)}")
    for user in users:
        print(f"   {user.get('username', 'N/A')} - {user.get('email', 'N/A')} - Role: {user.get('role', 'N/A')} - ID: {user.get('_id')}")
    
    # 3. Examiner la collection tasks
    print("\n3. Collection 'tasks':")
    tasks = list(db.tasks.find({}, {"title": 1, "status": 1, "created_by": 1, "_id": 1, "created_at": 1}))
    print(f"   Nombre total de taches: {len(tasks)}")
    
    for task in tasks:
        created_by = task.get('created_by', 'N/A')
        # Trouver le nom d'utilisateur
        user = db.users.find_one({"_id": created_by})
        username = user.get('username', 'Utilisateur inconnu') if user else 'Utilisateur inconnu'
        
        created_at = task.get('created_at')
        if created_at:
            date_str = created_at.strftime('%d/%m/%Y %H:%M')
        else:
            date_str = 'Date inconnue'
            
        print(f"   '{task.get('title', 'N/A')}' - Statut: {task.get('status', 'N/A')} - Cree par: {username} - Date: {date_str} - ID: {task.get('_id')}")
    
    # 4. Chercher "visiter mon cousin"
    print("\n4. Recherche 'visiter mon cousin':")
    cousin_tasks = list(db.tasks.find({"title": {"$regex": "visiter.*cousin", "$options": "i"}}))
    print(f"   Taches trouvees avec 'visiter mon cousin': {len(cousin_tasks)}")
    
    for task in cousin_tasks:
        created_by = task.get('created_by', 'N/A')
        user = db.users.find_one({"_id": created_by})
        username = user.get('username', 'Utilisateur inconnu') if user else 'Utilisateur inconnu'
        print(f"   '{task.get('title', 'N/A')}' - Statut: {task.get('status', 'N/A')} - Cree par: {username} - ID: {task.get('_id')}")
    
    # 5. Chercher "aller chez mon cousin"
    print("\n5. Recherche 'aller chez mon cousin':")
    aller_tasks = list(db.tasks.find({"title": {"$regex": "aller.*cousin", "$options": "i"}}))
    print(f"   Taches trouvees avec 'aller chez mon cousin': {len(aller_tasks)}")
    
    for task in aller_tasks:
        created_by = task.get('created_by', 'N/A')
        user = db.users.find_one({"_id": created_by})
        username = user.get('username', 'Utilisateur inconnu') if user else 'Utilisateur inconnu'
        print(f"   '{task.get('title', 'N/A')}' - Statut: {task.get('status', 'N/A')} - Cree par: {username} - ID: {task.get('_id')}")
    
    # 6. Toutes les tâches contenant "cousin"
    print("\n6. Toutes les taches contenant 'cousin':")
    all_cousin_tasks = list(db.tasks.find({"title": {"$regex": "cousin", "$options": "i"}}))
    print(f"   Taches trouvees avec 'cousin': {len(all_cousin_tasks)}")
    
    for task in all_cousin_tasks:
        created_by = task.get('created_by', 'N/A')
        user = db.users.find_one({"_id": created_by})
        username = user.get('username', 'Utilisateur inconnu') if user else 'Utilisateur inconnu'
        print(f"   '{task.get('title', 'N/A')}' - Statut: {task.get('status', 'N/A')} - Cree par: {username} - ID: {task.get('_id')}")
    
    client.close()
    print("\n" + "=" * 60)
    print("Examen de la base de donnees termine!")

if __name__ == "__main__":
    debug_database() 