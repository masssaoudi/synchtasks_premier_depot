import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    # MongoDB Configuration
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "synchtasks_db")

    # FastAPI Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = 8001  # Forcer le port 8001
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "synchtasks-dev-secret-key-2024-change-in-production-very-long-secure-key",
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/google/callback"
    )


settings = Settings()
