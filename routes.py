from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models import TaskInDB, TaskCreate, TaskUpdate, UserInDB, CategoryEnum, PriorityEnum, TaskStatusEnum
from services import task_service, DelegationService
from auth import get_current_user
from database import get_database

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# Service de délégation pour vérifier les permissions
delegation_service = DelegationService()

async def can_modify_task(task_owner_id: str, current_user_id: str) -> bool:
    """
    Vérifie si l'utilisateur actuel peut modifier une tâche.
    Retourne True si :
    - L'utilisateur est le propriétaire de la tâche
    - L'utilisateur est un PA avec une délégation acceptée
    """
    # Si c'est le propriétaire de la tâche
    if task_owner_id == current_user_id:
        return True
    
    # Vérifier si c'est un PA avec une délégation acceptée
    try:
        delegation = await delegation_service._get_collection().find_one({
            "user_id": task_owner_id,  # L'utilisateur aidé
            "aidant_id": current_user_id,  # Le PA actuel
            "status": "accepted"
        })
        return delegation is not None
    except Exception as e:
        print(f"Erreur vérification délégation: {e}")
        return False

@router.get("/categories/")
async def get_categories():
    """Récupérer toutes les catégories disponibles"""
    return {
        "categories": [
            {"value": cat.value, "label": cat.value.title(), "icon": get_category_icon(cat.value)}
            for cat in CategoryEnum
        ]
    }

@router.get("/priorities/")
async def get_priorities():
    """Récupérer toutes les priorités disponibles"""
    return {
        "priorities": [
            {"value": pri.value, "label": pri.value.title()}
            for pri in PriorityEnum
        ]
    }

def get_category_icon(category: str) -> str:
    """Retourne l'icône correspondante à la catégorie"""
    icons = {
        "travail": "💼",
        "domicile": "🏠",
        "famille": "👨‍👩‍👧‍👦",
        "loisir": "🎮",
        "course": "🛒",
        "sante": "🏥",
        "apprentissage": "📚",
        "personnel": "👤",
        "urgence": "🚨",
        "reunion": "🤝"
    }
    return icons.get(category, "📋")

@router.get("/", response_model=List[TaskInDB])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user)
):
    """Récupérer toutes les tâches de l'utilisateur"""
    tasks = await task_service.get_user_tasks(current_user.id, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=TaskInDB)
async def create_task(
    task: TaskCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Créer une nouvelle tâche"""
    return await task_service.create_task(task, current_user.id)

@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Récupérer une tâche spécifique"""
    task = await task_service.get_task_by_id(task_id)
    if not task or task.created_by != current_user.id:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task

@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Mettre à jour une tâche (mise à jour complète)"""
    print(f"🔍 User {current_user.email} tente de modifier la tâche {task_id}")
    
    # Vérifier d'abord que la tâche existe
    existing_task = await task_service.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    # Vérifier les permissions (propriétaire ou PA avec délégation)
    can_modify = await can_modify_task(existing_task.created_by, current_user.id)
    if not can_modify:
        print(f"❌ Accès refusé: {current_user.email} ne peut pas modifier la tâche {task_id}")
        raise HTTPException(status_code=403, detail="Vous n'avez pas les permissions pour modifier cette tâche")
    
    print(f"✅ Permissions OK pour {current_user.email} sur tâche {task_id}")
    
    task = await task_service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task

@router.patch("/{task_id}", response_model=TaskInDB)
async def patch_task_status(
    task_id: str,
    status_update: dict,
    current_user: UserInDB = Depends(get_current_user)
):
    """Mettre à jour uniquement le statut d'une tâche (pour drag & drop)"""
    print(f"🔍 User {current_user.email} tente de modifier le statut de la tâche {task_id}")
    print(f"📦 Données reçues: {status_update}")
    
    # Vérifier d'abord que la tâche existe
    existing_task = await task_service.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    # Vérifier les permissions (propriétaire ou PA avec délégation)
    can_modify = await can_modify_task(existing_task.created_by, current_user.id)
    if not can_modify:
        print(f"❌ Accès refusé: {current_user.email} ne peut pas modifier la tâche {task_id}")
        raise HTTPException(status_code=403, detail="Vous n'avez pas les permissions pour modifier cette tâche")
    
    print(f"✅ Permissions OK pour {current_user.email} sur tâche {task_id}")
    
    # Extraire le nouveau statut
    new_status = status_update.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="Le champ 'status' est requis")
    
    # Valider le statut
    try:
        validated_status = TaskStatusEnum(new_status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Statut invalide. Valeurs autorisées: {[s.value for s in TaskStatusEnum]}")
    
    print(f"🔄 Changement de statut: {existing_task.status} → {validated_status}")
    
    # Créer l'objet de mise à jour
    task_update = TaskUpdate(status=validated_status)
    
    # Mettre à jour la tâche
    task = await task_service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    print(f"✅ Tâche {task_id} mise à jour avec succès")
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Supprimer une tâche"""
    print(f"🔍 User {current_user.email} tente de supprimer la tâche {task_id}")
    
    # Vérifier d'abord que la tâche existe
    existing_task = await task_service.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    # Vérifier les permissions (propriétaire ou PA avec délégation)
    can_modify = await can_modify_task(existing_task.created_by, current_user.id)
    if not can_modify:
        print(f"❌ Accès refusé: {current_user.email} ne peut pas supprimer la tâche {task_id}")
        raise HTTPException(status_code=403, detail="Vous n'avez pas les permissions pour supprimer cette tâche")
    
    print(f"✅ Permissions OK pour {current_user.email} sur tâche {task_id}")
    
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return {"message": "Tâche supprimée avec succès"}

@router.get("/health/", tags=["health"])
async def health_check():
    """Vérification de santé des tâches"""
    return {
        "status": "healthy",
        "service": "tasks-api",
        "message": "Service des tâches opérationnel"
    } 