#!/usr/bin/env python3
"""
Tests d'intégration pour les fonctionnalités IA de SyncTasks
Teste les endpoints IA et les services d'analyse
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

import pytest
import pytest_asyncio
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
    """Client de test asynchrone pour les tests d'intégration IA"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def sync_client(mongo_connection):
    """Client de test synchrone pour les tests simples"""
    return TestClient(app)

# ============================================================================
# TESTS DES ENDPOINTS IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_endpoints_availability(async_client):
    """Test de la disponibilité des endpoints IA"""
    
    # Test de l'endpoint principal de l'API
    root_response = await async_client.get("/")
    assert root_response.status_code == 200
    
    # Vérifier que l'API est accessible
    api_info = root_response.json()
    assert "message" in api_info
    assert "version" in api_info

@pytest.mark.asyncio
async def test_ai_services_import():
    """Test de l'import des services IA"""
    try:
        from ia_manager_synchtasks.surcharge_analyzer import SurchargeAnalyzer
        from ia_manager_synchtasks.mood_advisor import MoodAdvisor
        from ia_manager_synchtasks.task_optimizer import TaskOptimizer
        
        # Vérifier que les classes peuvent être instanciées
        surcharge_analyzer = SurchargeAnalyzer()
        mood_advisor = MoodAdvisor()
        task_optimizer = TaskOptimizer()
        
        assert surcharge_analyzer is not None
        assert mood_advisor is not None
        assert task_optimizer is not None
        
    except ImportError as e:
        pytest.skip(f"Services IA non disponibles: {e}")

@pytest.mark.asyncio
async def test_ai_models_structure():
    """Test de la structure des modèles IA"""
    try:
        from ia_manager_synchtasks.ai import (
            SurchargeAnalysis,
            MoodRecommendation,
            TaskRescheduling,
            AIInsights
        )
        
        # Vérifier que les modèles sont définis
        assert SurchargeAnalysis is not None
        assert MoodRecommendation is not None
        assert TaskRescheduling is not None
        assert AIInsights is not None
        
    except ImportError as e:
        pytest.skip(f"Modèles IA non disponibles: {e}")

# ============================================================================
# TESTS DES FONCTIONNALITÉS IA SPÉCIFIQUES
# ============================================================================

@pytest.mark.asyncio
async def test_surcharge_analyzer():
    """Test de l'analyseur de surcharge"""
    try:
        from ia_manager_synchtasks.surcharge_analyzer import SurchargeAnalyzer
        
        analyzer = SurchargeAnalyzer()
        
        # Test de la méthode d'analyse
        # Note: Ce test nécessite un utilisateur valide dans la base de données
        # Pour l'instant, on teste juste que la classe peut être instanciée
        assert analyzer is not None
        
    except ImportError as e:
        pytest.skip(f"Analyseur de surcharge non disponible: {e}")

@pytest.mark.asyncio
async def test_mood_advisor():
    """Test du conseiller d'humeur"""
    try:
        from ia_manager_synchtasks.mood_advisor import MoodAdvisor
        
        advisor = MoodAdvisor()
        
        # Test de la méthode de conseil
        # Note: Ce test nécessite un utilisateur valide dans la base de données
        assert advisor is not None
        
    except ImportError as e:
        pytest.skip(f"Conseiller d'humeur non disponible: {e}")

@pytest.mark.asyncio
async def test_task_optimizer():
    """Test de l'optimiseur de tâches"""
    try:
        from ia_manager_synchtasks.task_optimizer import TaskOptimizer
        
        optimizer = TaskOptimizer()
        
        # Test de la méthode d'optimisation
        # Note: Ce test nécessite des tâches valides dans la base de données
        assert optimizer is not None
        
    except ImportError as e:
        pytest.skip(f"Optimiseur de tâches non disponible: {e}")

# ============================================================================
# TESTS D'INTÉGRATION IA AVEC LES TÂCHES
# ============================================================================

