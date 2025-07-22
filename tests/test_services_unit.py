"""
Tests unitaires pour les services SyncTasks
Ces tests ne dépendent pas de MongoDB et testent la logique métier
"""

import pytest
from datetime import datetime
from bson import ObjectId
from unittest.mock import Mock, AsyncMock, patch

# Import des services et modèles
from services import TaskService, fill_missing_fields
from models import TaskCreate, TaskUpdate, TaskInDB, PriorityEnum, CategoryEnum

# ============================================================================
# TESTS DE LA FONCTION fill_missing_fields
# ============================================================================

def test_fill_missing_fields_complete():
    """Test de fill_missing_fields avec des données complètes"""
    task_data = {
        "_id": ObjectId(),
        "title": "Test Task",
        "category": "travail",
        "priority": "haute",
        "description": "Test description",
        "completed": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = fill_missing_fields(task_data)
    
    assert result["id"] == str(task_data["_id"])
    assert result["title"] == task_data["title"]
    assert result["category"] == task_data["category"]
    assert result["priority"] == task_data["priority"]
    assert result["description"] == task_data["description"]
    assert result["completed"] == task_data["completed"]
    assert "created_at" in result
    assert "updated_at" in result

def test_fill_missing_fields_minimal():
    """Test de fill_missing_fields avec des données minimales"""
    task_data = {
        "_id": ObjectId(),
        "title": "Test Task",
        "category": "travail",
        "priority": "normale"
    }
    
    result = fill_missing_fields(task_data)
    
    assert result["id"] == str(task_data["_id"])
    assert result["title"] == task_data["title"]
    assert result["category"] == task_data["category"]
    assert result["priority"] == task_data["priority"]
    assert result["description"] == ""  # Doit être une chaîne vide, pas None
    assert result["completed"] == False
    assert "created_at" in result
    assert "updated_at" in result

def test_fill_missing_fields_with_id():
    """Test de fill_missing_fields avec un champ 'id' au lieu de '_id'"""
    task_data = {
        "id": str(ObjectId()),
        "title": "Test Task",
        "category": "personnel",
        "priority": "basse"
    }
    
    result = fill_missing_fields(task_data)
    
    assert result["id"] == task_data["id"]
    assert result["title"] == task_data["title"]
    assert result["category"] == task_data["category"]
    assert result["priority"] == task_data["priority"]

# ============================================================================
# TESTS DES MODÈLES PYDANTIC
# ============================================================================

def test_task_create_valid():
    """Test de création d'un TaskCreate valide"""
    task_data = {
        "title": "Test Task",
        "category": "travail",
        "priority": "haute",
        "description": "Test description"
    }
    
    task = TaskCreate(**task_data)
    
    assert task.title == "Test Task"
    assert task.category == CategoryEnum.travail
    assert task.priority == PriorityEnum.haute
    assert task.description == "Test description"

def test_task_create_invalid_category():
    """Test de création d'un TaskCreate avec catégorie invalide"""
    task_data = {
        "title": "Test Task",
        "category": "invalid_category",
        "priority": "haute"
    }
    
    with pytest.raises(ValueError):
        TaskCreate(**task_data)

def test_task_create_invalid_priority():
    """Test de création d'un TaskCreate avec priorité invalide"""
    task_data = {
        "title": "Test Task",
        "category": "travail",
        "priority": "invalid_priority"
    }
    
    with pytest.raises(ValueError):
        TaskCreate(**task_data)

def test_task_create_empty_title():
    """Test de création d'un TaskCreate avec titre vide"""
    task_data = {
        "title": "",
        "category": "travail",
        "priority": "haute"
    }
    
    with pytest.raises(ValueError):
        TaskCreate(**task_data)

# ============================================================================
# TESTS DU SERVICE TASK (AVEC MOCKS)
# ============================================================================

@pytest.fixture
def mock_collection():
    """Fixture pour mocker la collection MongoDB"""
    collection = Mock()
    collection.insert_one = AsyncMock()
    collection.find_one = AsyncMock()
    collection.find = AsyncMock()
    collection.update_one = AsyncMock()
    collection.delete_one = AsyncMock()
    collection.count_documents = AsyncMock()
    collection.aggregate = AsyncMock()
    return collection

@pytest.fixture
def task_service(mock_collection):
    """Fixture pour créer un TaskService avec une collection mockée"""
    service = TaskService()
    
    # Mock de la méthode _get_collection
    with patch.object(service, '_get_collection', return_value=mock_collection):
        yield service

@pytest.mark.asyncio
async def test_create_task_success(task_service, mock_collection):
    """Test de création réussie d'une tâche"""
    # Préparer les données
    task_create = TaskCreate(
        title="Test Task",
        category=CategoryEnum.travail,
        priority=PriorityEnum.haute,
        description="Test description"
    )
    
    # Mock de la réponse de MongoDB
    inserted_id = ObjectId()
    mock_collection.insert_one.return_value.inserted_id = inserted_id
    
    # Mock de find_one pour retourner la tâche créée
    created_task_data = {
        "_id": inserted_id,
        "title": "Test Task",
        "category": "travail",
        "priority": "haute",
        "description": "Test description",
        "completed": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    mock_collection.find_one.return_value = created_task_data
    
    # Exécuter le test
    result = await task_service.create_task(task_create)
    
    # Vérifications
    assert result is not None
    assert result.title == "Test Task"
    assert result.category == CategoryEnum.travail
    assert result.priority == PriorityEnum.haute
    assert result.description == "Test description"
    assert result.completed == False
    
    # Vérifier que insert_one a été appelé
    mock_collection.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_task_by_id_success(task_service, mock_collection):
    """Test de récupération réussie d'une tâche par ID"""
    # Préparer les données
    task_id = str(ObjectId())
    task_data = {
        "_id": ObjectId(task_id),
        "title": "Test Task",
        "category": "travail",
        "priority": "haute",
        "description": "Test description",
        "completed": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Mock de la réponse de MongoDB
    mock_collection.find_one.return_value = task_data
    
    # Exécuter le test
    result = await task_service.get_task_by_id(task_id)
    
    # Vérifications
    assert result is not None
    assert result.id == task_id
    assert result.title == "Test Task"
    
    # Vérifier que find_one a été appelé
    mock_collection.find_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_task_by_id_not_found(task_service, mock_collection):
    """Test de récupération d'une tâche inexistante"""
    # Préparer les données
    task_id = str(ObjectId())
    
    # Mock de la réponse de MongoDB (tâche non trouvée)
    mock_collection.find_one.return_value = None
    
    # Exécuter le test
    result = await task_service.get_task_by_id(task_id)
    
    # Vérifications
    assert result is None
    
    # Vérifier que find_one a été appelé
    mock_collection.find_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_task_by_id_invalid_format(task_service, mock_collection):
    """Test de récupération avec un ID invalide"""
    # Préparer les données
    invalid_task_id = "invalid_id"
    
    # Exécuter le test
    result = await task_service.get_task_by_id(invalid_task_id)
    
    # Vérifications
    assert result is None
    
    # Vérifier que find_one n'a pas été appelé (car l'ID est invalide)
    mock_collection.find_one.assert_not_called()

@pytest.mark.asyncio
async def test_get_all_tasks(task_service, mock_collection):
    """Test de récupération de toutes les tâches"""
    # Préparer les données
    tasks_data = [
        {
            "_id": ObjectId(),
            "title": "Task 1",
            "category": "travail",
            "priority": "haute",
            "completed": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "title": "Task 2",
            "category": "personnel",
            "priority": "normale",
            "completed": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Mock du curseur avec une méthode sort qui retourne le même curseur
    mock_cursor = Mock()
    mock_cursor.sort = Mock(return_value=mock_cursor)
    mock_cursor.to_list = AsyncMock(return_value=tasks_data)
    mock_collection.find.return_value = mock_cursor
    
    # Exécuter le test
    result = await task_service.get_all_tasks()
    
    # Vérifications
    assert len(result) == 2
    assert result[0].title == "Task 1"
    assert result[1].title == "Task 2"
    
    # Vérifier que find a été appelé
    mock_collection.find.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_tasks_with_filter(task_service, mock_collection):
    """Test de récupération de tâches avec filtres"""
    # Préparer les données
    tasks_data = [
        {
            "_id": ObjectId(),
            "title": "Task 1",
            "category": "travail",
            "priority": "haute",
            "completed": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Mock du curseur avec une méthode sort qui retourne le même curseur
    mock_cursor = Mock()
    mock_cursor.sort = Mock(return_value=mock_cursor)
    mock_cursor.to_list = AsyncMock(return_value=tasks_data)
    mock_collection.find.return_value = mock_cursor
    
    # Exécuter le test avec filtre par catégorie
    result = await task_service.get_all_tasks(category="travail")
    
    # Vérifications
    assert len(result) == 1
    assert result[0].category == CategoryEnum.travail
    
    # Vérifier que find a été appelé avec le bon filtre
    mock_collection.find.assert_called_once()

@pytest.mark.asyncio
async def test_update_task_success(task_service, mock_collection):
    """Test de mise à jour réussie d'une tâche"""
    # Préparer les données
    task_id = str(ObjectId())
    task_update = TaskUpdate(title="Updated Task")
    
    # Mock de la réponse de MongoDB
    mock_collection.update_one.return_value.modified_count = 1
    
    # Mock de get_task_by_id pour retourner la tâche mise à jour
    updated_task_data = {
        "_id": ObjectId(task_id),
        "title": "Updated Task",
        "category": "travail",
        "priority": "haute",
        "completed": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    mock_collection.find_one.return_value = updated_task_data
    
    # Exécuter le test
    result = await task_service.update_task(task_id, task_update)
    
    # Vérifications
    assert result is not None
    assert result.title == "Updated Task"
    
    # Vérifier que update_one a été appelé
    mock_collection.update_one.assert_called_once()

@pytest.mark.asyncio
async def test_delete_task_success(task_service, mock_collection):
    """Test de suppression réussie d'une tâche"""
    # Préparer les données
    task_id = str(ObjectId())
    
    # Mock de la réponse de MongoDB
    mock_collection.delete_one.return_value.deleted_count = 1
    
    # Exécuter le test
    result = await task_service.delete_task(task_id)
    
    # Vérifications
    assert result == True
    
    # Vérifier que delete_one a été appelé
    mock_collection.delete_one.assert_called_once()

@pytest.mark.asyncio
async def test_delete_task_not_found(task_service, mock_collection):
    """Test de suppression d'une tâche inexistante"""
    # Préparer les données
    task_id = str(ObjectId())
    
    # Mock de la réponse de MongoDB (tâche non trouvée)
    mock_collection.delete_one.return_value.deleted_count = 0
    
    # Exécuter le test
    result = await task_service.delete_task(task_id)
    
    # Vérifications
    assert result == False
    
    # Vérifier que delete_one a été appelé
    mock_collection.delete_one.assert_called_once()

@pytest.mark.asyncio
async def test_toggle_task_completion(task_service, mock_collection):
    """Test de basculement du statut de complétion"""
    # Préparer les données
    task_id = str(ObjectId())
    
    # Mock de get_task_by_id pour retourner une tâche non terminée
    task_data = {
        "_id": ObjectId(task_id),
        "title": "Test Task",
        "category": "travail",
        "priority": "haute",
        "completed": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    mock_collection.find_one.return_value = task_data
    
    # Mock de la réponse de MongoDB
    mock_collection.update_one.return_value.modified_count = 1
    
    # Mock de get_task_by_id après mise à jour pour retourner la tâche terminée
    updated_task_data = {
        "_id": ObjectId(task_id),
        "title": "Test Task",
        "category": "travail",
        "priority": "haute",
        "completed": True,  # Maintenant terminée
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Configurer find_one pour retourner des valeurs différentes selon l'appel
    mock_collection.find_one.side_effect = [task_data, updated_task_data]
    
    # Exécuter le test
    result = await task_service.toggle_task_completion(task_id)
    
    # Vérifications
    assert result is not None
    assert result.completed == True
    
    # Vérifier que update_one a été appelé
    mock_collection.update_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_task_stats(task_service, mock_collection):
    """Test de récupération des statistiques des tâches"""
    # Mock des réponses de MongoDB
    mock_collection.count_documents.side_effect = [10, 3]  # total_tasks, completed_tasks
    
    # Mock de l'agrégation avec des curseurs itérables
    mock_cursor_category = Mock()
    mock_cursor_category.__aiter__ = Mock(return_value=iter([
        {"_id": "travail", "count": 5},
        {"_id": "personnel", "count": 3},
        {"_id": "sante", "count": 2}
    ]))
    mock_cursor_priority = Mock()
    mock_cursor_priority.__aiter__ = Mock(return_value=iter([
        {"_id": "haute", "count": 4},
        {"_id": "normale", "count": 4},
        {"_id": "basse", "count": 2}
    ]))
    mock_collection.aggregate.side_effect = [mock_cursor_category, mock_cursor_priority]
    
    # Exécuter le test
    result = await task_service.get_task_stats()
    
    # Vérifications
    assert result["total_tasks"] == 10
    assert result["completed_tasks"] == 3
    assert result["pending_tasks"] == 7
    assert result["completion_rate"] == 30.0
    assert "tasks_by_category" in result
    assert "tasks_by_priority" in result
    
    # Vérifier que count_documents a été appelé
    assert mock_collection.count_documents.call_count == 2 