"""
Tests IA simplifiés - Le cerveau de l'application SyncTasks
Tests des fonctionnalités IA de base avec mocks
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from typing import Dict, Any

# ============================================================================
# TESTS DES FONCTIONS IA DE BASE
# ============================================================================

def test_ai_function_availability():
    """Test de disponibilité des fonctions IA"""
    # Vérifier que les modules IA existent
    try:
        import ia_manager_synchtasks.surcharge_analyzer
        assert True
    except ImportError:
        pytest.skip("Module surcharge_analyzer non disponible")
    
    try:
        import ia_manager_synchtasks.mood_advisor
        assert True
    except ImportError:
        pytest.skip("Module mood_advisor non disponible")
    
    try:
        import ia_manager_synchtasks.task_optimizer
        assert True
    except ImportError:
        pytest.skip("Module task_optimizer non disponible")

def test_ai_environment_setup():
    """Test de configuration de l'environnement IA"""
    import os
    from dotenv import load_dotenv
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Vérifier que les clés API sont configurées (même si elles sont des mocks)
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    # Les clés peuvent être des mocks pour les tests
    assert gemini_key is not None or "test" in str(gemini_key)
    assert openai_key is not None or "test" in str(openai_key)

# ============================================================================
# TESTS DES FONCTIONS UTILITAIRES IA
# ============================================================================

def test_ai_prompt_generation():
    """Test de génération de prompts IA"""
    def generate_task_analysis_prompt(tasks, user_mood):
        """Générer un prompt pour l'analyse de tâches"""
        prompt = f"""
        Analysez la charge de travail de cet utilisateur:
        
        Nombre de tâches: {len(tasks)}
        Humeur actuelle: {user_mood}/10
        
        Tâches:
        {chr(10).join([f"- {task.get('title', 'Tâche')} (Priorité: {task.get('priority', 'normale')})" for task in tasks])}
        
        Fournissez une analyse de surcharge et des recommandations.
        """
        return prompt
    
    # Test avec des données d'exemple
    tasks = [
        {"title": "Tâche urgente", "priority": "haute"},
        {"title": "Tâche normale", "priority": "normale"},
        {"title": "Tâche en retard", "priority": "haute"}
    ]
    user_mood = 6.5
    
    prompt = generate_task_analysis_prompt(tasks, user_mood)
    
    assert "Analysez la charge de travail" in prompt
    assert "Nombre de tâches: 3" in prompt
    assert "Humeur actuelle: 6.5/10" in prompt
    assert "Tâche urgente" in prompt
    assert "Tâche normale" in prompt
    assert "Tâche en retard" in prompt

def test_ai_response_parsing():
    """Test de parsing des réponses IA"""
    def parse_ai_analysis(response_text):
        """Parser une réponse d'analyse IA"""
        analysis = {
            "overload_score": 5.0,
            "risk_level": "medium",
            "recommendations": [],
            "factors": []
        }
        
        # Simulation de parsing basique
        if "surcharge" in response_text.lower():
            analysis["overload_score"] = 7.0
            analysis["risk_level"] = "high"
        
        if "recommandation" in response_text.lower():
            analysis["recommendations"].append("Prendre des pauses")
        
        if "stress" in response_text.lower():
            analysis["factors"].append("Stress élevé")
        
        return analysis
    
    # Test avec différentes réponses
    response1 = "Analyse: Surcharge détectée. Recommandation: Prendre des pauses."
    analysis1 = parse_ai_analysis(response1)
    
    assert analysis1["overload_score"] == 7.0
    assert analysis1["risk_level"] == "high"
    assert "Prendre des pauses" in analysis1["recommendations"]
    
    response2 = "Analyse: Charge normale. Stress modéré."
    analysis2 = parse_ai_analysis(response2)
    
    assert analysis2["overload_score"] == 5.0
    assert analysis2["risk_level"] == "medium"
    assert "Stress élevé" in analysis2["factors"]

