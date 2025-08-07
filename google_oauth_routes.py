from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from jose import jwt
import httpx

from config import settings
from database import get_database
from models import UserResponse, APIResponse, UserRoleEnum
from auth import create_access_token, get_password_hash

# ============================================================================
# ROUTER GOOGLE OAUTH
# ============================================================================

router = APIRouter(prefix="/auth/google", tags=["google-oauth"])

# ============================================================================
# CONFIGURATION OAUTH
# ============================================================================

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# ============================================================================
# ROUTES GOOGLE OAUTH
# ============================================================================


@router.get("/login")
async def google_login(request: Request):
    """Redirige vers Google OAuth pour l'authentification"""
    try:
        redirect_uri = request.url_for("google_callback")
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la redirection Google: {str(e)}",
        )


@router.get("/callback")
async def google_callback(request: Request):
    """Gère le callback de Google OAuth et crée/connecte l'utilisateur"""
    try:
        # Récupérer le token et les informations utilisateur
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de récupérer les informations utilisateur",
            )

        # Extraire les informations utilisateur
        email = user_info.get("email")
        name = user_info.get("name")
        google_id = user_info.get("sub")
        picture = user_info.get("picture")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email requis pour l'authentification",
            )

        # Connexion à la base de données
        db = await get_database()

        # Vérifier si l'utilisateur existe déjà
        existing_user = await db[settings.DATABASE_NAME].users.find_one(
            {"email": email}
        )

        if existing_user:
            # Utilisateur existe - créer un token JWT
            user_data = UserResponse(
                id=str(existing_user["_id"]),
                username=existing_user["username"],
                email=existing_user["email"],
                full_name=existing_user["full_name"],
                role=existing_user.get("role", UserRoleEnum.USER),
                is_active=existing_user.get("is_active", True),
                created_at=existing_user["created_at"],
            )

            # Créer le token d'accès
            jwt_token = create_access_token(
                data={"sub": user_data.username},
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )

            # Rediriger vers le frontend avec le token
            redirect_url = f"http://localhost:3000/auth/callback?token={jwt_token}&user={user_data.username}"
            return RedirectResponse(url=redirect_url)

        else:
            # Créer un nouvel utilisateur
            username = email.split("@")[0]  # Utiliser la partie locale de l'email

            # Vérifier si le username existe déjà
            username_counter = 1
            original_username = username
            while await db[settings.DATABASE_NAME].users.find_one(
                {"username": username}
            ):
                username = f"{original_username}{username_counter}"
                username_counter += 1

            # Créer le nouvel utilisateur
            new_user_data = {
                "username": username,
                "email": email,
                "full_name": name,
                "hashed_password": get_password_hash(
                    "google_oauth_user"
                ),  # Mot de passe factice
                "is_active": True,
                "role": UserRoleEnum.USER,
                "created_at": datetime.utcnow(),
                "google_id": google_id,
                "google_picture": picture,
                "auth_provider": "google",
            }

            result = await db[settings.DATABASE_NAME].users.insert_one(new_user_data)

            # Créer la réponse utilisateur
            user_data = UserResponse(
                id=str(result.inserted_id),
                username=username,
                email=email,
                full_name=name,
                role=UserRoleEnum.USER,
                is_active=True,
                created_at=new_user_data["created_at"],
            )

            # Créer le token d'accès
            jwt_token = create_access_token(
                data={"sub": user_data.username},
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )

            # Rediriger vers le frontend avec le token
            redirect_url = f"http://localhost:3000/auth/callback?token={jwt_token}&user={user_data.username}"
            return RedirectResponse(url=redirect_url)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'authentification Google: {str(e)}",
        )


@router.get("/config")
async def get_google_config():
    """Retourne la configuration Google OAuth pour le frontend"""
    return {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }
