from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ============================================================================
# ENUMS EXISTANTS
# ============================================================================

class PriorityEnum(str, Enum):
    basse = "basse"
    normale = "normale"
    haute = "haute"
    urgente = "urgente"

class CategoryEnum(str, Enum):
    travail = "travail"
    domicile = "domicile"
    famille = "famille"
    loisir = "loisir"
    course = "course"
    sante = "sante"
    apprentissage = "apprentissage"
    personnel = "personnel"
    urgence = "urgence"
    reunion = "reunion"

class TaskStatusEnum(str, Enum):
    todo = "todo"        # À faire
    progress = "progress"  # En cours
    done = "done"        # Terminé

# ============================================================================
# MODÈLES UTILISATEURS
# ============================================================================

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="Nom d'utilisateur")
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    full_name: Optional[str] = Field(None, max_length=100, description="Nom complet")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Mot de passe")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6)

class UserInDB(UserBase):
    id: str = Field(..., alias="_id")
    hashed_password: str = Field(..., description="Mot de passe hashé")
    is_active: bool = Field(default=True, description="Utilisateur actif")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            "ObjectId": str
        },
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    }

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime

# ============================================================================
# MODÈLES PROJETS
# ============================================================================

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nom du projet")
    description: Optional[str] = Field(None, max_length=500, description="Description du projet")
    color: Optional[str] = Field("#6366f1", description="Couleur du projet")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = None

class ProjectInDB(ProjectBase):
    id: str = Field(..., alias="_id")
    owner_id: str = Field(..., description="ID du créateur du projet")
    members: List[str] = Field(default=[], description="Liste des IDs des membres")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            "ObjectId": str
        },
        "json_schema_extra": {
            "example": {
                "name": "Projet SynchTAsks",
                "description": "Application de gestion de tâches collaborative",
                "color": "#6366f1",
                "owner_id": "user123",
                "members": ["user123", "user456"]
            }
        }
    }

class ProjectResponse(ProjectInDB):
    pass

# ============================================================================
# MODÈLES TÂCHES (ÉTENDUS)
# ============================================================================

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Titre de la tâche")
    category: CategoryEnum = Field(..., description="Catégorie de la tâche")
    priority: PriorityEnum = Field(default=PriorityEnum.normale, description="Priorité de la tâche")
    description: Optional[str] = Field(None, max_length=500, description="Description optionnelle")
    project_id: Optional[str] = Field(None, description="ID du projet associé")
    assignee_id: Optional[str] = Field(None, description="ID de l'utilisateur assigné")
    due_date: Optional[datetime] = Field(None, description="Date d'échéance")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[CategoryEnum] = None
    priority: Optional[PriorityEnum] = None
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
    project_id: Optional[str] = None
    assignee_id: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatusEnum] = None

class TaskInDB(TaskBase):
    id: str = Field(..., alias="_id")
    status: TaskStatusEnum = Field(default=TaskStatusEnum.todo, description="Statut de la tâche")
    completed: bool = Field(default=False, description="Statut de complétion (déprécié, utiliser status)")
    created_by: str = Field(..., description="ID du créateur de la tâche")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date de création")
    completed_at: Optional[datetime] = Field(None, description="Date de complétion")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Date de mise à jour")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            "ObjectId": str
        },
        "json_schema_extra": {
            "example": {
                "title": "Commencer le projet SynchTAsks",
                "category": "travail",
                "priority": "haute",
                "description": "Créer l'architecture de base du projet",
                "project_id": "project123",
                "assignee_id": "user123",
                "completed": False,
                "created_by": "user123",
                "created_at": "2024-01-15T10:30:00Z",
                "completed_at": None,
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }
    }

class TaskResponse(TaskInDB):
    pass

# ============================================================================
# MODÈLES AUTHENTIFICATION
# ============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="Nom d'utilisateur")
    password: str = Field(..., min_length=6, description="Mot de passe")

# ============================================================================
# MODÈLES STATISTIQUES (ÉTENDUS)
# ============================================================================

class TaskStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float
    tasks_by_category: dict
    tasks_by_priority: dict
    tasks_by_user: dict
    tasks_by_project: dict

class ProjectStats(BaseModel):
    project_id: str
    project_name: str
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    active_members: int

# ============================================================================
# MODÈLES RÉPONSE API
# ============================================================================

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int 

class DelegationStatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    revoked = "revoked"

class DelegationInDB(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str = Field(..., description="ID de l'utilisateur aidé")
    aidant_id: str = Field(..., description="ID de la personne aidante")
    status: DelegationStatusEnum = Field(default=DelegationStatusEnum.pending)
    invited_at: datetime = Field(default_factory=datetime.utcnow)
    accepted_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            "ObjectId": str
        },
        "json_schema_extra": {
            "example": {
                "user_id": "user123",
                "aidant_id": "aidant456",
                "status": "pending",
                "invited_at": "2024-01-15T10:30:00Z",
                "accepted_at": None,
                "revoked_at": None
            }
        }
    } 

class DelegationCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    user_id: Optional[str] = None  # L'utilisateur qui délègue 