# Task ID: 8.2
# Title: Design rate limiting strategy
# Status: [x] Completed
# Priority: medium
# Owner: Backend Dev
# Estimated Effort: 2h

## Description
Design a basic rate limiting strategy (per-user or per-IP) at the API boundary that satisfies the requirements from task 8.1.

**Step-by-step:**
1. Review rate limiting requirements from task 8.1 (per-user or per-IP, meaningful errors, basic implementation).
2. Decide on limit key (scope):
   - **Option 1: Per-user** (by authenticated user ID) - better for authenticated APIs, prevents user abuse.
   - **Option 2: Per-IP** (by client IP address) - better for unauthenticated endpoints, prevents IP-based abuse.
   - **Option 3: Both** - per-user for authenticated endpoints, per-IP for unauthenticated endpoints.
   - **Recommendation**: Per-user for authenticated endpoints (most API endpoints require auth), per-IP as fallback.
3. Define limit thresholds and window:
   - **Window**: Fixed window (e.g., 1 minute, 1 hour) or sliding window (more complex, optional).
   - **Threshold**: Requests per window (e.g., 100 requests per minute, 1000 requests per hour).
   - **Recommendation**: 100 requests per minute per user (adjustable via config).
4. Design rate limiting mechanism:
   - **Storage**: In-memory (Redis, Memcached) or database (slower but simpler).
   - **Algorithm**: Token bucket, fixed window counter, or sliding window (fixed window is simplest).
   - **Recommendation**: Fixed window counter with Redis (simple, fast, scalable).
5. Design error response:
   - HTTP status: 429 Too Many Requests.
   - Response body: `{"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Rate limit exceeded. Please try again in X seconds.", "retry_after": X}}`.
   - Include `Retry-After` header (seconds until limit resets).
6. Design implementation approach:
   - Middleware/guard at API boundary (before request reaches handlers).
   - Check rate limit before processing request.
   - Increment counter on request, check if limit exceeded.
   - Return 429 if exceeded, continue if not.
7. Document design:
   - Create `backend/docs/rate-limiting.md` or add to code comments.
   - Document limit key, thresholds, window, storage, algorithm, error response.

**Implementation hints:**
- Use Redis for rate limiting storage (fast, scalable, supports TTL for window expiration).
- Use fixed window counter algorithm (simple, good enough for basic rate limiting).
- Place rate limiting middleware in `backend/api/middleware/rate_limiting.py`.
- Use dependency injection for rate limiter (inject into middleware).

## Dependencies
- [x] Task ID: 8.1 (Rate limiting requirements must be confirmed)

## Testing Instructions
- N/A for design task. Verify design describes limits, window, and scope (user or IP).
- Review design document to ensure all requirements from task 8.1 are addressed.

## Security Review
- Consider how the design handles malicious traffic and avoids easy bypass:
  - Per-user limits prevent user-based abuse (harder to bypass than IP).
  - Per-IP limits can be bypassed with proxy/VPN (acceptable for basic protection).
  - Rate limiting should be at API boundary (before request processing, not after).

## Risk Assessment
- Poor design may either fail to protect the system or degrade UX.
- Too strict limits may block legitimate users.
- Too loose limits may not protect against abuse.

## Acceptance Criteria
- [x] Strategy documented (type of limit, window, thresholds) with specific values (e.g., 100 requests per minute per user).
- [x] Decision on whether limits are per-user or per-IP (or both) is explicit (documented choice with rationale).
- [x] Storage and algorithm chosen (Redis + fixed window counter or similar).
- [x] Error response format documented (429 status, error message, retry_after).
- [x] Design is implementable (clear enough to code without guesswork).

## Definition of Done
- [ ] Design captured in comments or design doc (file committed or documented).
- [ ] Limit key, thresholds, window, storage, algorithm, error response all documented.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Implementation can follow design without guesswork (all aspects specified).
- **Observable Outcomes**: Design document shows complete rate limiting strategy.

## Notes
Actual implementation is covered in task 8.3. This task only designs the strategy.

**Completed**: Created `backend/docs/rate-limiting.md` with complete rate limiting strategy:
- Limit key: Per-user for authenticated endpoints, per-IP for unauthenticated endpoints
- Thresholds: 100 requests per minute (configurable via environment variables)
- Algorithm: Fixed window counter with Redis
- Storage: Redis (with graceful degradation if unavailable)
- Error response: 429 status with detailed message and retry_after header
- Implementation: Middleware at API boundary
- Architecture: Rate limiter service, middleware, Redis client components

## Strengths
Provides a clear blueprint for implementing limits. Ensures consistent rate limiting approach.

## Sub-tasks (Children)
- [ ] Review rate limiting requirements from task 8.1 (per-user or per-IP, meaningful errors).
- [ ] Decide on limit key (user ID, IP, or both) with rationale.
- [ ] Define limit thresholds and window duration (e.g., 100 requests per minute per user).
- [ ] Choose storage mechanism (Redis, in-memory, database) and algorithm (fixed window, token bucket, sliding window).
- [ ] Design error response format (429 status, error message, retry_after header).
- [ ] Design implementation approach (middleware/guard at API boundary).
- [ ] Document design (limit key, thresholds, window, storage, algorithm, error response) in code comments or design doc.

## Completed
[x] Completed


