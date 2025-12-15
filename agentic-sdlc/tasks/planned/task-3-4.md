# Task ID: 3.4
# Title: Implement read task endpoints
# Status: [x] Completed
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement endpoints to read a single task by ID and to list tasks (later extended with search/filter/sort/pagination), per `docs/requirements.md` section "2. Task Management" and `docs/technical-specs.md` section "3.2 Task Management".

**Step-by-step:**
1. Review requirements: users can "view all records" (read access to all tasks, not just own).
2. Create get-by-ID use-case (e.g., `backend/application/tasks/get_task.py`):
   - Accept task ID and authenticated user ID (for logging, not filtering).
   - Query task from repository by ID.
   - Return task data (all users can view all tasks, no ownership check for reads).
3. Create list tasks use-case (e.g., `backend/application/tasks/list_tasks.py`):
   - Accept authenticated user ID (for logging, not filtering).
   - Query all tasks from repository (no ownership filter - all users see all tasks).
   - Return list of tasks (basic list, no search/filter yet - that's task 5).
4. Create API endpoints:
   - `GET /api/tasks/:id` (get single task):
     - Require authentication (extract user ID from token).
     - Call get-by-ID use-case.
     - Return 200 OK with task data, or 404 Not Found if task doesn't exist.
   - `GET /api/tasks` (list tasks):
     - Require authentication (extract user ID from token).
     - Call list tasks use-case.
     - Return 200 OK with array of tasks (all tasks, not filtered by owner).
5. Define response schemas (e.g., Pydantic models):
   - Task response: id, title, description, status, priority, due_date, tags, owner_user_id, created_at, updated_at
   - List response: array of task objects
6. Write integration tests:
   - Test get single task by ID (verify 200, task data returned).
   - Test get non-existent task (verify 404).
   - Test list tasks (verify all tasks returned, including tasks from other users).
   - Test unauthenticated access (verify 401).

**Implementation hints:**
- Follow Clean Architecture: use-case in `backend/application/tasks/`, endpoint in `backend/api/routes/tasks.py`.
- Use repository interface (defined in task 3.2) to query tasks.
- Response format: `{"id": 1, "title": "...", "description": "...", ...}` for single task, `[{"id": 1, ...}, {"id": 2, ...}]` for list.
- No ownership filtering for reads (all authenticated users can view all tasks per requirements).

## Dependencies
- [x] Task ID: 3.2 (Task model must exist)

## Testing Instructions
- Integration tests (API + DB):
  - Fetch single task by ID (verify 200, correct task data returned).
  - Fetch non-existent task (verify 404 Not Found).
  - List tasks for the current user context (including others' tasks in read-only fashion - verify all tasks returned).
  - Test unauthenticated access (verify 401 Unauthorized).
- Manual test: Use API client to get task by ID and list tasks, verify responses.

## Security Review
- Ensure read endpoints do not leak sensitive data and respect auth rules:
  - Authentication required (401 if not authenticated).
  - All authenticated users can view all tasks (no ownership filter for reads).
  - Response does not include sensitive fields (if any - task data should be safe to expose).

## Risk Assessment
- Incorrect read logic could expose or hide tasks incorrectly.
- Missing authentication check could allow unauthorized access.

## Acceptance Criteria
- [x] Endpoint to fetch a single task by ID (`GET /api/tasks/:id`) implemented (returns 200 with task data or 404 if not found).
- [x] Endpoint to list tasks (`GET /api/tasks`) implemented, returning tasks the user is allowed to view (all tasks, not filtered by owner).
- [x] Both endpoints require authentication (return 401 if not authenticated).
- [x] Tests for basic read operations are passing (get by ID, list all, 404, 401).

## Definition of Done
- [ ] Read endpoints wired to the task model (use-cases and API handlers implemented).
- [ ] Get-by-ID use-case implemented (query by ID, return task or None).
- [ ] List tasks use-case implemented (query all tasks, return list).
- [ ] Response schemas defined (Pydantic models or similar).
- [ ] Tests added and passing (success cases, 404, 401).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Read tests confirm that tasks are returned as expected (correct data, all tasks visible, proper error handling).
- **Observable Outcomes**: Endpoints respond correctly, tasks are returned, authentication is enforced.

## Notes
Advanced search/filter functionality is implemented in Task 5. This task only implements basic read operations (get by ID, list all).

**Completed**: 
- Get task by ID endpoint: GET /api/tasks/:id
- List tasks endpoint: GET /api/tasks
- Both endpoints require authentication
- All users can view all tasks (no ownership filter for reads)
- Use cases implemented: get_task_by_id, list_tasks
- Integration tests for success, 404, and unauthenticated cases

## Strengths
Implements the "View" part of Task Management. Provides foundation for search/filter operations in task 5.

## Sub-tasks (Children)
- [ ] Review read requirements from `docs/requirements.md` (view all records, read access to all tasks).
- [ ] Create get-by-ID use-case (accept task ID, query repository, return task or None).
- [ ] Create list tasks use-case (query all tasks from repository, return list).
- [ ] Create API endpoint `GET /api/tasks/:id` (require auth, call use-case, return 200/404).
- [ ] Create API endpoint `GET /api/tasks` (require auth, call use-case, return 200 with all tasks).
- [ ] Define response schemas (Pydantic models for task response and list response).
- [ ] Write integration tests (get by ID success, get by ID 404, list all tasks, unauthenticated 401).
- [ ] Test manually with API client to verify behavior.

## Completed
[x] Completed


