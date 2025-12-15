"""Worker scheduler setup using APScheduler."""

import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from worker.jobs.reminder_job import process_reminders

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def start_scheduler() -> None:
    """Start the background scheduler."""
    global scheduler
    
    if scheduler is not None and scheduler.running:
        logger.warning("Scheduler is already running")
        return
    
    scheduler = BackgroundScheduler()
    
    # Add reminder job: run every hour
    scheduler.add_job(
        process_reminders,
        trigger=IntervalTrigger(hours=1),
        id='reminder_job',
        name='Process reminders for tasks due in next 24 hours',
        replace_existing=True,
        max_instances=1  # Prevent concurrent runs
    )
    
    scheduler.start()
    logger.info("Worker scheduler started - reminder job will run every hour")
    
    # Register shutdown handler
    atexit.register(stop_scheduler)


def stop_scheduler() -> None:
    """Stop the background scheduler."""
    global scheduler
    
    if scheduler is None or not scheduler.running:
        return
    
    scheduler.shutdown(wait=True)
    logger.info("Worker scheduler stopped")
    scheduler = None


def get_scheduler() -> BackgroundScheduler:
    """Get the scheduler instance."""
    return scheduler
