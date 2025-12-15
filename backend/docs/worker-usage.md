# Reminder Worker Usage Guide

## Overview

The reminder worker is a background service that automatically checks for tasks due in the next 24 hours and logs "reminder sent" events. It runs automatically when the API starts.

## How It Works

1. **Scheduling**: The worker runs every hour automatically (using APScheduler)
2. **Query**: Finds tasks where:
   - `due_date` is between NOW() and NOW() + 24 hours
   - `reminder_sent_at` is NULL or older than 24 hours (idempotency check)
3. **Action**: For each qualifying task:
   - Logs "reminder sent" event
   - Sets `reminder_sent_at` timestamp (atomic operation)
4. **Idempotency**: Same task won't get duplicate reminders in the same 24-hour window
5. **Retry**: Automatically retries on transient database errors (exponential backoff: 1s, 2s, 4s)

## Automatic Startup

The worker starts automatically when the FastAPI application starts (unless `ENVIRONMENT=test`).

```bash
# Start API (worker starts automatically)
cd backend
uvicorn api.main:app --reload
```

The worker scheduler is integrated with FastAPI lifecycle:
- **Startup**: Worker scheduler starts automatically
- **Shutdown**: Worker scheduler stops gracefully

## Manual Testing

### Test the Worker Function Directly

```python
from worker.jobs.reminder_job import process_reminders

# Run reminder job manually
process_reminders()
```

### Test with Sample Data

```python
from datetime import datetime, timedelta
from domain.models.task import Task
from domain.models.user import User
from infrastructure.database import SessionLocal
from worker.jobs.reminder_job import process_reminders

db = SessionLocal()

# Create a task due in 12 hours
now = datetime.utcnow()
task = Task(
    title="Test Task",
    due_date=now + timedelta(hours=12),
    owner_user_id=user_id,
    status="todo"
)
db.add(task)
db.commit()

# Run worker
process_reminders()

# Check if reminder was sent
db.refresh(task)
print(f"Reminder sent at: {task.reminder_sent_at}")
```

## Checking Worker Status

### View Logs

The worker logs all activities. Check logs for:
- Worker run start/end times
- Number of tasks found
- Number of reminders sent
- Errors (if any)

Example log output:
```
INFO - Starting reminder job run: worker-run-2024-01-15-10-00-00
INFO - Found 5 tasks due in next 24 hours
INFO - Reminder sent for task 123 (due: 2024-01-15 22:00:00), worker_run_id: worker-run-2024-01-15-10-00-00
INFO - Reminder job completed: worker-run-2024-01-15-10-00-00, reminders_sent: 5, errors: 0
```

### Check Database

Query tasks to see which ones have reminders:

```sql
-- Tasks with reminders sent
SELECT id, title, due_date, reminder_sent_at 
FROM tasks 
WHERE reminder_sent_at IS NOT NULL
ORDER BY reminder_sent_at DESC;

-- Tasks due soon that haven't been reminded
SELECT id, title, due_date, reminder_sent_at
FROM tasks
WHERE due_date >= NOW()
  AND due_date <= NOW() + INTERVAL '24 hours'
  AND (reminder_sent_at IS NULL OR reminder_sent_at < NOW() - INTERVAL '24 hours')
ORDER BY due_date ASC;
```

## Configuration

### Schedule Frequency

Default: Every hour. To change, edit `backend/worker/scheduler.py`:

```python
scheduler.add_job(
    process_reminders,
    trigger=IntervalTrigger(hours=1),  # Change this
    ...
)
```

### Retry Configuration

Default: 3 retries with delays [1s, 2s, 4s]. To change, edit `backend/worker/jobs/reminder_job.py`:

```python
MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # Change these
```

## Disabling Worker (for Testing)

Set `ENVIRONMENT=test` to prevent worker from starting:

```bash
export ENVIRONMENT=test
uvicorn api.main:app --reload
```

## Troubleshooting

### Worker Not Running

1. Check if scheduler started:
   - Look for log: `"Worker scheduler started - reminder job will run every hour"`
   - Check if `ENVIRONMENT=test` is set (disables worker)

2. Check for errors:
   - Look for error logs in console
   - Check database connection

### No Reminders Being Sent

1. Check if tasks are due in next 24 hours:
   ```sql
   SELECT * FROM tasks 
   WHERE due_date >= NOW() 
     AND due_date <= NOW() + INTERVAL '24 hours';
   ```

2. Check if tasks already have reminders:
   ```sql
   SELECT * FROM tasks 
   WHERE reminder_sent_at IS NOT NULL 
     AND reminder_sent_at > NOW() - INTERVAL '24 hours';
   ```

3. Check worker logs for errors

### Duplicate Reminders

The worker is idempotent by design. If you see duplicates:
1. Check if multiple workers are running (should only be one)
2. Check database for race conditions
3. Verify `reminder_sent_at` column is being set correctly

## Running Tests

```bash
# Run worker tests
cd backend
pytest tests/test_worker_reminders.py -v

# Run all tests
pytest tests/ -v
```

## Example: Full Test Scenario

```python
from datetime import datetime, timedelta
from infrastructure.database import SessionLocal, init_db, engine, Base
from domain.models.user import User
from domain.models.task import Task
from worker.jobs.reminder_job import process_reminders
import bcrypt

# Setup
init_db()
db = SessionLocal()

# Create user
user = User(username="test", email="test@test.com", 
            hashed_password=bcrypt.hashpw(b"pass", bcrypt.gensalt()).decode('utf-8'))
db.add(user)
db.commit()

# Create tasks
now = datetime.utcnow()
task1 = Task(title="Due soon", due_date=now + timedelta(hours=12), owner_user_id=user.id)
task2 = Task(title="Due later", due_date=now + timedelta(hours=30), owner_user_id=user.id)
db.add_all([task1, task2])
db.commit()

# Run worker
process_reminders()

# Check results
db.refresh(task1)
db.refresh(task2)
print(f"Task 1 reminder: {task1.reminder_sent_at}")  # Should have timestamp
print(f"Task 2 reminder: {task2.reminder_sent_at}")  # Should be None (beyond 24h)

db.close()
```

## Integration with API

The worker runs in the same process as the FastAPI application. It:
- Shares the same database connection pool
- Uses the same logging configuration
- Starts/stops with the API lifecycle

For production, consider:
- Running worker in a separate process/container
- Using a message queue (Celery) for distributed workers
- Adding monitoring/alerting for worker failures
