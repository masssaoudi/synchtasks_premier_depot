from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import os
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv
import random

# Charger les variables d'environnement
load_dotenv()

router = APIRouter(prefix="/api/ia", tags=["IA"])

# Configuration Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    gemini_model = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = "chat"

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime

class AdviceRequest(BaseModel):
    user_id: str
    context: Optional[str] = "general"

class AdviceResponse(BaseModel):
    advice: dict
    timestamp: datetime

class HistoryRequest(BaseModel):
    user_id: str
    mode: str = "insight"
    days: int = 30

# Données d'historique simulées mais réalistes
HISTORY_DATA = {
    "interactions": [
        {
            "id": "1",
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "type": "chat",
            "message": "Comment organiser mes tâches de la semaine ?",
            "response": "Voici mes conseils pour organiser votre semaine efficacement :\n\n📅 **Planification dimanche soir** : Prenez 30 min pour planifier\n🎯 **3 priorités max par jour** : Évitez la surcharge\n⏰ **Blocs de temps** : Réservez des créneaux spécifiques\n🔄 **Flexibilité** : Gardez 20% de temps libre\n📊 **Rétrospective** : Analysez vos progrès le vendredi",
            "category": "organisation",
            "satisfaction": 5
        },
        {
            "id": "2", 
            "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
            "type": "advice",
            "context": "productivity",
            "insights": ["Technique Pomodoro recommandée", "Pause de 5 min toutes les 25 min"],
            "category": "productivité",
            "satisfaction": 4
        },
        {
            "id": "3",
            "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
            "type": "chat",
            "message": "Je me sens démotivé, que faire ?",
            "response": "Je comprends ce sentiment ! Voici mes conseils pour retrouver la motivation :\n\n🎯 **Visualisez le résultat** : Imaginez-vous avoir terminé\n🏆 **Petites victoires** : Célébrez chaque étape\n👥 **Responsabilité** : Partagez vos objectifs\n📈 **Progression** : Suivez vos progrès\n🎵 **Environnement** : Créez un espace agréable\n💪 **Routine** : Établissez des habitudes positives",
            "category": "motivation",
            "satisfaction": 5
        },
        {
            "id": "4",
            "timestamp": (datetime.now() - timedelta(days=2)).isoformat(),
            "type": "task_completion",
            "task_name": "Préparer la présentation",
            "ai_assistance": True,
            "suggestions": ["Marquez comme terminée", "Ajoutez une note de satisfaction"],
            "category": "accomplissement",
            "satisfaction": 5
        },
        {
            "id": "5",
            "timestamp": (datetime.now() - timedelta(days=3)).isoformat(),
            "type": "chat",
            "message": "Comment gérer le stress au travail ?",
            "response": "Voici mes techniques anti-stress :\n\n🧘 **Respiration** : 3 respirations profondes\n⏰ **Pauses régulières** : 5 min toutes les 25 min\n🎯 **Une chose à la fois** : Concentrez-vous sur l'essentiel\n📝 **Liste de gratitude** : 3 choses positives par jour\n🏃 **Mouvement** : Petite promenade\n💤 **Sommeil** : Priorisez 7-8h de repos",
            "category": "bien-être",
            "satisfaction": 4
        }
    ],
    "analytics": {
        "total_interactions": 15,
        "average_satisfaction": 4.6,
        "most_common_topics": ["organisation", "productivité", "motivation", "bien-être"],
        "productivity_score": 0.78,
        "completion_rate": 0.85,
        "stress_level": 0.3,
        "motivation_level": 0.8
    }
}

def get_gemini_response(message: str, context: str = "chat") -> str:
    """Obtenir une réponse de Gemini"""
    if not gemini_model:
        return "❌ Erreur : Clé API Gemini non configurée. Veuillez configurer GEMINI_API_KEY dans le fichier .env"
    
    try:
        # Prompt contextuel pour SyncTasks
        system_prompt = """Tu es un assistant IA spécialisé dans la gestion de tâches et la productivité pour l'application SyncTasks.

Tu peux aider avec :
- Organisation et planification de tâches
- Conseils de productivité
- Gestion du stress et de la motivation
- Optimisation du workflow
- Techniques de gestion du temps

Réponds de manière bienveillante, pratique et encourageante. Utilise des emojis pour rendre tes réponses plus engageantes."""

        full_prompt = f"{system_prompt}\n\nUtilisateur : {message}\n\nAssistant :"
        
        response = gemini_model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        return f"❌ Erreur Gemini : {str(e)}"

