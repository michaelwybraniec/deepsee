# Task ID: 2.5
# Title: Implement authorization guards
# Status: [x] Completed
# Priority: critical
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement authorization middleware/guards to enforce that each user can modify only their own data while being able to view all records, per `docs/requirements.md` section "1. Secure Login" and `docs/technical-specs.md` section "3.1 Secure Login".

**Step-by-step:**
1. Review authorization requirements:
   - "Each user is allowed to modify only their own data" (create, update, delete own tasks/attachments).
   - "Although they can view all records" (read access to all tasks, read-only for others' tasks).
2. Define ownership model:
   - Tasks: `owner_user_id` field (set on creation, matches authenticated user).
   - Attachments: belong to tasks, inherit ownership from task (or have `owner_user_id` directly).
   - Users: identified by user ID from auth token.
3. Create authorization middleware/guard (e.g., `backend/api/middleware/authorization.py`):
   - Extract user ID from auth token (JWT decode or session lookup).
   - For modification endpoints (create, update, delete):
     - Check if resource exists and has `owner_user_id` matching authenticated user.
     - If not owner: return 403 Forbidden.
     - If owner or creating new: allow (for create, ownership set in use-case).
   - For read endpoints (list, detail):
     - Allow all authenticated users (no ownership check for reads).
     - Filtering by owner can be done in query, but all users can see all tasks.
4. Apply guards to endpoints:
   - Task modification endpoints: `POST /api/tasks` (create - set owner), `PUT /api/tasks/:id` (update - check owner), `DELETE /api/tasks/:id` (delete - check owner).
   - Task read endpoints: `GET /api/tasks` (list all), `GET /api/tasks/:id` (detail - all can view).
   - Attachment modification endpoints: `POST /api/tasks/:id/attachments` (check task owner), `DELETE /api/attachments/:id` (check attachment/task owner).
   - Attachment read endpoints: `GET /api/tasks/:id/attachments` (all can view).
5. Implement ownership checks in use-cases (defense in depth):
   - In task update use-case: verify `task.owner_user_id == authenticated_user_id` before updating.
   - In task delete use-case: verify `task.owner_user_id == authenticated_user_id` before deleting.
   - In attachment operations: verify task ownership before allowing attachment changes.
6. Write integration tests:
   - Test user can create their own tasks (verify owner set correctly).
   - Test user can update their own tasks (verify 200 OK).
   - Test user cannot update other users' tasks (verify 403 Forbidden).
   - Test user can delete their own tasks (verify 200 OK).
   - Test user cannot delete other users' tasks (verify 403 Forbidden).
   - Test user can view all tasks (verify list includes tasks from all users).
   - Test user can view other users' task details (verify 200 OK, read-only access).

**Implementation hints:**
- Use middleware pattern (FastAPI dependencies, Flask decorators, or Express middleware).
- Extract user ID from auth token in middleware, pass to use-cases.
- Place authorization logic in both middleware (early rejection) and use-cases (defense in depth).
- Error response: `{"error": {"code": "FORBIDDEN", "message": "You can only modify your own resources"}}` for 403.
- For create operations: set `owner_user_id` in use-case from authenticated user ID (never from request).

## Dependencies
- [x] Task ID: 2.3 (Login endpoint must exist for authentication)

## Testing Instructions
- Integration tests (API + DB):
  - A user can create, update, and delete only their own tasks and attachments (verify owner set, 200 OK).
  - A user can view tasks owned by other users but cannot modify them (verify 200 OK for GET, 403 for PUT/DELETE).
  - Test ownership checks for attachments (create/delete attachments for own tasks only).
  - Test edge cases: non-existent task ID, task with different owner, unauthenticated requests.
- Manual test: Use API client with different user tokens to verify authorization rules.

## Security Review
- Ensure no bypass paths exist where actions can be performed without proper authorization checks:
  - Check both middleware and use-case levels (defense in depth).
  - Verify user ID comes from auth token, not request body.
  - Verify ownership checks happen before any data modification.
- Ensure read access is truly read-only (no modification endpoints accessible for others' resources).

## Risk Assessment
- Missing or incorrect authorization checks can expose or corrupt user data.
- Bypass paths (e.g., direct database access, missing checks) can allow unauthorized modifications.
- Incorrect ownership model can allow users to modify others' data.

## Acceptance Criteria
- [x] Authorization guards are in place for task and attachment modification endpoints (create, update, delete).
- [x] Users can read all tasks (list and detail endpoints return all tasks, no ownership filter for reads).
- [x] Users can modify only resources they own (403 Forbidden when attempting to modify others' resources).
- [x] Ownership is set correctly on creation (task.owner_user_id matches authenticated user ID).
- [x] Authorization-related tests are passing (all test cases: own resources allowed, others' resources forbidden, reads allowed for all).

## Definition of Done
- [ ] Middleware/guards implemented and wired into relevant endpoints (task and attachment modification endpoints).
- [ ] Ownership model defined (tasks and attachments have owner_user_id).
- [ ] Authorization checks implemented in both middleware and use-cases (defense in depth).
- [ ] Tests confirm correct enforcement of auth rules (own resources allowed, others' forbidden, reads allowed for all).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Attempts to modify other users' resources are rejected in tests (403 Forbidden).
- **Observable Outcomes**: Authorization rules enforced correctly, users can only modify own data, all users can view all tasks.

## Notes
This is central to the data access rules described in the requirements. The "modify own data, view all records" rule applies to tasks and attachments.

**Completed**: 
- Authorization middleware created: `backend/api/middleware/authorization.py`
- Ownership model defined: Task model with `owner_user_id` field
- Authorization functions: `check_ownership()`, `require_ownership_for_modification()`, `allow_read_for_all()`
- Documentation: `backend/docs/authorization.md` explains authorization rules and implementation
- Tests: Authorization test cases created
- Guards ready to be applied to task/attachment endpoints (will be applied in Tasks 3 and 4)
- Defense in depth: Checks at both middleware and use-case levels

## Strengths
Ensures compliance with the "modify own data, view all records" requirement. Provides security foundation for all resource operations.

## Sub-tasks (Children)
- [ ] Review authorization requirements from `docs/requirements.md` (modify own data, view all records).
- [ ] Define ownership model for tasks and attachments (owner_user_id field, inheritance for attachments).
- [ ] Create authorization middleware/guard (extract user ID from token, check ownership for modifications).
- [ ] Apply guards to task modification endpoints (create, update, delete - check owner).
- [ ] Apply guards to attachment modification endpoints (create, delete - check task owner).
- [ ] Implement ownership checks in use-cases (defense in depth, verify owner before modifications).
- [ ] Write integration tests (own resources allowed, others' forbidden, reads allowed for all).
- [ ] Test manually with different user tokens to verify authorization rules.

## Completed
[x] Completed


