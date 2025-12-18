# Backend

FastAPI backend with Clean Architecture, JWT authentication, PostgreSQL, Redis rate limiting, background workers, and observability.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or SQLite for development)
- Redis (optional, for rate limiting)

### Installation

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Setup

1. **Copy environment template:**

   ```bash
   cp .env.example .env
   ```

2. **Set JWT_SECRET_KEY** (required, min 32 characters):

   ```bash
   # Generate secure key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   # Or: openssl rand -hex 32
   ```

   Edit `.env` and set:

   ```bash
   JWT_SECRET_KEY=your-generated-key-here-min-32-chars
   ```

3. **Database URL** (optional, defaults to SQLite):

   ```bash
   # PostgreSQL (Docker) - Note: sslmode=disable for local Docker setup
   DATABASE_URL=postgresql://tasktracker:changeme@localhost:5432/task_tracker?sslmode=disable
   
   # SQLite (default, no config needed)
   # DATABASE_URL=sqlite:///./task_tracker.db
   ```

4. **Redis** (optional, for rate limiting):

   ```bash
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

### Run Server

```bash
uvicorn api.main:app --reload
```

**Access:** <http://localhost:8000> | **Docs:** <http://localhost:8000/docs>

### Database Initialization

**First time setup:**

```bash
# Schema is auto-created on first API request
# Or manually:
.venv/bin/python3 -c "from infrastructure.database import init_db; init_db()"
```

**Create first user:**

```bash
.venv/bin/python3 scripts/create_user.py username email@example.com password
```

## Documentation

All documentation in [`docs/`](docs/):

- **[Architecture](docs/architecture.md)** - Clean Architecture layers
- **[API](docs/api.md)** - Swagger/OpenAPI endpoints
- **[Testing](docs/testing.md)** - Testing guide
- **[Database](docs/database-access.md)** - Database access
- **[Auth](docs/auth-design.md)** - JWT authentication
- **[Authorization](docs/authorization.md)** - Access control
- **[Tasks](docs/task-model.md)** - Task model
- **[Search & Filter](docs/search-filter-api-design.md)** - Search/filter API
- **[Attachments](docs/attachments.md)** - File storage
- **[Worker](docs/worker.md)** - Background jobs
- **[Audit](docs/audit.md)** - Audit trail
- **[Rate Limiting](docs/rate-limiting-design.md)** - Rate limiting
- **[Monitoring](docs/monitoring-usage.md)** - Logs & metrics
- **[Grafana](docs/grafana.md)** - Dashboards

## Scripts

**User Management:**

```bash
# Create user
.venv/bin/python3 scripts/create_user.py <username> <email> <password>

# Reset password
.venv/bin/python3 scripts/reset_password.py <username> <new_password>
```

**Database:**

```bash
# Seed sample tasks
.venv/bin/python3 scripts/seed_tasks.py [--count 50] [--user-id 1]

# Reset database (drop all tables)
.venv/bin/python3 scripts/reset_database.py [--force] [--no-recreate]

# Query audit events
.venv/bin/python3 scripts/query_audit_events.py
```

**Docker:**

```bash
# Auto-initialization (runs on Docker startup)
.venv/bin/python3 scripts/init_docker.py
```

## Testing

**Run tests:**

```bash
.venv/bin/pytest tests/ -v
```

**Test coverage:**

- 68 backend tests (unit + integration)
- Tests use temporary SQLite database
- See [Testing Guide](docs/testing.md) for details

**Environment:** Tests automatically set `ENVIRONMENT=test` (disables worker scheduler)

## Docker

**Using Docker Compose:**

- See [Docker Setup](../docs/docker.md) for full guide
- Backend auto-initializes: schema, test user, seed data
- Test user: `testuser` / `testpassword` (auto-created)

**Docker-specific scripts:**

```bash
# From host, run scripts in container
docker exec task-tracker-api python scripts/create_user.py username email password
docker exec task-tracker-api python scripts/seed_tasks.py --count 50
```

**Database access:**

- pgAdmin: <http://localhost:8888> (login: `admin@example.com` / password: `admin`)
- Console: `docker exec -it task-tracker-db psql -U tasktracker -d task_tracker`
- See [Database Access](docs/database-access.md) for details
