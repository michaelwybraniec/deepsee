# Testing

## Test Database

**Location**: `backend/tests/conftest.py`

**Critical**: Tests use temporary file-based SQLite (not `:memory:`) to ensure all connections share the same database instance.

## Fixtures

**Available**: `db_session`, `client`, `test_user`, `test_user2`

**Location**: `backend/tests/conftest.py`

## Worker Tests

**Critical**: Worker tests must patch `SessionLocal` to use test database:

```python
from tests.conftest import TestSessionLocal
monkeypatch.setattr("worker.jobs.reminder_job.SessionLocal", TestSessionLocal)
```

## Environment Variables

- `ENVIRONMENT=test` - Disables worker scheduler (set automatically)
- `JWT_SECRET_KEY` - Required for JWT token generation
