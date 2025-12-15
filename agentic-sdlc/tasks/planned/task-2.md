# Task ID: 2
# Title: Secure login and authorization
# Status: [x] Completed
# Priority: critical
# Owner: Backend Dev
# Estimated Effort: 8h

## Description
Implement modern authentication (OIDC/OAuth2 or JWT-based) and authorization rules so that each user can modify only their own data while being able to view all records.

## Dependencies
- [x] Task ID: 1

## Testing Instructions
- API integration tests for:
  - Successful login with valid credentials.
  - Rejection of invalid credentials.
  - Access control checks: user can modify only own tasks but can read others.
- UI smoke test for login flow.

## Security Review
- Verify token handling, password storage, and session/refresh behavior.
- Ensure no sensitive data is logged.

## Risk Assessment
- Weak or incorrect auth logic may expose user data or allow unauthorized modification.

## Acceptance Criteria
- [x] Login endpoint implemented with OIDC/OAuth2 or JWT.
- [x] Auth middleware/guards enforce modification rules.
- [x] Users can read all tasks but only create/update/delete their own.
- [x] Auth failures return meaningful error responses.
- [x] Basic tests for login and auth rules are passing.

## Definition of Done
- [ ] Auth endpoints and middleware implemented.
- [ ] Core auth tests (unit/integration) written and pass.
- [ ] No obvious security flaws in auth flow.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Auth-protected endpoints cannot be modified by unauthorized users in tests.
- **Quality Attributes**: Authentication and authorization behavior is predictable and covered by tests.

## Notes
This task provides the foundation for all other protected operations (tasks, attachments, etc.).

## Strengths
Directly satisfies the “Secure Login” requirement and per-user modification rules.

## Sub-tasks (Children)
- [x] [Task 2.1: Analyze authentication and authorization requirements](task-2-1.md)
- [x] [Task 2.2: Choose and configure authentication approach](task-2-2.md)
- [x] [Task 2.3: Implement login endpoint](task-2-3.md)
- [x] [Task 2.4: Implement change-password endpoint](task-2-4.md)
- [x] [Task 2.5: Implement authorization guards](task-2-5.md)

## Completed
[x] Completed


