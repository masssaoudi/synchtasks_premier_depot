#!/usr/bin/env python3
"""
Nettoyer les tâches orphelines (créées par des utilisateurs supprimés)
"""

from pymongo import MongoClient

# Configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "synchtasks_db"

def nettoyer_taches_orphelines():
    """Supprimer les tâches créées par des utilisateurs supprimés"""
    
    print("NETTOYAGE DES TACHES ORPHELINES")
    print("=" * 40)
    
    # Connexion MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # 1. Compter les tâches avant nettoyage
    total_taches_avant = db.tasks.count_documents({})
    print(f"Tâches avant nettoyage: {total_taches_avant}")
    
    # 2. Trouver les tâches orphelines
    taches_orphelines = []
    for task in db.tasks.find({}):
        created_by = task.get('created_by')
        if created_by:
            # Vérifier si l'utilisateur existe encore
            user = db.users.find_one({"_id": created_by})
            if not user:
                taches_orphelines.append(task)
    
    print(f"Tâches orphelines trouvées: {len(taches_orphelines)}")
    
    # 3. Afficher les tâches qui vont être supprimées
    if taches_orphelines:
        print("\nTâches qui vont être supprimées:")
        for task in taches_orphelines:
            print(f"  - {task.get('title', 'Sans titre')} (ID: {task.get('_id')})")
    
    # 4. Supprimer les tâches orphelines
    if taches_orphelines:
        task_ids = [task['_id'] for task in taches_orphelines]
        result = db.tasks.delete_many({"_id": {"$in": task_ids}})
        print(f"\n✅ {result.deleted_count} tâches supprimées")
    else:
        print("\n✅ Aucune tâche orpheline à supprimer")
    
    # 5. Compter les tâches après nettoyage
    total_taches_apres = db.tasks.count_documents({})
    print(f"Tâches après nettoyage: {total_taches_apres}")
    
    # 6. Afficher les tâches restantes
    taches_restantes = list(db.tasks.find({}, {"title": 1, "created_by": 1}))
    if taches_restantes:
        print("\nTâches restantes:")
        for task in taches_restantes:
            created_by = task.get('created_by')
            user = db.users.find_one({"_id": created_by})
            username = user.get('username', 'Utilisateur inconnu') if user else 'Utilisateur inconnu'
            print(f"  - {task.get('title', 'Sans titre')} (par: {username})")
    
    client.close()
    print("\n" + "=" * 40)
    print("Nettoyage terminé!")

if __name__ == "__main__":
    nettoyer_taches_orphelines() 