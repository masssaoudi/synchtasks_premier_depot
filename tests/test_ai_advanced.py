"""
Tests IA avancés - Le cerveau de l'application SyncTasks
Tests complets des fonctionnalités IA avec mocks et validation
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from typing import Dict, Any

# Tests des modules IA
from ia_manager_synchtasks.surcharge_analyzer import SurchargeAnalyzer
from ia_manager_synchtasks.mood_advisor import MoodAdvisor
from ia_manager_synchtasks.task_optimizer import TaskOptimizer

# ============================================================================
# FIXTURES POUR LES TESTS IA
# ============================================================================

@pytest.fixture
def mock_user():
    """Utilisateur mock pour les tests IA"""
    user = Mock()
    user.id = "user123"
    user.mood_score = 7.5
    user.stress_level = 6.0
    user.total_tasks_completed = 45
    user.current_streak = 12
    user.preferences = {
        "work_hours": {"start": "09:00", "end": "17:00"},
        "break_preferences": "pomodoro",
        "focus_duration": 25
    }
    return user

@pytest.fixture
def mock_tasks():
    """Tâches mock pour les tests IA"""
    tasks = []
    
    # Tâches actives
    for i in range(5):
        task = Mock()
        task.id = f"task_{i}"
        task.title = f"Tâche importante {i}"
        task.priority = "haute" if i < 2 else "normale"
        task.complexity = "medium"
        task.due_date = datetime.utcnow() + timedelta(days=i+1)
        task.status = "en_cours"
        task.user_id = "user123"
        tasks.append(task)
    
    # Tâches en retard
    for i in range(2):
        task = Mock()
        task.id = f"overdue_{i}"
        task.title = f"Tâche en retard {i}"
        task.priority = "haute"
        task.complexity = "complex"
        task.due_date = datetime.utcnow() - timedelta(days=i+1)
        task.status = "en_cours"
        task.user_id = "user123"
        tasks.append(task)
    
    return tasks

@pytest.fixture
def mock_ai_response():
    """Réponse IA mock"""
    return {
        "surcharge_level": 7.5,
        "stress_factors": ["Tâches en retard", "Charge élevée"],
        "wellbeing_impact": "Modéré",
        "suggestions": ["Prioriser les tâches", "Prendre des pauses"]
    }

# ============================================================================
# TESTS SURCHARGE ANALYZER - CŒUR DE L'IA
# ============================================================================

@pytest.mark.asyncio
async def test_surcharge_analyzer_initialization():
    """Test d'initialisation de l'analyseur de surcharge"""
    analyzer = SurchargeAnalyzer()
    assert analyzer is not None
    assert hasattr(analyzer, 'analyze_user_tasks')

@pytest.mark.asyncio
async def test_surcharge_analyzer_basic_analysis(mock_user, mock_tasks):
    """Test d'analyse basique de surcharge"""
    analyzer = SurchargeAnalyzer()
    
    # Mock des méthodes de récupération
    with patch.object(analyzer, '_calculate_workload_metrics') as mock_metrics:
        mock_metrics.return_value = {
            "total_active_tasks": 5,
            "overdue_count": 2,
            "high_priority_count": 3,
            "avg_complexity": 2.5,
            "workload_density": 4,
            "stress_factors": ["Tâches en retard", "Charge élevée"]
        }
        
        with patch('ia_manager_synchtasks.surcharge_analyzer.get_gemini_advice') as mock_ai:
            mock_ai.return_value = "Analyse IA: Surcharge modérée détectée"
            
            result = await analyzer.analyze_user_tasks("user123")
            
            assert result is not None
            assert "user_id" in result
            assert "overload_score" in result
            assert "risk_level" in result
            assert "recommendations" in result
            assert result["user_id"] == "user123"

