## Backend

### Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

**Getting Started:**
- **[Quick Start Guide](docs/quick-start.md)** - Setup and running the API
- **[API Endpoints Summary](docs/api-endpoints-summary.md)** - Complete API reference ⭐
- **[Swagger Auth Guide](docs/swagger-auth-guide.md)** - How to authenticate in Swagger UI
- **[Testing Guide](docs/testing.md)** - Complete testing guide and best practices ⭐

**Key Features:**
- **[Audit Trail Usage](docs/audit-trail-usage.md)** - How to query and use audit events ⭐
- **[Worker Usage](docs/worker-usage.md)** - Background worker documentation
- **[Monitoring Usage](docs/monitoring-usage.md)** - How to access logs and metrics
- **[Prometheus & Grafana Usage](docs/prometheus-grafana-usage.md)** - Observability dashboards

**Full Documentation Index:**
- **[Complete Documentation Index](docs/README.md)** - All backend documentation organized by category

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

**Seed Sample Tasks:**
```bash
cd backend
.venv/bin/python3 scripts/seed_tasks.py
# Or specify count and user ID:
.venv/bin/python3 scripts/seed_tasks.py --count 50 --user-id 1
```

**View API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc