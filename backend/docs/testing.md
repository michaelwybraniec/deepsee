# Testing Guide

## Overview

The backend uses **pytest** for all testing. The test suite includes:
- Unit tests for business logic
- Integration tests for API endpoints
- Worker tests for background jobs
- Rate limiting tests
- Audit trail tests

## Test Setup

### Test Database

Tests use a **temporary file-based SQLite database** (not `:memory:`) to ensure all database connections share the same database instance. This is critical for proper test isolation.

**Location**: `backend/tests/conftest.py`

**Key Features**:
- Fresh database for each test function
- Automatic table creation and cleanup
- Shared fixtures for common test data

### Running Tests

**Run all tests:**
```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

**Run specific test file:**
```bash
pytest tests/test_tasks_create.py -v
```

**Run specific test:**
```bash
pytest tests/test_tasks_create.py::test_create_task_success -v
```

**Run with coverage:**
```bash
pytest tests/ --cov=. --cov-report=html
```

## Test Fixtures

### Available Fixtures

All fixtures are defined in `backend/tests/conftest.py`:

- **`db_session`**: Fresh database session for each test
- **`client`**: FastAPI TestClient with database override
- **`test_user`**: Standard test user (username: "testuser", password: "testpassword")
- **`test_user2`**: Second test user (username: "user2", password: "password2")
- **`user1`**: Alias for compatibility (username: "user1", password: "password1")
- **`user2`**: Alias for compatibility (username: "user2", password: "password2")

### Using Fixtures

```python
def test_example(client: TestClient, test_user: User):
    # Login
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["token"]
    
    # Make authenticated request
    response = client.get(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

## Test Organization

### Test Files

- `test_auth_*.py` - Authentication tests
- `test_tasks_*.py` - Task CRUD tests
- `test_worker_*.py` - Background worker tests
- `test_rate_limiting.py` - Rate limiting tests
- `test_audit_*.py` - Audit trail tests

### Test Structure

All test files use the shared fixtures from `conftest.py`. **Do not create custom database sessions** - always use the provided fixtures.

## Common Patterns

### Testing Authenticated Endpoints

```python
def test_authenticated_endpoint(client: TestClient, test_user: User):
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    token = login_response.json()["token"]
    
    # Use token in requests
    response = client.get(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### Testing Worker Jobs

Worker tests need to patch `SessionLocal` to use the test database:

```python
def test_worker_job(db_session: Session, monkeypatch):
    # Patch SessionLocal to use test database
    from tests.conftest import TestSessionLocal
    monkeypatch.setattr("worker.jobs.reminder_job.SessionLocal", TestSessionLocal)
    
    # Run worker job
    process_reminders()
    
    # Verify results
    # ...
```

### Creating Test Data

```python
def test_with_custom_data(db_session: Session, test_user: User):
    # Create task in test database
    task = Task(
        title="Test Task",
        owner_user_id=test_user.id
    )
    db_session.add(task)
    db_session.commit()
    
    # Test with the task
    # ...
```

## Test Isolation

### Why File-Based Database?

SQLite `:memory:` creates a **separate database for each connection**, which causes test isolation issues. Using a temporary file ensures all connections share the same database.

### Cleanup

- Each test gets a fresh database session
- Tables are created before each test
- Tables are dropped after each test
- Database file is cleaned up automatically

## Environment Variables

Tests use these environment variables (set automatically in test fixtures):

- `ENVIRONMENT=test` - Disables worker scheduler
- `JWT_SECRET_KEY` - Required for JWT token generation
- `RATE_LIMIT_ENABLED` - Can be overridden in tests

## Troubleshooting

### "no such table" errors

- Ensure you're using `client` and `test_user` fixtures from `conftest.py`
- Don't create custom database sessions
- Check that all models are imported in `conftest.py`

### UNIQUE constraint violations

- This should not happen with the current setup
- If it does, check that tests are using the shared fixtures
- Ensure `db_session` fixture is properly scoped

### Worker tests failing

- Worker tests must patch `SessionLocal` to use `TestSessionLocal`
- Ensure test data is committed before running worker jobs
- Use `monkeypatch.setattr("worker.jobs.reminder_job.SessionLocal", TestSessionLocal)`

## Best Practices

1. **Always use shared fixtures** - Don't create custom database sessions
2. **One test per scenario** - Keep tests focused and independent
3. **Use descriptive test names** - `test_create_task_success` not `test_1`
4. **Clean up test data** - Fixtures handle this automatically
5. **Test both success and failure cases** - Don't just test happy paths

## Test Coverage

Current test status: **47/47 tests passing (100%)**

Test categories covered:
- ✅ Authentication (login, change password)
- ✅ Task CRUD operations
- ✅ Attachments
- ✅ Worker/background jobs
- ✅ Rate limiting
- ✅ Audit trail
- ✅ Authorization

## Related Documentation

- [Quick Start Guide](quick-start.md)
- [Audit Trail Usage](audit-trail-usage.md)
- [Worker Usage](worker-usage.md)
