# Rate Limiting Requirements

This document summarizes all rate limiting requirements extracted from the project documentation.

## Source References
- `docs/requirements.md` section "7. Rate Limiting"
- `docs/technical-specs.md` section "3.7 Rate Limiting"

## Requirements Summary

### 1. Scope

**Requirement**: Apply basic per-user or per-IP rate limiting on API requests.

**Source**: 
- `docs/requirements.md` §7: "Apply basic per-user or per-IP rate limiting on API requests."
- `docs/technical-specs.md` §3.7: "Apply basic per‑user or per‑IP rate limiting on API requests."

**Details**:
- **Per-user**: Rate limiting based on authenticated user ID (for authenticated endpoints)
- **Per-IP**: Rate limiting based on client IP address (for unauthenticated endpoints or as fallback)
- **Choice**: Design decision - can implement per-user, per-IP, or both (recommendation: per-user for authenticated endpoints, per-IP as fallback)

### 2. Target

**Requirement**: Rate limiting applies to API requests.

**Source**:
- `docs/requirements.md` §7: "Apply basic per-user or per-IP rate limiting on API requests."
- `docs/technical-specs.md` §3.7: "Apply basic per‑user or per‑IP rate limiting on API requests."

**Details**:
- **Target**: All API requests (or specific endpoints - design decision)
- **Location**: At API boundary (middleware/guard level, before request processing)
- **Scope**: All endpoints or specific endpoints (design decision - recommendation: all authenticated endpoints)

### 3. Error Responses

**Requirement**: Return meaningful error responses when limits are exceeded.

**Source**:
- `docs/requirements.md` §7: "Return meaningful error responses when limits are exceeded."
- `docs/technical-specs.md` §3.7: "When limits are exceeded: Return meaningful error responses."

**Details**:
- **HTTP Status**: 429 Too Many Requests (standard for rate limiting)
- **Error Message**: Clear, meaningful message (e.g., "Rate limit exceeded. Please try again in X seconds.")
- **Retry Information**: Include information about when to retry (e.g., `Retry-After` header with seconds until limit resets)

### 4. Basic Implementation

**Requirement**: Basic rate limiting (not advanced features).

**Source**: Implicit from "basic" in requirements.

**Details**:
- **Algorithm**: Simple rate limiting algorithm (fixed window counter, token bucket, or sliding window - design decision)
- **Complexity**: Keep it simple, avoid over-engineering
- **Features**: Basic limits are sufficient (no need for advanced features like distributed rate limiting, multiple tiers, etc.)

## Implicit Requirements

### 5. API Boundary

**Requirement**: Rate limiting should be at API boundary.

**Source**: Implicit (best practice for rate limiting).

**Details**:
- Rate limiting should happen before request processing (middleware/guard level)
- Should not break legitimate usage (reasonable limits)
- Should be fast and non-blocking (should not significantly slow down requests)

### 6. Reasonable Limits

**Requirement**: Rate limiting should not break legitimate usage.

**Source**: Implicit (best practice for rate limiting).

**Details**:
- Limits should be reasonable (not too strict, not too loose)
- Should allow normal API usage without triggering limits
- Should protect against abuse without blocking legitimate users
- Exact limits are design decisions (e.g., 100 requests per minute per user)

### 7. Security Considerations

**Requirement**: Rate limiting should not be trivially bypassed.

**Source**: Implicit (security best practice).

**Details**:
- Per-user limits should use authenticated user ID (from auth token, not from request header)
- Per-IP limits should use real client IP (from request, not from X-Forwarded-For header without validation)
- Rate limiting should be at API boundary (before request processing, not after)

## Design Decisions Needed

1. **Limit Key**:
   - Per-user (by authenticated user ID)
   - Per-IP (by client IP address)
   - Both (per-user for authenticated endpoints, per-IP for unauthenticated endpoints)
   - **Decision**: To be made in task 8.2 (recommendation: per-user for authenticated endpoints, per-IP as fallback)

2. **Limit Thresholds**:
   - Requests per window (e.g., 100 requests per minute)
   - Window duration (e.g., 1 minute, 1 hour)
   - **Decision**: To be made in task 8.2 (recommendation: 100 requests per minute per user)

3. **Algorithm**:
   - Fixed window counter (simple, good enough for basic rate limiting)
   - Token bucket (more complex, better for burst handling)
   - Sliding window (more complex, more accurate)
   - **Decision**: To be made in task 8.2 (recommendation: fixed window counter)

4. **Storage**:
   - In-memory (Redis, Memcached) - fast, scalable
   - Database (slower but simpler, no additional infrastructure)
   - **Decision**: To be made in task 8.2 (recommendation: Redis for fast, scalable rate limiting)

5. **Target Endpoints**:
   - All API endpoints
   - Specific endpoints (e.g., only authenticated endpoints)
   - **Decision**: To be made in task 8.2 (recommendation: all authenticated endpoints)

## Error Response Format

**Requirement**: Meaningful error responses when limits are exceeded.

**Recommended Format**:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again in X seconds.",
    "retry_after": X
  }
}
```

**HTTP Headers**:
- `Retry-After: X` (seconds until limit resets)
- `X-RateLimit-Limit: 100` (optional: limit per window)
- `X-RateLimit-Remaining: 0` (optional: remaining requests in window)
- `X-RateLimit-Reset: <timestamp>` (optional: when limit resets)

## Summary

**Required behaviors**:
- ✅ Apply rate limiting per-user or per-IP (design decision)
- ✅ Apply to API requests (all or specific endpoints - design decision)
- ✅ Return meaningful error responses when limits exceeded (429 status, error message, retry_after)
- ✅ Basic implementation (simple algorithm, reasonable limits)
- ✅ At API boundary (middleware/guard level)
- ✅ Not trivially bypassable (use authenticated user ID or real client IP)

**Design decisions needed**:
- Limit key (per-user, per-IP, or both)
- Limit thresholds (requests per window, window duration)
- Algorithm (fixed window, token bucket, sliding window)
- Storage (Redis, in-memory, database)
- Target endpoints (all or specific)

All requirements from `docs/requirements.md` §7 and `docs/technical-specs.md` §3.7 are accounted for.
