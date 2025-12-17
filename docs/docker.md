# Docker Setup

## Overview

Docker Compose runs the entire application stack:

- **database** - PostgreSQL (port 5432, internal only)
- **redis** - Rate limiting (port 6379)
- **api** - Backend API (port 8000)
- **worker** - Background worker
- **frontend** - React UI (port 5173)
- **prometheus** - Metrics (port 9090)
- **grafana** - Dashboards (port 3000)
- **pgadmin** - Database UI (port 8888)

## Quick Start

```bash
# Start all services
npm run docker:up
# or
docker compose up

# Stop all services
npm run docker:down
# or
docker compose down

# View logs
npm run docker:logs
# or
docker compose logs -f
```

## Automatic Initialization

On first startup, the API automatically:
1. Waits for database to be ready
2. Creates database schema
3. Creates test user (`testuser` / `testpassword`)
4. Seeds 50 sample tasks

**Test User Credentials** (displayed in API logs):
- Username: `testuser`
- Email: `test@example.com`
- Password: `testpassword`

**View credentials:**
```bash
docker compose logs api | grep -A 5 "TEST USER CREDENTIALS"
```

The credentials are clearly displayed in the API container logs when initialization completes.

Customize via environment variables:
- `TEST_USERNAME` - Test username (default: `testuser`)
- `TEST_EMAIL` - Test email (default: `test@example.com`)
- `TEST_PASSWORD` - Test password (default: `testpassword`)
- `SEED_TASK_COUNT` - Number of tasks to seed (default: `50`)

## Access Points

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3000 (admin/admin)
- **pgAdmin**: http://localhost:8888 (admin@example.com/admin)

## Volumes

Data persists in Docker volumes:
- `postgres_data` - Database data
- `redis_data` - Redis data
- `uploads_data` - File uploads
- `prometheus_data` - Metrics data
- `grafana_data` - Grafana dashboards
- `pgadmin_data` - pgAdmin settings

## Clean Slate

Remove all data and start fresh:
```bash
docker compose down -v
docker compose up
```
