"""
Configuration de la base de données de test avec mongomock
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Import conditionnel pour mongomock
try:
    from mongomock_motor import AsyncMongoMockClient
    MONGOMOCK_AVAILABLE = True
except ImportError:
    MONGOMOCK_AVAILABLE = False
    AsyncMongoMockClient = None

# Variable d'environnement pour utiliser mongomock en mode test
USE_MOCK_DB = os.getenv("USE_MOCK_DB", "true").lower() == "true"

class TestDatabaseManager:
    """Gestionnaire de base de données pour les tests"""
    
    def __init__(self):
        self.client = None
        self.database = None
    
    async def connect(self):
        """Se connecter à la base de données de test"""
        if USE_MOCK_DB and MONGOMOCK_AVAILABLE:
            # Utiliser mongomock pour les tests
            self.client = AsyncMongoMockClient()
            self.database = self.client.test_database
            print("🔧 Connecté à MongoDB Mock pour les tests")
        else:
            # Utiliser une vraie base de données MongoDB
            mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/synchtasks_test")
            self.client = AsyncIOMotorClient(mongo_url)
            self.database = self.client.get_database()
            print("🔧 Connecté à MongoDB réel pour les tests")
    
    async def disconnect(self):
        """Se déconnecter de la base de données"""
        if self.client:
            self.client.close()
            print("🔌 Déconnecté de la base de données de test")
    
    def get_database(self):
        """Obtenir l'instance de la base de données"""
        return self.database
    
    async def cleanup(self):
        """Nettoyer la base de données de test"""
        if self.database:
            # Supprimer toutes les collections
            collections = await self.database.list_collection_names()
            for collection_name in collections:
                await self.database[collection_name].delete_many({})
            print("🧹 Base de données de test nettoyée")

# Instance globale du gestionnaire de base de données de test
test_db_manager = TestDatabaseManager()

async def connect_test_database():
    """Se connecter à la base de données de test"""
    await test_db_manager.connect()

async def disconnect_test_database():
    """Se déconnecter de la base de données de test"""
    await test_db_manager.disconnect()

def get_test_database():
    """Obtenir l'instance de la base de données de test"""
    return test_db_manager.get_database()

async def cleanup_test_database():
    """Nettoyer la base de données de test"""
    await test_db_manager.cleanup() 