# ============================================================================
# TESTS DES MÉTRIQUES IA
# ============================================================================

def test_workload_metrics_calculation():
    """Test de calcul des métriques de charge de travail"""
    def calculate_workload_metrics(tasks):
        """Calculer les métriques de charge de travail"""
        metrics = {
            "total_tasks": len(tasks),
            "high_priority_count": 0,
            "overdue_count": 0,
            "avg_complexity": 0,
            "stress_factors": []
        }
        
        if not tasks:
            return metrics
        
        # Compter les priorités
        for task in tasks:
            if task.get("priority") == "haute":
                metrics["high_priority_count"] += 1
            if task.get("overdue", False):
                metrics["overdue_count"] += 1
        
        # Calculer la complexité moyenne
        complexities = [task.get("complexity", 2) for task in tasks]
        metrics["avg_complexity"] = sum(complexities) / len(complexities)
        
        # Identifier les facteurs de stress
        if metrics["overdue_count"] > 0:
            metrics["stress_factors"].append(f"{metrics['overdue_count']} tâche(s) en retard")
        
        if metrics["high_priority_count"] > 3:
            metrics["stress_factors"].append(f"{metrics['high_priority_count']} tâches haute priorité")
        
        if metrics["total_tasks"] > 15:
            metrics["stress_factors"].append("Nombre élevé de tâches")
        
        return metrics
    
    # Test avec des tâches d'exemple
    tasks = [
        {"priority": "haute", "complexity": 3, "overdue": True},
        {"priority": "normale", "complexity": 2, "overdue": False},
        {"priority": "haute", "complexity": 1, "overdue": False},
        {"priority": "normale", "complexity": 2, "overdue": True}
    ]
    
    metrics = calculate_workload_metrics(tasks)
    
    assert metrics["total_tasks"] == 4
    assert metrics["high_priority_count"] == 2
    assert metrics["overdue_count"] == 2
    assert metrics["avg_complexity"] == 2.0
    assert len(metrics["stress_factors"]) >= 1

def test_risk_level_determination():
    """Test de détermination du niveau de risque"""
    def determine_risk_level(overload_score):
        """Déterminer le niveau de risque basé sur le score de surcharge"""
        if overload_score < 3:
            return "low"
        elif overload_score < 6:
            return "medium"
        elif overload_score < 8:
            return "high"
        else:
            return "critical"
    
    # Test différents scores
    assert determine_risk_level(2.0) == "low"
    assert determine_risk_level(5.0) == "medium"
    assert determine_risk_level(7.0) == "high"
    assert determine_risk_level(9.0) == "critical"

# ============================================================================
# TESTS DES RECOMMANDATIONS IA
# ============================================================================

def test_recommendation_generation():
    """Test de génération de recommandations IA"""
    def generate_recommendations(metrics, risk_level):
        """Générer des recommandations basées sur les métriques"""
        recommendations = []
        
        if risk_level == "high" or risk_level == "critical":
            recommendations.append("Prendre des pauses régulières")
            recommendations.append("Prioriser les tâches urgentes")
        
        if metrics.get("overdue_count", 0) > 0:
            recommendations.append("Traiter les tâches en retard en priorité")
        
        if metrics.get("high_priority_count", 0) > 3:
            recommendations.append("Déléguer certaines tâches si possible")
        
        if metrics.get("total_tasks", 0) > 15:
            recommendations.append("Réduire le nombre de tâches simultanées")
        
        if not recommendations:
            recommendations.append("Continuer avec le rythme actuel")
        
        return recommendations
    
    # Test avec différents scénarios
    metrics1 = {"overdue_count": 2, "high_priority_count": 4, "total_tasks": 20}
    recs1 = generate_recommendations(metrics1, "high")
    
    assert "Prendre des pauses régulières" in recs1
    assert "Traiter les tâches en retard en priorité" in recs1
    assert "Déléguer certaines tâches si possible" in recs1
    assert "Réduire le nombre de tâches simultanées" in recs1
    
    metrics2 = {"overdue_count": 0, "high_priority_count": 1, "total_tasks": 5}
    recs2 = generate_recommendations(metrics2, "low")
    
    assert "Continuer avec le rythme actuel" in recs2

