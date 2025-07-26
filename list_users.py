import pymongo

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "synchtasks_db"
COLLECTION = "users"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
users = list(db[COLLECTION].find())

if not users:
    print("Aucun utilisateur trouvé dans la base.")
else:
    print(f"Utilisateurs trouvés dans '{DB_NAME}.{COLLECTION}' :")
    for user in users:
        print(user) 