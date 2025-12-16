## Backend

### Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[Quick Start Guide](docs/quick-start.md)** - Setup and running the API
- **[Testing Guide](docs/testing.md)** - Complete testing guide and best practices ⭐
- **[Audit Trail Usage](docs/audit-trail-usage.md)** - How to query and use audit events ⭐
- **[Worker Usage](docs/worker-usage.md)** - Background worker documentation
- **[Database Access](docs/database-access.md)** - Database management
- **[Full Documentation Index](docs/README.md)** - Complete list of all documentation

### Quick Reference

**Start the API:**
```bash
cd backend
source .venv/bin/activate
uvicorn api.main:app --reload
```

**Query Audit Events:**
```bash
cd backend
.venv/bin/python3 scripts/query_audit_events.py
```

**View API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc