from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_collection
from auth import get_current_active_user
from models import UserResponse

router = APIRouter()

class UserProfile(BaseModel):
    segment: str
    preferences: Optional[dict] = None

@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str, current_user: UserResponse = Depends(get_current_active_user)):
    """Récupérer le profil utilisateur"""
    try:
        # Vérifier que l'utilisateur accède à son propre profil
        if str(current_user.id) != user_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        collection = get_collection("user_profiles")
        profile = await collection.find_one({"user_id": user_id})
        
        if profile:
            return {
                "segment": profile.get("segment", "auto"),
                "preferences": profile.get("preferences", {}),
                "updated_at": profile.get("updated_at"),
                "success": True
            }
        else:
            return {
                "segment": "auto",
                "preferences": {},
                "success": True
            }
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du profil: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération du profil")

@router.post("/users/{user_id}/profile")
async def update_user_profile(user_id: str, profile_data: UserProfile, current_user: UserResponse = Depends(get_current_active_user)):
    """Mettre à jour le profil utilisateur"""
    try:
        # Vérifier que l'utilisateur met à jour son propre profil
        if str(current_user.id) != user_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Valider le segment
        valid_segments = ["particuliers", "etudiants", "medical", "memoire", "professionnels", "entreprises", "auto"]
        if profile_data.segment not in valid_segments:
            raise HTTPException(status_code=400, detail="Segment invalide")
        
        collection = get_collection("user_profiles")
        
        # Mettre à jour ou créer le profil
        result = await collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "segment": profile_data.segment,
                    "preferences": profile_data.preferences or {},
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        return {
            "message": "Profil mis à jour avec succès",
            "segment": profile_data.segment,
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du profil: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la mise à jour du profil")

@router.delete("/users/{user_id}/profile")
async def delete_user_profile(user_id: str, current_user: UserResponse = Depends(get_current_active_user)):
    """Supprimer le profil utilisateur"""
    try:
        # Vérifier que l'utilisateur supprime son propre profil
        if str(current_user.id) != user_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        collection = get_collection("user_profiles")
        result = await collection.delete_one({"user_id": user_id})
        
        if result.deleted_count > 0:
            return {
                "message": "Profil supprimé avec succès",
                "success": True
            }
        else:
            return {
                "message": "Aucun profil trouvé",
                "success": True
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la suppression du profil: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du profil") 