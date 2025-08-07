#!/usr/bin/env python3
"""
Recréation des utilisateurs PA avec les bons rôles
"""

from pymongo import MongoClient
from passlib.context import CryptContext

def recreate_pa_users():
    try:
        client = MongoClient('mongodb://localhost:27017')
        db = client.synchtasks_db
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        
        print("🔄 Recréation des utilisateurs PA...\n")
        
        # Supprimer les anciens utilisateurs PA
        pa_users_to_delete = ['marie_pa', 'pierre_pa', 'sophie_pa']
        for username in pa_users_to_delete:
            result = db.users.delete_one({'username': username})
            if result.deleted_count > 0:
                print(f"🗑️  Supprimé: {username}")
            else:
                print(f"⚠️  {username} non trouvé à supprimer")
        
        print()
        
        # Recréer les utilisateurs PA avec le bon rôle
        pa_users = [
            {
                'username': 'marie_pa',
                'email': 'marie.pa@test.com',
                'full_name': 'Marie Dubois',
                'password': 'marie123',
                'role': 'pa'
            },
            {
                'username': 'pierre_pa',
                'email': 'pierre.pa@test.com',
                'full_name': 'Pierre Martin',
                'password': 'pierre123',
                'role': 'pa'
            },
            {
                'username': 'sophie_pa',
                'email': 'sophie.pa@test.com',
                'full_name': 'Sophie Leroy',
                'password': 'sophie123',
                'role': 'pa'
            }
        ]
        
        for user_data in pa_users:
            # Hasher le mot de passe
            hashed_password = pwd_context.hash(user_data['password'])
            
            # Créer l'utilisateur
            new_user = {
                'username': user_data['username'],
                'email': user_data['email'],
                'full_name': user_data['full_name'],
                'hashed_password': hashed_password,
                'role': user_data['role'],
                'is_active': True,
                'phone': None,
                'delegations': [],
                'created_at': '2025-07-27T00:00:00Z',
                'updated_at': '2025-07-27T00:00:00Z'
            }
            
            result = db.users.insert_one(new_user)
            print(f"✅ Recréé: {user_data['username']} (role: {user_data['role']}) - {user_data['password']}")
        
        print(f"\n🎉 Recréation terminée!")
        
        # Vérifier les rôles
        print(f"\n🔍 Vérification des rôles:")
        for user_data in pa_users:
            user = db.users.find_one({'username': user_data['username']})
            if user:
                print(f"   - {user['username']}: role = '{user.get('role', 'NON DÉFINI')}'")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    recreate_pa_users() 