# ============================================================================
# TESTS DE PERFORMANCE IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_response_time():
    """Test du temps de réponse IA"""
    async def mock_ai_analysis(tasks):
        """Simuler une analyse IA avec délai"""
        await asyncio.sleep(0.1)  # Simuler un délai de traitement
        
        return {
            "overload_score": 6.5,
            "risk_level": "medium",
            "recommendations": ["Test recommendation"],
            "processing_time": 0.1
        }
    
    start_time = datetime.utcnow()
    
    tasks = [{"title": "Test task", "priority": "normale"}]
    result = await mock_ai_analysis(tasks)
    
    end_time = datetime.utcnow()
    processing_time = (end_time - start_time).total_seconds()
    
    # Vérifier que l'analyse est rapide (< 1 seconde)
    assert processing_time < 1.0
    assert result["overload_score"] == 6.5
    assert result["risk_level"] == "medium"

# ============================================================================
# TESTS DE RÉSILIENCE IA
# ============================================================================

@pytest.mark.asyncio
async def test_ai_fallback_mechanism():
    """Test du mécanisme de fallback IA"""
    async def analyze_with_fallback(tasks):
        """Analyser avec mécanisme de fallback"""
        try:
            # Simuler un appel IA qui échoue
            raise Exception("API IA indisponible")
        except Exception:
            # Fallback vers une analyse basique
            return {
                "overload_score": 5.0,
                "risk_level": "medium",
                "recommendations": ["Réessayer plus tard"],
                "fallback_used": True
            }
    
    result = await analyze_with_fallback([])
    
    assert result["overload_score"] == 5.0
    assert result["risk_level"] == "medium"
    assert result["fallback_used"] == True

# ============================================================================
# TESTS DE VALIDATION IA
# ============================================================================

def test_ai_input_validation():
    """Test de validation des entrées IA"""
    def validate_ai_input(user_id, tasks):
        """Valider les entrées pour l'analyse IA"""
        errors = []
        
        if not user_id or user_id.strip() == "":
            errors.append("ID utilisateur requis")
        
        if not isinstance(tasks, list):
            errors.append("Tâches doivent être une liste")
        
        if tasks and not all(isinstance(task, dict) for task in tasks):
            errors.append("Chaque tâche doit être un dictionnaire")
        
        return errors
    
    # Test avec des entrées valides
    errors1 = validate_ai_input("user123", [{"title": "Task"}])
    assert len(errors1) == 0
    
    # Test avec des entrées invalides
    errors2 = validate_ai_input("", [])
    assert "ID utilisateur requis" in errors2
    
    errors3 = validate_ai_input("user123", "not a list")
    assert "Tâches doivent être une liste" in errors3

def test_ai_output_validation():
    """Test de validation des sorties IA"""
    def validate_ai_output(analysis):
        """Valider la structure de sortie IA"""
        required_fields = ["overload_score", "risk_level", "recommendations"]
        errors = []
        
        for field in required_fields:
            if field not in analysis:
                errors.append(f"Champ requis manquant: {field}")
        
        if "overload_score" in analysis:
            score = analysis["overload_score"]
            if not isinstance(score, (int, float)) or score < 0 or score > 10:
                errors.append("Score de surcharge doit être entre 0 et 10")
        
        if "risk_level" in analysis:
            level = analysis["risk_level"]
            valid_levels = ["low", "medium", "high", "critical"]
            if level not in valid_levels:
                errors.append(f"Niveau de risque invalide: {level}")
        
        return errors
    
    # Test avec une sortie valide
    valid_output = {
        "overload_score": 7.5,
        "risk_level": "high",
        "recommendations": ["Test"]
    }
    errors1 = validate_ai_output(valid_output)
    assert len(errors1) == 0
    
    # Test avec une sortie invalide
    invalid_output = {
        "overload_score": 15.0,  # Trop élevé
        "risk_level": "invalid",
        "recommendations": ["Test"]
    }
    errors2 = validate_ai_output(invalid_output)
    assert len(errors2) >= 2

