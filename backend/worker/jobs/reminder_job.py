"""Reminder worker job - checks for tasks due in next 24 hours and logs reminder sent events."""

import uuid
import time
from datetime import datetime, timedelta, UTC
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, update
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from infrastructure.database import SessionLocal
from infrastructure.logging.config import get_logger
from domain.models.task import Task
from domain.audit.audit_event import AuditActionType
from application.audit.audit_logger import AuditLogger
from infrastructure.audit.audit_logger import AuditLoggerImpl
from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository

logger = get_logger(__name__)

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # Exponential backoff delays in seconds


def _process_single_reminder(db: Session, task: Task, now: datetime, last_24h: datetime) -> bool:
    """
    Process reminder for a single task with retry logic.
    
    Args:
        db: Database session
        task: Task to process
        now: Current timestamp
        last_24h: Timestamp 24 hours ago
    
    Returns:
        True if reminder was sent, False otherwise
    """
    for attempt in range(MAX_RETRIES):
        try:
            # Atomic check-and-set: only update if reminder not sent recently
            result = db.execute(
                update(Task)
                .where(
                    and_(
                        Task.id == task.id,
                        or_(
                            Task.reminder_sent_at.is_(None),
                            Task.reminder_sent_at < last_24h
                        )
                    )
                )
                .values(reminder_sent_at=now)
            )
            
            if result.rowcount == 0:
                # Reminder already sent (race condition or already processed)
                logger.debug("task_reminder_already_sent", task_id=task.id, message="Task already has reminder sent, skipping")
                return False
            
            # Commit transaction for this task
            db.commit()
            return True
            
        except (OperationalError, SQLAlchemyError) as e:
            # Transient database error - retry
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAYS[attempt]
                logger.warning(
                    "reminder_processing_transient_error",
                    task_id=task.id,
                    attempt=attempt + 1,
                    max_retries=MAX_RETRIES,
                    error=str(e),
                    retry_delay=delay,
                    message=f"Transient error processing reminder, retrying in {delay}s"
                )
                db.rollback()
                time.sleep(delay)
                continue
            else:
                # All retries exhausted
                logger.error(
                    "reminder_processing_failed_after_retries",
                    task_id=task.id,
                    max_retries=MAX_RETRIES,
                    error=str(e),
                    exc_info=True
                )
                db.rollback()
                return False
        except Exception as e:
            # Non-transient error - don't retry
            logger.error(
                "reminder_processing_non_transient_error",
                task_id=task.id,
                error=str(e),
                exc_info=True
            )
            db.rollback()
            return False
    
    return False


def process_reminders() -> None:
    """
    Process reminders for tasks due in the next 24 hours.
    
    This function:
    1. Queries tasks due in next 24 hours that haven't been reminded recently
    2. Logs "reminder sent" events for each qualifying task
    3. Marks tasks as having reminder sent (idempotency)
    4. Handles errors gracefully (continues with next task on error)
    5. Retries on transient failures with exponential backoff
    6. Logs audit events for reminder sent actions
    """
    db: Session = SessionLocal()
    worker_run_id = datetime.now(UTC).strftime("worker-run-%Y-%m-%d-%H-%M-%S")
    
    # Generate correlation ID for this worker run
    correlation_id = str(uuid.uuid4())
    
    # Bind correlation ID to logging context
    import structlog
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
    
    # Initialize audit logger
    audit_repository = SQLAlchemyAuditRepository(db)
    audit_logger = AuditLoggerImpl(audit_repository)
    
    try:
        logger.info("reminder_job_started", worker_run_id=worker_run_id, correlation_id=correlation_id)
        
        # Calculate time window: now to now + 24 hours
        now = datetime.now(UTC)
        next_24h = now + timedelta(hours=24)
        last_24h = now - timedelta(hours=24)
        
        # Query tasks due in next 24 hours that haven't been reminded in last 24 hours
        query = db.query(Task).filter(
            and_(
                Task.due_date >= now,
                Task.due_date <= next_24h,
                or_(
                    Task.reminder_sent_at.is_(None),
                    Task.reminder_sent_at < last_24h
                )
            )
        ).order_by(Task.due_date.asc())
        
        tasks = query.all()
        logger.info("reminder_job_tasks_found", task_count=len(tasks), worker_run_id=worker_run_id)
        
        reminders_sent = 0
        errors = 0
        
        for task in tasks:
            try:
                # Process reminder with retry logic
                success = _process_single_reminder(db, task, now, last_24h)
                
                if success:
                    # Log reminder sent event
                    logger.info(
                        "reminder_sent",
                        task_id=task.id,
                        due_date=task.due_date.isoformat() if task.due_date else None,
                        worker_run_id=worker_run_id
                    )
                    
                    # Log audit event (system action - user_id is None)
                    audit_logger.log(
                        action_type=AuditActionType.REMINDER_SENT,
                        user_id=None,  # System action, not user-driven
                        resource_type="reminder",
                        resource_id=str(task.id),
                        metadata={
                            "task_id": task.id,
                            "due_date": task.due_date.isoformat() if task.due_date else None
                        }
                    )
                    
                    reminders_sent += 1
                else:
                    # Already sent or failed after retries
                    # Refresh task to check current state
                    db.refresh(task)
                    if task.reminder_sent_at is None or task.reminder_sent_at < last_24h:
                        # Failed after retries
                        errors += 1
                    # Otherwise, already sent (not an error)
                    
            except Exception as e:
                # Unexpected error - log and continue
                logger.error(
                    "reminder_processing_unexpected_error",
                    task_id=task.id,
                    error=str(e),
                    exc_info=True
                )
                db.rollback()
                errors += 1
                continue
        
        logger.info(
            "reminder_job_completed",
            worker_run_id=worker_run_id,
            reminders_sent=reminders_sent,
            errors=errors,
            total_tasks=len(tasks)
        )
        
    except (OperationalError, SQLAlchemyError) as e:
        # Database connection error - retry on next scheduled run
        logger.error(
            "reminder_job_database_connection_error",
            worker_run_id=worker_run_id,
            error=str(e),
            message="Will retry on next scheduled run",
            exc_info=True
        )
        db.rollback()
    except Exception as e:
        logger.error(
            "reminder_job_fatal_error",
            worker_run_id=worker_run_id,
            error=str(e),
            exc_info=True
        )
        db.rollback()
    finally:
        db.close()
