from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from typing import Optional, List

from config import settings
from database import connect_to_mongo, close_mongo_connection
from routes import router
from auth_routes import router as auth_router
from ia_routes import router as ia_router
from models import TaskInDB
from ws_manager import manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting SyncTasks API...")
    await connect_to_mongo()
    logger.info("✅ SyncTasks API started successfully!")
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down SyncTasks API...")
    await close_mongo_connection()
    logger.info("✅ SyncTasks API shutdown complete!")

# Create FastAPI app
app = FastAPI(
    title="SyncTasks API",
    description="API minimaliste pour la gestion de tâches",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"📥 {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"📤 {request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
    
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erreur interne du serveur",
            "detail": str(exc) if settings.DEBUG else "Une erreur inattendue s'est produite"
        }
    )

# Include routes
app.include_router(router)
app.include_router(auth_router)
app.include_router(ia_router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "SyncTasks API",
        "version": "1.0.0",
        "description": "API pour la gestion de tâches avec IA",
        "docs": "/docs",
        "frontend": "http://localhost:3000"
    }

@app.get("/api", tags=["api"])
async def api_info():
    """API information endpoint"""
    return {
        "message": "SyncTasks API",
        "version": "1.0.0",
        "description": "API minimaliste pour la gestion de tâches",
        "docs": "/docs",
        "health": "/api/tasks/health"
    }

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "synchtasks-api"
    }

# WebSocket endpoint pour la synchronisation temps réel
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket pour la synchronisation temps réel des tâches"""
    await manager.connect(websocket)
    try:
        while True:
            # Écouter les messages du client
            data = await websocket.receive_text()
            logger.info(f"📨 Message WebSocket reçu: {data}")
            
            # Pour l'instant, on peut juste logger les messages
            # Plus tard, on pourra traiter des commandes spécifiques
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("🔌 WebSocket déconnecté")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    ) 