"""
Task Tracker API - Enterprise-grade task management system.

A comprehensive RESTful API for secure task management with advanced features including 
authentication, file attachments, search capabilities, notifications, and comprehensive audit trails.

## Architecture

Built following **Clean Architecture** principles with clear separation of concerns across 
domain, application, and infrastructure layers. Developed using the **Agentic Workflow Protocol (AWP)** 
for structured, systematic development. See `agentic-sdlc/AWP.md` for workflow details.

## Key Features

- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Task Management**: Full CRUD operations with ownership-based authorization
- **File Attachments**: Upload and manage files associated with tasks
- **Advanced Search**: Filter and search tasks by multiple criteria
- **Notifications**: Automated reminder system for due tasks
- **Audit Trail**: Comprehensive logging of all system actions
- **Rate Limiting**: Per-user and per-IP request rate limiting
- **Monitoring**: Structured logging with correlation IDs and health checks

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Authentication**: JWT tokens with python-jose
- **Validation**: Pydantic for request/response validation

## Author

Michael Wybraniec (ONE-FRONT)
"""

from fastapi import FastAPI
from infrastructure.database import init_db
from infrastructure.auth.config import auth_config
from api.routes import auth, tasks
import os

# API Metadata - automatically used by FastAPI
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_TITLE = "Task Tracker API"
API_AUTHOR = "Michael Wybraniec (ONE-FRONT)"

# Initialize database
init_db()

# Validate auth config on startup
try:
    auth_config.validate()
except ValueError as e:
    print(f"Warning: Auth configuration validation failed: {e}")
    print("Please set JWT_SECRET_KEY environment variable (min 32 characters)")

app = FastAPI(
    title=API_TITLE,
    description=__doc__,  # Automatically uses module docstring above
    version=API_VERSION,
    contact={
        "name": API_AUTHOR,
    },
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
app.include_router(tasks.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Task Tracker API"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
