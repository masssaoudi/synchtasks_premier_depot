from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from auth import get_current_user
from models import UserInDB
from services import task_service
from datetime import datetime

load_dotenv()

router = APIRouter(prefix="/api/ia", tags=["ia"])

# Configuration Gemini - Import conditionnel
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai = None

try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    print("⚠️ google.generativeai non disponible - fonctionnalités IA limitées")
except Exception as e:
    print(f"⚠️ Erreur lors de la configuration de Gemini: {e}")

class ChatMessage(BaseModel):
    """Message de chat"""
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Réponse du chat IA"""
    response: str
    suggestions: List[str] = []
    task_suggestions: List[dict] = []

class TaskHistoryRequest(BaseModel):
    """Demande d'historique des tâches"""
    include_completed: bool = True
    include_archived: bool = False
    time_period: Optional[str] = "all"  # "week", "month", "all"

class TaskHistoryResponse(BaseModel):
    """Réponse d'historique intelligent"""
    summary: str
    insights: List[str]
    recommendations: List[str]
    productivity_score: float
    completion_rate: float
    task_distribution: dict

class TaskCompletionRequest(BaseModel):
    """Demande de gestion d'une tâche terminée"""
    task_id: str
    action: str  # "archive" ou "delete"
    keep_memory: bool = True

class TaskCompletionResponse(BaseModel):
    """Réponse de gestion de tâche terminée"""
    success: bool
    message: str
    archived_task: Optional[dict] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    """Chat avec l'IA pour obtenir de l'aide sur les tâches"""
    try:
        if not GEMINI_API_KEY or not genai:
            return ChatResponse(
                response="Désolé, l'IA n'est pas configurée pour le moment. Contactez l'administrateur.",
                suggestions=["Ajouter une tâche manuellement", "Organiser vos priorités"],
                task_suggestions=[]
            )

        # Prompt contextuel pour SyncTasks
        context_prompt = f"""
        Tu es un assistant IA spécialisé dans la gestion de tâches et la productivité pour SyncTasks.
        L'utilisateur te dit : "{chat_message.message}"
        
        Réponds de manière utile et encourageante. Tu peux :
        - Suggérer des tâches basées sur leur message
        - Donner des conseils de productivité
        - Aider à organiser et prioriser
        - Proposer des techniques de gestion du temps
        
        Réponds en français, de manière naturelle et bienveillante.
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(context_prompt)
        
        # Générer des suggestions basées sur le message
        suggestions = generate_suggestions(chat_message.message)
        
        # Générer des suggestions de tâches
        task_suggestions = generate_task_suggestions(chat_message.message)
        
        return ChatResponse(
            response=response.text,
            suggestions=suggestions,
            task_suggestions=task_suggestions
        )
        
    except Exception as e:
        return ChatResponse(
            response=f"Désolé, j'ai rencontré une erreur : {str(e)}",
            suggestions=["Réessayer", "Contacter le support"],
            task_suggestions=[]
        )

def generate_suggestions(user_message: str) -> List[str]:
    """Générer des suggestions basées sur le message utilisateur"""
    suggestions = []
    
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ["fatigué", "épuisé", "stressé"]):
        suggestions.extend([
            "Prendre une pause de 5 minutes",
            "Faire des exercices de respiration",
            "Prioriser les tâches importantes"
        ])
    
    if any(word in message_lower for word in ["beaucoup", "trop", "surchargé"]):
        suggestions.extend([
            "Diviser les grandes tâches",
            "Déléguer si possible",
            "Utiliser la technique Pomodoro"
        ])
    
    if any(word in message_lower for word in ["motivation", "envie", "difficile"]):
        suggestions.extend([
            "Commencer par une tâche simple",
            "Se récompenser après chaque accomplissement",
            "Visualiser l'objectif final"
        ])
    
    # Suggestions par défaut
    if not suggestions:
        suggestions = [
            "Créer une nouvelle tâche",
            "Organiser vos priorités",
            "Prendre une pause"
        ]
    
    return suggestions[:3]  # Limiter à 3 suggestions

def generate_task_suggestions(user_message: str) -> List[dict]:
    """Générer des suggestions de tâches basées sur le message"""
    suggestions = []
    
    message_lower = user_message.lower()
    
    # Suggestions contextuelles
    if any(word in message_lower for word in ["réunion", "meeting"]):
        suggestions.append({
            "title": "Préparer la réunion",
            "category": "travail",
            "priority": "haute",
            "description": "Organiser les points à aborder"
        })
    
    if any(word in message_lower for word in ["projet", "deadline"]):
        suggestions.append({
            "title": "Planifier le projet",
            "category": "travail", 
            "priority": "haute",
            "description": "Définir les étapes et échéances"
        })
    
    if any(word in message_lower for word in ["sport", "exercice", "santé"]):
        suggestions.append({
            "title": "Séance de sport",
            "category": "personnel",
            "priority": "normale", 
            "description": "Maintenir une bonne santé"
        })
    
    return suggestions

@router.get("/health")
async def ia_health_check():
    """Vérifier l'état de l'IA"""
    return {
        "status": "healthy",
        "gemini_configured": bool(GEMINI_API_KEY),
        "message": "IA SyncTasks opérationnelle"
    } 

@router.get("/history", response_model=TaskHistoryResponse)
async def get_history_get(
    current_user: UserInDB = Depends(get_current_user)
):
    """Récupérer l'historique intelligent des tâches (GET)"""
    try:
        # Récupérer toutes les tâches de l'utilisateur
        tasks = await task_service.get_tasks_by_user(current_user.id)
        
        if not tasks:
            return TaskHistoryResponse(
                summary="Aucune tâche trouvée pour le moment.",
                insights=["Commencez par créer votre première tâche"],
                recommendations=["Ajoutez une tâche simple pour commencer"],
                productivity_score=0.0,
                completion_rate=0.0,
                task_distribution={}
            )
        
        # Analyser avec l'IA si disponible
        if GEMINI_API_KEY and genai:
            return await analyze_task_history_with_ai(tasks, current_user)
        else:
            return generate_basic_analysis(tasks)
            
    except Exception as e:
        print(f"Erreur lors de la récupération de l'historique: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération de l'historique"
        )

