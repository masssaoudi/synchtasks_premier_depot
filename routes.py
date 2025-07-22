from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models import TaskInDB, TaskCreate, TaskUpdate, UserInDB, CategoryEnum, PriorityEnum
from services import task_service
from auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

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
    """Mettre à jour une tâche"""
    # Vérifier d'abord que la tâche appartient à l'utilisateur
    existing_task = await task_service.get_task_by_id(task_id)
    if not existing_task or existing_task.created_by != current_user.id:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    task = await task_service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Supprimer une tâche"""
    # Vérifier d'abord que la tâche appartient à l'utilisateur
    existing_task = await task_service.get_task_by_id(task_id)
    if not existing_task or existing_task.created_by != current_user.id:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
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