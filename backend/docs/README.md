# Backend Documentation

This directory contains comprehensive documentation for the Task Tracker API backend.

## Documentation Index

### Getting Started

- [Monitoring & Logging Usage](monitoring-usage.md) - How to use structured logging, metrics, and health checks
- **[Quick Start Guide](quick-start.md)** - Setup, installation, and running the API
- **[Testing Guide](testing.md)** - Complete testing guide and best practices ⭐
- **[Database Access](database-access.md)** - How to access and manage the SQLite database

### Authentication & Authorization
- **[Auth Requirements](auth-requirements.md)** - Authentication and authorization requirements
- **[Authorization Documentation](authorization.md)** - Authorization rules and implementation
- **[Swagger Auth Guide](swagger-auth-guide.md)** - How to use authentication in Swagger UI

### Features
- **[Task Fields](task-fields.md)** - Task data model fields
- **[Task Model](task-model.md)** - Task data model design
- **[Search & Filter Requirements](search-filter-requirements.md)** - Search, filter, sort, and pagination requirements
- **[Search & Filter API Design](search-filter-api-design.md)** - API design for search and filtering
- **[Tag Filtering (Partial Match)](tag-filtering-partial-match.md)** - Tag matching implementation details
- **[Attachment Requirements](attachment-requirements.md)** - Attachment feature requirements
- **[Attachment Design](attachment-design.md)** - Attachment storage and model design

### Background Workers
- **[Worker Usage](worker-usage.md)** - How to use the reminder worker
- **[Worker Design](worker-design.md)** - Reminder worker architecture and design
- **[Notification Requirements](notification-requirements.md)** - Notification system requirements

### Audit Trail
- **[Audit Trail Requirements](audit-trail-requirements.md)** - Audit trail requirements and specifications
- **[Audit Schema Design](audit-schema-design.md)** - Database schema and domain model design
- **[Audit Trail Usage](audit-trail-usage.md)** - How to query and use audit events ⭐

### API Documentation
- **[API Documentation](api-documentation.md)** - API documentation (if exists)

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
- Task fields and model: `task-fields.md`, `task-model.md`
- Search and filtering: `search-filter-requirements.md`, `search-filter-api-design.md`
- Tag filtering: `tag-filtering-partial-match.md`

### Attachments
- Requirements: `attachment-requirements.md`
- Design: `attachment-design.md`

### Authentication
- Setup: `auth-requirements.md`
- Usage: `swagger-auth-guide.md`
- Authorization: `authorization.md`

### Workers & Notifications
- Worker usage: `worker-usage.md`
- Worker design: `worker-design.md`
- Requirements: `notification-requirements.md`

### Audit Trail
- Requirements: `audit-trail-requirements.md`
- Schema: `audit-schema-design.md`
- **Usage: `audit-trail-usage.md`** ⭐

### Rate Limiting
- Requirements: `rate-limiting-requirements.md`
- Design: `rate-limiting-design.md`

### Monitoring & Observability
- Requirements: `monitoring-logging-requirements.md`
- Usage: `monitoring-usage.md`
- Dashboards: `prometheus-grafana-usage.md`

## Contributing

When adding new features, please:
1. Document requirements in a `*-requirements.md` file
2. Document design decisions in a `*-design.md` file
3. Document usage in a `*-usage.md` file
4. Update this README with links to new documentation
