import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import logging

from database import get_database
from models import TaskCreate, TaskInDB, TaskUpdate, CategoryEnum, PriorityEnum
from ws_manager import broadcast_task_created, broadcast_task_updated, broadcast_task_deleted, broadcast_task_completed

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
            
            # Diffuser la création via WebSocket (désactivé en mode test)
            try:
                await broadcast_task_created(task_data)
            except Exception as e:
                # Ignorer les erreurs WebSocket en mode test
                pass
            
            return task_in_db
            
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise

    async def get_user_tasks(self, user_id: str, skip: int = 0, limit: int = 100) -> List[TaskInDB]:
        """Get all tasks for a specific user"""
        try:
            collection = self._get_collection()
            filter_query = {"created_by": user_id}
            
            cursor = collection.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
            tasks = await cursor.to_list(length=None)
            
            return [TaskInDB(**fill_missing_fields(task)) for task in tasks]
            
        except Exception as e:
            logger.error(f"Error getting user tasks: {e}")
            raise

    async def get_all_tasks(self, category: Optional[str] = None, completed: Optional[bool] = None) -> List[TaskInDB]:
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

    async def update_task(self, task_id: str, task_update: TaskUpdate) -> Optional[TaskInDB]:
        """Update a task"""
        try:
            collection = self._get_collection()
            update_data = task_update.model_dump(exclude_unset=True)  # Utiliser model_dump
            update_data["updated_at"] = datetime.utcnow()
            
            # If marking as completed, set completed_at
            if task_update.completed and not update_data.get("completed_at"):
                update_data["completed_at"] = datetime.utcnow()
            elif task_update.completed is False:
                update_data["completed_at"] = None
            
            # Gérer le statut en fonction du completed
            if "status" in update_data:
                if update_data["status"] == "done":
                    update_data["completed"] = True
                    if not update_data.get("completed_at"):
                        update_data["completed_at"] = datetime.utcnow()
                else:
                    update_data["completed"] = False
                    update_data["completed_at"] = None
            
            result = await collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                updated_task = await self.get_task_by_id(task_id)
                if updated_task:
                    # Diffuser la mise à jour via WebSocket (désactivé en mode test)
                    try:
                        await broadcast_task_updated(updated_task.model_dump())
                    except Exception as e:
                        # Ignorer les erreurs WebSocket en mode test
                        pass
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
                # Diffuser la suppression via WebSocket (désactivé en mode test)
                try:
                    await broadcast_task_deleted(task_id)
                except Exception as e:
                    # Ignorer les erreurs WebSocket en mode test
                    pass
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
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count:
                updated_task = await self.get_task_by_id(task_id)
                if updated_task:
                    # Diffuser la completion via WebSocket (désactivé en mode test)
                    try:
                        await broadcast_task_completed(updated_task.model_dump())
                    except Exception as e:
                        # Ignorer les erreurs WebSocket en mode test
                        pass
                    return updated_task
            return None
                
        except Exception as e:
            logger.error(f"Error toggling task completion: {e}")
            raise

    async def get_task_stats(self) -> dict: # Changed return type to dict as TaskStats model is removed
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
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # Tasks by category
            pipeline_category = [
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            tasks_by_category_cursor = collection.aggregate(pipeline_category)
            tasks_by_category = {}
            async for doc in tasks_by_category_cursor:
                tasks_by_category[doc["_id"]] = doc["count"]
            
            # Tasks by priority
            pipeline_priority = [
                {"$group": {"_id": "$priority", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
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
                "tasks_by_priority": tasks_by_priority
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