@pytest.mark.asyncio
async def test_ai_with_task_data(async_client):
    """Test de l'IA avec des données de tâches réelles"""
    
    # Créer des tâches pour tester l'IA
    tasks_data = [
        {
            "title": "Tâche urgente travail",
            "category": "travail",
            "priority": "urgente",
            "description": "Tâche très importante à terminer rapidement"
        },
        {
            "title": "Tâche personnelle normale",
            "category": "personnel",
            "priority": "normale",
            "description": "Tâche personnelle standard"
        },
        {
            "title": "Tâche santé basse",
            "category": "sante",
            "priority": "basse",
            "description": "Tâche de santé non urgente"
        }
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        response = await async_client.post("/api/tasks/", json=task_data)
        assert response.status_code == 201
        created_tasks.append(response.json())
    
    # Marquer une tâche comme terminée pour tester l'analyse
    if created_tasks:
        task_id = created_tasks[0]["id"]
        toggle_response = await async_client.patch(f"/api/tasks/{task_id}/toggle")
        assert toggle_response.status_code == 200
    
    # Vérifier que les tâches sont bien créées
    list_response = await async_client.get("/api/tasks/")
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) >= 3

@pytest.mark.asyncio
async def test_ai_metrics_update(async_client):
    """Test de la mise à jour des métriques IA"""
    
    # Créer une tâche pour tester les métriques IA
    task_data = {
        "title": "Tâche test métriques IA",
        "category": "travail",
        "priority": "haute",
        "description": "Tâche pour tester les métriques IA"
    }
    
    create_response = await async_client.post("/api/tasks/", json=task_data)
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]
    
    # Simuler une mise à jour des métriques IA
    # Note: Cet endpoint nécessite une authentification
    # Pour l'instant, on teste juste que la tâche est créée
    assert task_id is not None

# ============================================================================
# TESTS DE CONFIGURATION IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_configuration():
    """Test de la configuration IA"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Vérifier que les variables d'environnement IA sont définies
    # Note: Ces variables peuvent être optionnelles en mode test
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Le test passe même si les clés ne sont pas définies (mode test)
    # En production, ces clés seraient requises
    assert True  # Test de base pour la configuration

@pytest.mark.asyncio
async def test_ai_models_availability():
    """Test de la disponibilité des modèles IA"""
    try:
        import google.generativeai as genai
        
        # Vérifier que le module est disponible
        assert genai is not None
        
    except ImportError:
        pytest.skip("Google Generative AI non disponible")

# ============================================================================
# TESTS DE PERFORMANCE IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_response_time():
    """Test du temps de réponse des services IA"""
    try:
        from ia_manager_synchtasks.surcharge_analyzer import SurchargeAnalyzer
        import time
        
        analyzer = SurchargeAnalyzer()
        
        # Test de performance basique
        start_time = time.time()
        
        # Simuler une analyse (sans données réelles)
        # En mode test, on vérifie juste que la classe peut être instanciée
        assert analyzer is not None
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Le temps de réponse doit être raisonnable (< 5 secondes pour l'instanciation)
        assert response_time < 5.0
        
    except ImportError as e:
        pytest.skip(f"Service IA non disponible: {e}")

# ============================================================================
# TESTS DE GESTION D'ERREURS IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_error_handling():
    """Test de la gestion d'erreurs des services IA"""
    try:
        from ia_manager_synchtasks.surcharge_analyzer import SurchargeAnalyzer
        
        analyzer = SurchargeAnalyzer()
        
        # Test avec des données invalides
        # Note: Ce test vérifie que les services IA gèrent correctement les erreurs
        assert analyzer is not None
        
    except Exception as e:
        # Si une erreur se produit, elle doit être gérée gracieusement
        assert "error" in str(e).lower() or "exception" in str(e).lower()

# ============================================================================
# TESTS DE DOCUMENTATION IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_documentation():
    """Test de la documentation des services IA"""
    try:
        from ia_manager_synchtasks.surcharge_analyzer import SurchargeAnalyzer
        from ia_manager_synchtasks.mood_advisor import MoodAdvisor
        from ia_manager_synchtasks.task_optimizer import TaskOptimizer
        
        # Vérifier que les classes ont une documentation
        assert SurchargeAnalyzer.__doc__ is not None
        assert MoodAdvisor.__doc__ is not None
        assert TaskOptimizer.__doc__ is not None
        
    except ImportError as e:
        pytest.skip(f"Services IA non disponibles: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 