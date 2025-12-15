# Task ID: 3.3
# Title: Implement create task endpoint
# Status: [x] Completed
# Priority: critical
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement the API endpoint to create tasks with all required fields and meaningful validation error responses, per `docs/requirements.md` section "2. Task Management" and `docs/technical-specs.md` section "3.2 Task Management".

**Step-by-step:**
1. Review requirements: task fields are `title`, `description`, `status`, `priority`, `due date`, `tags` (per `docs/requirements.md`).
2. Define request schema (e.g., Pydantic model in `backend/application/tasks/schemas.py`):
   - Required: `title` (string, non-empty).
   - Optional: `description`, `status`, `priority`, `due_date` (date), `tags` (list of strings).
   - Validate formats (e.g., date format, non-empty title).
3. Create use-case/service (e.g., `backend/application/tasks/create_task.py`):
   - Accept validated request data and authenticated user ID.
   - Create task entity with owner set to current user ID.
   - Persist via repository interface.
   - Return created task data.
4. Create API endpoint (e.g., `POST /api/tasks` in `backend/api/routes/tasks.py`):
   - Require authentication (use auth middleware from task 2.4).
   - Extract user ID from auth token/session.
   - Call use-case with request data and user ID.
   - Return 201 Created with task data on success.
   - Return 400 Bad Request with validation errors on failure.
5. Implement validation error format (consistent JSON shape, e.g., `{"error": {"code": "VALIDATION_ERROR", "message": "...", "fields": {...}}}`).
6. Write integration tests:
   - Test successful creation with all fields.
   - Test successful creation with minimal fields (title only).
   - Test validation errors (missing title, invalid date format, etc.).
   - Test authentication requirement (401 if not authenticated).
   - Test owner is set correctly (verify task.owner_user_id matches authenticated user).

**Implementation hints:**
- Follow Clean Architecture: endpoint in `backend/api/`, use-case in `backend/application/`, domain entity in `backend/domain/`.
- Use dependency injection for repository (interface in application, implementation in infrastructure).
- Request validation should happen at API boundary (Pydantic models or similar).
- Error responses should be consistent (use centralized error handler if available).
- Task owner must be set from authenticated user (never trust client-provided user ID).

## Dependencies
- [x] Task ID: 3.2 (Task data model must exist)
- [x] Task ID: 2.4 (Authorization guards must exist to extract user ID)

## Testing Instructions
- Integration tests (API + DB):
  - Successful task creation with valid data (all fields).
  - Successful task creation with minimal data (title only, defaults for optional fields).
  - Rejection with clear errors for missing/invalid fields (e.g., empty title, invalid date format).
  - Authentication requirement (401 if no auth token).
  - Owner is set correctly (verify task.owner_user_id matches authenticated user ID).
- Manual test: Use API client (Postman/curl) to create task, verify response and database state.

## Security Review
- Ensure only authenticated users can create tasks (auth middleware required).
- Ensure owner is set from authenticated user ID (never from request body).
- Validate input to prevent injection attacks (use parameterized queries, validate data types).

## Risk Assessment
- Incorrect creation logic or missing validation may cause data issues.
- Missing owner assignment could allow users to create tasks for other users.

## Acceptance Criteria
- [x] Create task endpoint (`POST /api/tasks`) accepts all required fields (`title`, `description`, `status`, `priority`, `due_date`, `tags`) and persists them.
- [x] Endpoint requires authentication (returns 401 if not authenticated).
- [x] Task owner is set to authenticated user ID (never from request).
- [x] Validation errors are returned in a user-friendly format (consistent JSON error shape).
- [x] Validation covers: missing title, invalid date format, invalid status/priority values (if enums).
- [x] Integration tests for successful and failing creation are passing.
- [x] Task is persisted in database with correct fields and owner.

## Definition of Done
- [ ] Endpoint implemented and wired to the task model.
- [ ] Request/response schemas defined (Pydantic or similar).
- [ ] Use-case/service implemented following Clean Architecture.
- [ ] Validation logic added (API boundary and use-case level).
- [ ] Authentication requirement enforced.
- [ ] Owner assignment verified (from auth, not request).
- [ ] Integration tests added and passing (success and failure cases).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Integration tests confirm correct behavior and validation (all test cases pass).
- **Observable Outcomes**: Endpoint responds correctly to valid/invalid requests, tasks appear in database with correct owner.

## Notes
This endpoint is used by the frontend create-task view (task 10.4). Ensure error format is consistent for frontend consumption.

**Completed**: 
- Create task endpoint implemented: POST /api/tasks
- Request/response schemas defined with Pydantic
- Use case implemented following Clean Architecture
- Repository pattern implemented (interface + SQLAlchemy implementation)
- Owner set from authenticated user (never from request)
- Validation with user-friendly error responses
- Integration tests for success and failure cases

## Strengths
Implements the "Create" part of Task Management requirement.

## Sub-tasks (Children)
- [ ] Review task fields from `docs/requirements.md` (title, description, status, priority, due date, tags).
- [ ] Define request/response schema (Pydantic models or similar) with validation rules.
- [ ] Implement use-case/service for task creation (accept data + user ID, create entity, persist).
- [ ] Create API endpoint handler (`POST /api/tasks`) with auth requirement.
- [ ] Implement validation error responses (consistent JSON format).
- [ ] Write integration tests (success cases, validation errors, auth requirement, owner verification).
- [ ] Test manually with API client to verify behavior.

## Completed
[x] Completed


