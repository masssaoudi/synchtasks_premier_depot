from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_collection
from typing import Optional
from datetime import datetime

router = APIRouter()


class ThemeModel(BaseModel):
    theme: str


@router.get("/theme/{user_id}")
async def get_theme(user_id: str):
    """Récupérer les préférences de thème d'un utilisateur"""
    try:
        collection = get_collection("theme_preferences")
        doc = await collection.find_one({"user_id": user_id})
        if doc:
            return {"theme": doc["theme"], "success": True}
        else:
            # Retourner le thème par défaut
            return {"theme": "auto", "success": True}
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du thème: {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la récupération du thème"
        )


@router.post("/theme/{user_id}")
async def set_theme(user_id: str, data: ThemeModel):
    """Sauvegarder les préférences de thème d'un utilisateur"""
    try:
        # Valider le thème
        if data.theme not in ["light", "dark", "auto"]:
            raise HTTPException(
                status_code=400,
                detail="Thème invalide. Valeurs acceptées: light, dark, auto",
            )

        # Sauvegarder ou mettre à jour
        collection = get_collection("theme_preferences")
        result = await collection.update_one(
            {"user_id": user_id},
            {"$set": {"theme": data.theme, "updated_at": datetime.utcnow()}},
            upsert=True,
        )

        print(f"✅ Thème sauvegardé pour {user_id}: {data.theme}")
        return {
            "status": "success",
            "theme": data.theme,
            "message": f"Thème {data.theme} sauvegardé avec succès",
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du thème: {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la sauvegarde du thème"
        )


@router.delete("/theme/{user_id}")
async def delete_theme(user_id: str):
    """Supprimer les préférences de thème d'un utilisateur"""
    try:
        collection = get_collection("theme_preferences")
        result = await collection.delete_one({"user_id": user_id})

        if result.deleted_count > 0:
            return {"status": "success", "message": "Préférences de thème supprimées"}
        else:
            return {
                "status": "success",
                "message": "Aucune préférence de thème trouvée",
            }

    except Exception as e:
        print(f"❌ Erreur lors de la suppression du thème: {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la suppression du thème"
        )


@router.get("/theme/{user_id}/status")
async def get_theme_status(user_id: str):
    """Vérifier le statut des préférences de thème"""
    try:
        collection = get_collection("theme_preferences")
        doc = await collection.find_one({"user_id": user_id})

        return {
            "has_preferences": doc is not None,
            "theme": doc["theme"] if doc else "auto",
            "last_updated": doc["updated_at"] if doc else None,
        }

    except Exception as e:
        print(f"❌ Erreur lors de la vérification du statut: {e}")
        raise HTTPException(
            status_code=500, detail="Erreur lors de la vérification du statut"
        )
