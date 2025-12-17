# Worker

**API Endpoints**: See [API Documentation](api.md) (Swagger UI: `/docs`, ReDoc: `/redoc`)

## Implementation

**Location**: `backend/worker/jobs/reminder_job.py`

**Schedule**: Runs every hour automatically (APScheduler)

**Query**: Tasks where `due_date` is between NOW() and NOW() + 24 hours, excluding tasks with `reminder_sent_at` within last 24 hours

**Idempotency**: Uses `reminder_sent_at` timestamp column (atomic UPDATE prevents duplicates)

**Disable**: Set `ENVIRONMENT=test` to prevent worker from starting
