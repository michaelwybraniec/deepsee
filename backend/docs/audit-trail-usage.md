# Audit Trail Usage Guide

This guide explains how to use and query the audit trail system.

**Quick Links:**
- [Quick Start](#quick-start-using-the-query-script) - Fastest way to query events
- [Event Structure](#event-structure) - What's in each event
- [Common Use Cases](#common-use-cases) - Practical examples
- [Database Schema](#database-schema) - Technical details

## Table of Contents

1. [Overview](#overview)
2. [Automatic Logging](#automatic-logging)
3. [Quick Start: Using the Query Script](#quick-start-using-the-query-script)
4. [Querying Audit Events](#querying-audit-events)
   - [Using Python Interactively](#using-python-interactively)
   - [Using the Repository Interface](#using-the-repository-interface)
   - [Using SQLite Command Line](#using-sqlite-command-line)
5. [Event Structure](#event-structure)
6. [Common Use Cases](#common-use-cases)
7. [Database Schema](#database-schema)
8. [Important Notes](#important-notes)
9. [Troubleshooting](#troubleshooting)
10. [Example: Complete Audit Trail for a Task](#example-complete-audit-trail-for-a-task)

## Overview

The audit trail automatically logs all key actions in the system:
- **Task operations**: Creation, updates, deletion
- **Attachment operations**: Upload, deletion
- **Reminder operations**: Reminder sent (system action)

All audit events include:
- **Timestamp**: When the action occurred
- **User ID**: Who performed the action (NULL for system actions)
- **Action type**: What action was performed
- **Resource information**: What resource was affected
- **Metadata**: Additional context (task title, status changes, filename, etc.)

## Automatic Logging

Audit logging happens automatically - you don't need to do anything special. When you:

- Create a task → `task_created` event is logged
- Update a task → `task_updated` event is logged
- Delete a task → `task_deleted` event is logged
- Upload an attachment → `attachment_uploaded` event is logged
- Delete an attachment → `attachment_deleted` event is logged
- Worker sends a reminder → `reminder_sent` event is logged

## Quick Start: Using the Query Script

The easiest way to query audit events is using the provided script:

```bash
cd backend

# Show last 20 events
python3 scripts/query_audit_events.py

# Show all task creation events
python3 scripts/query_audit_events.py --action-type task_created

# Show events for a specific user
python3 scripts/query_audit_events.py --user-id 1

# Show events for a specific task
python3 scripts/query_audit_events.py --resource-type task --resource-id 123

# Show events from last 7 days
python3 scripts/query_audit_events.py --days 7

# Show all events (no limit)
python3 scripts/query_audit_events.py --all
```

## Querying Audit Events

### Using Python Interactively

Start Python with the backend directory in your path:

```bash
cd backend
python3
```

Then in Python:

```python
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from infrastructure.persistence.models.audit_event import AuditEvent
from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository
from domain.audit.audit_event import AuditActionType

# Get database session
db: Session = SessionLocal()

# Get all events, most recent first
events = db.query(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(20).all()

for event in events:
    user_info = f"user {event.user_id}" if event.user_id else "system"
    print(f"{event.timestamp} - {event.action_type} by {user_info}")
    print(f"  Resource: {event.resource_type}:{event.resource_id}")
    if event.event_metadata:
        print(f"  Metadata: {event.event_metadata}")

# Close session
db.close()
```

#### Get events by action type

```python
# Get all task creation events
created_events = db.query(AuditEvent).filter(
    AuditEvent.action_type == AuditActionType.TASK_CREATED
).order_by(AuditEvent.timestamp.desc()).all()
```

#### Get events by user

```python
# Get all events for a specific user
user_events = db.query(AuditEvent).filter(
    AuditEvent.user_id == user_id
).order_by(AuditEvent.timestamp.desc()).all()
```

#### Get events for a specific resource

```python
# Get all events for a specific task
task_events = db.query(AuditEvent).filter(
    AuditEvent.resource_type == "task",
    AuditEvent.resource_id == str(task_id)
).order_by(AuditEvent.timestamp.desc()).all()
```

#### Get recent events

```python
from datetime import datetime, timedelta

# Get events from last 7 days
seven_days_ago = datetime.utcnow() - timedelta(days=7)
recent_events = db.query(AuditEvent).filter(
    AuditEvent.timestamp >= seven_days_ago
).order_by(AuditEvent.timestamp.desc()).all()
```

### Using the Repository Interface

```python
from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository

# Initialize repository
audit_repository = SQLAlchemyAuditRepository(db_session)

# Find by action type
task_created_events = audit_repository.find_by_action_type(AuditActionType.TASK_CREATED)

# Find by user ID
user_events = audit_repository.find_by_user_id(user_id=1)

# Find by resource
task_events = audit_repository.find_by_resource("task", "123")
```

### Using SQLite Command Line

#### Connect to database

```bash
cd backend
sqlite3 task_tracker.db
```

#### Query audit events

```sql
-- Get all audit events (most recent first)
SELECT * FROM audit_events ORDER BY timestamp DESC LIMIT 20;

-- Get task creation events
SELECT * FROM audit_events 
WHERE action_type = 'task_created' 
ORDER BY timestamp DESC;

-- Get events for a specific user
SELECT * FROM audit_events 
WHERE user_id = 1 
ORDER BY timestamp DESC;

-- Get events for a specific task
SELECT * FROM audit_events 
WHERE resource_type = 'task' AND resource_id = '123'
ORDER BY timestamp DESC;

-- Get events from last 24 hours
SELECT * FROM audit_events 
WHERE timestamp >= datetime('now', '-1 day')
ORDER BY timestamp DESC;

-- Count events by action type
SELECT action_type, COUNT(*) as count 
FROM audit_events 
GROUP BY action_type 
ORDER BY count DESC;
```

## Event Structure

### Task Created Event

```json
{
  "id": 1,
  "action_type": "task_created",
  "user_id": 1,
  "resource_type": "task",
  "resource_id": "123",
  "timestamp": "2024-01-15T10:00:00Z",
  "event_metadata": {
    "title": "Complete project documentation",
    "status": "todo",
    "priority": "high"
  }
}
```

### Task Updated Event

```json
{
  "id": 2,
  "action_type": "task_updated",
  "user_id": 1,
  "resource_type": "task",
  "resource_id": "123",
  "timestamp": "2024-01-15T11:00:00Z",
  "event_metadata": {
    "task_id": 123,
    "changes": {
      "status": {
        "old": "todo",
        "new": "in_progress"
      },
      "priority": {
        "old": "low",
        "new": "high"
      }
    }
  }
}
```

### Task Deleted Event

```json
{
  "id": 3,
  "action_type": "task_deleted",
  "user_id": 1,
  "resource_type": "task",
  "resource_id": "123",
  "timestamp": "2024-01-15T12:00:00Z",
  "event_metadata": {
    "task_id": 123,
    "title": "Complete project documentation"
  }
}
```

### Attachment Uploaded Event

```json
{
  "id": 4,
  "action_type": "attachment_uploaded",
  "user_id": 1,
  "resource_type": "attachment",
  "resource_id": "456",
  "timestamp": "2024-01-15T13:00:00Z",
  "event_metadata": {
    "attachment_id": 456,
    "task_id": 123,
    "filename": "document.pdf",
    "file_size": 1024000
  }
}
```

### Attachment Deleted Event

```json
{
  "id": 5,
  "action_type": "attachment_deleted",
  "user_id": 1,
  "resource_type": "attachment",
  "resource_id": "456",
  "timestamp": "2024-01-15T14:00:00Z",
  "event_metadata": {
    "attachment_id": 456,
    "task_id": 123,
    "filename": "document.pdf"
  }
}
```

### Reminder Sent Event

```json
{
  "id": 6,
  "action_type": "reminder_sent",
  "user_id": null,
  "resource_type": "reminder",
  "resource_id": "123",
  "timestamp": "2024-01-15T15:00:00Z",
  "event_metadata": {
    "task_id": 123,
    "due_date": "2024-01-16T10:00:00Z"
  }
}
```

## Common Use Cases

### 1. Track User Activity

```python
# Get all actions by a specific user
user_activity = db.query(AuditEvent).filter(
    AuditEvent.user_id == user_id
).order_by(AuditEvent.timestamp.desc()).all()

for event in user_activity:
    print(f"{event.timestamp}: {event.action_type} on {event.resource_type}:{event.resource_id}")
```

### 2. Audit Task Lifecycle

```python
# Get complete history of a task
task_history = db.query(AuditEvent).filter(
    AuditEvent.resource_type == "task",
    AuditEvent.resource_id == str(task_id)
).order_by(AuditEvent.timestamp.asc()).all()

for event in task_history:
    print(f"{event.timestamp}: {event.action_type}")
    if event.event_metadata:
        print(f"  Details: {event.event_metadata}")
```

### 3. Find Recent Changes

```python
from datetime import datetime, timedelta

# Get all changes in last hour
one_hour_ago = datetime.utcnow() - timedelta(hours=1)
recent_changes = db.query(AuditEvent).filter(
    AuditEvent.timestamp >= one_hour_ago
).order_by(AuditEvent.timestamp.desc()).all()
```

### 4. Generate Activity Report

```python
# Count events by type for a user
from sqlalchemy import func

activity_report = db.query(
    AuditEvent.action_type,
    func.count(AuditEvent.id).label('count')
).filter(
    AuditEvent.user_id == user_id
).group_by(AuditEvent.action_type).all()

for action_type, count in activity_report:
    print(f"{action_type}: {count} events")
```

### 5. Detect System Actions

```python
# Get all system-generated events (reminders, etc.)
system_events = db.query(AuditEvent).filter(
    AuditEvent.user_id.is_(None)
).order_by(AuditEvent.timestamp.desc()).all()
```

## Database Schema

The `audit_events` table has the following structure:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `action_type` | VARCHAR | Type of action (indexed) |
| `user_id` | INTEGER | User who performed action (NULL for system, indexed) |
| `timestamp` | DATETIME | When event occurred (indexed) |
| `resource_type` | VARCHAR | Type of resource (indexed) |
| `resource_id` | VARCHAR | ID of affected resource |
| `event_metadata` | JSON | Additional context |

### Indexes

The table has indexes on:
- `action_type` - Fast filtering by action type
- `user_id` - Fast filtering by user
- `timestamp` - Fast time-based queries
- `(action_type, timestamp)` - Composite index for action queries with time filtering
- `(user_id, timestamp)` - Composite index for user activity queries
- `(resource_type, resource_id)` - Composite index for resource-specific queries

## Important Notes

1. **Immutability**: Audit events are append-only and never deleted or modified
2. **Non-blocking**: Audit logging failures don't break main operations
3. **System Actions**: Reminder sent events have `user_id = NULL` (system-generated)
4. **Metadata Format**: Metadata is stored as JSON for flexibility
5. **Performance**: Indexes ensure fast queries even with large audit logs

## Troubleshooting

### No audit events appearing

1. Check that the database table exists:
   ```sql
   SELECT name FROM sqlite_master WHERE type='table' AND name='audit_events';
   ```

2. Verify events are being created:
   ```sql
   SELECT COUNT(*) FROM audit_events;
   ```

3. Check application logs for audit logging errors (they won't break operations but will be logged)

### Query performance issues

- Use indexed columns in WHERE clauses (`action_type`, `user_id`, `timestamp`)
- Use LIMIT for large result sets
- Consider date range filters for time-based queries

## Example: Complete Audit Trail for a Task

```python
def get_task_audit_trail(db: Session, task_id: int):
    """Get complete audit trail for a task."""
    events = db.query(AuditEvent).filter(
        AuditEvent.resource_type == "task",
        AuditEvent.resource_id == str(task_id)
    ).order_by(AuditEvent.timestamp.asc()).all()
    
    trail = []
    for event in events:
        trail.append({
            "timestamp": event.timestamp.isoformat(),
            "action": event.action_type,
            "user_id": event.user_id,
            "details": event.event_metadata
        })
    
    return trail

# Usage
trail = get_task_audit_trail(db, task_id=123)
for entry in trail:
    print(f"{entry['timestamp']}: {entry['action']} by user {entry['user_id']}")
    print(f"  {entry['details']}")
```

This will show the complete history of a task from creation through all updates and deletions.
