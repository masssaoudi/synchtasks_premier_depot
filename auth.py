from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional

from models import UserCreate, UserInDB, UserResponse, Token, TokenData
from config import settings
from database import get_database

# ============================================================================
# CONFIGURATION SÉCURITÉ
# ============================================================================

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash un mot de passe"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crée un token d'accès JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def verify_token(token: str) -> Optional[TokenData]:
    """Vérifie un token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        return None

# ============================================================================
# FONCTIONS D'AUTHENTIFICATION
# ============================================================================

async def get_user_by_username(db: AsyncIOMotorClient, username: str) -> Optional[UserInDB]:
    """Récupère un utilisateur par email (si @) ou par username sinon, insensible à la casse."""
    if "@" in username:
        user_data = await db.users.find_one({"email": {"$regex": f"^{username}$", "$options": "i"}})
    else:
        user_data = await db.users.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
    if user_data:
        user_data["_id"] = str(user_data["_id"])
        return UserInDB(**user_data)
    return None

async def get_user_by_id(db: AsyncIOMotorClient, user_id: str) -> Optional[UserInDB]:
    """Récupère un utilisateur par son ID"""
    from bson import ObjectId
    try:
        user_data = await db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return UserInDB(**user_data)
    except:
        pass
    return None

async def authenticate_user(db: AsyncIOMotorClient, username: str, password: str) -> Optional[UserInDB]:
    """Authentifie un utilisateur"""
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def register_user(db: AsyncIOMotorClient, user: UserCreate) -> UserInDB:
    """Enregistre un nouvel utilisateur"""
    # Vérifier si l'utilisateur existe déjà
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur déjà utilisé"
        )
    
    # Vérifier si l'email existe déjà
    existing_email = await db.users.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé"
        )
    
    # Créer l'utilisateur
    hashed_password = get_password_hash(user.password)
    user_data = user.model_dump()
    user_data["hashed_password"] = hashed_password
    user_data["created_at"] = datetime.utcnow()
    user_data["updated_at"] = datetime.utcnow()
    
    result = await db.users.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    
    return UserInDB(**user_data)

async def login_user(db: AsyncIOMotorClient, username: str, password: str) -> Optional[Token]:
    """Connecte un utilisateur et retourne un token"""
    user = await authenticate_user(db, username, password)
    if not user:
        return None
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
    )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorClient = Depends(get_database)
) -> UserInDB:
    """Récupère l'utilisateur actuel depuis le token"""
    token_data = await verify_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserResponse:
    """Récupère l'utilisateur actuel actif"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif"
        )
    
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    ) 