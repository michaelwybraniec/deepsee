# Worker Design: Reminder Notification System

## Overview

This document describes the design for the background worker that checks for tasks due in the next 24 hours and logs "reminder sent" events in an idempotent and fault-tolerant way.

## Scheduling Mechanism

### Schedule Frequency
**Decision**: Run every hour at :00 minutes (e.g., 1:00, 2:00, 3:00, etc.)

**Rationale**:
- Balance between responsiveness and resource usage
- Ensures tasks are checked regularly without excessive database queries
- Simple to implement and understand
- Allows for timely reminders (tasks due within 24h are checked at least once per hour)

### Scheduling Library
**Decision**: Use `APScheduler` (Advanced Python Scheduler) 3.10+

**Rationale**:
- Simple, no external dependencies (no message broker required)
- Supports interval-based and cron-based scheduling
- Easy to integrate with FastAPI application
- Lightweight compared to `celery` (which requires Redis/RabbitMQ)
- Recommended in `docs/technology.md` for worker scheduling

**Implementation**:
```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler()
scheduler.add_job(
    process_reminders,
    trigger=IntervalTrigger(hours=1),
    id='reminder_job',
    replace_existing=True
)
scheduler.start()
```

## Query Logic

### "Due in Next 24 Hours" Query

**Definition**: Tasks where `due_date` is between `NOW()` and `NOW() + 24 hours`.

**SQL Query**:
```sql
SELECT * FROM tasks 
WHERE due_date >= NOW() 
  AND due_date <= NOW() + INTERVAL '24 hours'
  AND (reminder_sent_at IS NULL OR reminder_sent_at < NOW() - INTERVAL '24 hours')
ORDER BY due_date ASC;
```

**SQLAlchemy Query**:
```python
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

now = datetime.utcnow()
next_24h = now + timedelta(hours=24)
last_24h = now - timedelta(hours=24)

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
```

### Timezone Handling
**Decision**: Use UTC for all datetime operations

**Rationale**:
- Consistent across different server timezones
- Avoids daylight saving time issues
- Standard practice for backend systems
- Database stores timestamps in UTC

### Query Efficiency
- Index on `due_date` column (already exists in Task model)
- Index on `reminder_sent_at` column (to be added)
- Query uses indexed columns for efficient filtering

## Idempotency Mechanism

### Tracking Reminders
**Decision**: Use `reminder_sent_at` timestamp column on `tasks` table

**Rationale**:
- Simple and efficient (no separate table needed)
- Directly associated with task
- Easy to query and update
- Atomic updates prevent race conditions

### Idempotency Check
**Logic**: 
- Before logging reminder, check if `reminder_sent_at` is NULL or older than 24 hours
- Use atomic database update to prevent race conditions:
  ```sql
  UPDATE tasks 
  SET reminder_sent_at = NOW() 
  WHERE id = ? 
    AND (reminder_sent_at IS NULL OR reminder_sent_at < NOW() - INTERVAL '24 hours')
  RETURNING id;
  ```
- Only update if no recent reminder (atomic check-and-set)

### Atomic Operations
**Implementation**:
- Use database transaction for each task reminder
- Atomic UPDATE with WHERE condition ensures only one worker can set reminder
- If UPDATE returns 0 rows, reminder was already sent (skip)

**Example**:
```python
# Atomic check-and-set
result = db.execute(
    update(Task)
    .where(
        and_(
            Task.id == task_id,
            or_(
                Task.reminder_sent_at.is_(None),
                Task.reminder_sent_at < (datetime.utcnow() - timedelta(hours=24))
            )
        )
    )
    .values(reminder_sent_at=datetime.utcnow())
    .returning(Task.id)
)
if result.rowcount == 0:
    # Reminder already sent, skip
    continue
```

## Fault Tolerance Strategy

### Error Handling

1. **Database Connection Errors**:
   - Retry connection with exponential backoff (1s, 2s, 4s)
   - Max 3 retries
   - If all retries fail: log error, skip this run, continue on next schedule

2. **Individual Task Processing Errors**:
   - Wrap each task processing in try-catch
   - Log error with task ID and error details
   - Continue with next task (don't crash entire run)
   - Failed tasks can be retried on next run

3. **Worker Restartability**:
   - State stored in database (`reminder_sent_at` column)
   - Worker can restart and resume without duplicates
   - No in-memory state that could be lost on restart

### Transaction Boundaries
- Process each task reminder in its own transaction
- If reminder logging fails, transaction rolls back (no partial state)
- Ensures consistency even on failures

### Retry Strategy
- **Transient failures**: Retry with exponential backoff (1s, 2s, 4s)
- **Max retries**: 3 attempts
- **Permanent failures**: Log error, skip task, continue with next task
- **Idempotency on retries**: Check `reminder_sent_at` even on retries (if reminder was sent during retry, skip)

## Reminder Logging

### Audit Trail Integration
**Decision**: Log reminder events to audit trail (separate `audit_log` table or existing audit system)

**Log Entry Fields**:
- `task_id`: ID of the task
- `action`: "reminder_sent"
- `timestamp`: When reminder was logged
- `worker_run_id`: Optional identifier for this worker run (for debugging)

### Logging Format
```python
{
    "task_id": 123,
    "action": "reminder_sent",
    "timestamp": "2024-01-15T10:00:00Z",
    "worker_run_id": "worker-run-2024-01-15-10-00-00"
}
```

## Worker Architecture

### Directory Structure
```
backend/
  worker/
    __init__.py
    scheduler.py          # APScheduler setup
    jobs/
      __init__.py
      reminder_job.py     # Reminder processing logic
    models/
      __init__.py
      audit_log.py        # Audit log model (if separate table)
```

### Worker Service
- Separate service/process (can run in same container as API or separate)
- Can be started independently: `python -m worker.scheduler`
- Integrates with FastAPI app lifecycle (start on app startup, shutdown on app shutdown)

### Database Connection
- Use same database connection pool as API
- Or separate connection pool for worker (recommended for isolation)
- Connection pool handles connection errors and retries

## Implementation Notes

### Scheduling Integration
- Start scheduler when worker service starts
- Stop scheduler gracefully on shutdown (handle SIGTERM/SIGINT)
- Scheduler runs in background thread (doesn't block main process)

### Query Performance
- Index on `due_date` (already exists)
- Index on `reminder_sent_at` (to be added)
- Query uses indexed columns for efficient filtering
- Limit query to reasonable batch size if needed (e.g., 1000 tasks per run)

### Monitoring
- Log worker run start/end times
- Log number of tasks processed
- Log number of reminders sent
- Log errors and retries
- Use structured logging (JSON format) for easy parsing

## Summary

**Schedule**: Run every hour at :00 minutes using `APScheduler`

**Query**: Select tasks where `due_date` is between NOW() and NOW() + 24 hours, excluding tasks with `reminder_sent_at` within last 24 hours

**Idempotency**: Use `reminder_sent_at` timestamp column with atomic UPDATE operations

**Fault Tolerance**: 
- Retry database connection errors (exponential backoff, 3 retries)
- Handle individual task errors gracefully (log, continue)
- Worker is restartable (state in database)

**Logging**: Log reminder events to audit trail with task_id, action, timestamp

This design ensures idempotent, fault-tolerant reminder processing without duplicates.
