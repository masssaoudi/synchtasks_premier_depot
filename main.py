from fastapi import FastAPI, Request, WebSocket
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

# WebSocket - configuration simple à venir
from delegation_routes import router as delegation_router
from theme_routes import router as theme_router
from user_profile_routes import router as user_profile_router

from websocket_routes import router as websocket_router

try:
    from google_oauth_routes import router as google_oauth_router

    print("✅ Google OAuth routes importées avec succès")
except Exception as e:
    print(f"❌ Erreur import Google OAuth routes: {e}")
    google_oauth_router = None

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting SyncTasks API...")
    await connect_to_mongo()
    logger.info("✅ SyncTasks API started successfully!")
    logger.info("✅ Routes WebSocket enregistrées")

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
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:80",
        "http://127.0.0.1:80",
        "http://localhost",
        "http://127.0.0.1",
        "*",  # Temporaire pour le développement
    ],
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
    logger.info(
        f"📤 {request.method} {request.url} - {response.status_code} - {process_time:.3f}s"
    )

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
            "detail": (
                str(exc) if settings.DEBUG else "Une erreur inattendue s'est produite"
            ),
        },
    )


# Include routes
app.include_router(router)
app.include_router(auth_router)
app.include_router(ia_router)
app.include_router(delegation_router)
app.include_router(theme_router, prefix="/api")
app.include_router(user_profile_router, prefix="/api")
app.include_router(websocket_router, prefix="/api")
if google_oauth_router:
    app.include_router(google_oauth_router, prefix="/api")
    logger.info("✅ Routes Google OAuth enregistrées")
else:
    logger.warning("⚠️ Routes Google OAuth non disponibles")

logger.info("✅ Routes WebSocket simples enregistrées")


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "SyncTasks API",
        "version": "1.0.0",
        "description": "API pour la gestion de tâches avec IA",
        "docs": "/docs",
        "frontend": "http://localhost:3000",
    }


@app.get("/api", tags=["api"])
async def api_info():
    """API information endpoint"""
    return {
        "message": "SyncTasks API",
        "version": "1.0.0",
        "description": "API minimaliste pour la gestion de tâches",
        "docs": "/docs",
        "health": "/api/tasks/health",
    }


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": time.time(), "service": "synchtasks-api"}


# Database ping endpoint
@app.get("/ping-db", tags=["database"])
async def ping_db():
    """Test database connection"""
    try:
        from database import get_database

        db = get_database()
        await db.command("ping")
        return {
            "status": "ok",
            "message": "MongoDB connection successful",
            "timestamp": time.time(),
        }
    except Exception as e:
        return {"error": str(e), "status": "failed", "timestamp": time.time()}


# WebSocket endpoints à recréer


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
