# Backend

## Quick Start

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Set JWT_SECRET_KEY (min 32 chars)
uvicorn api.main:app --reload
```

Server: http://localhost:8000 | Docs: http://localhost:8000/docs

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

```bash
# Query audit events
.venv/bin/python3 scripts/query_audit_events.py

# Create user
.venv/bin/python3 scripts/create_user.py <username> <email> <password>

# Seed tasks
.venv/bin/python3 scripts/seed_tasks.py [--count 50] [--user-id 1]
```
