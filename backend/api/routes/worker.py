"""Worker API routes - status, manual trigger, statistics."""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from infrastructure.database import get_db
from domain.models.user import User
from domain.models.task import Task
from api.middleware.auth import get_current_user
from worker.scheduler import get_scheduler
from worker.jobs.reminder_job import process_reminders

router = APIRouter(prefix="/api/worker", tags=["worker"])


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"}
    }
)
def get_worker_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get worker status and information.
    
    Returns:
    - Worker running status
    - Next scheduled run time
    - Last run information (if available)
    """
    scheduler = get_scheduler()
    
    if scheduler is None or not scheduler.running:
        return {
            "status": "stopped",
            "running": False,
            "next_run": None,
            "message": "Worker scheduler is not running"
        }
    
    # Get next run time
    job = scheduler.get_job('reminder_job')
    next_run = job.next_run_time if job else None
    
    # Get last run info from database (check most recent reminder_sent_at)
    db: Session = next(get_db())
    try:
        last_reminder = db.query(func.max(Task.reminder_sent_at)).scalar()
        
        return {
            "status": "running",
            "running": True,
            "next_run": next_run.isoformat() if next_run else None,
            "last_reminder_sent": last_reminder.isoformat() if last_reminder else None,
            "schedule": "Every hour",
            "message": "Worker is running and will check for due tasks every hour"
        }
    except Exception:
        return {
            "status": "running",
            "running": True,
            "next_run": next_run.isoformat() if next_run else None,
            "last_reminder_sent": None,
            "schedule": "Every hour",
            "message": "Worker is running and will check for due tasks every hour"
        }
    finally:
        db.close()


@router.post(
    "/trigger",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"},
        503: {"description": "Worker not available"}
    }
)
def trigger_worker_manually(
    current_user: User = Depends(get_current_user)
):
    """
    Manually trigger the reminder worker job.
    
    This will immediately run the reminder check process.
    Useful for testing or manual execution.
    """
    try:
        # Run reminder job manually
        process_reminders()
        
        return {
            "status": "success",
            "message": "Reminder worker job executed successfully",
            "triggered_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "WORKER_ERROR",
                    "message": f"Failed to execute worker job: {str(e)}"
                }
            }
        )


@router.get(
    "/statistics",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"}
    }
)
def get_worker_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get worker statistics.
    
    Returns:
    - Total tasks with reminders sent
    - Tasks due in next 24 hours
    - Tasks due in next 24 hours that need reminders
    - Recent reminder activity
    """
    now = datetime.utcnow()
    next_24h = now + timedelta(hours=24)
    last_24h = now - timedelta(hours=24)
    
    # Total tasks with reminders sent
    total_with_reminders = db.query(func.count(Task.id)).filter(
        Task.reminder_sent_at.isnot(None)
    ).scalar()
    
    # Tasks due in next 24 hours
    tasks_due_next_24h = db.query(func.count(Task.id)).filter(
        and_(
            Task.due_date >= now,
            Task.due_date <= next_24h
        )
    ).scalar()
    
    # Tasks due in next 24 hours that need reminders
    tasks_needing_reminders = db.query(func.count(Task.id)).filter(
        and_(
            Task.due_date >= now,
            Task.due_date <= next_24h,
            or_(
                Task.reminder_sent_at.is_(None),
                Task.reminder_sent_at < last_24h
            )
        )
    ).scalar()
    
    # Recent reminders (last 24 hours)
    recent_reminders = db.query(func.count(Task.id)).filter(
        Task.reminder_sent_at >= last_24h
    ).scalar()
    
    return {
        "statistics": {
            "total_tasks_with_reminders": total_with_reminders or 0,
            "tasks_due_next_24h": tasks_due_next_24h or 0,
            "tasks_needing_reminders": tasks_needing_reminders or 0,
            "recent_reminders_24h": recent_reminders or 0
        },
        "timestamp": now.isoformat()
    }
