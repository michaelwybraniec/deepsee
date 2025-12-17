# Rate Limiting

## Configuration

**Location**: Set in `backend/.env` file (copy from `.env.example`)

**Environment Variables**:

- `RATE_LIMIT_ENABLED` (default: `true`) - Enable/disable rate limiting
- `RATE_LIMIT_REQUESTS` (default: `100`) - Requests per window
- `RATE_LIMIT_WINDOW_SECONDS` (default: `60`) - Window duration in seconds
- `REDIS_HOST` (default: `localhost`) - Redis host
- `REDIS_PORT` (default: `6379`) - Redis port
- `REDIS_PASSWORD` (optional) - Redis password
- `REDIS_DB` (default: `0`) - Redis database number

## Implementation

**Location**: `backend/api/middleware/rate_limiting.py`

**Algorithm**: Fixed window counter with Redis

**Scope**: Per-user for authenticated endpoints, per-IP for unauthenticated endpoints

**Fallback**: If Redis unavailable, rate limiting is disabled (graceful degradation)
