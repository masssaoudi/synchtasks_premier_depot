#!/usr/bin/env python3
"""
Script pour créer le fichier .env avec la configuration par défaut
"""

import os
import secrets


def create_env_file():
    """Créer le fichier .env s'il n'existe pas"""

    if os.path.exists(".env"):
        print("✅ Le fichier .env existe déjà")
        return

    # Générer une clé secrète sécurisée
    secret_key = secrets.token_urlsafe(32)

    env_content = f"""# =====================================
# CONFIGURATION SYNCHTASKS - ENVIRONNEMENT LOCAL
# =====================================

# Base de données MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=synchtasks_db

# Configuration FastAPI
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Sécurité JWT - Clé générée automatiquement
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuration WebSocket
WEBSOCKET_ENABLED=true
WEBSOCKET_RECONNECT_ATTEMPTS=5

# Logging
LOG_LEVEL=INFO
"""

    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)

        print("🎉 Fichier .env créé avec succès !")
        print("🔑 Clé JWT générée automatiquement")
        print("📝 Vous pouvez modifier les valeurs dans .env si nécessaire")

    except Exception as e:
        print(f"❌ Erreur lors de la création du .env: {e}")


if __name__ == "__main__":
    create_env_file()
