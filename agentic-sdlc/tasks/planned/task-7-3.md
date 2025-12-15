# Task ID: 7.3
# Title: Implement audit logging service
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement an audit logging API/service that other modules can call to record audit events, using the schema from task 7.2.

**Step-by-step:**
1. Review audit schema from task 7.2 (AuditEvent model with action_type, user_id, timestamp, resource_type, resource_id, metadata).
2. Create audit logging interface (port in Clean Architecture):
   - Create `AuditLogger` interface in `backend/application/audit/audit_logger.py`:
     - Method: `log(action_type: str, user_id: Optional[int], resource_type: str, resource_id: str, metadata: Optional[dict]) -> None`
     - Or use more specific methods: `log_task_created(task_id, user_id, metadata)`, `log_task_updated(task_id, user_id, metadata)`, etc.
3. Create audit logging implementation (adapter):
   - Create `AuditLoggerImpl` in `backend/infrastructure/audit/audit_logger.py`:
     - Implement interface methods.
     - Create AuditEvent entity from parameters.
     - Persist via repository (save to database).
     - Handle errors gracefully (log error, don't throw - audit should not break main flow).
4. Create audit repository:
   - Create `AuditRepository` interface in `backend/application/audit/repository.py`.
   - Create `AuditRepositoryImpl` in `backend/infrastructure/persistence/repositories/audit_repository.py`:
     - Methods: `save(event: AuditEvent) -> None`, `find_by_action_type(action_type: str) -> List[AuditEvent]`, etc.
5. Wire up dependency injection:
   - Register audit logger in DI container (or use factory pattern).
   - Make audit logger available to use-cases and API handlers.
6. Write unit/integration tests:
   - Test audit service logs events correctly (verify event persisted in database).
   - Test audit service handles errors gracefully (verify errors logged, main flow continues).
   - Test audit service with different action types (verify all action types work).

**Implementation hints:**
- Place interface in `backend/application/audit/` (port).
- Place implementation in `backend/infrastructure/audit/` (adapter).
- Use dependency injection for audit logger (inject into use-cases, not directly instantiate).
- Make audit logging non-blocking (async or fire-and-forget) to avoid slowing down main operations - optional enhancement.
- Use structured logging for audit service errors (log action_type, user_id, error details).

## Dependencies
- [ ] Task ID: 7.2 (Audit schema must be complete)

## Testing Instructions
- Unit or integration tests (API + DB):
  - Call the audit service and verify events are persisted correctly (verify event in database with correct fields).
  - Test different action types (task_created, task_updated, attachment_uploaded, etc.).
  - Test error handling (simulate database error, verify error logged, main flow continues).
- Manual test: Call audit service directly, verify events appear in database.

## Security Review
- Ensure service does not log secrets or overly detailed sensitive data:
  - Don't log passwords, tokens, or other secrets in metadata.
  - Log only necessary context (e.g., task title, status changes, not full task content with sensitive data).

## Risk Assessment
- If audit logging is unreliable, important events may be lost.
- Blocking audit logging can slow down main operations (consider async/fire-and-forget).
- Missing error handling can cause audit failures to break main flow.

## Acceptance Criteria
- [ ] Audit logging service/API implemented with a clear interface (interface and implementation exist).
- [ ] Events persisted using the audit schema (events saved to database with correct fields).
- [ ] Service handles errors gracefully (errors logged, main flow continues, doesn't throw).
- [ ] Tests for audit service behavior are passing (logging works, error handling works).

## Definition of Done
- [ ] Service wired to persistence layer (repository implemented, events saved to database).
- [ ] Audit logger interface and implementation created.
- [ ] Dependency injection configured (audit logger available to use-cases).
- [ ] Error handling implemented (errors logged, main flow continues).
- [ ] Tests added and passing (logging works, error handling works).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests confirm that events are logged and retrievable as expected (events in database, correct fields, queryable).
- **Observable Outcomes**: Audit service can be called, events are persisted, errors are handled gracefully.

## Notes
This service is the central integration point for all audited actions. It will be used by task CRUD, attachment operations, and reminder worker in task 7.4.

## Strengths
Encapsulates audit logic and reduces duplication across modules. Provides consistent audit logging interface.

## Sub-tasks (Children)
- [ ] Review audit schema from task 7.2 (AuditEvent model).
- [ ] Create audit logging interface (port in `backend/application/audit/audit_logger.py`).
- [ ] Create audit logging implementation (adapter in `backend/infrastructure/audit/audit_logger.py`).
- [ ] Create audit repository (interface and implementation).
- [ ] Wire up dependency injection (register audit logger in DI container).
- [ ] Implement error handling (errors logged, main flow continues).
- [ ] Write unit/integration tests (logging works, error handling works, different action types).
- [ ] Test manually by calling audit service and verifying events in database.

## Completed
[ ] Pending / [ ] Completed


