r"""
Task Tracker API - Enterprise-grade task management system.

A comprehensive RESTful API for secure task management with advanced features including 
authentication, file attachments, search capabilities, notifications, comprehensive audit trails, and rate limiting.
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

from contextlib import asynccontextmanager
from fastapi import FastAPI
from infrastructure.database import init_db
from infrastructure.auth.config import auth_config
from infrastructure.logging.config import configure_structured_logging, get_logger
from api.routes import auth, tasks, attachments, worker, metrics
from api.middleware.rate_limiting import RateLimitingMiddleware
from api.middleware.correlation_id import CorrelationIDMiddleware
from api.middleware.metrics import MetricsMiddleware
from worker.scheduler import start_scheduler, stop_scheduler
import os

# API Metadata - automatically used by FastAPI
API_VERSION = os.getenv("API_VERSION", "1.0.0")
API_TITLE = "Task Tracker API"
API_AUTHOR = "Michael Wybraniec"

# Initialize database
init_db()

# Configure structured logging (must be done before creating loggers)
configure_structured_logging()
logger = get_logger(__name__)

# Validate auth config on startup
try:
    auth_config.validate()
except ValueError as e:
    logger.warning("auth_config_validation_failed", error=str(e), message="Please set JWT_SECRET_KEY environment variable (min 32 characters)")

# Build dynamic API description with rate limiting info
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_WINDOW_MINUTES = RATE_LIMIT_WINDOW_SECONDS // 60

api_description = __doc__.strip()

if RATE_LIMIT_ENABLED:
    api_description += f"""

**Rate Limiting:**
- Rate limiting is applied to all API endpoints ({RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW_MINUTES} minute{'s' if RATE_LIMIT_WINDOW_MINUTES != 1 else ''} per user/IP)
- Authenticated requests are rate-limited per user (based on user ID)
- Unauthenticated requests are rate-limited per IP address
- When rate limit is exceeded, the API returns HTTP 429 (Too Many Requests) with:
  - Error message: "Rate limit exceeded. Please try again in X seconds."
  - `Retry-After` header: Seconds until limit resets
  - `X-RateLimit-Limit` header: Maximum requests per window
  - `X-RateLimit-Remaining` header: Remaining requests in current window
- Health check endpoint (`/health`) is excluded from rate limiting
- Configure via environment variables: `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW_SECONDS`
"""
else:
    api_description += "\n\n**Note:** Rate limiting is currently disabled."


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    if os.getenv("ENVIRONMENT") != "test":
        try:
            start_scheduler()
            logger.info("worker_scheduler_started", message="Worker scheduler started successfully")
        except Exception as e:
            logger.error("worker_scheduler_start_failed", error=str(e), exc_info=True)
    
    yield
    
    # Shutdown
    try:
        stop_scheduler()
        logger.info("worker_scheduler_stopped", message="Worker scheduler stopped successfully")
    except Exception as e:
        logger.error("worker_scheduler_stop_failed", error=str(e), exc_info=True)
    
    # Close Redis connection
    try:
        from infrastructure.rate_limiting.redis_client import close_redis_client
        close_redis_client()
        logger.info("redis_client_closed", message="Redis client closed successfully")
    except Exception as e:
        logger.error("redis_client_close_failed", error=str(e), exc_info=True)


app = FastAPI(
    title=API_TITLE,
    description=api_description,  # Dynamic description with rate limiting info
    version=API_VERSION,
    contact={
        "name": API_AUTHOR,
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
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
app.include_router(metrics.router)

# Add middleware (order matters: correlation ID first, then rate limiting)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(RateLimitingMiddleware)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Task Tracker API"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
