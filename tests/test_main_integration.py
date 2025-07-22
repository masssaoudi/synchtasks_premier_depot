#!/usr/bin/env python3
"""
Tests d'intégration pour SyncTasks API
Teste la synchronisation et la logique de basculement entre les pages
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app
from database import connect_to_mongo, close_mongo_connection

@pytest_asyncio.fixture
async def mongo_connection():
    await connect_to_mongo()
    yield
    await close_mongo_connection()

@pytest_asyncio.fixture
async def async_client(mongo_connection):
    """Client de test asynchrone pour les tests d'intégration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def sync_client(mongo_connection):
    """Client de test synchrone pour les tests simples"""
    return TestClient(app)

# ============================================================================
# TESTS DE SYNCHRONISATION DES DONNÉES
# ============================================================================

@pytest.mark.asyncio
async def test_debug_response_structure(async_client):
    """Test de debug pour voir la structure de la réponse"""
    
    # Créer une tâche simple
    task_data = {
        "title": "Debug Test",
        "category": "travail",
        "priority": "normale"
    }
    
    create_response = await async_client.post("/api/tasks/", json=task_data)
    print(f"Status Code: {create_response.status_code}")
    print(f"Response: {create_response.json()}")
    
    if create_response.status_code == 201:
        response_data = create_response.json()
        print(f"Keys in response: {list(response_data.keys())}")
        assert "id" in response_data or "_id" in response_data

@pytest.mark.asyncio
async def test_basic_task_operations(async_client):
    """Test basique des opérations CRUD sur les tâches"""
    
    # 1. Créer une tâche
    task_data = {
        "title": "Tâche de test basique",
        "category": "travail",
        "priority": "normale"
    }
    
    create_response = await async_client.post("/api/tasks/", json=task_data)
    assert create_response.status_code == 201
    created_task = create_response.json()
    
    # Vérifier que la tâche a un ID
    task_id = created_task.get("id") or created_task.get("_id")
    assert task_id is not None
    
    # 2. Récupérer la tâche
    get_response = await async_client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["title"] == "Tâche de test basique"
    
    # 3. Modifier la tâche
    update_data = {"title": "Tâche modifiée"}
    update_response = await async_client.put(f"/api/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 200
    
    # 4. Vérifier la modification
    get_response = await async_client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 200
    updated_task = get_response.json()
    assert updated_task["title"] == "Tâche modifiée"
    
    # 5. Supprimer la tâche
    delete_response = await async_client.delete(f"/api/tasks/{task_id}")
    assert delete_response.status_code == 200

@pytest.mark.asyncio
async def test_task_listing(async_client):
    """Test de la liste des tâches"""
    
    # Créer quelques tâches
    tasks_data = [
        {"title": "Tâche 1", "category": "travail", "priority": "haute"},
        {"title": "Tâche 2", "category": "personnel", "priority": "normale"}
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        response = await async_client.post("/api/tasks/", json=task_data)
        if response.status_code == 201:
            created_tasks.append(response.json())
    
    # Récupérer la liste des tâches
    list_response = await async_client.get("/api/tasks/")
    assert list_response.status_code == 200
    tasks = list_response.json()
    
    # Vérifier que les tâches sont présentes
    assert len(tasks) >= len(created_tasks)
    
    # Nettoyer
    for task in created_tasks:
        task_id = task.get("id") or task.get("_id")
        if task_id:
            await async_client.delete(f"/api/tasks/{task_id}")

@pytest.mark.asyncio
async def test_task_validation_basic(async_client):
    """Test basique de validation des tâches"""
    
    # Test avec titre vide
    invalid_task = {
        "title": "",
        "category": "travail",
        "priority": "normale"
    }
    response = await async_client.post("/api/tasks/", json=invalid_task)
    assert response.status_code == 422
    
    # Test avec catégorie invalide
    invalid_task = {
        "title": "Test",
        "category": "invalid_category",
        "priority": "normale"
    }
    response = await async_client.post("/api/tasks/", json=invalid_task)
    assert response.status_code == 422
    
    # Test avec priorité invalide
    invalid_task = {
        "title": "Test",
        "category": "travail",
        "priority": "invalid_priority"
    }
    response = await async_client.post("/api/tasks/", json=invalid_task)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_health_endpoints_simple(async_client):
    """Test simple des endpoints de santé"""
    
    # Test de l'endpoint principal
    root_response = await async_client.get("/")
    assert root_response.status_code == 200
    root_data = root_response.json()
    assert "message" in root_data
    
    # Test de l'endpoint de santé des tâches
    health_response = await async_client.get("/api/tasks/health")
    assert health_response.status_code == 200
    health_data = health_response.json()
    assert health_data["success"] == True

@pytest.mark.asyncio
async def test_task_statistics(async_client):
    """Test des statistiques des tâches"""
    
    # Créer quelques tâches pour tester les statistiques
    tasks_data = [
        {"title": "Stat Test 1", "category": "travail", "priority": "haute"},
        {"title": "Stat Test 2", "category": "personnel", "priority": "normale"},
        {"title": "Stat Test 3", "category": "sante", "priority": "basse"}
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        response = await async_client.post("/api/tasks/", json=task_data)
        if response.status_code == 201:
            created_tasks.append(response.json())
    
    # Vérifier les statistiques
    stats_response = await async_client.get("/api/tasks/stats/overview")
    assert stats_response.status_code == 200
    stats = stats_response.json()
    
    # Vérifier que les statistiques sont cohérentes
    assert stats["total_tasks"] >= len(created_tasks)
    assert "completed_tasks" in stats
    assert "pending_tasks" in stats
    assert "completion_rate" in stats
    
    # Nettoyer
    for task in created_tasks:
        task_id = task.get("id") or task.get("_id")
        if task_id:
            await async_client.delete(f"/api/tasks/{task_id}")

@pytest.mark.asyncio
async def test_task_toggle_completion(async_client):
    """Test du basculement de statut des tâches"""
    
    # Créer une tâche
    task_data = {
        "title": "Test Toggle",
        "category": "travail",
        "priority": "normale"
    }
    
    create_response = await async_client.post("/api/tasks/", json=task_data)
    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task.get("id") or created_task.get("_id")
    
    # Vérifier l'état initial
    assert created_task["completed"] == False
    
    # Basculer vers terminé
    toggle_response = await async_client.patch(f"/api/tasks/{task_id}/toggle")
    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["completed"] == True
    
    # Basculer vers non terminé
    toggle_response2 = await async_client.patch(f"/api/tasks/{task_id}/toggle")
    assert toggle_response2.status_code == 200
    untoggled_task = toggle_response2.json()
    assert untoggled_task["completed"] == False
    
    # Nettoyer
    await async_client.delete(f"/api/tasks/{task_id}")

@pytest.mark.asyncio
async def test_error_handling(async_client):
    """Test de la gestion d'erreurs"""
    
    # Test d'accès à une tâche inexistante
    response = await async_client.get("/api/tasks/nonexistent_id")
    assert response.status_code == 404
    
    # Test de mise à jour d'une tâche inexistante
    update_response = await async_client.put("/api/tasks/nonexistent_id", json={"title": "Test"})
    assert update_response.status_code == 404
    
    # Test de suppression d'une tâche inexistante
    delete_response = await async_client.delete("/api/tasks/nonexistent_id")
    assert delete_response.status_code == 404 