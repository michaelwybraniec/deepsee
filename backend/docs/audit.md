# Audit Trail

Audit trail tracks specific user actions (task created, updated, deleted, attachments, reminders) with user IDs and timestamps. For system metrics (request rates, errors, latency), see [Grafana](grafana.md).

## Action Types

Automatically logged actions:

- `task_created`, `task_updated`, `task_deleted`
- `attachment_uploaded`, `attachment_deleted`
- `reminder_sent` (system action, no user_id)

## Query Events

```bash
cd backend

# Show last 20 events
python3 scripts/query_audit_events.py

# Filter by action type
python3 scripts/query_audit_events.py --action-type task_created

# Filter by user
python3 scripts/query_audit_events.py --user-id 1

# Filter by resource
python3 scripts/query_audit_events.py --resource-type task --resource-id 123

# Filter by time
python3 scripts/query_audit_events.py --days 7

# Show all events
python3 scripts/query_audit_events.py --all
```

## Event Structure

Each event contains:
- `action_type`: Type of action
- `user_id`: User who performed action (NULL for system actions)
- `resource_type`: Type of resource (e.g., "task", "attachment")
- `resource_id`: ID of affected resource
- `timestamp`: When event occurred
- `event_metadata`: JSON with additional context (task title, changes, filename, etc.)
