# Backend Documentation

This directory contains comprehensive documentation for the Task Tracker API backend.

## Documentation Index

### Getting Started

- [Monitoring & Logging Usage](monitoring-usage.md) - How to use structured logging, metrics, and health checks
- **[Testing Guide](testing.md)** - Complete testing guide and best practices ⭐
- **[Database Access](database-access.md)** - How to access and manage the SQLite database

### Authentication & Authorization
- **[API Documentation](api.md)** - API docs including authentication in Swagger UI
- **[Auth Design](auth-design.md)** - JWT authentication architecture
- **[Authorization](authorization.md)** - Authorization rules and implementation

### Features
- **[Task Model](task-model.md)** - Task model implementation
- **[Search & Filter API](search-filters.md)** - Search/filter implementation notes
- **[Tag Filtering](tag-filtering.md)** - Tag matching implementation details
- **[Attachment Design](attachments.md)** - Attachment storage and security

### Background Workers
- **[Worker](worker.md)** - Background worker implementation

### Audit Trail
- **[Audit Trail](audit.md)** - Query audit events and action types ⭐

### API Documentation
- **[API Documentation](api.md)** - Swagger/OpenAPI usage guide

## Quick Reference

### Most Common Tasks

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

**Create a User:**
```bash
cd backend
.venv/bin/python3 scripts/create_user.py
```

**Access Database:**
```bash
cd backend
sqlite3 task_tracker.db
```

**View API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Documentation by Feature

### Task Management
- Task model: `task-model.md`
- Search and filtering: `search-filters.md`
- Tag filtering: `tag-filtering.md`

### Attachments
- Design: `attachments.md`

### Authentication
- API usage: `api.md`
- Design: `auth-design.md`
- Authorization: `authorization.md`

### Workers & Notifications
- Worker: `worker.md`

### Audit Trail
- **Usage: `audit.md`** ⭐

### Rate Limiting
- Design: `rate-limiting.md`

### Monitoring & Observability
- Usage: `monitoring-usage.md`
- Dashboards: `grafana.md`

## Contributing

When adding new features, please:
1. Document requirements in a `*-requirements.md` file
2. Document design decisions in a `*-design.md` file
3. Document usage in a `*-usage.md` file
4. Update this README with links to new documentation
