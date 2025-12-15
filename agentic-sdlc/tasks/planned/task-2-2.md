# Task ID: 2.2
# Title: Choose and configure authentication approach
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Choose and configure the authentication mechanism (OIDC/OAuth2 or JWT) for the backend API in line with the requirements from `docs/requirements.md` section "1. Secure Login" and `docs/technical-specs.md` section "3.1 Secure Login".

**Step-by-step:**
1. Review requirements: must support "modern authentication (OIDC/OAuth2 or JWT-based)" per `docs/requirements.md`.
2. Review technology decisions: See `docs/technology.md` section "3. Authentication & Security" for recommended choices, versions, and rationale.
3. Evaluate options:
   - **JWT**: Simpler for single-tenant, stateless, good for API-first. Requires token generation/validation logic.
   - **OIDC/OAuth2**: Better for multi-tenant, external identity providers, but adds complexity.
4. Make decision and document rationale (consider: project scope, time constraints, security needs). Update `docs/technology.md` decision log if choice differs from recommendation.
5. Install/configure chosen library (e.g., `python-jose[cryptography]` 3.3.2+ for JWT, `authlib` 1.2+ for OAuth2) per `docs/technology.md`.
6. Create auth configuration module (e.g., `backend/infrastructure/auth/config.py`).
7. Set up environment variables for secrets (JWT secret key, OAuth client ID/secret, etc.).
8. Create `.env.example` documenting required variables.
9. Verify backend starts without errors when auth config is loaded.

**Implementation hints:**
- See `docs/technology.md` section "3. Authentication & Security" for specific library versions and implementation guidance.
- For JWT: Store secret key in env var (e.g., `JWT_SECRET_KEY`), use HS256 or RS256 algorithm. Use `python-jose[cryptography]` 3.3.2+.
- For OAuth2: Store client ID/secret in env vars, configure redirect URIs. Use `authlib` 1.2+.
- Place auth config in `backend/infrastructure/auth/` following Clean Architecture.
- Use dependency injection for auth dependencies in API layer.

## Dependencies
- [ ] Task ID: 2.1

## Testing Instructions
- Attempt to start the backend with auth configuration enabled and ensure configuration loads without errors.
- Verify environment variables are read correctly (no hardcoded secrets).
- Check that auth middleware/guards can be imported without import errors.

## Security Review
- Ensure no secrets are hardcoded; use environment variables or secure configuration.
- JWT secret key must be strong (min 32 chars, random).
- OAuth client secrets must be stored securely and never logged.
- Document security considerations in code comments.

## Risk Assessment
- Poorly chosen or configured auth mechanism may be insecure or hard to integrate with the frontend.
- Missing environment variables will cause runtime errors.

## Acceptance Criteria
- [ ] A clear decision is documented (in code comments or `docs/`): OIDC/OAuth2 or JWT, with brief rationale.
- [ ] Backend is configured to use the chosen auth method (library installed, config module exists).
- [ ] Sensitive configuration (client secrets, keys) is not hardcoded and is documented for local setup (`.env.example` present).
- [ ] Backend starts successfully with auth configuration active (no import/config errors).
- [ ] Auth configuration module follows Clean Architecture (placed in infrastructure layer).

## Definition of Done
- [ ] Configuration files and/or environment variables for auth are in place.
- [ ] Backend starts successfully with auth configuration active.
- [ ] `.env.example` documents required auth-related environment variables.
- [ ] Code comments explain auth choice and configuration.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Backend service starts and exposes auth-ready endpoints without configuration errors.
- **Observable Outcomes**: Auth config module exists, `.env.example` includes auth variables, backend logs show auth config loaded.

## Notes
Front-end wiring and actual login endpoints are handled in other tasks (2.3, 2.4). This task only sets up the foundation.

## Strengths
Provides a secure, standards-aligned foundation for all subsequent auth work.

## Sub-tasks (Children)
- [ ] Review `docs/requirements.md` and `docs/technical-specs.md` for auth requirements.
- [ ] Evaluate trade-offs between OIDC/OAuth2 and JWT based on project context (time, complexity, security needs).
- [ ] Document decision and rationale (in code comments or design notes).
- [ ] Install chosen auth library (e.g., `pip install python-jose[cryptography]` for JWT).
- [ ] Create auth configuration module (e.g., `backend/infrastructure/auth/config.py`).
- [ ] Define environment variables needed (e.g., `JWT_SECRET_KEY`, `JWT_ALGORITHM`).
- [ ] Create `.env.example` with auth variables documented.
- [ ] Test backend startup with auth config loaded (verify no errors).

## Completed
[ ] Pending / [ ] Completed