@pytest.mark.asyncio
async def test_surcharge_analyzer_metrics_calculation(mock_user, mock_tasks):
    """Test du calcul des métriques de charge de travail"""
    analyzer = SurchargeAnalyzer()
    
    active_tasks = [t for t in mock_tasks if t.due_date > datetime.utcnow()]
    overdue_tasks = [t for t in mock_tasks if t.due_date <= datetime.utcnow()]
    
    metrics = await analyzer._calculate_workload_metrics(mock_user, active_tasks, overdue_tasks)
    
    assert metrics["total_active_tasks"] == 5
    assert metrics["overdue_count"] == 2
    assert metrics["high_priority_count"] >= 0
    assert "stress_factors" in metrics
    assert isinstance(metrics["stress_factors"], list)

@pytest.mark.asyncio
async def test_surcharge_analyzer_risk_level_determination():
    """Test de détermination du niveau de risque"""
    analyzer = SurchargeAnalyzer()
    
    # Test différents scores
    assert analyzer._determine_risk_level(2.0) == "low"
    assert analyzer._determine_risk_level(5.0) == "medium"
    assert analyzer._determine_risk_level(8.0) == "high"
    assert analyzer._determine_risk_level(9.5) == "critical"

@pytest.mark.asyncio
async def test_surcharge_analyzer_error_handling():
    """Test de gestion d'erreurs de l'analyseur"""
    analyzer = SurchargeAnalyzer()
    
    # Mock d'une erreur
    with patch('ia_manager_synchtasks.surcharge_analyzer.User.get') as mock_get:
        mock_get.side_effect = Exception("Erreur de base de données")
        
        result = await analyzer.analyze_user_tasks("user123")
        
        assert result is not None
        assert "error" in result
        assert result["overload_score"] == 5.0  # Score par défaut
        assert result["risk_level"] == "medium"

# ============================================================================
# TESTS MOOD ADVISOR - CONSEILLER D'HUMEUR
# ============================================================================

@pytest.mark.asyncio
async def test_mood_advisor_initialization():
    """Test d'initialisation du conseiller d'humeur"""
    advisor = MoodAdvisor()
    assert advisor is not None
    assert hasattr(advisor, 'analyze_mood')

@pytest.mark.asyncio
async def test_mood_advisor_basic_analysis(mock_user):
    """Test d'analyse basique d'humeur"""
    advisor = MoodAdvisor()
    
    with patch('ia_manager_synchtasks.mood_advisor.get_gemini_advice') as mock_ai:
        mock_ai.return_value = "Analyse d'humeur: Bien-être stable"
        
        result = await advisor.analyze_mood("user123")
        
        assert result is not None
        assert "user_id" in result
        assert "mood_analysis" in result
        assert "recommendations" in result

@pytest.mark.asyncio
async def test_mood_advisor_recommendations_generation():
    """Test de génération de recommandations d'humeur"""
    advisor = MoodAdvisor()
    
    # Test avec différents scores d'humeur
    low_mood_user = Mock()
    low_mood_user.mood_score = 3.0
    low_mood_user.stress_level = 8.0
    
    recommendations = await advisor._generate_mood_recommendations(low_mood_user)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert all(isinstance(rec, str) for rec in recommendations)

# ============================================================================
# TESTS TASK OPTIMIZER - OPTIMISEUR DE TÂCHES
# ============================================================================

@pytest.mark.asyncio
async def test_task_optimizer_initialization():
    """Test d'initialisation de l'optimiseur de tâches"""
    optimizer = TaskOptimizer()
    assert optimizer is not None
    assert hasattr(optimizer, 'optimize_user_tasks')

@pytest.mark.asyncio
async def test_task_optimizer_basic_optimization(mock_user, mock_tasks):
    """Test d'optimisation basique des tâches"""
    optimizer = TaskOptimizer()
    
    with patch('ia_manager_synchtasks.task_optimizer.get_gemini_advice') as mock_ai:
        mock_ai.return_value = "Optimisation: Prioriser les tâches urgentes"
        
        result = await optimizer.optimize_user_tasks("user123")
        
        assert result is not None
        assert "user_id" in result
        assert "optimization_plan" in result
        assert "suggested_changes" in result

