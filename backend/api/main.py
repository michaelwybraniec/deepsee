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
    description="Task Tracker API with authentication",
    version="1.0.0"
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
