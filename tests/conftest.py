#!/usr/bin/env python3
"""
Configuration pytest pour les tests d'intégration SyncTasks
Contient les fixtures communes utilisées par tous les tests
"""

import sys
import os
import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from main import app
from tests.test_database import connect_test_database, disconnect_test_database, get_test_database, cleanup_test_database

# ============================================================================
# FIXTURES COMMUNES
# ============================================================================

@pytest_asyncio.fixture(scope="session")
async def mongo_connection():
    """Connexion MongoDB partagée pour tous les tests"""
    # Configurer l'environnement pour utiliser mongomock
    os.environ["USE_MOCK_DB"] = "true"
    os.environ["DISABLE_WEBSOCKETS"] = "true"
    
    # Se connecter à la base de données de test (mongomock)
    await connect_test_database()
    
    yield
    
    # Fermer la connexion
    await disconnect_test_database()

@pytest_asyncio.fixture
async def async_client(mongo_connection):
    """Client de test asynchrone pour les tests d'intégration"""
    # Nettoyer la base de données avant chaque test
    await cleanup_test_database()
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Nettoyer après le test
    await cleanup_test_database()

@pytest.fixture
def sync_client(mongo_connection):
    """Client de test synchrone pour les tests simples"""
    return TestClient(app)

# ============================================================================
# FIXTURES DE DONNÉES DE TEST
# ============================================================================

@pytest.fixture
def sample_task_data():
    """Données de tâche d'exemple pour les tests"""
    return {
        "title": "Tâche de test",
        "category": "travail",
        "priority": "normale",
        "description": "Description de test"
    }

@pytest.fixture
def sample_tasks_data():
    """Liste de tâches d'exemple pour les tests"""
    return [
        {
            "title": "Tâche 1",
            "category": "travail",
            "priority": "haute",
            "description": "Tâche importante"
        },
        {
            "title": "Tâche 2",
            "category": "personnel",
            "priority": "normale",
            "description": "Tâche personnelle"
        },
        {
            "title": "Tâche 3",
            "category": "sante",
            "priority": "basse",
            "description": "Tâche de santé"
        }
    ]

@pytest.fixture
def sample_user_data():
    """Données utilisateur d'exemple pour les tests"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }

# ============================================================================
# FIXTURES DE NETTOYAGE
# ============================================================================

@pytest_asyncio.fixture(autouse=True)
async def cleanup_database(mongo_connection):
    """Nettoie la base de données après chaque test"""
    yield
    # Nettoyage après chaque test
    try:
        await cleanup_test_database()
    except Exception:
        pass  # Ignorer les erreurs de nettoyage

# ============================================================================
# FIXTURES DE CONFIGURATION
# ============================================================================

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configure l'environnement de test"""
    # Variables d'environnement pour les tests
    os.environ["USE_MOCK_DB"] = "true"  # Utiliser mongomock
    os.environ["DISABLE_WEBSOCKETS"] = "true"  # Désactiver les WebSockets en mode test
    os.environ["TESTING"] = "true"
    
    # Variables d'environnement pour les services externes (optionnelles)
    if not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = "test_key"
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "test_key"
    
    yield
    
    # Nettoyage après les tests
    if "TESTING" in os.environ:
        del os.environ["TESTING"]
    if "DISABLE_WEBSOCKETS" in os.environ:
        del os.environ["DISABLE_WEBSOCKETS"]
    if "USE_MOCK_DB" in os.environ:
        del os.environ["USE_MOCK_DB"]

# ============================================================================
# MARQUEURS PERSONNALISÉS
# ============================================================================

def pytest_configure(config):
    """Configure les marqueurs pytest personnalisés"""
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration"
    )
    config.addinivalue_line(
        "markers", "ai: marque les tests liés à l'IA"
    )
    config.addinivalue_line(
        "markers", "auth: marque les tests d'authentification"
    )
    config.addinivalue_line(
        "markers", "slow: marque les tests lents"
    )

# ============================================================================
# UTILITAIRES DE TEST
# ============================================================================

async def create_test_task(async_client, task_data=None):
    """Utilitaire pour créer une tâche de test"""
    if task_data is None:
        task_data = {
            "title": "Tâche de test",
            "category": "travail",
            "priority": "normale"
        }
    
    response = await async_client.post("/api/tasks/", json=task_data)
    assert response.status_code == 201
    return response.json()

async def create_test_tasks(async_client, tasks_data):
    """Utilitaire pour créer plusieurs tâches de test"""
    created_tasks = []
    for task_data in tasks_data:
        task = await create_test_task(async_client, task_data)
        created_tasks.append(task)
    return created_tasks

def assert_task_structure(task):
    """Utilitaire pour vérifier la structure d'une tâche"""
    required_fields = ["id", "title", "category", "priority", "completed", "created_at", "updated_at"]
    for field in required_fields:
        assert field in task, f"Champ manquant: {field}"
    
    # Vérifier les types
    assert isinstance(task["title"], str)
    assert isinstance(task["category"], str)
    assert isinstance(task["priority"], str)
    assert isinstance(task["completed"], bool)

def assert_api_response_structure(response_data):
    """Utilitaire pour vérifier la structure d'une réponse API"""
    if isinstance(response_data, dict):
        if "success" in response_data:
            assert isinstance(response_data["success"], bool)
        if "message" in response_data:
            assert isinstance(response_data["message"], str) 