# Audit Trail Requirements

This document summarizes all audit trail requirements extracted from the project documentation.

## Source References
- `docs/requirements.md` section "6. Audit Trail"
- `docs/technical-specs.md` section "3.6 Audit Trail"

## Requirements Summary

### 1. Key Actions to Audit

**Requirement**: Record key actions with timestamps and user IDs.

**Source**: 
- `docs/requirements.md` §6: "Record key actions: task creation, update, attachment added/removed, reminder sent."
- `docs/technical-specs.md` §3.6: "Record key actions: Task creation. Task update. Attachment added. Attachment removed. Reminder sent."

**Required Actions**:
1. **Task creation** - When a task is created
2. **Task update** - When a task is updated
3. **Task deletion** - Implicit (update includes deletion per requirements)
4. **Attachment added** - When an attachment is uploaded
5. **Attachment removed** - When an attachment is deleted
6. **Reminder sent** - When a reminder is sent by the worker

### 2. Required Fields

**Requirement**: Include timestamps and user ID.

**Source**:
- `docs/requirements.md` §6: "Include timestamps and user ID."
- `docs/technical-specs.md` §3.6: "Include: Timestamps. User ID."

**Required Fields**:
- **Timestamp**: When the action occurred (required for all actions)
- **User ID**: Who performed the action (required for user-driven actions, NULL for system actions like reminder_sent)

### 3. Storage

**Requirement**: Audit events stored in database.

**Source**: Implicit (audit trail must be persistent and queryable).

**Details**:
- Store audit events in database (audit_log table or similar)
- Events should be immutable (append-only, never deleted)
- Events should be queryable (for analysis, debugging, compliance)

### 4. Metadata

**Requirement**: Include relevant context for each action.

**Source**: Implicit (needed for traceability and debugging).

**Details**:
- **Task actions**: Include task ID, task title, status changes (for updates)
- **Attachment actions**: Include attachment ID, task ID, filename, file size
- **Reminder actions**: Include task ID, due date
- **General**: Action type, resource type, resource ID

## Implicit Requirements

### 5. Immutability

**Requirement**: Audit events should be immutable.

**Source**: Implicit (audit trail best practice).

**Details**:
- Events are append-only (never updated or deleted)
- Ensures audit trail integrity
- Prevents tampering with historical records

### 6. Non-Blocking

**Requirement**: Audit logging should not break main operations.

**Source**: Implicit (best practice for audit logging).

**Details**:
- Audit logging errors should not cause main operations to fail
- Log errors gracefully, continue with main flow
- Audit logging should be fire-and-forget (optional: async)

### 7. Security

**Requirement**: Do not store sensitive data in audit logs.

**Source**: Implicit (security best practice).

**Details**:
- Do not log passwords, tokens, or other secrets
- Log only necessary context (task title, status, filename, not full content)
- Ensure audit logs don't expose sensitive information

## Action Types

Based on requirements, the following action types need to be audited:

1. **`task_created`** - Task creation
   - User ID: Required (user who created the task)
   - Metadata: task_id, title, status, priority, due_date

2. **`task_updated`** - Task update
   - User ID: Required (user who updated the task)
   - Metadata: task_id, old_status, new_status, changes (what fields changed)

3. **`task_deleted`** - Task deletion
   - User ID: Required (user who deleted the task)
   - Metadata: task_id, title (for reference)

4. **`attachment_uploaded`** - Attachment upload
   - User ID: Required (user who uploaded the attachment)
   - Metadata: attachment_id, task_id, filename, file_size

5. **`attachment_deleted`** - Attachment deletion
   - User ID: Required (user who deleted the attachment)
   - Metadata: attachment_id, task_id, filename

6. **`reminder_sent`** - Reminder sent by worker
   - User ID: NULL (system action, not user-driven)
   - Metadata: task_id, due_date

## Design Decisions Needed

1. **Storage Format**:
   - Database table structure
   - Metadata format (JSON/JSONB vs separate columns)
   - Decision: To be made in task 7.2 (recommend JSON for flexibility)

2. **Action Type Enum**:
   - Fixed enum vs free-form string
   - Decision: To be made in task 7.2 (recommend enum for consistency)

3. **Metadata Structure**:
   - Structured vs flexible JSON
   - Decision: To be made in task 7.2 (recommend JSON for flexibility)

4. **Query Interface**:
   - Read-only API endpoints for querying audit logs
   - Decision: Optional enhancement (not required by assignment)

## Implementation Tasks

- Task 7.2: Design audit event schema (database table, domain entity, ORM model)
- Task 7.3: Implement audit logging service (interface, implementation, repository)
- Task 7.4: Integrate audit logging with tasks, attachments, and reminders

## Security Considerations

1. **Data Minimization**: Log only necessary context, not full content
2. **No Secrets**: Never log passwords, tokens, or other sensitive data
3. **Access Control**: Audit logs should be readable only by authorized users (optional enhancement)
4. **Immutability**: Audit events should never be modified or deleted

## Summary

**Required behaviors**:
- ✅ Record task creation, update, deletion
- ✅ Record attachment upload and deletion
- ✅ Record reminder sent
- ✅ Include timestamp for all actions
- ✅ Include user ID for user-driven actions (NULL for system actions)
- ✅ Store in database (immutable, queryable)
- ✅ Include relevant metadata (task ID, attachment ID, filename, etc.)
- ✅ Do not store sensitive data

**Design decisions needed**:
- Storage format (database table structure)
- Action type enum values
- Metadata structure (JSON vs structured)
- Query interface (optional)

All requirements from `docs/requirements.md` §6 and `docs/technical-specs.md` §3.6 are accounted for.
