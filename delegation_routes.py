from fastapi import APIRouter, HTTPException, Depends, status
from models import DelegationInDB, DelegationCreate
from services import DelegationService, fill_missing_fields
from auth import get_current_user
from services import TaskService

router = APIRouter(prefix="/delegations", tags=["delegations"])

delegation_service = DelegationService()

task_service = TaskService()

@router.post("/", response_model=DelegationInDB)
async def create_delegation_endpoint(
    delegation: DelegationCreate,
    current_user=Depends(get_current_user)
):
    """Créer une nouvelle délégation (invitation d'un aidant)."""
    # Injecter l'user_id du délégant
    delegation.user_id = current_user.id
    created = await delegation_service.create_delegation(delegation)
    return created

@router.post("/invite", response_model=DelegationInDB)
async def invite_aidant_endpoint(
    aidant_id: str,
    current_user=Depends(get_current_user)
):
    """Endpoint pour inviter une personne aidante."""
    try:
        delegation = await delegation_service.invite_aidant(user_id=current_user.id, aidant_id=aidant_id)
        return delegation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/accept", response_model=DelegationInDB)
async def accept_delegation_endpoint(
    delegation_id: str,
    current_user=Depends(get_current_user)
):
    """Endpoint pour accepter une invitation de délégation (par l'aidant)."""
    try:
        delegation = await delegation_service.accept_delegation(delegation_id=delegation_id, aidant_id=current_user.id)
        return delegation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/revoke", response_model=DelegationInDB)
async def revoke_delegation_endpoint(
    delegation_id: str,
    current_user=Depends(get_current_user)
):
    """Endpoint pour révoquer une délégation (par l'utilisateur principal)."""
    try:
        delegation = await delegation_service.revoke_delegation(delegation_id=delegation_id, user_id=current_user.id)
        return delegation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/kanban", response_model=list)
async def kanban_for_aidant(
    user_id: str,  # l'utilisateur aidé
    current_user=Depends(get_current_user)
):
    """Permet à la PA d'accéder au Kanban de l'utilisateur aidé si la délégation est acceptée."""
    # Vérifier la délégation acceptée
    delegation = await delegation_service._get_collection().find_one({
        "user_id": user_id,
        "aidant_id": current_user.id,
        "status": "accepted"
    })
    if not delegation:
        raise HTTPException(status_code=403, detail="Aucune délégation acceptée pour cet utilisateur.")
    # Récupérer les tâches du user_id aidé
    tasks_cursor = task_service._get_collection().find({"created_by": user_id})
    tasks = []
    async for task in tasks_cursor:
        tasks.append(fill_missing_fields(task))
    return tasks

@router.post("/check_aidant_email")
async def check_aidant_email(email: str):
    """Vérifie si l'email correspond à une personne aidante acceptée."""
    is_aidant = await delegation_service.is_email_aidant(email)
    return {"is_aidant": is_aidant}

@router.get("/mine")
async def get_my_delegations(current_user=Depends(get_current_user)):
    """Récupère les délégations où l'utilisateur connecté est aidant."""
    delegations = await delegation_service.get_delegations_for_aidant(current_user.id)
    # Convertir les documents MongoDB en modèles Pydantic
    from models import DelegationInDB
    return [DelegationInDB(**{**delegation, "_id": str(delegation["_id"])}) for delegation in delegations] 