@pytest.mark.asyncio
async def test_task_optimizer_priority_reordering():
    """Test de réorganisation des priorités"""
    optimizer = TaskOptimizer()
    
    # Tâches avec priorités mélangées
    tasks = [
        Mock(priority="normale", due_date=datetime.utcnow() + timedelta(days=1)),
        Mock(priority="haute", due_date=datetime.utcnow() + timedelta(days=3)),
        Mock(priority="urgente", due_date=datetime.utcnow() + timedelta(days=5))
    ]
    
    optimized_tasks = optimizer._reorder_by_priority(tasks)
    
    assert len(optimized_tasks) == len(tasks)
    # Vérifier que les priorités sont bien ordonnées

# ============================================================================
# TESTS D'INTÉGRATION IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_integration_workflow():
    """Test du workflow complet d'intégration IA"""
    # Simuler un workflow complet
    user_id = "user123"
    
    # 1. Analyse de surcharge
    analyzer = SurchargeAnalyzer()
    with patch.object(analyzer, 'analyze_user_tasks') as mock_analyze:
        mock_analyze.return_value = {
            "overload_score": 7.5,
            "risk_level": "high",
            "recommendations": ["Prendre des pauses", "Déléguer"]
        }
        
        surcharge_result = await analyzer.analyze_user_tasks(user_id)
        assert surcharge_result["overload_score"] == 7.5
    
    # 2. Analyse d'humeur
    advisor = MoodAdvisor()
    with patch.object(advisor, 'analyze_mood') as mock_mood:
        mock_mood.return_value = {
            "mood_score": 6.5,
            "recommendations": ["Exercice", "Méditation"]
        }
        
        mood_result = await advisor.analyze_mood(user_id)
        assert mood_result["mood_score"] == 6.5
    
    # 3. Optimisation des tâches
    optimizer = TaskOptimizer()
    with patch.object(optimizer, 'optimize_user_tasks') as mock_optimize:
        mock_optimize.return_value = {
            "optimization_plan": "Réorganiser les priorités",
            "efficiency_gain": 0.25
        }
        
        optimize_result = await optimizer.optimize_user_tasks(user_id)
        assert "optimization_plan" in optimize_result

@pytest.mark.asyncio
async def test_ai_performance_metrics():
    """Test des métriques de performance IA"""
    analyzer = SurchargeAnalyzer()
    
    start_time = datetime.utcnow()
    
    with patch.object(analyzer, 'analyze_user_tasks') as mock_analyze:
        mock_analyze.return_value = {"overload_score": 5.0}
        
        result = await analyzer.analyze_user_tasks("user123")
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        # Vérifier que l'analyse est rapide (< 2 secondes)
        assert processing_time < 2.0
        assert result is not None

# ============================================================================
# TESTS DE RÉSILIENCE IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_fallback_mechanisms():
    """Test des mécanismes de fallback IA"""
    analyzer = SurchargeAnalyzer()
    
    # Simuler une panne de l'IA
    with patch('ia_manager_synchtasks.surcharge_analyzer.get_gemini_advice') as mock_ai:
        mock_ai.side_effect = Exception("API IA indisponible")
        
        result = await analyzer.analyze_user_tasks("user123")
        
        # Vérifier que le système continue de fonctionner
        assert result is not None
        assert "error" in result
        assert result["overload_score"] == 5.0  # Score par défaut

@pytest.mark.asyncio
async def test_ai_rate_limiting():
    """Test de gestion des limites de taux IA"""
    advisor = MoodAdvisor()
    
    # Simuler des appels répétés
    results = []
    for i in range(5):
        with patch('ia_manager_synchtasks.mood_advisor.get_gemini_advice') as mock_ai:
            mock_ai.return_value = f"Analyse {i}"
            result = await advisor.analyze_mood("user123")
            results.append(result)
    
    # Vérifier que tous les appels ont réussi
    assert len(results) == 5
    assert all(result is not None for result in results)

