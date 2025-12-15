# Task ID: 7.2
# Title: Design audit event schema
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 2h

## Description
Design the audit event schema including action type, timestamp, user ID, and relevant metadata, based on requirements from task 7.1.

**Step-by-step:**
1. Review audit requirements from task 7.1 (key actions: task CRUD, attachment operations, reminder sent; fields: timestamp, user ID).
2. Design database schema (SQL or ORM model):
   - Table: `audit_log` or `audit_events`
   - Columns:
     - `id` (primary key, auto-increment/UUID)
     - `action_type` (string/enum, NOT NULL - e.g., "task_created", "task_updated", "task_deleted", "attachment_uploaded", "attachment_deleted", "reminder_sent")
     - `user_id` (foreign key to users table, nullable - NULL for system actions like reminder_sent)
     - `timestamp` (timestamp/TIMESTAMP, NOT NULL, auto-set to NOW())
     - `resource_type` (string, optional - e.g., "task", "attachment", "reminder")
     - `resource_id` (string/integer, optional - ID of the affected resource, e.g., task ID, attachment ID)
     - `metadata` (JSON/JSONB, optional - additional context, e.g., `{"task_title": "...", "old_status": "...", "new_status": "..."}`)
3. Design domain entity (Clean Architecture):
   - Create `AuditEvent` entity in `backend/domain/audit/audit_event.py`:
     - Properties: id, action_type, user_id, timestamp, resource_type, resource_id, metadata
     - Methods: validation logic if needed
4. Design ORM model (if using SQLAlchemy, Django ORM, etc.):
   - Create `AuditEvent` model in `backend/infrastructure/persistence/models/audit_event.py`:
     - Map to database table
     - Define relationships (e.g., belongs_to user via user_id)
     - Define indexes (e.g., on action_type, user_id, timestamp for queries)
5. Document schema:
   - Create schema diagram or code comments
   - Document field types, constraints, indexes
   - Document action types enum values

**Implementation hints:**
- Use SQLAlchemy (Python) or Django ORM for ORM model.
- Place domain entity in `backend/domain/audit/audit_event.py` (pure Python, no ORM dependencies).
- Place ORM model in `backend/infrastructure/persistence/models/audit_event.py` (depends on ORM).
- Use JSON/JSONB column for metadata (flexible, allows different metadata per action type).
- Index on timestamp, action_type, user_id for query performance.

## Dependencies
- [ ] Task ID: 7.1 (Audit requirements must be confirmed)

## Testing Instructions
- N/A for design task. Verify schema supports required actions and fields.
- Review schema definition to ensure all fields from task 7.1 are present.

## Security Review
- Ensure no unnecessary sensitive data is stored in audit metadata:
  - Don't store passwords, tokens, or other secrets in metadata.
  - Store only necessary context (e.g., task title, status changes, not full task content).

## Risk Assessment
- Poor schema design may make audit logs hard to use or query.
- Missing fields may limit audit trail usefulness.
- Missing indexes can cause slow queries.

## Acceptance Criteria
- [ ] Audit schema includes action type, timestamp, user ID, and metadata field(s) (all required fields present).
- [ ] Schema supports all required actions (task CRUD, attachment operations, reminder sent).
- [ ] Schema is documented and implemented in code (database table/model exists).
- [ ] Indexes defined for query performance (timestamp, action_type, user_id).

## Definition of Done
- [ ] Schema defined and implemented in the database/model layer (audit_log table or AuditEvent model exists).
- [ ] Database schema defined (migration file or SQL script).
- [ ] Domain entity and ORM model implemented.
- [ ] Indexes defined for query performance.
- [ ] Schema documented (code comments or design doc).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Schema definition exists and is committed (code files exist, database table can be created).
- **Observable Outcomes**: Schema can be used in code, database table can be created, indexes are defined.

## Notes
This will be used by all audit-producing components (tasks 7.3, 7.4). Ensure schema is flexible enough to support all action types.

## Strengths
Provides a consistent structure for all audit events. Enables querying and analysis of audit trail.

## Sub-tasks (Children)
- [ ] Review audit requirements from task 7.1 (key actions, required fields).
- [ ] Draft audit schema (table name, columns, types, constraints, indexes).
- [ ] Design domain entity (pure Python class in `backend/domain/audit/audit_event.py`).
- [ ] Design ORM model (SQLAlchemy/Django model in `backend/infrastructure/persistence/models/audit_event.py`).
- [ ] Define action types enum (task_created, task_updated, task_deleted, attachment_uploaded, attachment_deleted, reminder_sent).
- [ ] Define indexes for query performance (timestamp, action_type, user_id).
- [ ] Document schema (code comments or design doc).
- [ ] Create database migration or SQL script to create table.

## Completed
[ ] Pending / [ ] Completed


