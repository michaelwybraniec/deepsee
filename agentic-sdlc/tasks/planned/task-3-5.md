# Task ID: 3.5
# Title: Implement update and delete task endpoints
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement update and delete endpoints for tasks, enforcing that only the owner can modify or delete tasks, per `docs/requirements.md` section "2. Task Management" and `docs/technical-specs.md` section "3.2 Task Management".

**Step-by-step:**
1. Review authorization requirements: "modify only their own data" (update and delete require ownership check).
2. Create update task use-case (e.g., `backend/application/tasks/update_task.py`):
   - Accept task ID, update data (title, description, status, priority, due_date, tags), and authenticated user ID.
   - Query task from repository by ID.
   - Verify `task.owner_user_id == authenticated_user_id` (ownership check).
   - If not owner: return authorization error.
   - If owner: update task fields, persist via repository, return updated task.
3. Create delete task use-case (e.g., `backend/application/tasks/delete_task.py`):
   - Accept task ID and authenticated user ID.
   - Query task from repository by ID.
   - Verify `task.owner_user_id == authenticated_user_id` (ownership check).
   - If not owner: return authorization error.
   - If owner: delete task via repository, return success.
4. Create API endpoints:
   - `PUT /api/tasks/:id` or `PATCH /api/tasks/:id` (update task):
     - Require authentication (extract user ID from token).
     - Accept update request (partial task data).
     - Call update use-case with task ID, update data, and user ID.
     - Return 200 OK with updated task, 403 Forbidden if not owner, 404 Not Found if task doesn't exist.
   - `DELETE /api/tasks/:id` (delete task):
     - Require authentication (extract user ID from token).
     - Call delete use-case with task ID and user ID.
     - Return 204 No Content on success, 403 Forbidden if not owner, 404 Not Found if task doesn't exist.
5. Define request schemas (e.g., Pydantic models):
   - Update request: partial task fields (title, description, status, priority, due_date, tags - all optional for PATCH).
   - Validate fields (e.g., status enum, date format).
6. Write integration tests:
   - Test owner can update their task (verify 200, task updated).
   - Test owner can delete their task (verify 204, task deleted).
   - Test non-owner cannot update others' tasks (verify 403 Forbidden).
   - Test non-owner cannot delete others' tasks (verify 403 Forbidden).
   - Test update/delete non-existent task (verify 404).
   - Test unauthenticated access (verify 401).

**Implementation hints:**
- Follow Clean Architecture: use-cases in `backend/application/tasks/`, endpoints in `backend/api/routes/tasks.py`.
- Ownership check should happen in use-case (defense in depth, even if middleware checks).
- Use PATCH for partial updates (only send fields to update) or PUT for full replacement.
- Response format: `{"id": 1, "title": "...", ...}` for update, 204 No Content for delete.
- Authorization errors: `{"error": {"code": "FORBIDDEN", "message": "You can only modify your own tasks"}}`.

## Dependencies
- [ ] Task ID: 2.5 (Authorization guards must exist - middleware checks)
- [ ] Task ID: 3.2 (Task model must exist)

## Testing Instructions
- Integration tests (API + DB):
  - Owner can update and delete their tasks (verify 200/204, changes persisted).
  - Non-owners receive authorization errors when trying to update or delete (verify 403 Forbidden).
  - Test update/delete non-existent task (verify 404 Not Found).
  - Test unauthenticated access (verify 401 Unauthorized).
- Manual test: Use API client with different user tokens to verify ownership enforcement.

## Security Review
- Verify that ownership checks are in place and cannot be bypassed:
  - Check in both middleware (task 2.5) and use-case (defense in depth).
  - Verify user ID comes from auth token, not request body.
  - Verify ownership check happens before any data modification.

## Risk Assessment
- Missing checks may allow users to modify or delete others' tasks.
- Bypass paths (e.g., direct repository access) can allow unauthorized modifications.

## Acceptance Criteria
- [ ] Update task endpoint (`PUT /api/tasks/:id` or `PATCH /api/tasks/:id`) implemented and enforces ownership (403 if not owner, 200 if owner).
- [ ] Delete task endpoint (`DELETE /api/tasks/:id`) implemented and enforces ownership (403 if not owner, 204 if owner).
- [ ] Both endpoints require authentication (401 if not authenticated).
- [ ] Ownership checks happen in use-case (defense in depth, even if middleware checks).
- [ ] Tests for allowed and forbidden operations are passing (owner can update/delete, non-owner gets 403).

## Definition of Done
- [ ] Endpoints implemented and wired to auth/authorization logic (use-cases and API handlers).
- [ ] Update task use-case implemented (ownership check, update fields, persist).
- [ ] Delete task use-case implemented (ownership check, delete, return success).
- [ ] Request schemas defined (Pydantic models for update request).
- [ ] Tests added and passing (owner success, non-owner 403, 404, 401).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests confirm that only owners can modify/delete tasks (403 for non-owners, 200/204 for owners).
- **Observable Outcomes**: Endpoints enforce ownership correctly, tasks are updated/deleted only by owners.

## Notes
This completes the "Edit" and "Delete" parts of Task Management. Authorization middleware from task 2.5 provides additional protection, but use-case checks are required for defense in depth.

## Strengths
Enforces data ownership rules as required by the assignment. Provides secure task modification and deletion.

## Sub-tasks (Children)
- [ ] Review authorization requirements from `docs/requirements.md` (modify only own data).
- [ ] Create update task use-case (accept task ID, update data, user ID; verify ownership, update, persist).
- [ ] Create delete task use-case (accept task ID, user ID; verify ownership, delete, return success).
- [ ] Create API endpoint `PUT /api/tasks/:id` or `PATCH /api/tasks/:id` (require auth, call use-case, return 200/403/404).
- [ ] Create API endpoint `DELETE /api/tasks/:id` (require auth, call use-case, return 204/403/404).
- [ ] Define request schemas (Pydantic models for update request with validation).
- [ ] Write integration tests (owner success, non-owner 403, 404, 401).
- [ ] Test manually with different user tokens to verify ownership enforcement.

## Completed
[ ] Pending / [ ] Completed


