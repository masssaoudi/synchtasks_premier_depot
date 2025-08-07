import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def get_last_otp():
    # Connexion à MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.synchtasks_db
    
    # Récupérer le dernier OTP généré
    last_otp = await db.otp_codes.find_one(
        {"phone": "+33123456789"},
        sort=[("_id", -1)]  # Le plus récent
    )
    
    if last_otp:
        print(f"📱 Dernier OTP pour +33123456789:")
        print(f"   Code: {last_otp['code']}")
        print(f"   Expire: {last_otp['expires_at']}")
        print(f"   Utilisé: {last_otp.get('used', False)}")
        
        # Vérifier s'il est encore valide
        if datetime.utcnow() < last_otp['expires_at'] and not last_otp.get('used', False):
            print("✅ Code OTP valide et utilisable")
            return last_otp['code']
        else:
            print("❌ Code OTP expiré ou déjà utilisé")
    else:
        print("❌ Aucun OTP trouvé pour ce numéro")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(get_last_otp()) 