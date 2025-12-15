# Rate Limiting Design

This document describes the rate limiting strategy and implementation design.

## Overview

Rate limiting is implemented at the API boundary using a fixed window counter algorithm with Redis storage. Limits are applied per-user for authenticated endpoints and per-IP for unauthenticated endpoints.

## Design Decisions

### 1. Limit Key (Scope)

**Decision**: Per-user for authenticated endpoints, per-IP as fallback.

**Rationale**:
- **Per-user (authenticated endpoints)**: Most API endpoints require authentication. Per-user limits prevent user-based abuse and are harder to bypass than IP-based limits.
- **Per-IP (unauthenticated endpoints)**: For endpoints that don't require authentication (e.g., `/api/auth/login`, `/api/auth/register`), use IP-based limits as a fallback.
- **Implementation**: Extract user ID from JWT token for authenticated requests, extract IP address from request for unauthenticated requests.

**Key Format**:
- Authenticated: `rate_limit:user:{user_id}:{window_timestamp}`
- Unauthenticated: `rate_limit:ip:{ip_address}:{window_timestamp}`

### 2. Limit Thresholds

**Decision**: 100 requests per minute per user/IP.

**Rationale**:
- **100 requests/minute**: Reasonable limit that allows normal API usage without triggering limits
- **1 minute window**: Short enough to prevent abuse, long enough to allow legitimate bursts
- **Configurable**: Limits can be adjusted via environment variables for different environments

**Configuration**:
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per window (default: 100)
- `RATE_LIMIT_WINDOW_SECONDS`: Window duration in seconds (default: 60)

### 3. Algorithm

**Decision**: Fixed window counter.

**Rationale**:
- **Simple**: Easy to implement and understand
- **Efficient**: Fast Redis operations (INCR, EXPIRE)
- **Good enough**: Sufficient for basic rate limiting requirements
- **Scalable**: Works well with Redis for distributed systems

