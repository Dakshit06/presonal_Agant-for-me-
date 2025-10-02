"""
Agentice - Personal AI Assistant
Main FastAPI application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import structlog
import logging
import sys
import os

from src.config.settings import settings
from src.api.routes import (
    auth,
    tasks,
    events,
    emails,
    opportunities,
    resumes,
    applications,
    profiles,
    content,
    notifications,
    agents,
    websocket,
)
from src.database.session import init_db
from src.monitoring.metrics import setup_metrics

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Agentice Personal AI Assistant", environment=settings.ENVIRONMENT)
    
    # Initialize database
    await init_db()
    
    # Setup monitoring
    setup_metrics(app)
    
    logger.info("Agentice initialized successfully")
    
    yield
    
    logger.info("Shutting down Agentice")


# Create FastAPI application
app = FastAPI(
    title="Agentice - Personal AI Assistant",
    description="""
    Jarvis-like AI assistant for task management, career development, and automated job applications.
    
    Features:
    - Automated job search and application
    - Resume & cover letter customization
    - Task & email management
    - Calendar integration
    - Profile optimization (LinkedIn, GitHub, Portfolio)
    - Content generation & curation
    - Multi-agent system with AutoGen
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define frontend path (before creating app routes)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Create FastAPI application
app = FastAPI(
    title="Agentice - Personal AI Assistant",
    description="""
    Jarvis-like AI assistant for task management, career development, and automated job applications.
    
    Features:
    - Automated job search and application
    - Resume & cover letter customization
    - Task & email management
    - Calendar integration
    - Profile optimization (LinkedIn, GitHub, Portfolio)
    - Content generation & curation
    - Multi-agent system with AutoGen
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend - MUST be before route definitions
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/")
async def root():
    """Serve the frontend dashboard"""
    frontend_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(frontend_file):
        return FileResponse(frontend_file)
    return {
        "message": "Welcome to Agentice - Your Personal AI Assistant",
        "documentation": "/docs",
        "health": "/health",
        "note": "Frontend dashboard not found. Please ensure frontend files exist.",
    }

# Serve static files (CSS, JS) from frontend directory
@app.get("/style.css")
async def serve_css():
    css_file = os.path.join(frontend_path, "style.css")
    if os.path.exists(css_file):
        return FileResponse(css_file, media_type="text/css")
    return JSONResponse({"error": "CSS file not found"}, status_code=404)

@app.get("/app.js")
async def serve_js():
    js_file = os.path.join(frontend_path, "app.js")
    if os.path.exists(js_file):
        return FileResponse(js_file, media_type="application/javascript")
    return JSONResponse({"error": "JS file not found"}, status_code=404)

@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Welcome to Agentice API",
        "documentation": "/docs",
        "health": "/health",
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(websocket.router, prefix="/api/v1", tags=["WebSocket"])  # WebSocket for real-time chat
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(emails.router, prefix="/api/v1/emails", tags=["Emails"])
app.include_router(opportunities.router, prefix="/api/v1/opportunities", tags=["Opportunities"])
app.include_router(resumes.router, prefix="/api/v1/resumes", tags=["Resumes"])
app.include_router(applications.router, prefix="/api/v1/applications", tags=["Job Applications"])
app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["Profiles"])
app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["AI Agents"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        workers=settings.API_WORKERS if not settings.DEBUG else 1,
    )
