from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

from models import UserCreate, UserResponse, Token, UserUpdate, APIResponse, LoginRequest, OTPRequest, OTPVerify, UserRoleEnum
from auth import login_user, register_user, get_current_active_user, get_user_by_id, get_user_by_username
from database import get_database
from delegation_routes import router as delegation_router
import random
import string
from datetime import datetime, timedelta

# ============================================================================
# ROUTER AUTHENTIFICATION
# ============================================================================

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# ============================================================================
# ROUTES D'AUTHENTIFICATION
# ============================================================================

@router.post("/register", response_model=APIResponse)
async def register(
    user: UserCreate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """Enregistre un nouvel utilisateur"""
    try:
        new_user = await register_user(db, user)
        return APIResponse(
            success=True,
            message="Utilisateur créé avec succès",
            data={
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "full_name": new_user.full_name,
                    "is_active": new_user.is_active,
                    "created_at": new_user.created_at.isoformat()
                }
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'utilisateur: {str(e)}"
        )



@router.post("/login", response_model=APIResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncIOMotorClient = Depends(get_database)
):
    username = login_data.username
    password = login_data.password
    """Authentifie un utilisateur et retourne un token"""
    try:
        token = await login_user(db, username, password)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nom d'utilisateur ou mot de passe incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return APIResponse(
            success=True,
            message="Connexion réussie",
            data={
                "access_token": token.access_token,
                "token_type": token.token_type,
                "user": {
                    "id": token.user.id,
                    "username": token.user.username,
                    "email": token.user.email,
                    "full_name": token.user.full_name,
                    "role": token.user.role,
                    "is_active": token.user.is_active,
                    "created_at": token.user.created_at.isoformat()
                }
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la connexion: {str(e)}"
        )

@router.get("/me", response_model=APIResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Récupère les informations de l'utilisateur connecté"""
    return APIResponse(
        success=True,
        message="Informations utilisateur récupérées",
        data={
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "full_name": current_user.full_name,
                "role": current_user.role,
                "is_active": current_user.is_active,
                "created_at": current_user.created_at.isoformat()
            }
        }
    )

@router.put("/me", response_model=APIResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database)
):
    """Met à jour les informations de l'utilisateur connecté"""
    try:
        # Récupérer l'utilisateur complet depuis la DB
        db_user = await get_user_by_id(db, current_user.id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Préparer les données de mise à jour
        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aucune donnée à mettre à jour"
            )
        
        # Vérifier si le nouveau username existe déjà
        if "username" in update_data:
            existing_user = await get_user_by_username(db, update_data["username"])
            if existing_user and existing_user.id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nom d'utilisateur déjà utilisé"
                )
        
        # Ajouter la date de mise à jour
        update_data["updated_at"] = datetime.utcnow()
        
        # Mettre à jour dans la base de données
        result = await db.users.update_one(
            {"_id": current_user.id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aucune modification effectuée"
            )
        
        # Récupérer l'utilisateur mis à jour
        updated_user = await get_user_by_id(db, current_user.id)
        
        return APIResponse(
            success=True,
            message="Utilisateur mis à jour avec succès",
            data={
                "user": {
                    "id": updated_user.id,
                    "username": updated_user.username,
                    "email": updated_user.email,
                    "full_name": updated_user.full_name,
                    "role": updated_user.role,
                    "is_active": updated_user.is_active,
                    "created_at": updated_user.created_at.isoformat(),
                    "updated_at": updated_user.updated_at.isoformat()
                }
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )

# ============================================================================
# ROUTES OTP ET PERSONNE AIDANTE
# ============================================================================

@router.post("/send-otp", response_model=APIResponse)
async def send_otp(
    otp_request: OTPRequest,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """Envoie un code OTP par SMS (simulé)"""
    try:
        # Générer un code OTP à 6 chiffres
        code = ''.join(random.choices(string.digits, k=6))
        
        # Supprimer les anciens codes pour ce téléphone
        await db.synchtasks_db.otp_codes.delete_many({"phone": otp_request.phone})
        
        # Insérer le nouveau code avec expiration (5 minutes)
        otp_data = {
            "phone": otp_request.phone,
            "code": code,
            "expires_at": datetime.utcnow() + timedelta(minutes=5),
            "used": False
        }
        await db.synchtasks_db.otp_codes.insert_one(otp_data)
        
        # Simulation d'envoi SMS (en production, utiliser un service SMS)
        print(f"✅ Code OTP envoyé au {otp_request.phone}: {code}")
        
        return APIResponse(
            success=True,
            message="Code OTP envoyé avec succès",
            data={"phone": otp_request.phone}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'envoi de l'OTP: {str(e)}"
        )

@router.post("/verify-otp", response_model=APIResponse)
async def verify_otp(
    otp_verify: OTPVerify,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """Vérifie un code OTP"""
    try:
        # Récupérer le code OTP
        otp_data = await db.synchtasks_db.otp_codes.find_one({
            "phone": otp_verify.phone,
            "code": otp_verify.code,
            "used": False
        })
        
        if not otp_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Code OTP invalide"
            )
        
        # Vérifier l'expiration
        if datetime.utcnow() > otp_data["expires_at"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Code OTP expiré"
            )
        
        # Marquer le code comme utilisé
        await db.synchtasks_db.otp_codes.update_one(
            {"_id": otp_data["_id"]},
            {"$set": {"used": True}}
        )
        
        return APIResponse(
            success=True,
            message="Code OTP validé avec succès",
            data={"phone": otp_verify.phone}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la vérification de l'OTP: {str(e)}"
        )

@router.post("/register-pa", response_model=APIResponse)
async def register_personne_aidante(
    user: UserCreate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """Enregistre une nouvelle personne aidante"""
    try:
        # Forcer le rôle PA
        user.role = UserRoleEnum.pa
        
        new_user = await register_user(db, user)
        return APIResponse(
            success=True,
            message="Personne aidante créée avec succès",
            data={
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                    "full_name": new_user.full_name,
                    "role": new_user.role,
                    "is_active": new_user.is_active,
                    "created_at": new_user.created_at.isoformat()
                }
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la personne aidante: {str(e)}"
        )

# ============================================================================
# ROUTES UTILISATEURS
# ============================================================================

@router.get("/users", response_model=APIResponse)
async def get_users(
    current_user: UserResponse = Depends(get_current_active_user),
    db: AsyncIOMotorClient = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    """Récupère la liste des utilisateurs (pour les admins)"""
    try:
        # TODO: Ajouter vérification admin
        users = []
        cursor = db.users.find().skip(skip).limit(limit)
        
        async for user_data in cursor:
            user_data["_id"] = str(user_data["_id"])
            users.append({
                "id": user_data["_id"],
                "username": user_data["username"],
                "email": user_data["email"],
                "full_name": user_data.get("full_name"),
                "is_active": user_data.get("is_active", True),
                "created_at": user_data["created_at"].isoformat()
            })
        
        return APIResponse(
            success=True,
            message=f"{len(users)} utilisateurs récupérés",
            data={"users": users}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des utilisateurs: {str(e)}"
        ) 