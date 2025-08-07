import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import logging
from enum import Enum

from database import get_database
from models import TaskCreate, TaskInDB, TaskUpdate, CategoryEnum, PriorityEnum
# WebSocket functions à recréer proprement
async def notify_task_update(task_data: dict, action: str):
    """Notifier une mise à jour de tâche via WebSocket"""
    try:
        from websocket_simple import send_task_update
        await send_task_update(task_data)
    except Exception as e:
        logger.warning(f"Erreur WebSocket notification: {e}")

async def notify_user_action(user_id: str, action: str, data: dict = None):
    """Notifier une action utilisateur via WebSocket"""
    try:
        from websocket_simple import manager
        # Logique de notification utilisateur
        logger.info(f"Action utilisateur {action} pour {user_id}")
    except Exception as e:
        logger.warning(f"Erreur WebSocket notification utilisateur: {e}")

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {
    "title": None,
    "category": None,
    "priority": "normale",
    "description": None,
    "project_id": None,
    "assignee_id": None,
    "due_date": None,
    "id": None,
    "status": "todo",
    "completed": False,
    "created_by": None,
    "created_at": None,
    "completed_at": None,
    "updated_at": None,
}


def fill_missing_fields(task: dict) -> dict:
    # Copie pour éviter de modifier l'original
    task_copy = task.copy()

    # Gestion de l'ObjectId MongoDB
    if "_id" in task_copy:
        task_copy["id"] = str(task_copy["_id"])
        del task_copy["_id"]  # Supprimer _id car Pydantic attend "id"

    # Remplir les champs manquants avec des valeurs par défaut
    for key, default in REQUIRED_FIELDS.items():
        if key not in task_copy or task_copy[key] is None:
            if key == "created_by" and default is None:
                # Pour created_by, utiliser un ID par défaut ou l'ID de l'utilisateur système
                task_copy[key] = "system"  # ou "default_user"
            elif key == "created_at" and default is None:
                task_copy[key] = datetime.utcnow()
            elif key == "updated_at" and default is None:
                task_copy[key] = datetime.utcnow()
            elif key == "status" and default is not None:
                # Ne pas écraser le statut s'il existe déjà
                continue
            else:
                task_copy[key] = default

    return task_copy


