"""Main FastAPI application."""

from fastapi import FastAPI
from infrastructure.database import init_db
from infrastructure.auth.config import auth_config
from api.routes import auth

# Initialize database
init_db()

# Validate auth config on startup
try:
    auth_config.validate()
except ValueError as e:
    print(f"Warning: Auth configuration validation failed: {e}")
    print("Please set JWT_SECRET_KEY environment variable (min 32 characters)")

app = FastAPI(
    title="Task Tracker API",
    description="""
    Task Tracker API - Full-stack task management application.
    
    **Built with Agentic Workflow Protocol (AWP)** - See `agentic-sdlc/AWP.md` for structured development workflow.
    
    Features: JWT authentication, task management, file attachments, search & filtering, notifications, audit trail.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    # Simple, standard Swagger UI styling
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
    }
)

# Include routers
app.include_router(auth.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Task Tracker API"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