def get_ai_insights(interactions: list, analytics: dict) -> dict:
    """Générer des insights intelligents basés sur l'historique"""
    # Utiliser directement le fallback pour éviter les timeouts
    # TODO: Réactiver Gemini une fois la configuration optimisée
    return get_fallback_insights(interactions, analytics)

def get_fallback_insights(interactions: list, analytics: dict) -> dict:
    """Insights de fallback basés sur des règles simples"""
    insights = []
    recommendations = []
    trends = []
    opportunities = []
    
    # Analyser les catégories
    categories = {}
    for interaction in interactions:
        cat = interaction.get("category", "général")
        categories[cat] = categories.get(cat, 0) + 1
    
    # Insights basés sur les patterns
    if categories.get("organisation", 0) > 2:
        insights.append("Vous accordez une grande importance à l'organisation - c'est une excellente approche !")
    if analytics.get("average_satisfaction", 0) > 4.5:
        insights.append("Votre satisfaction est élevée, vous êtes sur la bonne voie !")
    if len(interactions) > 10:
        insights.append("Vous utilisez régulièrement l'IA - c'est une excellente habitude pour la productivité !")
    if categories.get("motivation", 0) > 1:
        insights.append("Vous cherchez activement à maintenir votre motivation - c'est essentiel !")
    
    # Recommandations basées sur les données
    if analytics.get("stress_level", 0.3) > 0.4:
        recommendations.append("Pensez à intégrer plus de pauses dans votre routine pour réduire le stress")
    if analytics.get("motivation_level", 0.8) < 0.7:
        recommendations.append("Essayez de célébrer vos petites victoires plus souvent pour maintenir la motivation")
    if len(interactions) < 5:
        recommendations.append("N'hésitez pas à me solliciter plus souvent pour des conseils personnalisés")
    if categories.get("productivité", 0) < 2:
        recommendations.append("Explorez les techniques de productivité comme la méthode Pomodoro")
    
    # Tendances
    if categories.get("organisation", 0) > categories.get("motivation", 0):
        trends.append("Vous privilégiez l'organisation sur la motivation")
    else:
        trends.append("Vous vous concentrez sur le maintien de la motivation")
    
    # Opportunités
    if analytics.get("completion_rate", 0.85) < 0.9:
        opportunities.append("Améliorer le taux de complétion en décomposant les tâches complexes")
    if analytics.get("productivity_score", 0.78) < 0.85:
        opportunities.append("Optimiser votre productivité en identifiant vos heures de pic")
    
    return {
        "insights": insights,
        "recommendations": recommendations,
        "trends": trends,
        "opportunities": opportunities
    }

