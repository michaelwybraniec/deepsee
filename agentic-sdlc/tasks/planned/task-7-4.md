# Task ID: 7.4
# Title: Integrate audit logging with tasks, attachments, and reminders
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Integrate audit logging into task creation/update/deletion, attachment added/removed, and reminder sent flows, using the audit service from task 7.3.

**Step-by-step:**
1. Review audit service from task 7.3 (AuditLogger interface and implementation available).
2. Integrate audit logging into task CRUD operations:
   - **Task creation** (task 3.3): In create task use-case, after task is created, call `audit_logger.log("task_created", user_id, "task", task_id, {"title": task.title, "status": task.status})`.
   - **Task update** (task 3.5): In update task use-case, after task is updated, call `audit_logger.log("task_updated", user_id, "task", task_id, {"old_status": old_task.status, "new_status": task.status, "changes": {...}})`.
   - **Task deletion** (task 3.5): In delete task use-case, after task is deleted, call `audit_logger.log("task_deleted", user_id, "task", task_id, {"title": task.title})`.
3. Integrate audit logging into attachment operations:
   - **Attachment upload** (task 4.3): In upload attachment use-case, after attachment is saved, call `audit_logger.log("attachment_uploaded", user_id, "attachment", attachment_id, {"task_id": task_id, "filename": filename, "file_size": file_size})`.
   - **Attachment deletion** (task 4.4): In delete attachment use-case, after attachment is deleted, call `audit_logger.log("attachment_deleted", user_id, "attachment", attachment_id, {"task_id": task_id, "filename": filename})`.
4. Integrate audit logging into reminder worker:
   - **Reminder sent** (task 6.3): In reminder worker job, after reminder is logged, call `audit_logger.log("reminder_sent", None, "reminder", task_id, {"task_id": task_id, "due_date": task.due_date})` (user_id is None for system actions).
5. Inject audit logger into use-cases:
   - Add audit_logger parameter to use-case constructors or methods.
   - Use dependency injection to provide audit logger instance.
6. Write integration tests:
   - Test task creation creates audit event (verify event in database with action_type="task_created", user_id, timestamp).
   - Test task update creates audit event (verify event with action_type="task_updated", metadata with changes).
   - Test task deletion creates audit event (verify event with action_type="task_deleted").
   - Test attachment upload creates audit event (verify event with action_type="attachment_uploaded").
   - Test attachment deletion creates audit event (verify event with action_type="attachment_deleted").
   - Test reminder sent creates audit event (verify event with action_type="reminder_sent", user_id=None).

**Implementation hints:**
- Inject audit logger into use-cases via constructor or method parameter (dependency injection).
- Call audit logger after successful operation (not before, to ensure operation succeeded).
- Include relevant metadata in audit events (task title, status changes, filename, etc.) but avoid sensitive data.
- For system actions (reminder sent), user_id is None (system-generated, not user-driven).

## Dependencies
- [ ] Task ID: 3.3 (Task creation must exist)
- [ ] Task ID: 3.4 (Task read must exist - for context)
- [ ] Task ID: 3.5 (Task update/delete must exist)
- [ ] Task ID: 4.3 (Attachment upload must exist)
- [ ] Task ID: 4.4 (Attachment delete must exist)
- [ ] Task ID: 6.3 (Reminder worker must exist)
- [ ] Task ID: 7.3 (Audit service must exist)

## Testing Instructions
- Integration tests (API + DB + Audit):
  - Creating, updating, deleting tasks results in appropriate audit events (verify events in database with correct action_type, user_id, metadata).
  - Adding/removing attachments results in appropriate audit events (verify events with action_type="attachment_uploaded"/"attachment_deleted").
  - Reminder worker logs "reminder sent" events (verify events with action_type="reminder_sent", user_id=None).
- Manual test: Perform operations (create task, update task, upload attachment, etc.), verify audit events in database.

## Security Review
- Ensure audit entries do not leak sensitive payloads:
  - Don't log passwords, tokens, or other secrets in metadata.
  - Log only necessary context (task title, status changes, filename, not full task content with sensitive data).

## Risk Assessment
- Missing or incorrect integration may leave gaps in the audit trail.
- Audit logging errors may break main operations (ensure error handling in audit service).
- Missing metadata may reduce audit trail usefulness.

## Acceptance Criteria
- [ ] Audit events are written for all required actions (task CRUD, attachment operations, reminder sent).
- [ ] Events contain timestamp and user ID for user-driven actions (task CRUD, attachment operations - user_id present).
- [ ] Events contain timestamp for system actions (reminder sent - user_id is None, timestamp present).
- [ ] Events contain relevant metadata (task title, status changes, filename, etc.) but no sensitive data.
- [ ] Tests verifying audit entries for each action are passing (all action types create audit events).

## Definition of Done
- [ ] All relevant flows call the audit logging service (task CRUD, attachment operations, reminder worker).
- [ ] Audit logger injected into use-cases (dependency injection configured).
- [ ] Audit events created with correct action_type, user_id, timestamp, metadata.
- [ ] Tests added and passing (all action types create audit events).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests show the presence of audit records for each key operation type (all action types have corresponding audit events).
- **Observable Outcomes**: Audit events appear in database after operations, events have correct fields, events are queryable.

## Notes
Completes the integration layer for the audit trail requirement. This task wires up the audit service from task 7.3 into all relevant operations.

## Strengths
Provides full traceability for key operations in the system. Enables compliance and debugging.

## Sub-tasks (Children)
- [ ] Review audit service from task 7.3 (AuditLogger interface and implementation).
- [ ] Hook audit logging into task creation (call audit_logger.log("task_created", ...) after task created).
- [ ] Hook audit logging into task update (call audit_logger.log("task_updated", ...) after task updated).
- [ ] Hook audit logging into task deletion (call audit_logger.log("task_deleted", ...) after task deleted).
- [ ] Hook audit logging into attachment upload (call audit_logger.log("attachment_uploaded", ...) after attachment saved).
- [ ] Hook audit logging into attachment deletion (call audit_logger.log("attachment_deleted", ...) after attachment deleted).
- [ ] Hook audit logging into reminder worker job (call audit_logger.log("reminder_sent", ...) after reminder logged).
- [ ] Inject audit logger into use-cases (dependency injection).
- [ ] Add integration tests to validate audit coverage (all action types create audit events).
- [ ] Test manually by performing operations and verifying audit events in database.

## Completed
[ ] Pending / [ ] Completed


