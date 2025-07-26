import pymongo
from pymongo.errors import ConnectionFailure

# Adapter l'URI à ta config si besoin
MONGO_URI = "mongodb://localhost:27017/"

try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    # Essaye d'obtenir les infos du serveur
    info = client.server_info()
    print("✅ Connexion à MongoDB réussie !")
    print("Bases de données disponibles :", client.list_database_names())
    # Affiche les collections de la base principale si elle existe
    db_name = "synchtasks_db"  # nom corrigé
    if db_name in client.list_database_names():
        print(f"Collections dans la base '{db_name}' :", client[db_name].list_collection_names())
    else:
        print(f"La base '{db_name}' n'existe pas.")
except ConnectionFailure as e:
    print("❌ Connexion à MongoDB impossible :", e) 