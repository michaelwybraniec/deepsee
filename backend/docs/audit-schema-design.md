# Audit Event Schema Design

## Overview

This document describes the database schema and domain model for audit trail events.

## Database Schema

### Table: `audit_events`

**Purpose**: Store immutable audit log entries for all key system actions.

### Columns

| Column | Type | Nullable | Description | Index |
|--------|------|----------|-------------|-------|
| `id` | INTEGER | NO | Primary key, auto-increment | Primary Key |
| `action_type` | VARCHAR | NO | Type of action (enum: task_created, task_updated, etc.) | Yes |
| `user_id` | INTEGER | YES | Foreign key to users.id (NULL for system actions) | Yes |
| `timestamp` | DATETIME | NO | When the event occurred (auto-set to NOW()) | Yes |
| `resource_type` | VARCHAR | NO | Type of resource (e.g., "task", "attachment", "reminder") | Yes |
| `resource_id` | VARCHAR | NO | ID of the affected resource (as string for flexibility) | Yes |
| `event_metadata` | JSON | YES | Additional context (JSON object) | No |

### Indexes

1. **Primary Key**: `id` (automatic)
2. **`action_type`**: For filtering by action type
3. **`user_id`**: For filtering by user
4. **`timestamp`**: For time-based queries
5. **Composite: `(action_type, timestamp)`**: For action type queries with time filtering
6. **Composite: `(user_id, timestamp)`**: For user activity queries
7. **Composite: `(resource_type, resource_id)`**: For resource-specific queries

### SQL Schema

```sql
CREATE TABLE audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type VARCHAR NOT NULL,
    user_id INTEGER,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resource_type VARCHAR NOT NULL,
    resource_id VARCHAR NOT NULL,
    event_metadata JSON,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_audit_action_timestamp (action_type, timestamp),
    INDEX idx_audit_user_timestamp (user_id, timestamp),
    INDEX idx_audit_resource (resource_type, resource_id)
);
```

## Domain Entity

### `AuditEvent` (Domain Layer)

**Location**: `backend/domain/audit/audit_event.py`

**Properties**:
- `id`: Optional[int] - Database ID (None for new events)
- `action_type`: str - Type of action
- `user_id`: Optional[int] - User ID (None for system actions)
- `resource_type`: str - Type of resource
- `resource_id`: str - Resource ID
- `metadata`: Optional[Dict[str, Any]] - Additional context
- `timestamp`: datetime - When event occurred

**Purpose**: Pure domain entity, no ORM dependencies. Used for business logic.

## ORM Model

### `AuditEvent` (Infrastructure Layer)

**Location**: `backend/infrastructure/persistence/models/audit_event.py`

**Purpose**: SQLAlchemy ORM model for database persistence.

**Relationships**:
- `user`: Relationship to User model (via `user_id` foreign key)

## Action Types

### Enum: `AuditActionType`

Defined in `backend/domain/audit/audit_event.py`:

```python
class AuditActionType(str, Enum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    ATTACHMENT_UPLOADED = "attachment_uploaded"
    ATTACHMENT_DELETED = "attachment_deleted"
    REMINDER_SENT = "reminder_sent"
```

## Metadata Structure

Metadata is stored as JSON for flexibility. Each action type has different metadata:

### Task Created
```json
{
  "task_id": 123,
  "title": "Task Title",
  "status": "todo",
  "priority": "high"
}
```

### Task Updated
```json
{
  "task_id": 123,
  "changes": {
    "status": {"old": "todo", "new": "in_progress"},
    "priority": {"old": "low", "new": "high"}
  }
}
```

### Task Deleted
```json
{
  "task_id": 123,
  "title": "Task Title"
}
```

### Attachment Uploaded
```json
{
  "attachment_id": 456,
  "task_id": 123,
  "filename": "document.pdf",
  "file_size": 1024000
}
```

### Attachment Deleted
```json
{
  "attachment_id": 456,
  "task_id": 123,
  "filename": "document.pdf"
}
```

### Reminder Sent
```json
{
  "task_id": 123,
  "due_date": "2024-01-15T10:00:00Z"
}
```

## Design Decisions

### 1. Metadata as JSON

**Decision**: Store metadata as JSON/JSONB column

**Rationale**:
- Flexible - different action types need different metadata
- Easy to extend without schema changes
- SQLite supports JSON (stored as TEXT, can be queried)
- PostgreSQL supports JSONB (better performance, indexing)

### 2. Resource ID as String

**Decision**: Store `resource_id` as VARCHAR/string

**Rationale**:
- Flexible - can store integer IDs, UUIDs, or other identifiers
- Consistent across different resource types
- Easy to query and filter

### 3. User ID Nullable

**Decision**: `user_id` can be NULL

**Rationale**:
- System actions (like reminder_sent) don't have a user
- NULL clearly indicates system-generated action
- Allows filtering: `WHERE user_id IS NULL` for system actions

### 4. Timestamp Auto-Set

**Decision**: `timestamp` defaults to `datetime.utcnow()`

**Rationale**:
- Ensures accurate timestamps
- Consistent timezone (UTC)
- No need to manually set in application code

### 5. Immutability

**Decision**: Audit events are append-only (never updated or deleted)

**Rationale**:
- Ensures audit trail integrity
- Prevents tampering with historical records
- Required for compliance and debugging

## Query Examples

### Get all audit events for a user
```sql
SELECT * FROM audit_events 
WHERE user_id = 1 
ORDER BY timestamp DESC;
```

### Get all task-related events
```sql
SELECT * FROM audit_events 
WHERE resource_type = 'task' 
ORDER BY timestamp DESC;
```

### Get events by action type
```sql
SELECT * FROM audit_events 
WHERE action_type = 'task_created' 
ORDER BY timestamp DESC;
```

### Get recent events
```sql
SELECT * FROM audit_events 
WHERE timestamp >= datetime('now', '-7 days')
ORDER BY timestamp DESC;
```

## Summary

**Schema Features**:
- ✅ Supports all required action types
- ✅ Includes timestamp and user ID
- ✅ Flexible metadata (JSON)
- ✅ Indexed for query performance
- ✅ Immutable (append-only)
- ✅ Relationships to users table

**Action Types**:
- ✅ task_created
- ✅ task_updated
- ✅ task_deleted
- ✅ attachment_uploaded
- ✅ attachment_deleted
- ✅ reminder_sent

This schema provides a flexible, performant foundation for the audit trail system.