class TaskService:
    def __init__(self):
        self.collection = None

    def _get_collection(self):
        """Get collection with lazy initialization"""
        if self.collection is None:
            self.collection = get_database().tasks
        return self.collection

    async def create_task(self, task: TaskCreate, user_id: str) -> TaskInDB:
        """Create a new task for a specific user"""
        try:
            collection = self._get_collection()
            task_data = task.model_dump()  # Utiliser model_dump au lieu de dict()
            task_data["created_at"] = datetime.utcnow()
            task_data["updated_at"] = datetime.utcnow()
            task_data["status"] = "todo"
            task_data["completed"] = False
            task_data["completed_at"] = None
            task_data["created_by"] = user_id  # Lier la tâche à l'utilisateur

            result = await collection.insert_one(task_data)

            # Get the created task
            created_task = await collection.find_one({"_id": result.inserted_id})
            task_in_db = TaskInDB(**fill_missing_fields(created_task))

            # Diffuser la création via WebSocket
            try:
                await notify_task_update(task_in_db.model_dump(), "create")
            except Exception as e:
                logger.warning(f"Erreur WebSocket broadcast création: {e}")

            return task_in_db

        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise

    async def get_user_tasks(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[TaskInDB]:
        """Get all tasks for a specific user"""
        try:
            collection = self._get_collection()
            filter_query = {"created_by": user_id}

            cursor = (
                collection.find(filter_query)
                .sort("created_at", -1)
                .skip(skip)
                .limit(limit)
            )
            tasks = await cursor.to_list(length=None)

            return [TaskInDB(**fill_missing_fields(task)) for task in tasks]

        except Exception as e:
            logger.error(f"Error getting user tasks: {e}")
            raise

    async def get_all_tasks(
        self, category: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[TaskInDB]:
        """Get all tasks with optional filtering"""
        try:
            collection = self._get_collection()
            filter_query = {}

            if category:
                filter_query["category"] = category
            if completed is not None:
                filter_query["completed"] = completed

            cursor = collection.find(filter_query).sort("created_at", -1)
            tasks = await cursor.to_list(length=None)

            return [TaskInDB(**fill_missing_fields(task)) for task in tasks]

        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            raise

    async def get_task_by_id(self, task_id: str) -> Optional[TaskInDB]:
        """Get a task by ID"""
        try:
            collection = self._get_collection()
            # Vérifier si l'ID est un ObjectId valide
            try:
                object_id = ObjectId(task_id)
            except Exception:
                # Si ce n'est pas un ObjectId valide, retourner None
                return None

            task = await collection.find_one({"_id": object_id})
            if task:
                return TaskInDB(**fill_missing_fields(task))
            return None

        except Exception as e:
            logger.error(f"Error getting task by ID: {e}")
            raise

    async def update_task(
        self, task_id: str, task_update: TaskUpdate
    ) -> Optional[TaskInDB]:
        """Update a task"""
        try:
            collection = self._get_collection()
            update_data = task_update.model_dump(
                exclude_unset=True
            )  # Utiliser model_dump
            update_data["updated_at"] = datetime.utcnow()

            # If marking as completed, set completed_at
            if task_update.completed and not update_data.get("completed_at"):
                update_data["completed_at"] = datetime.utcnow()
            elif task_update.completed is False:
                update_data["completed_at"] = None

            # Gérer le statut en fonction du completed
            if "status" in update_data:
                # Mapper "completed" vers "done" pour la compatibilité
                if update_data["status"] == "completed":
                    update_data["status"] = "done"

                # Mettre à jour completed et completed_at selon le statut
                if update_data["status"] == "done":
                    update_data["completed"] = True
                    if not update_data.get("completed_at"):
                        update_data["completed_at"] = datetime.utcnow()
                else:
                    update_data["completed"] = False
                    update_data["completed_at"] = None

            # Correction ultime : forcer la valeur string du status
            if "status" in update_data:
                s = update_data["status"]
                if hasattr(s, "value"):
                    update_data["status"] = s.value
                else:
                    update_data["status"] = str(s)
            print(f"🛠️ update_data envoyé à MongoDB: {update_data}")

            result = await collection.update_one(
                {"_id": ObjectId(task_id)}, {"$set": update_data}
            )

            if result.modified_count:
                updated_task = await self.get_task_by_id(task_id)
                if updated_task:
                    # Diffuser la mise à jour via WebSocket
                    try:
                        await notify_task_update(updated_task.model_dump(), "update")
                    except Exception as e:
                        logger.warning(f"Erreur WebSocket broadcast mise à jour: {e}")
                    return updated_task
            return None

        except Exception as e:
            logger.error(f"Error updating task: {e}")
            raise

    async def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        try:
            collection = self._get_collection()
            result = await collection.delete_one({"_id": ObjectId(task_id)})
            if result.deleted_count > 0:
                # Diffuser la suppression via WebSocket
                try:
                    await notify_task_update({"id": task_id}, "delete")
                except Exception as e:
                    logger.warning(f"Erreur WebSocket broadcast suppression: {e}")
            return result.deleted_count > 0

        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            raise

    async def toggle_task_completion(self, task_id: str) -> Optional[TaskInDB]:
        """Toggle task completion status"""
        try:
            collection = self._get_collection()
            task = await self.get_task_by_id(task_id)
            if not task:
                return None

            new_completed_status = not task.completed
            completed_at = datetime.utcnow() if new_completed_status else None

            result = await collection.update_one(
                {"_id": ObjectId(task_id)},
                {
                    "$set": {
                        "completed": new_completed_status,
                        "completed_at": completed_at,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            if result.modified_count:
                updated_task = await self.get_task_by_id(task_id)
                if updated_task:
                    # Diffuser la completion via WebSocket
                    try:
                        await notify_task_update(updated_task.model_dump(), "complete")
                    except Exception as e:
                        logger.warning(f"Erreur WebSocket broadcast completion: {e}")
                    return updated_task
            return None

        except Exception as e:
            logger.error(f"Error toggling task completion: {e}")
            raise

    async def get_task_stats(
        self,
    ) -> dict:  # Changed return type to dict as TaskStats model is removed
        """Get task statistics"""
        try:
            collection = self._get_collection()
            # Total tasks
            total_tasks = await collection.count_documents({})

            # Completed tasks
            completed_tasks = await collection.count_documents({"completed": True})

            # Pending tasks
            pending_tasks = total_tasks - completed_tasks

            # Completion rate
            completion_rate = (
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            )

            # Tasks by category
            pipeline_category = [
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            tasks_by_category_cursor = collection.aggregate(pipeline_category)
            tasks_by_category = {}
            async for doc in tasks_by_category_cursor:
                tasks_by_category[doc["_id"]] = doc["count"]

            # Tasks by priority
            pipeline_priority = [
                {"$group": {"_id": "$priority", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            tasks_by_priority_cursor = collection.aggregate(pipeline_priority)
            tasks_by_priority = {}
            async for doc in tasks_by_priority_cursor:
                tasks_by_priority[doc["_id"]] = doc["count"]

            return {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "completion_rate": round(completion_rate, 1),
                "tasks_by_category": tasks_by_category,
                "tasks_by_priority": tasks_by_priority,
            }

        except Exception as e:
            logger.error(f"Error getting task stats: {e}")
            raise

    async def bulk_delete_completed_tasks(self) -> int:
        """Delete all completed tasks"""
        try:
            collection = self._get_collection()
            result = await collection.delete_many({"completed": True})
            return result.deleted_count

        except Exception as e:
            logger.error(f"Error bulk deleting completed tasks: {e}")
            raise


# Create service instance
task_service = TaskService()


class DelegationService:
    def __init__(self):
        self.collection = None

    def _get_collection(self):
        if self.collection is None:
            self.collection = get_database().delegations
        return self.collection

    # Squelette pour les méthodes à venir (invite, accept, revoke, etc.)
    # async def invite_aidant(...):
    # async def accept_delegation(...):
    # async def revoke_delegation(...):

    async def invite_aidant(self, user_id: str, aidant_id: str):
        """Invite une personne aidante pour un utilisateur donné."""
        collection = self._get_collection()
        from models import DelegationInDB, DelegationStatusEnum
        from datetime import datetime
        from bson import ObjectId

        # Vérifier s'il existe déjà une délégation active
        existing = await collection.find_one(
            {
                "user_id": user_id,
                "aidant_id": aidant_id,
                "status": {
                    "$in": [DelegationStatusEnum.pending, DelegationStatusEnum.accepted]
                },
            }
        )
        if existing:
            raise Exception("Une délégation active existe déjà entre ces utilisateurs.")

        # Créer la délégation
        delegation_doc = {
            "user_id": user_id,
            "aidant_id": aidant_id,
            "status": DelegationStatusEnum.pending,
            "invited_at": datetime.utcnow(),
            "accepted_at": None,
            "revoked_at": None,
        }
        result = await collection.insert_one(delegation_doc)
        created = await collection.find_one({"_id": result.inserted_id})
        return DelegationInDB(**{**created, "_id": str(created["_id"])})

    async def accept_delegation(self, delegation_id: str, aidant_id: str):
        """Accepte une invitation de délégation (par l'aidant)."""
        collection = self._get_collection()
        from models import DelegationInDB, DelegationStatusEnum
        from datetime import datetime
        from bson import ObjectId

        delegation = await collection.find_one({"_id": ObjectId(delegation_id)})
        if not delegation:
            raise Exception("Délégation introuvable.")
        if delegation["aidant_id"] != aidant_id:
            raise Exception("Non autorisé à accepter cette délégation.")
        if delegation["status"] != DelegationStatusEnum.pending:
            raise Exception("La délégation n'est pas en attente.")

        await collection.update_one(
            {"_id": ObjectId(delegation_id)},
            {
                "$set": {
                    "status": DelegationStatusEnum.accepted,
                    "accepted_at": datetime.utcnow(),
                }
            },
        )
        updated = await collection.find_one({"_id": ObjectId(delegation_id)})
        return DelegationInDB(**{**updated, "_id": str(updated["_id"])})

    async def revoke_delegation(self, delegation_id: str, user_id: str):
        """Révoque une délégation (par l'utilisateur principal)."""
        collection = self._get_collection()
        from models import DelegationInDB, DelegationStatusEnum
        from datetime import datetime
        from bson import ObjectId

        delegation = await collection.find_one({"_id": ObjectId(delegation_id)})
        if not delegation:
            raise Exception("Délégation introuvable.")
        if delegation["user_id"] != user_id:
            raise Exception("Non autorisé à révoquer cette délégation.")
        if delegation["status"] == DelegationStatusEnum.revoked:
            raise Exception("La délégation est déjà révoquée.")

        await collection.update_one(
            {"_id": ObjectId(delegation_id)},
            {
                "$set": {
                    "status": DelegationStatusEnum.revoked,
                    "revoked_at": datetime.utcnow(),
                }
            },
        )
        updated = await collection.find_one({"_id": ObjectId(delegation_id)})
        return DelegationInDB(**{**updated, "_id": str(updated["_id"])})

    async def create_delegation(self, delegation_data):
        """Crée une nouvelle délégation avec nom, prénom, email, téléphone, user_id, aidant_id."""
        from database import get_database

        db = get_database()
        from models import DelegationInDB, DelegationStatusEnum, UserCreate
        from datetime import datetime
        from auth import get_password_hash

        collection = self._get_collection()

        # Chercher ou créer l'utilisateur aidant par email
        existing_aidant = await db.users.find_one({"email": delegation_data.email})
        if existing_aidant:
            aidant_id = str(existing_aidant["_id"])
        else:
            # Créer un utilisateur aidant avec un mot de passe temporaire
            username = f"aidant_{delegation_data.email.split('@')[0]}"
            password = get_password_hash("changeme123")
            user_doc = {
                "username": username,
                "email": delegation_data.email,
                "full_name": f"{delegation_data.prenom} {delegation_data.nom}",
                "hashed_password": password,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            result_user = await db.users.insert_one(user_doc)
            aidant_id = str(result_user.inserted_id)

        # user_id (celui qui délègue)
        user_id = delegation_data.user_id
        if not user_id:
            raise Exception("user_id (délégant) requis")

        # Créer la délégation
        doc = {
            "user_id": user_id,
            "aidant_id": aidant_id,
            "status": DelegationStatusEnum.pending,
            "invited_at": datetime.utcnow(),
            "accepted_at": None,
            "revoked_at": None,
            "nom": delegation_data.nom,
            "prenom": delegation_data.prenom,
            "email": delegation_data.email,
            "telephone": delegation_data.telephone,
        }
        result = await collection.insert_one(doc)
        created = await collection.find_one({"_id": result.inserted_id})
        return DelegationInDB(**{**created, "_id": str(created["_id"])})

    async def is_email_aidant(self, email: str) -> bool:
        """Vérifie si l'email correspond à un aidant accepté dans une délégation."""
        from database import get_database

        db = get_database()
        user = await db.users.find_one({"email": email})
        if not user:
            return False
        aidant_id = str(user["_id"])
        delegation = await self._get_collection().find_one(
            {"aidant_id": aidant_id, "status": "accepted"}
        )
        return delegation is not None

    async def get_delegations_for_aidant(self, aidant_id):
        """Retourne la liste des délégations où l'utilisateur est aidant."""
        collection = self._get_collection()
        cursor = collection.find({"aidant_id": str(aidant_id)})
        return [doc async for doc in cursor]
