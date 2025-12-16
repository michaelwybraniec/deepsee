r"""
Task Tracker API - Enterprise-grade task management system.

A comprehensive RESTful API for secure task management with advanced features including 
authentication, file attachments, search capabilities, notifications, and comprehensive audit trails.
```text


                        ____
                      (xXXXX|xx======---(-
                      /     |
                     /    XX|
                    /xxx XXX|
                   /xxx X   |
                  / ________|
          __ ____/_|_|_______\_
      ###|=||________|_________|_
          ~~   |==| __  _  __   /|~~~~~~~~~-------------_______
               |==| ||(( ||()| | |XXXXXXXX|                    >
          __   |==| ~~__~__~~__ \|_________-------------~~~~~~~
      ###|=||~~~~~~~~|_______  |"
          ~~ ~~~~\~|~|       /~
                  \ ~~~~~~~~~
                   \xxx X   |
                    \xxx XXX|
                     \    XX|                Incom's T-65B X-wing Space
                      \     |                Superiority Starfighter (4)
                      (xXXXX|xx======---(-
                        ~~~~                 The same as this API.



```


"""

from fastapi import FastAPI
from infrastructure.database import init_db
from infrastructure.auth.config import auth_config
from api.routes import auth, tasks, attachments, worker
from api.middleware.rate_limiting import RateLimitingMiddleware
from worker.scheduler import start_scheduler, stop_scheduler
import os
import logging

# API Metadata - automatically used by FastAPI
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_TITLE = "Task Tracker API"
API_AUTHOR = "Michael Wybraniec"

# Initialize database
init_db()

# Validate auth config on startup
try:
    auth_config.validate()
except ValueError as e:
    print(f"Warning: Auth configuration validation failed: {e}")
    print("Please set JWT_SECRET_KEY environment variable (min 32 characters)")

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
app.include_router(attachments.router)
app.include_router(worker.router)

# Add rate limiting middleware
app.add_middleware(RateLimitingMiddleware)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Task Tracker API"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    # Start worker scheduler (only if not in test mode)
    if os.getenv("ENVIRONMENT") != "test":
        try:
            start_scheduler()
        except Exception as e:
            logging.error(f"Failed to start worker scheduler: {e}", exc_info=True)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    # Stop worker scheduler
    try:
        stop_scheduler()
    except Exception as e:
        logging.error(f"Error stopping worker scheduler: {e}", exc_info=True)
    
    # Close Redis connection
    try:
        from infrastructure.rate_limiting.redis_client import close_redis_client
        close_redis_client()
    except Exception as e:
        logging.error(f"Error closing Redis client: {e}", exc_info=True)
