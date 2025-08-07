#!/usr/bin/env python3
"""
Script de création d'utilisateurs de test pour SyncTasks
- Crée des utilisateurs normaux et des PA avec des mots de passe simples
"""

from pymongo import MongoClient
from passlib.context import CryptContext
import sys

def create_test_users():
    try:
        # Connexion à MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client.synchtasks_db
        
        print("👥 Création d'utilisateurs de test...")
        
        # Configuration du hashage des mots de passe
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        
        # Liste des utilisateurs à créer
        test_users = [
            # Utilisateurs normaux
            {
                'username': 'alice',
                'email': 'alice@test.com',
                'full_name': 'Alice Martin',
                'password': 'alice123',
                'role': 'user'
            },
            {
                'username': 'bob',
                'email': 'bob@test.com',
                'full_name': 'Bob Dupont',
                'password': 'bob123',
                'role': 'user'
            },
            {
                'username': 'charlie',
                'email': 'charlie@test.com',
                'full_name': 'Charlie Bernard',
                'password': 'charlie123',
                'role': 'user'
            },
            # Personnes Aidantes (PA)
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
        
        created_count = 0
        
        for user_data in test_users:
            # Vérifier si l'utilisateur existe déjà
            existing_user = db.users.find_one({'username': user_data['username']})
            if existing_user:
                print(f"⚠️  L'utilisateur '{user_data['username']}' existe déjà")
                continue
            
            # Créer l'utilisateur
            hashed_password = pwd_context.hash(user_data['password'])
            
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
            created_count += 1
            print(f"✅ Créé: {user_data['username']} ({user_data['role']}) - {user_data['password']}")
        
        # Afficher le résumé
        print(f"\n📊 Résumé:")
        print(f"- {created_count} nouveaux utilisateurs créés")
        
        # Compter par rôle
        user_count = db.users.count_documents({'role': 'user'})
        pa_count = db.users.count_documents({'role': 'pa'})
        total_count = db.users.count_documents({})
        
        print(f"- Total utilisateurs: {total_count}")
        print(f"  - Utilisateurs normaux: {user_count}")
        print(f"  - Personnes Aidantes: {pa_count}")
        
        # Afficher tous les utilisateurs
        print(f"\n👥 Liste des utilisateurs disponibles:")
        all_users = db.users.find({}, {'username': 1, 'role': 1, 'email': 1})
        
        for user in all_users:
            role_emoji = "👤" if user.get('role') == 'user' else "🤝"
            print(f"  {role_emoji} {user['username']} ({user.get('role', 'user')}) - {user['email']}")
        
        print(f"\n🎉 Création terminée!")
        print(f"Vous pouvez maintenant tester avec ces identifiants simples.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_test_users() 