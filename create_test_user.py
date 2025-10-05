#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test pour SyncTasks
"""

import asyncio
import sys
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

# Configuration
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "synchtasks_db"

# Contexte de hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash un mot de passe avec bcrypt"""
    return pwd_context.hash(password)

async def create_test_user():
    """Crée un utilisateur de test"""
    try:
        # Connexion à MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = await db.users.find_one({"email": "alic@test.com"})
        if existing_user:
            print("✅ L'utilisateur alic@test.com existe déjà")
            return
        
        # Créer l'utilisateur de test
        user_data = {
            "username": "alic",
            "email": "alic@test.com",
            "full_name": "Alice Test",
            "role": "user",
            "hashed_password": hash_password("alice123"),
            "is_active": True,
            "phone": None,
            "delegations": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insérer l'utilisateur
        result = await db.users.insert_one(user_data)
        
        if result.inserted_id:
            print("✅ Utilisateur de test créé avec succès !")
            print("📧 Email: alic@test.com")
            print("🔑 Mot de passe: alice123")
            print("🆔 ID: " + str(result.inserted_id))
        else:
            print("❌ Erreur lors de la création de l'utilisateur")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("🚀 Création d'un utilisateur de test pour SyncTasks...")
    asyncio.run(create_test_user()) 