@router.post("/history", response_model=TaskHistoryResponse)
async def get_intelligent_history(
    request: TaskHistoryRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    """Obtenir un historique intelligent des tâches avec analyse IA"""
    try:
        # Récupérer toutes les tâches de l'utilisateur
        all_tasks = await task_service.get_user_tasks(current_user.id, skip=0, limit=1000)
        
        # Filtrer selon les paramètres
        if not request.include_completed:
            all_tasks = [task for task in all_tasks if task.status != "completed"]
        
        # Analyser avec l'IA
        if GEMINI_API_KEY and genai:
            analysis = await analyze_task_history_with_ai(all_tasks, current_user)
        else:
            analysis = generate_basic_analysis(all_tasks)
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

@router.post("/complete-task", response_model=TaskCompletionResponse)
async def handle_completed_task(
    request: TaskCompletionRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    """Gérer une tâche terminée avec suggestions IA"""
    try:
        # Vérifier que la tâche appartient à l'utilisateur
        task = await task_service.get_task_by_id(request.task_id)
        if not task or task.created_by != current_user.id:
            raise HTTPException(status_code=404, detail="Tâche non trouvée")
        
        if request.action == "archive":
            # Archiver la tâche
            archived_task = await archive_task(request.task_id, request.keep_memory)
            message = "Tâche archivée avec succès" if request.keep_memory else "Tâche supprimée définitivement"
            
            return TaskCompletionResponse(
                success=True,
                message=message,
                archived_task=archived_task
            )
        
        elif request.action == "delete":
            # Supprimer définitivement
            await task_service.delete_task(request.task_id)
            return TaskCompletionResponse(
                success=True,
                message="Tâche supprimée définitivement"
            )
        
        else:
            raise HTTPException(status_code=400, detail="Action invalide")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

async def analyze_task_history_with_ai(tasks: List, user: UserInDB) -> TaskHistoryResponse:
    """Analyser l'historique des tâches avec l'IA"""
    if not GEMINI_API_KEY or not genai:
        return generate_basic_analysis(tasks)
    
    # Préparer les données pour l'IA
    task_data = []
    for task in tasks:
        task_data.append({
            "title": task.title,
            "category": task.category,
            "priority": task.priority,
            "status": task.status,
            "created_at": str(task.created_at),
            "completed_at": str(task.completed_at) if task.completed_at else None,
            "due_date": str(task.due_date) if task.due_date else None
        })
    
    # Prompt pour l'analyse IA
    prompt = f"""
    Tu es un assistant IA spécialisé dans l'analyse de productivité pour SyncTasks.
    
    Voici l'historique des tâches de l'utilisateur {user.username}:
    {task_data}
    
    Analyse cet historique et fournis :
    1. Un résumé concis de la productivité
    2. 3-5 insights pertinents sur les habitudes de travail
    3. 3-5 recommandations pour améliorer la productivité
    4. Un score de productivité sur 100
    5. Un taux de complétion en pourcentage
    6. La distribution des tâches par catégorie
    
    Réponds en français, de manière encourageante et constructive.
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Parser la réponse de l'IA (simplifié pour l'exemple)
        ai_response = response.text
        
        # Extraire les informations (dans un vrai cas, on utiliserait un parsing plus sophistiqué)
        summary = extract_summary(ai_response)
        insights = extract_insights(ai_response)
        recommendations = extract_recommendations(ai_response)
        
        # Calculer les métriques
        productivity_score = calculate_productivity_score(tasks)
        completion_rate = calculate_completion_rate(tasks)
        task_distribution = calculate_task_distribution(tasks)
        
        return TaskHistoryResponse(
            summary=summary,
            insights=insights,
            recommendations=recommendations,
            productivity_score=productivity_score,
            completion_rate=completion_rate,
            task_distribution=task_distribution
        )
        
    except Exception as e:
        print(f"Erreur IA: {e}")
        return generate_basic_analysis(tasks)

def generate_basic_analysis(tasks: List) -> TaskHistoryResponse:
    """Générer une analyse basique sans IA"""
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == "completed"])
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Distribution par catégorie
    categories = {}
    for task in tasks:
        cat = task.category
        categories[cat] = categories.get(cat, 0) + 1
    
    return TaskHistoryResponse(
        summary=f"Vous avez {total_tasks} tâches au total, dont {completed_tasks} terminées.",
        insights=[
            f"Taux de complétion: {completion_rate:.1f}%",
            f"Catégorie la plus active: {max(categories.items(), key=lambda x: x[1])[0] if categories else 'Aucune'}"
        ],
        recommendations=[
            "Continuez à organiser vos priorités",
            "Prenez des pauses régulières",
            "Célébrez vos accomplissements"
        ],
        productivity_score=min(completion_rate, 100),
        completion_rate=completion_rate,
        task_distribution=categories
    )

async def archive_task(task_id: str, keep_memory: bool) -> Optional[dict]:
    """Archiver une tâche terminée"""
    # Pour l'instant, on marque juste comme archivée
    # Dans une vraie implémentation, on pourrait déplacer vers une collection d'archives
    task = await task_service.get_task_by_id(task_id)
    if task:
        # Ajouter un champ archived
        task.archived = keep_memory
        task.archived_at = datetime.utcnow()
        # Sauvegarder les modifications
        return {
            "id": task.id,
            "title": task.title,
            "archived": keep_memory,
            "archived_at": str(task.archived_at)
        }
    return None

def extract_summary(ai_response: str) -> str:
    """Extraire le résumé de la réponse IA"""
    # Logique simplifiée - dans un vrai cas, on utiliserait un parsing plus sophistiqué
    lines = ai_response.split('\n')
    for line in lines:
        if "résumé" in line.lower() or "productivité" in line.lower():
            return line.strip()
    return "Analyse de productivité terminée."

def extract_insights(ai_response: str) -> List[str]:
    """Extraire les insights de la réponse IA"""
    insights = []
    lines = ai_response.split('\n')
    for line in lines:
        if any(word in line.lower() for word in ["insight", "habitude", "tendance", "pattern"]):
            insights.append(line.strip())
    return insights[:5] if insights else ["Continuez votre excellent travail!"]

def extract_recommendations(ai_response: str) -> List[str]:
    """Extraire les recommandations de la réponse IA"""
    recommendations = []
    lines = ai_response.split('\n')
    for line in lines:
        if any(word in line.lower() for word in ["recommandation", "conseil", "suggestion", "améliorer"]):
            recommendations.append(line.strip())
    return recommendations[:5] if recommendations else ["Gardez votre rythme!"]

def calculate_productivity_score(tasks: List) -> float:
    """Calculer un score de productivité"""
    if not tasks:
        return 0.0
    
    completed = len([t for t in tasks if t.status == "completed"])
    total = len(tasks)
    
    # Score basé sur le taux de complétion et la diversité des catégories
    completion_score = (completed / total) * 70  # 70% du score
    
    # Bonus pour la diversité des catégories
    categories = set(t.category for t in tasks)
    diversity_score = min(len(categories) * 5, 30)  # 30% max pour la diversité
    
    return min(completion_score + diversity_score, 100)

def calculate_completion_rate(tasks: List) -> float:
    """Calculer le taux de complétion"""
    if not tasks:
        return 0.0
    
    completed = len([t for t in tasks if t.status == "completed"])
    return (completed / len(tasks)) * 100

def calculate_task_distribution(tasks: List) -> dict:
    """Calculer la distribution des tâches par catégorie"""
    distribution = {}
    for task in tasks:
        cat = task.category
        distribution[cat] = distribution.get(cat, 0) + 1
    return distribution 