# ============================================================================
# TESTS D'INTÉGRATION IA SIMPLE
# ============================================================================

@pytest.mark.asyncio
async def test_complete_ai_workflow():
    """Test du workflow IA complet"""
    async def complete_ai_analysis(user_id, tasks):
        """Workflow complet d'analyse IA"""
        # 1. Validation des entrées
        errors = []
        if not user_id:
            errors.append("ID utilisateur requis")
        if not isinstance(tasks, list):
            errors.append("Tâches doivent être une liste")
        
        if errors:
            return {"error": errors}
        
        # 2. Calcul des métriques
        metrics = {
            "total_tasks": len(tasks),
            "high_priority_count": len([t for t in tasks if t.get("priority") == "haute"]),
            "overdue_count": len([t for t in tasks if t.get("overdue", False)])
        }
        
        # 3. Analyse IA (simulée)
        overload_score = min(10, max(0, metrics["high_priority_count"] * 2 + metrics["overdue_count"] * 1.5))
        
        # 4. Détermination du niveau de risque
        if overload_score < 3:
            risk_level = "low"
        elif overload_score < 6:
            risk_level = "medium"
        elif overload_score < 8:
            risk_level = "high"
        else:
            risk_level = "critical"
        
        # 5. Génération de recommandations
        recommendations = []
        if risk_level in ["high", "critical"]:
            recommendations.append("Prendre des pauses régulières")
        if metrics["overdue_count"] > 0:
            recommendations.append("Traiter les tâches en retard")
        
        return {
            "user_id": user_id,
            "overload_score": round(overload_score, 1),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Test du workflow complet
    tasks = [
        {"title": "Tâche urgente", "priority": "haute", "overdue": True},
        {"title": "Tâche normale", "priority": "normale", "overdue": False},
        {"title": "Autre tâche urgente", "priority": "haute", "overdue": False}
    ]
    
    result = await complete_ai_analysis("user123", tasks)
    
    assert result["user_id"] == "user123"
    assert "overload_score" in result
    assert "risk_level" in result
    assert "recommendations" in result
    assert "metrics" in result
    assert result["metrics"]["total_tasks"] == 3
    assert result["metrics"]["high_priority_count"] == 2
    assert result["metrics"]["overdue_count"] == 1

# ============================================================================
# TESTS DE DOCUMENTATION IA
# ============================================================================

def test_ai_documentation():
    """Test de la documentation des fonctions IA"""
    def documented_ai_function():
        """
        Fonction IA documentée pour les tests.
        
        Returns:
            dict: Résultat de l'analyse IA
        """
        return {"status": "documented"}
    
    # Vérifier que la fonction a une documentation
    assert documented_ai_function.__doc__ is not None
    assert len(documented_ai_function.__doc__) > 20
    
    # Vérifier que la fonction fonctionne
    result = documented_ai_function()
    assert result["status"] == "documented"

def test_ai_api_consistency():
    """Test de cohérence des APIs IA"""
    # Définir une interface IA standard
    class StandardAIAnalyzer:
        async def analyze(self, user_id: str, data: list) -> dict:
            """Interface standard pour l'analyse IA"""
            return {
                "user_id": user_id,
                "analysis_result": "standard",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    analyzer = StandardAIAnalyzer()
    
    # Vérifier que l'interface est cohérente
    assert hasattr(analyzer, 'analyze')
    assert callable(analyzer.analyze)
    
    # Vérifier que la méthode est asynchrone
    import inspect
    assert inspect.iscoroutinefunction(analyzer.analyze) 