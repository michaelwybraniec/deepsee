# Task ID: 8.3
# Title: Implement rate limiting and tests
# Status: [ ] Pending
# Priority: medium
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement rate limiting checks at the API boundary according to the chosen strategy from task 8.2, per `docs/requirements.md` section "7. Rate Limiting" and `docs/technical-specs.md` section "3.7 Rate Limiting".

**Step-by-step:**
1. Review rate limiting design from task 8.2 (limit key, thresholds, window, storage, algorithm, error response).
2. Set up rate limiting storage:
   - Install Redis client library (e.g., `redis-py` for Python).
   - Configure Redis connection (host, port, password if needed).
   - Create Redis client instance (singleton or dependency injection).
3. Implement rate limiting service:
   - Create `RateLimiter` service in `backend/infrastructure/rate_limiting/rate_limiter.py`:
     - Method: `check_rate_limit(key: str, limit: int, window_seconds: int) -> Tuple[bool, int]` (returns allowed: bool, retry_after: int).
     - Algorithm: Fixed window counter with Redis:
       - Key format: `rate_limit:{key}:{window_timestamp}` (e.g., `rate_limit:user:123:1704067200`).
       - Increment counter: `INCR rate_limit:{key}:{window_timestamp}`.
       - Set TTL: `EXPIRE rate_limit:{key}:{window_timestamp} {window_seconds}`.
       - Check limit: if counter > limit, return False with retry_after.
4. Create rate limiting middleware:
   - Create middleware in `backend/api/middleware/rate_limiting.py`:
     - Extract limit key (user ID from auth token or IP address from request).
     - Call rate limiter service to check limit.
     - If limit exceeded: return 429 Too Many Requests with error message and retry_after.
     - If limit not exceeded: continue to next handler.
5. Apply middleware to API endpoints:
   - Register middleware in API framework (FastAPI middleware, Flask before_request, Express middleware).
   - Apply to all API endpoints or specific endpoints (per design from task 8.2).
6. Implement error response:
   - Return 429 status code.
   - Response body: `{"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Rate limit exceeded. Please try again in X seconds.", "retry_after": X}}`.
   - Include `Retry-After` header: `X` seconds.
7. Write integration tests:
   - Test normal request rates do not trigger rate limiting (verify requests succeed within limit).
   - Test bursts from same user/IP trigger limits (verify 429 returned after limit exceeded).
   - Test error response format (verify 429 status, error message, retry_after header).
   - Test rate limit resets after window expires (verify requests succeed after window).

**Implementation hints:**
- See `docs/technology.md` section "5. Infrastructure & Services" → "Rate Limiting Storage" for Redis version and rationale.
- Use Redis 7+ for rate limiting storage (fast, supports TTL, scalable) per `docs/technology.md`.
- Use `redis-py` library for Python Redis client.
- Use fixed window counter algorithm (simple, good enough for basic rate limiting).
- Place rate limiting middleware in `backend/api/middleware/rate_limiting.py`.
- Extract user ID from auth token (for per-user limits) or IP from request (for per-IP limits).
- Use dependency injection for rate limiter service (inject into middleware).

## Dependencies
- [ ] Task ID: 8.2 (Rate limiting design must be complete)

## Testing Instructions
- Integration tests (API + Redis):
  - Normal request rates do not trigger rate limiting (verify requests succeed within limit, e.g., 99 requests per minute).
  - Bursts from the same user/IP trigger limits and return meaningful errors (verify 429 returned after 100th request, error message present, retry_after header present).
  - Test rate limit resets after window expires (verify requests succeed after 1 minute window expires).
  - Test different users have separate limits (verify user A's requests don't affect user B's limit).
- Manual test: Use API client to send many requests, verify rate limiting triggers correctly.

## Security Review
- Ensure rate limiting cannot be trivially bypassed (e.g., by changing a header alone):
  - Per-user limits use authenticated user ID (from auth token, not from request header).
  - Per-IP limits use real client IP (from request, not from X-Forwarded-For header without validation).
  - Rate limiting happens at API boundary (before request processing, not after).

## Risk Assessment
- Incorrect implementation may either allow abuse or block legitimate users.
- Missing error handling may cause rate limiting failures to break API.
- Race conditions in counter increment may cause inaccurate limits.

## Acceptance Criteria
- [ ] Rate limiting checks integrated into appropriate API endpoints (middleware applied to all or specific endpoints).
- [ ] Rate limiting uses correct limit key (user ID or IP per design from task 8.2).
- [ ] Exceeded limits return clear error responses (429 status, error message, retry_after header).
- [ ] Rate limiting uses fixed window counter algorithm (or chosen algorithm from task 8.2).
- [ ] Integration tests for typical and abusive patterns are passing (normal rates succeed, bursts trigger limits, error response correct).

## Definition of Done
- [ ] Implementation added to API layer (rate limiting middleware and service).
- [ ] Rate limiting service implemented (check_rate_limit method, Redis integration).
- [ ] Rate limiting middleware implemented (extract key, check limit, return 429 if exceeded).
- [ ] Error responses implemented (429 status, error message, retry_after header).
- [ ] Tests added and passing (normal rates, bursts, error response, reset after window).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests confirm correct behavior for normal and abusive traffic (normal rates succeed, bursts trigger limits, error response correct).
- **Observable Outcomes**: Rate limiting works correctly, 429 errors returned when limits exceeded, retry_after header present.

## Notes
Fulfills the "Rate Limiting" requirement from the assignment. This task implements the design from task 8.2.

## Strengths
Protects the API from basic abuse while preserving usability. Provides clear error messages for rate limit exceedance.

## Sub-tasks (Children)
- [ ] Review rate limiting design from task 8.2 (limit key, thresholds, window, storage, algorithm, error response).
- [ ] Set up rate limiting storage (install Redis client, configure connection, create client instance).
- [ ] Implement rate limiting service (check_rate_limit method, fixed window counter algorithm, Redis integration).
- [ ] Create rate limiting middleware (extract limit key, call rate limiter, return 429 if exceeded, continue if not).
- [ ] Apply middleware to API endpoints (register in API framework, apply to all or specific endpoints).
- [ ] Implement error responses (429 status, error message, retry_after header).
- [ ] Write integration tests (normal rates, bursts, error response, reset after window, different users).
- [ ] Test manually by sending many requests and verifying rate limiting behavior.

## Completed
[ ] Pending / [ ] Completed


