#!/usr/bin/env python3
"""
Création de l'utilisateur Alice avec le bon hash
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

async def create_alice():
    """Créer l'utilisateur Alice avec le bon hash"""
    
    # Configuration
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    
    # Connexion à MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.synchtasks_db
    
    # Données utilisateur
    user_data = {
        'username': 'alice',
        'email': 'alice@test.com',
        'full_name': 'Alice Martin',
        'hashed_password': pwd_context.hash('alice123'),
        'role': 'user',
        'is_active': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    try:
        # Insérer l'utilisateur
        result = await db.users.insert_one(user_data)
        print(f"✅ Utilisateur Alice créé avec l'ID: {result.inserted_id}")
        
        # Vérifier que l'utilisateur existe
        user = await db.users.find_one({'email': 'alice@test.com'})
        if user:
            print(f"✅ Utilisateur trouvé: {user['username']} - {user['email']}")
            print(f"✅ Hash: {user['hashed_password'][:20]}...")
        else:
            print("❌ Utilisateur non trouvé")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_alice()) 