**How it works**:
1. Generate key: `rate_limit:{key}:{window_timestamp}` (window_timestamp = current_time // window_seconds)
2. Increment counter: `INCR rate_limit:{key}:{window_timestamp}`
3. Set TTL: `EXPIRE rate_limit:{key}:{window_timestamp} {window_seconds}`
4. Check limit: if counter > limit, return rate limit exceeded
5. Window resets automatically when TTL expires

**Example**:
- Current time: 1704067200 (seconds since epoch)
- Window: 60 seconds
- Window timestamp: 1704067200 // 60 = 28401120
- Key: `rate_limit:user:123:28401120`
- Counter increments for each request in this 60-second window
- After 60 seconds, TTL expires, new window starts

### 4. Storage

**Decision**: Redis.

**Rationale**:
- **Fast**: In-memory storage, very fast operations
- **Scalable**: Works well in distributed systems
- **TTL support**: Built-in expiration for automatic window reset
- **Atomic operations**: INCR and EXPIRE are atomic, preventing race conditions
- **Industry standard**: Widely used for rate limiting

**Connection**:
- Host: `REDIS_HOST` (default: `localhost`)
- Port: `REDIS_PORT` (default: `6379`)
- Password: `REDIS_PASSWORD` (optional)
- Database: `REDIS_DB` (default: `0`)

**Fallback**: If Redis is unavailable, rate limiting is disabled (graceful degradation) to avoid breaking the API.

### 5. Error Response

**Decision**: 429 Too Many Requests with detailed error message and retry information.

**Format**:
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
- `X-RateLimit-Limit: 100` (limit per window)
- `X-RateLimit-Remaining: 0` (remaining requests in window)
- `X-RateLimit-Reset: <timestamp>` (when limit resets)

**Rationale**:
- **429 status**: Standard HTTP status code for rate limiting
- **Clear message**: Users understand what happened and when to retry
- **Retry-After header**: Standard header for rate limiting, helps clients implement backoff
- **Optional headers**: Additional information for debugging and client implementation

### 6. Implementation Approach

**Decision**: Middleware at API boundary.

**Location**: `backend/api/middleware/rate_limiting.py`

**Flow**:
1. Extract limit key (user ID from auth token or IP from request)
2. Call rate limiter service to check limit
3. If limit exceeded: return 429 response immediately (before request processing)
4. If limit not exceeded: continue to next handler

**Integration**:
- FastAPI middleware: Applied to all requests before route handlers
- Dependency injection: Rate limiter service injected into middleware
- Error handling: Graceful degradation if Redis unavailable

### 7. Target Endpoints

**Decision**: All authenticated endpoints, optional for unauthenticated endpoints.

**Rationale**:
- **Authenticated endpoints**: Most API endpoints require authentication, so per-user rate limiting applies
- **Unauthenticated endpoints**: Optional rate limiting for login/register endpoints (per-IP) to prevent brute force attacks
- **Health check**: Exclude `/health` endpoint from rate limiting

**Implementation**:
- Apply middleware to all routes by default
- Exclude specific routes (e.g., `/health`) from rate limiting
- Optional: Apply stricter limits to specific endpoints (e.g., login endpoint)

## Architecture

### Components

1. **Rate Limiter Service** (`backend/infrastructure/rate_limiting/rate_limiter.py`)
   - Interface: `check_rate_limit(key: str, limit: int, window_seconds: int) -> Tuple[bool, int, int]`
   - Returns: `(allowed: bool, retry_after: int, remaining: int)`
   - Implementation: Fixed window counter with Redis

2. **Rate Limiting Middleware** (`backend/api/middleware/rate_limiting.py`)
   - Extracts limit key (user ID or IP)
   - Calls rate limiter service
   - Returns 429 if limit exceeded
   - Continues if limit not exceeded

3. **Redis Client** (`backend/infrastructure/rate_limiting/redis_client.py`)
   - Redis connection management
   - Connection pooling
   - Error handling

### Sequence Diagram

```
Request → Middleware → Extract Key (user_id or IP)
                        ↓
                   Rate Limiter Service
                        ↓
                   Redis: INCR key
                        ↓
                   Check limit
                        ↓
              ┌─────────┴─────────┐
              │                   │
         Limit Exceeded      Within Limit
              │                   │
         Return 429          Continue to Handler
```

## Configuration

### Environment Variables

```bash
# Rate limiting configuration
RATE_LIMIT_ENABLED=true                    # Enable/disable rate limiting
RATE_LIMIT_REQUESTS=100                    # Requests per window
RATE_LIMIT_WINDOW_SECONDS=60               # Window duration in seconds

# Redis configuration
REDIS_HOST=localhost                       # Redis host
REDIS_PORT=6379                            # Redis port
REDIS_PASSWORD=                            # Redis password (optional)
REDIS_DB=0                                 # Redis database number
```

### Default Values

- **Rate limiting enabled**: `true` (can be disabled for development)
- **Requests per window**: `100`
- **Window duration**: `60` seconds (1 minute)
- **Redis host**: `localhost`
- **Redis port**: `6379`
- **Redis database**: `0`

## Security Considerations

### Bypass Prevention

1. **Per-user limits**: Use authenticated user ID from JWT token (not from request header)
2. **Per-IP limits**: Use real client IP from request (validate X-Forwarded-For header if behind proxy)
3. **API boundary**: Rate limiting happens before request processing (not after)

### Edge Cases

1. **Redis unavailable**: Graceful degradation (disable rate limiting, log warning)
2. **Race conditions**: Redis INCR is atomic, prevents race conditions
3. **Clock skew**: Window timestamp uses server time, acceptable for basic rate limiting
4. **Distributed systems**: Redis ensures consistent limits across multiple API instances

## Testing Strategy

### Unit Tests

- Rate limiter service: Test fixed window counter algorithm
- Redis client: Test connection and error handling
- Middleware: Test key extraction and error response

### Integration Tests

- Normal request rates: Verify requests succeed within limit
- Burst requests: Verify 429 returned after limit exceeded
- Error response: Verify 429 status, error message, retry_after header
- Window reset: Verify requests succeed after window expires
- Different users: Verify user A's requests don't affect user B's limit
- Redis unavailable: Verify graceful degradation

## Summary

**Design decisions**:
- ✅ Limit key: Per-user for authenticated endpoints, per-IP for unauthenticated endpoints
- ✅ Thresholds: 100 requests per minute (configurable)
- ✅ Algorithm: Fixed window counter
- ✅ Storage: Redis
- ✅ Error response: 429 status with detailed message and retry_after
- ✅ Implementation: Middleware at API boundary
- ✅ Target: All authenticated endpoints, optional for unauthenticated endpoints

**Next steps**: Implementation in task 8.3.
