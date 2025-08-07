#!/usr/bin/env python3
"""
Correction des utilisateurs PA - Mise à jour des rôles
"""

from pymongo import MongoClient

def fix_pa_users():
    try:
        client = MongoClient('mongodb://localhost:27017')
        db = client.synchtasks_db
        
        print("🔧 Correction des utilisateurs PA...\n")
        
        # Liste des utilisateurs PA à corriger
        pa_users = ['marie_pa', 'pierre_pa', 'sophie_pa']
        
        for username in pa_users:
            # Vérifier l'état actuel
            user = db.users.find_one({'username': username})
            if user:
                print(f"👤 {username}:")
                print(f"   - Role actuel: '{user.get('role', 'NON DÉFINI')}'")
                
                # Mettre à jour le rôle
                result = db.users.update_one(
                    {'username': username},
                    {'$set': {'role': 'pa'}}
                )
                
                if result.modified_count > 0:
                    print(f"   ✅ Role mis à jour vers 'pa'")
                else:
                    print(f"   ⚠️  Aucune modification nécessaire")
                
                # Vérifier après mise à jour
                updated_user = db.users.find_one({'username': username})
                print(f"   - Role après mise à jour: '{updated_user.get('role', 'NON DÉFINI')}'")
            else:
                print(f"❌ {username} non trouvé")
            
            print()
        
        print("🎉 Correction terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_pa_users() 