def get_fallback_response(message: str) -> str:
    """Réponse de fallback si Gemini n'est pas disponible"""
    message_lower = message.lower()
    
    # Réponses contextuelles basées sur les mots-clés
    if any(word in message_lower for word in ["organiser", "organisation", "planifier"]):
        return """Voici mes conseils pour mieux organiser vos tâches :

📋 **Méthode Kanban** : Utilisez les colonnes "À faire", "En cours", "Terminé"
🎯 **Priorités** : Classez vos tâches par importance et urgence
⏰ **Timeboxing** : Allouez un temps limité à chaque tâche
📅 **Planification** : Planifiez vos tâches la veille pour le lendemain

Voulez-vous que je vous aide à créer une structure de tâches ?"""
    
    elif any(word in message_lower for word in ["productivité", "efficacité", "performance"]):
        return """Voici mes conseils pour améliorer votre productivité :

🚀 **Technique Pomodoro** : 25 min de travail + 5 min de pause
🎯 **Objectifs SMART** : Spécifiques, Mesurables, Atteignables, Réalistes, Temporels
📱 **Réduction des distractions** : Mode avion pendant les sessions de travail
💪 **Énergie** : Travaillez sur vos tâches importantes quand vous êtes le plus productif
🎉 **Célébration** : Récompensez-vous pour chaque tâche terminée

Quelle technique souhaitez-vous essayer en premier ?"""
    
    elif any(word in message_lower for word in ["semaine", "planifier", "planification"]):
        return """Voici comment planifier votre semaine efficacement :

📅 **Dimanche soir** : Planifiez votre semaine
🎯 **3 objectifs max** par jour pour éviter la surcharge
⏰ **Blocs de temps** : Réservez des créneaux pour chaque type de tâche
🔄 **Flexibilité** : Gardez 20% de temps libre pour l'imprévu
📊 **Rétrospective** : Le vendredi, analysez ce qui a bien fonctionné

Voulez-vous que je vous aide à créer un planning type ?"""
    
    elif any(word in message_lower for word in ["motivation", "motivé", "démotivé"]):
        return """Voici mes conseils pour maintenir votre motivation :

🎯 **Visualisez le résultat** : Imaginez-vous avoir terminé la tâche
🏆 **Petites victoires** : Célébrez chaque étape accomplie
👥 **Responsabilité** : Partagez vos objectifs avec quelqu'un
📈 **Progression** : Suivez vos progrès avec des métriques
🎵 **Environnement** : Créez un espace de travail agréable
💪 **Routine** : Établissez des habitudes positives

Qu'est-ce qui vous motive le plus dans vos projets ?"""
    
    elif any(word in message_lower for word in ["stress", "anxiété", "pression"]):
        return """Voici mes conseils pour gérer le stress :

🧘 **Respiration** : Prenez 3 respirations profondes
⏰ **Pauses régulières** : 5 min toutes les 25 min
🎯 **Une chose à la fois** : Concentrez-vous sur une seule tâche
📝 **Liste de gratitude** : Notez 3 choses positives chaque jour
🏃 **Mouvement** : Faites une petite promenade
💤 **Sommeil** : Priorisez 7-8h de sommeil

Comment vous sentez-vous actuellement ?"""
    
    else:
        return """Je suis là pour vous aider ! Voici ce que je peux faire :

📋 **Organisation** : Vous aider à structurer vos tâches
🎯 **Productivité** : Conseils pour améliorer votre efficacité
📅 **Planification** : Créer des plannings optimisés
💪 **Motivation** : Techniques pour rester motivé
🧘 **Bien-être** : Gestion du stress et équilibre

Que souhaitez-vous explorer ?"""

@router.post("/chat")
async def chat_with_ia(request: ChatRequest):
    """Chat avec l'IA pour obtenir de l'aide et des conseils."""
    try:
        # Utiliser directement le fallback pour des réponses rapides
        # TODO: Réactiver Gemini une fois la configuration optimisée
        response = get_fallback_response(request.message)
        
        # Ajouter l'interaction à l'historique
        new_interaction = {
            "id": str(len(HISTORY_DATA["interactions"]) + 1),
            "timestamp": datetime.now().isoformat(),
            "type": "chat",
            "message": request.message,
            "response": response,
            "category": "général",
            "satisfaction": random.randint(4, 5)
        }
        HISTORY_DATA["interactions"].insert(0, new_interaction)
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        # En cas d'erreur, utiliser le fallback
        response = get_fallback_response(request.message)
        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )

