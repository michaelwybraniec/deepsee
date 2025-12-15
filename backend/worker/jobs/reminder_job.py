"""Reminder worker job - checks for tasks due in next 24 hours and logs reminder sent events."""

import logging
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from infrastructure.database import SessionLocal
from domain.models.task import Task

logger = logging.getLogger(__name__)


def process_reminders() -> None:
    """
    Process reminders for tasks due in the next 24 hours.
    
    This function:
    1. Queries tasks due in next 24 hours that haven't been reminded recently
    2. Logs "reminder sent" events for each qualifying task
    3. Marks tasks as having reminder sent (idempotency)
    4. Handles errors gracefully (continues with next task on error)
    """
    db: Session = SessionLocal()
    worker_run_id = datetime.utcnow().strftime("worker-run-%Y-%m-%d-%H-%M-%S")
    
    try:
        logger.info(f"Starting reminder job run: {worker_run_id}")
        
        # Calculate time window: now to now + 24 hours
        now = datetime.utcnow()
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
        logger.info(f"Found {len(tasks)} tasks due in next 24 hours")
        
        reminders_sent = 0
        errors = 0
        
        for task in tasks:
            try:
                # Atomic check-and-set: only update if reminder not sent recently
                from sqlalchemy import update
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
                
                if result == 0:
                    # Reminder already sent (race condition or already processed)
                    logger.debug(f"Task {task.id} already has reminder sent, skipping")
                    continue
                
                # Log reminder sent event
                logger.info(
                    f"Reminder sent for task {task.id} (due: {task.due_date}), "
                    f"worker_run_id: {worker_run_id}"
                )
                
                # Commit transaction for this task
                db.commit()
                reminders_sent += 1
                
            except Exception as e:
                # Log error and continue with next task
                logger.error(
                    f"Error processing reminder for task {task.id}: {str(e)}",
                    exc_info=True
                )
                db.rollback()
                errors += 1
                continue
        
        logger.info(
            f"Reminder job completed: {worker_run_id}, "
            f"reminders_sent: {reminders_sent}, errors: {errors}"
        )
        
    except Exception as e:
        logger.error(f"Fatal error in reminder job {worker_run_id}: {str(e)}", exc_info=True)
        db.rollback()
    finally:
        db.close()
