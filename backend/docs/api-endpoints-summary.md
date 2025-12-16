# API Endpoints Summary

This document provides a complete list of all API endpoints organized by category.

## Total Endpoints: 20

## 1. Authentication (3 endpoints)
**Prefix**: `/api/auth`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register a new user | No |
| POST | `/api/auth/login` | Login and get JWT token | No |
| POST | `/api/auth/change-password` | Change user password | Yes |

## 2. Tasks (5 endpoints)
**Prefix**: `/api/tasks`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/tasks/` | Create a new task | Yes |
| GET | `/api/tasks/` | List tasks (with search, filter, sort, pagination) | Yes |
| GET | `/api/tasks/{id}` | Get task by ID | Yes |
| PUT | `/api/tasks/{id}` | Update task (owner only) | Yes |
| DELETE | `/api/tasks/{id}` | Delete task (owner only) | Yes |

## 3. Attachments (3 endpoints)
**Prefix**: `/api`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/tasks/{task_id}/attachments` | Upload attachment to task | Yes (owner only) |
| GET | `/api/tasks/{task_id}/attachments` | List attachments for a task | Yes |
| DELETE | `/api/attachments/{id}` | Delete attachment | Yes (task owner only) |

## 4. Health Checks (4 endpoints)
**Prefix**: `/api/health`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/health` | Comprehensive health check (API, DB, Worker) | No |
| GET | `/api/health/api` | API health check only | No |
| GET | `/api/health/database` | Database health check only | No |
| GET | `/api/health/worker` | Worker health check only | No |

## 5. Metrics (1 endpoint)
**Prefix**: `/api/metrics`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/metrics` | Prometheus metrics endpoint | No |

## 6. Worker Management (3 endpoints)
**Prefix**: `/api/worker`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/worker/status` | Get worker status and schedule | Yes |
| POST | `/api/worker/trigger` | Manually trigger reminder job | Yes |
| GET | `/api/worker/statistics` | Get worker statistics (tasks processed, etc.) | Yes |

## 7. Root (1 endpoint)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API root/info | No |

## Endpoint Categories

### Core Application Endpoints (11)
- **Authentication**: 3 endpoints
- **Tasks**: 5 endpoints
- **Attachments**: 3 endpoints

### Operational Endpoints (8)
- **Health Checks**: 4 endpoints (monitoring/observability)
- **Metrics**: 1 endpoint (monitoring/observability)
- **Worker Management**: 3 endpoints (admin/operational)
- **Root**: 1 endpoint (info)

### Public vs Protected

**Public Endpoints (9)** - No authentication required:
- `/api/auth/register`
- `/api/auth/login`
- `/api/health/*` (4 endpoints)
- `/api/metrics`
- `/`

**Protected Endpoints (11)** - Authentication required:
- `/api/auth/change-password`
- `/api/tasks/*` (5 endpoints)
- `/api/tasks/{id}/attachments` (POST, GET)
- `/api/attachments/{id}` (DELETE)
- `/api/worker/*` (3 endpoints)

## Notes

1. **Health checks** are intentionally public for monitoring tools (Prometheus, load balancers, etc.)
2. **Metrics endpoint** is public for Prometheus scraping
3. **Worker endpoints** are protected but could be considered for admin-only access in production
4. **Task ownership** is enforced for:
   - Task updates (PUT `/api/tasks/{id}`)
   - Task deletion (DELETE `/api/tasks/{id}`)
   - Attachment upload (POST `/api/tasks/{task_id}/attachments`)
   - Attachment deletion (DELETE `/api/attachments/{id}`)

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