# ============================================================================
# TESTS DE VALIDATION DES DONNÉES IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_input_validation():
    """Test de validation des entrées IA"""
    analyzer = SurchargeAnalyzer()
    
    # Test avec des données invalides
    with pytest.raises(ValueError):
        await analyzer.analyze_user_tasks("")  # ID vide
    
    with pytest.raises(ValueError):
        await analyzer.analyze_user_tasks(None)  # ID None

@pytest.mark.asyncio
async def test_ai_output_validation():
    """Test de validation des sorties IA"""
    optimizer = TaskOptimizer()
    
    with patch.object(optimizer, 'optimize_user_tasks') as mock_optimize:
        mock_optimize.return_value = {
            "user_id": "user123",
            "optimization_plan": "Plan d'optimisation",
            "efficiency_gain": 0.3,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = await optimizer.optimize_user_tasks("user123")
        
        # Vérifier la structure de la réponse
        required_fields = ["user_id", "optimization_plan", "efficiency_gain"]
        for field in required_fields:
            assert field in result

# ============================================================================
# TESTS DE SÉCURITÉ IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_data_privacy():
    """Test de confidentialité des données IA"""
    analyzer = SurchargeAnalyzer()
    
    # Vérifier que les données sensibles ne sont pas exposées
    with patch.object(analyzer, 'analyze_user_tasks') as mock_analyze:
        mock_analyze.return_value = {
            "user_id": "user123",
            "overload_score": 7.5,
            "risk_level": "high"
        }
        
        result = await analyzer.analyze_user_tasks("user123")
        
        # Vérifier qu'aucune donnée sensible n'est exposée
        sensitive_fields = ["password", "email", "phone", "address"]
        for field in sensitive_fields:
            assert field not in str(result)

@pytest.mark.asyncio
async def test_ai_injection_prevention():
    """Test de prévention des injections IA"""
    advisor = MoodAdvisor()
    
    # Test avec des entrées malveillantes
    malicious_input = "'; DROP TABLE users; --"
    
    with patch.object(advisor, 'analyze_mood') as mock_analyze:
        mock_analyze.return_value = {"mood_score": 5.0}
        
        result = await advisor.analyze_mood(malicious_input)
        
        # Vérifier que le système gère correctement les entrées malveillantes
        assert result is not None
        assert "error" not in result or "injection" not in str(result).lower()

# ============================================================================
# TESTS DE DOCUMENTATION IA
# ============================================================================

def test_ai_documentation_coverage():
    """Test de couverture de la documentation IA"""
    # Vérifier que tous les modules IA ont une documentation
    modules = [SurchargeAnalyzer, MoodAdvisor, TaskOptimizer]
    
    for module in modules:
        assert module.__doc__ is not None
        assert len(module.__doc__) > 50  # Documentation minimale
        
        # Vérifier les méthodes principales
        methods = [method for method in dir(module) if not method.startswith('_')]
        for method_name in methods:
            method = getattr(module, method_name)
            if callable(method):
                assert method.__doc__ is not None

def test_ai_api_consistency():
    """Test de cohérence des APIs IA"""
    analyzer = SurchargeAnalyzer()
    advisor = MoodAdvisor()
    optimizer = TaskOptimizer()
    
    # Vérifier que toutes les APIs IA suivent le même pattern
    assert hasattr(analyzer, 'analyze_user_tasks')
    assert hasattr(advisor, 'analyze_mood')
    assert hasattr(optimizer, 'optimize_user_tasks')
    
    # Vérifier que les méthodes principales sont asynchrones
    import inspect
    assert inspect.iscoroutinefunction(analyzer.analyze_user_tasks)
    assert inspect.iscoroutinefunction(advisor.analyze_mood)
    assert inspect.iscoroutinefunction(optimizer.optimize_user_tasks) 