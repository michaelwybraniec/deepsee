"""Health check endpoints."""

import time
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from infrastructure.database import get_db
from infrastructure.logging.config import get_logger
from worker.scheduler import get_scheduler

router = APIRouter(prefix="/api", tags=["health"])

logger = get_logger(__name__)

# Health check timeout (seconds)
HEALTH_CHECK_TIMEOUT = 5.0


def check_database_health(db: Session) -> tuple[bool, str]:
    """
    Check database connectivity.
    
    Args:
        db: Database session
    
    Returns:
        Tuple of (is_healthy: bool, message: str)
    """
    try:
        # Execute simple query with timeout
        start_time = time.time()
        result = db.execute(text("SELECT 1"))
        duration = time.time() - start_time
        
        if duration > HEALTH_CHECK_TIMEOUT:
            return False, f"Database query timeout ({duration:.2f}s > {HEALTH_CHECK_TIMEOUT}s)"
        
        # Verify result
        result.fetchone()
        return True, "Database is healthy"
    except Exception as e:
        return False, f"Database error: {str(e)}"


def check_worker_health() -> tuple[bool, str]:
    """
    Check worker health by verifying scheduler is running and recent.
    
    Returns:
        Tuple of (is_healthy: bool, message: str)
    """
    scheduler = get_scheduler()
    
    if scheduler is None or not scheduler.running:
        return False, "Worker scheduler is not running"
    
    # Check if reminder job exists and is scheduled
    jobs = scheduler.get_jobs()
    reminder_job = next((job for job in jobs if job.id == 'reminder_job'), None)
    
    if reminder_job is None:
        return False, "Reminder job is not scheduled"
    
    return True, "Worker scheduler is running"


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check endpoint.
    
    Checks:
    - API: Always healthy if endpoint responds
    - Database: Connectivity check
    - Worker: Scheduler status check
    
    Returns:
    - 200 OK if all checks pass
    - 503 Service Unavailable if any check fails
    """
    checks = {}
    all_healthy = True
    
    # API check (always healthy if endpoint responds)
    checks["api"] = {"status": "healthy", "message": "API is responding"}
    
    # Database check
    db_healthy, db_message = check_database_health(db)
    checks["database"] = {
        "status": "healthy" if db_healthy else "unhealthy",
        "message": db_message
    }
    if not db_healthy:
        all_healthy = False
    
    # Worker check
    worker_healthy, worker_message = check_worker_health()
    checks["worker"] = {
        "status": "healthy" if worker_healthy else "unhealthy",
        "message": worker_message
    }
    if not worker_healthy:
        all_healthy = False
    
    # Determine overall status
    overall_status = "healthy" if all_healthy else "unhealthy"
    http_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    response_data = {
        "status": overall_status,
        "checks": checks
    }
    
    return JSONResponse(
        content=response_data,
        status_code=http_status
    )


@router.get("/health/api")
def health_check_api():
    """API health check only."""
    return {
        "status": "healthy",
        "check": "api",
        "message": "API is responding"
    }


@router.get("/health/database")
def health_check_database(db: Session = Depends(get_db)):
    """Database health check only."""
    is_healthy, message = check_database_health(db)
    
    http_status = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        content={
            "status": "healthy" if is_healthy else "unhealthy",
            "check": "database",
            "message": message
        },
        status_code=http_status
    )


@router.get("/health/worker")
def health_check_worker():
    """Worker health check only."""
    is_healthy, message = check_worker_health()
    
    http_status = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        content={
            "status": "healthy" if is_healthy else "unhealthy",
            "check": "worker",
            "message": message
        },
        status_code=http_status
    )
