## Backend

### Quick Start

**1. Install Dependencies:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Set Environment Variables:**

Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
# Edit .env and set your JWT_SECRET_KEY (minimum 32 characters)
```

**3. Start the Server:**
```bash
cd backend
source .venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs on `http://localhost:8000`

**4. Verify:**
- API: http://localhost:8000/health
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

**Getting Started:**
- **[API Documentation](docs/api.md)** - Swagger/OpenAPI usage guide (all endpoints in `/docs` and `/redoc`) ⭐
- **[Testing Guide](docs/testing.md)** - Complete testing guide and best practices ⭐

**Key Features:**
- **[Audit Trail](docs/audit.md)** - Query audit events and action types ⭐
- **[Worker](docs/worker.md)** - Background worker
- **[Monitoring Usage](docs/monitoring-usage.md)** - How to access logs and metrics
- **[Grafana](docs/grafana.md)** - Metrics dashboards

**Full Documentation Index:**
- **[Complete Documentation Index](docs/README.md)** - All backend documentation organized by category

### Quick Reference

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