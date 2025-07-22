import os
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# Import conditionnel pour mongomock
try:
    from mongomock_motor import AsyncMongoMockClient
    MONGOMOCK_AVAILABLE = True
except ImportError:
    MONGOMOCK_AVAILABLE = False

class Database:
    client = None
    database = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB"""
    # Vérifier si on doit utiliser mongomock pour les tests
    use_mock_db = os.getenv("USE_MOCK_DB", "false").lower() == "true"
    
    if use_mock_db and MONGOMOCK_AVAILABLE:
        # Utiliser mongomock pour les tests
        db.client = AsyncMongoMockClient()
        db.database = db.client.test_database
        print(f"🔧 Connected to MongoDB Mock for testing")
    else:
        # Utiliser la vraie base de données MongoDB
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.DATABASE_NAME]
        print(f"✅ Connected to MongoDB database: {settings.DATABASE_NAME}")

async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("🔌 MongoDB connection closed")

def get_collection(collection_name: str):
    """Get a collection from the database"""
    return db.database[collection_name]

def get_database():
    """Get the database instance for dependency injection"""
    return db.database 