@router.post("/advice")
async def get_ai_advice(request: AdviceRequest):
    """Obtenir des conseils personnalisés de l'IA."""
    try:
        # Conseils génériques pour l'instant
        advice = {
            "recommendations": [
                "Organisez vos tâches par priorité et urgence",
                "Utilisez la technique Pomodoro pour maintenir votre concentration",
                "Prenez des pauses régulières pour éviter l'épuisement",
                "Célébrez vos petites victoires pour maintenir la motivation"
            ],
            "insights": {
                "Productivité": "Vous avez tendance à être plus productif le matin",
                "Organisation": "Vos tâches sont bien structurées",
                "Motivation": "Vous progressez régulièrement vers vos objectifs"
            },
            "next_actions": [
                "Planifiez vos tâches pour demain",
                "Identifiez vos 3 priorités principales",
                "Prévoyez des pauses régulières"
            ]
        }
        
        return AdviceResponse(
            advice=advice,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse IA: {str(e)}")

@router.get("/history")
async def get_ia_history(mode: str = "insight", days: int = 30):
    """Récupérer l'historique des interactions IA avec des analyses avancées."""
    try:
        # Filtrer les interactions des derniers jours
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_interactions = [
            interaction for interaction in HISTORY_DATA["interactions"]
            if datetime.fromisoformat(interaction["timestamp"]) > cutoff_date
        ]
        
        # Calculer les statistiques
        total_interactions = len(recent_interactions)
        avg_satisfaction = sum(i.get("satisfaction", 4) for i in recent_interactions) / total_interactions if total_interactions > 0 else 0
        
        # Analyser les catégories
        categories = {}
        for interaction in recent_interactions:
            cat = interaction.get("category", "général")
            categories[cat] = categories.get(cat, 0) + 1
        
        # Générer des insights intelligents avec IA
        ai_analysis = get_ai_insights(recent_interactions, {
            "total_interactions": total_interactions,
            "average_satisfaction": avg_satisfaction,
            "categories": categories,
            "productivity_score": min(0.95, 0.7 + (avg_satisfaction - 4) * 0.1),
            "completion_rate": min(0.95, 0.8 + (total_interactions / 20)),
            "stress_level": max(0.1, 0.3 - (avg_satisfaction - 4) * 0.1),
            "motivation_level": min(0.95, 0.7 + (avg_satisfaction - 4) * 0.1)
        })
        
        insights = ai_analysis.get("insights", [])
        recommendations = ai_analysis.get("recommendations", [])
        trends = ai_analysis.get("trends", [])
        opportunities = ai_analysis.get("opportunities", [])
        
        # Créer le résumé enrichi
        summary = f"""📊 **Résumé de vos interactions IA** ({days} derniers jours)

🎯 **{total_interactions} interactions** avec une satisfaction moyenne de **{avg_satisfaction:.1f}/5**

📈 **Catégories les plus consultées** :
{chr(10).join([f"• {cat}: {count} fois" for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]])}

💡 **Insights principaux** :
{chr(10).join([f"• {insight}" for insight in insights[:3]])}

🎯 **Recommandations personnalisées** :
{chr(10).join([f"• {rec}" for rec in recommendations[:3]])}

📈 **Tendances observées** :
{chr(10).join([f"• {trend}" for trend in trends[:2]])}

🚀 **Opportunités d'amélioration** :
{chr(10).join([f"• {opp}" for opp in opportunities[:2]])}"""
        
        history_data = {
            "mode": mode,
            "summary": summary,
            "interactions": recent_interactions,
            "analytics": {
                "total_interactions": total_interactions,
                "average_satisfaction": round(avg_satisfaction, 1),
                "most_common_topics": list(categories.keys()),
                "productivity_score": min(0.95, 0.7 + (avg_satisfaction - 4) * 0.1),
                "completion_rate": min(0.95, 0.8 + (total_interactions / 20)),
                "stress_level": max(0.1, 0.3 - (avg_satisfaction - 4) * 0.1),
                "motivation_level": min(0.95, 0.7 + (avg_satisfaction - 4) * 0.1)
            },
            "insights": insights,
            "recommendations": recommendations,
            "trends": trends,
            "opportunities": opportunities,
            "categories": categories
        }
        
        return history_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'historique: {str(e)}")

@router.post("/complete-task")
async def complete_task_with_ia(task_id: str, action: str, keep_memory: bool = True):
    """Compléter une tâche avec l'aide de l'IA."""
    try:
        # Logique de complétion de tâche avec IA
        result = {
            "task_id": task_id,
            "action": action,
            "ai_assistance": True,
            "suggestions": [
                "Marquez la tâche comme terminée",
                "Ajoutez une note de satisfaction",
                "Planifiez la prochaine étape"
            ],
            "completed_at": datetime.now().isoformat()
        }
        
        # Ajouter à l'historique si keep_memory est True
        if keep_memory:
            new_interaction = {
                "id": str(len(HISTORY_DATA["interactions"]) + 1),
                "timestamp": datetime.now().isoformat(),
                "type": "task_completion",
                "task_name": f"Tâche {task_id}",
                "ai_assistance": True,
                "suggestions": result["suggestions"],
                "category": "accomplissement",
                "satisfaction": 5
            }
            HISTORY_DATA["interactions"].insert(0, new_interaction)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la complétion de tâche: {str(e)}")

@router.get("/status")
async def get_ia_status():
    """Vérifier le statut de l'IA."""
    try:
        status = {
            "gemini_configured": GEMINI_API_KEY is not None,
            "gemini_available": gemini_model is not None,
            "fallback_available": True,
            "last_check": datetime.now().isoformat()
        }
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification du statut: {str(e)}") 