# Task ID: 2.3
# Title: Implement login endpoint
# Status: [ ] Pending
# Priority: critical
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement a login endpoint that authenticates users using the chosen auth mechanism and returns appropriate responses for success and failure, per `docs/requirements.md` section "1. Secure Login" and `docs/technical-specs.md` section "3.1 Secure Login".

**Step-by-step:**
1. Review auth configuration from task 2.2 (JWT or OIDC/OAuth2 setup should be complete).
2. Define login request schema (e.g., Pydantic model in `backend/application/auth/schemas.py`):
   - Required: `username` or `email` (string), `password` (string).
   - Validate: non-empty fields, email format if using email.
3. Create login use-case/service (e.g., `backend/application/auth/login.py`):
   - Accept username/email and password.
   - Query user from database by username/email.
   - Verify password (use `bcrypt` or similar, never store plaintext).
   - If valid: generate auth token (JWT) or initiate OAuth flow.
   - If invalid: return error (generic message, don't reveal if user exists).
4. Create API endpoint (e.g., `POST /api/auth/login` in `backend/api/routes/auth.py`):
   - Accept login request (username/email + password).
   - Call login use-case.
   - On success: return 200 OK with token/session info (e.g., `{"token": "...", "user": {...}}`).
   - On failure: return 401 Unauthorized with generic error (e.g., `{"error": {"code": "INVALID_CREDENTIALS", "message": "Invalid username or password"}}`).
5. Implement security best practices:
   - Never log passwords.
   - Use constant-time password comparison (prevent timing attacks).
   - Rate limit login attempts (prevent brute force).
   - Return generic errors (don't reveal if username exists).
6. Write integration tests:
   - Test successful login with valid credentials (verify token returned).
   - Test failed login with invalid password (verify 401, generic error).
   - Test failed login with non-existent user (verify 401, generic error - same as invalid password).
   - Test rate limiting (if implemented).

**Implementation hints:**
- For JWT: Use `python-jose` to create token with user ID, expiration (e.g., 24h), and algorithm (HS256 or RS256).
- For password hashing: Use `bcrypt` or `argon2` (never store plaintext, hash on user creation).
- Place use-case in `backend/application/auth/` following Clean Architecture.
- Place endpoint in `backend/api/routes/auth.py`.
- Token should include user ID (for authorization checks later).
- Response format: `{"token": "jwt-token-string", "user": {"id": 1, "username": "..."}}` or similar.

## Dependencies
- [ ] Task ID: 2.2 (Auth configuration must be complete)

## Testing Instructions
- Integration tests (API + DB):
  - Successful login with valid credentials (verify 200, token returned, token is valid JWT).
  - Rejected login with invalid password (verify 401, generic error message).
  - Rejected login with non-existent user (verify 401, same generic error - no user enumeration).
  - Verify that responses contain tokens or session information as expected (token format, expiration).
- Manual test: Use API client (Postman/curl) to login, verify response and token validity.

## Security Review
- Ensure password handling and token/session issuance follow best practices:
  - Passwords hashed with bcrypt/argon2 (never plaintext).
  - Constant-time password comparison.
  - Generic error messages (no user enumeration).
  - Token expiration set (e.g., 24 hours).
  - Rate limiting on login endpoint (prevent brute force).
- Ensure no passwords are logged or exposed in error messages.

## Risk Assessment
- Incorrect login behavior may expose the system to unauthorized access.
- Weak password hashing or token generation can compromise security.
- User enumeration (revealing if username exists) can aid attackers.

## Acceptance Criteria
- [ ] Login endpoint (`POST /api/auth/login`) exists and authenticates users according to the chosen auth method (JWT or OAuth2).
- [ ] Successful login returns necessary auth information to the client (token + user info, 200 status).
- [ ] Failed login attempts return meaningful error responses without leaking sensitive details (401, generic "Invalid username or password").
- [ ] Password verification uses secure hashing (bcrypt/argon2, not plaintext).
- [ ] Integration tests for successful and failed login are passing.
- [ ] Rate limiting is implemented (optional but recommended).

## Definition of Done
- [ ] Endpoint implemented and wired to user credentials storage (database).
- [ ] Login use-case/service implemented (password verification, token generation).
- [ ] Request/response schemas defined (Pydantic or similar).
- [ ] Validation and error handling implemented (generic errors, no user enumeration).
- [ ] Security best practices applied (password hashing, token expiration, rate limiting if implemented).
- [ ] Integration tests added and passing (success and failure cases).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Login tests pass and manual login via API works as expected (token returned, token is valid).
- **Observable Outcomes**: Endpoint responds correctly to valid/invalid credentials, token can be used for subsequent requests.

## Notes
Frontend UI for login is covered in Task 10.4 and will consume this endpoint. Ensure response format is consistent for frontend consumption.

## Strengths
Directly supports the "Secure Login" requirement of the assignment. Provides foundation for all authenticated API calls.

## Sub-tasks (Children)
- [ ] Review auth configuration from task 2.2 (JWT secret, algorithm, etc.).
- [ ] Define login request/response schema (Pydantic models: username/email + password, token + user info).
- [ ] Create login use-case/service (query user, verify password with bcrypt, generate JWT token).
- [ ] Create API endpoint handler (`POST /api/auth/login`) with request validation.
- [ ] Implement security best practices (password hashing, generic errors, rate limiting if applicable).
- [ ] Write integration tests (successful login, invalid password, non-existent user, rate limiting).
- [ ] Test manually with API client to verify behavior and token validity.

## Completed
[ ] Pending / [ ] Completed


