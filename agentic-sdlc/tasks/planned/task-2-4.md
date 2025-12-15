# Task ID: 2.4
# Title: Implement change-password endpoint
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement a change-password endpoint that allows authenticated users to change their password securely, per `docs/requirements.md` section "10. Front-End" (change password functionality) and `docs/technical-specs.md` section "3.10 Front‑End".

**Step-by-step:**
1. Review requirements: change password must be supported (backend endpoint + frontend UI per docs).
2. Define change-password request schema (e.g., Pydantic model in `backend/application/auth/schemas.py`):
   - Required: `current_password` (string), `new_password` (string).
   - Optional: `confirm_password` (string, validate it matches new_password) or validate on frontend.
   - Validate: new_password meets strength requirements (min length, complexity if required).
3. Create change-password use-case/service (e.g., `backend/application/auth/change_password.py`):
   - Accept authenticated user ID (from auth token), current_password, new_password.
   - Query user from database by user ID.
   - Verify current_password matches stored hash (use bcrypt).
   - If current password incorrect: return error.
   - If correct: hash new_password with bcrypt, update user record.
   - Return success.
4. Create API endpoint (e.g., `POST /api/auth/change-password` or `PUT /api/auth/password` in `backend/api/routes/auth.py`):
   - Require authentication (extract user ID from auth token).
   - Accept change-password request (current_password + new_password).
   - Call change-password use-case with user ID and passwords.
   - On success: return 200 OK with success message.
   - On failure (wrong current password): return 401 Unauthorized or 400 Bad Request with error.
   - On failure (unauthenticated): return 401 Unauthorized.
5. Implement security best practices:
   - Never log passwords.
   - Hash new password with bcrypt before storing.
   - Validate password strength (min length 8, complexity if required).
   - Require authentication (user can only change their own password).
6. Write integration tests:
   - Test successful password change for authenticated user (verify new password works for login).
   - Test rejection when current password is incorrect (verify 401/400 error).
   - Test rejection when unauthenticated (verify 401 error).
   - Test password strength validation (if implemented, verify weak passwords rejected).

**Implementation hints:**
- Use same password hashing as login (bcrypt with same cost factor).
- Place use-case in `backend/application/auth/` following Clean Architecture.
- Place endpoint in `backend/api/routes/auth.py` (same file as login).
- Extract user ID from auth token (JWT decode or session lookup).
- Response format: `{"message": "Password changed successfully"}` on success.
- Error format: `{"error": {"code": "INVALID_CURRENT_PASSWORD", "message": "Current password is incorrect"}}`.

## Dependencies
- [ ] Task ID: 2.3 (Login endpoint must exist for authentication)

## Testing Instructions
- Integration tests (API + DB):
  - Successful password change for authenticated user (verify 200, new password works for login).
  - Rejection when current password is incorrect (verify 401/400, error message).
  - Rejection when unauthenticated (verify 401, no token provided).
  - Test password strength validation (if implemented, verify weak passwords rejected).
- Manual test: Use API client to change password, verify new password works for login.

## Security Review
- Verify password strength rules (if applied) and secure storage:
  - New password hashed with bcrypt (never plaintext).
  - Password strength validation (min length, complexity if required).
  - Current password verified before allowing change.
- Ensure no passwords are logged or exposed in error messages.
- Ensure only authenticated users can change password (auth required).

## Risk Assessment
- Weak or incorrect change-password logic can compromise user accounts.
- Missing current password verification allows unauthorized password changes.
- Weak password strength allows easily compromised accounts.

## Acceptance Criteria
- [ ] Change-password endpoint (`POST /api/auth/change-password` or similar) requires authentication (returns 401 if not authenticated).
- [ ] Endpoint verifies current password before allowing change (returns error if current password incorrect).
- [ ] Endpoint updates the user password in storage securely (hashed with bcrypt, not plaintext).
- [ ] Error responses are meaningful without exposing sensitive information (generic errors, no password hints).
- [ ] Integration tests for change-password flows are passing (success, wrong current password, unauthenticated).
- [ ] New password works for login after change (verify end-to-end).

## Definition of Done
- [ ] Endpoint implemented and integrated with user storage (database).
- [ ] Change-password use-case/service implemented (current password verification, new password hashing).
- [ ] Request/response schemas defined (Pydantic or similar).
- [ ] Authentication requirement enforced (extract user ID from token).
- [ ] Security best practices applied (password hashing, strength validation if implemented).
- [ ] Tests added and passing (success, wrong current password, unauthenticated).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests confirm that only authenticated users can change their password and that new password works for login.
- **Observable Outcomes**: Endpoint responds correctly to valid/invalid requests, password change persists, new password works.

## Notes
Frontend UI for change-password is implemented in Task 10.6 and will consume this endpoint. Ensure response format is consistent for frontend consumption.

## Strengths
Completes the "Change password functionality" part of the requirements. Provides secure password management for users.

## Sub-tasks (Children)
- [ ] Review change-password requirements from `docs/requirements.md` and `docs/technical-specs.md`.
- [ ] Define change-password request/response schema (current_password, new_password, validation rules).
- [ ] Create change-password use-case/service (verify current password, hash new password, update user).
- [ ] Create API endpoint handler (`POST /api/auth/change-password`) with auth requirement.
- [ ] Implement security best practices (password hashing, strength validation, generic errors).
- [ ] Write integration tests (successful change, wrong current password, unauthenticated, password strength).
- [ ] Test manually with API client and verify new password works for login.

## Completed
[ ] Pending / [ ] Completed


