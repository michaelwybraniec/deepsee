# Monitoring & Logging Requirements

This document extracts and summarizes all monitoring and logging requirements from the project documentation.

## Source References

- **Primary Source**: `docs/requirements.md` §8 "Monitoring & Logging"
- **Technical Spec**: `docs/technical-specs.md` §3.8 "Monitoring & Logging"
- **Technology Decisions**: `docs/technology.md` §6 "Observability & Monitoring"

## Requirements Summary

### 1. Structured Logging

**Requirement**: Use structured logging with correlation IDs for each request.

**Source**: `docs/requirements.md` §8, `docs/technical-specs.md` §3.8

**Details**:
- Use structured logging (JSON format or key-value pairs, not plain text)
- Generate or extract correlation ID for each request
- Include correlation ID in all log entries
- Correlation IDs should propagate through API handlers and worker jobs

**Technology Decision**: `structlog` 23.2+ (from `docs/technology.md` §6.1)

### 2. Correlation IDs

**Requirement**: Correlation ID for each request.

**Source**: `docs/requirements.md` §8, `docs/technical-specs.md` §3.8

**Details**:
- Generate or extract correlation ID from request header (e.g., `X-Correlation-ID`)
- If not present in request, generate new UUID
- Store correlation ID in request context
- Add correlation ID to response header (e.g., `X-Correlation-ID`)
- Propagate correlation ID through API handlers
- Include correlation ID in worker job logs (when applicable)
- For scheduled jobs (reminder worker), generate correlation ID per job run

**Implicit Requirements**:
- Correlation IDs should be unique per request
- Correlation IDs should be preserved across the request lifecycle
- Correlation IDs should be included in all log entries for a given request

### 3. Basic Metrics

**Requirement**: Add basic metrics (e.g., request count, error rate, latency, reminders processed).

**Source**: `docs/requirements.md` §8, `docs/technical-specs.md` §3.8

**Required Metrics**:

#### 3.1 Request Count
- **Metric**: Total API requests
- **Type**: Counter
- **Labels**: method, endpoint, status_code
- **Purpose**: Track total number of API requests

#### 3.2 Error Rate
- **Metric**: Percentage or count of errors
- **Type**: Counter (or calculated from request count with status_code >= 400)
- **Labels**: method, endpoint, error_type
- **Purpose**: Track error frequency

#### 3.3 Latency
- **Metric**: Response time (e.g., p50, p95, p99)
- **Type**: Histogram
- **Labels**: method, endpoint
- **Buckets**: [0.1, 0.5, 1.0, 2.0, 5.0] seconds (recommended)
- **Purpose**: Track response time distribution

#### 3.4 Reminders Processed
- **Metric**: Count of reminders sent by worker
- **Type**: Counter
- **Labels**: status (success/failure)
- **Purpose**: Track reminder worker activity

**Technology Decision**: `prometheus-client` 0.19+ (from `docs/technology.md` §6.2)

**Implicit Requirements**:
- Metrics should be exposed via endpoint (e.g., `/metrics` for Prometheus format)
- Metrics should be thread-safe
- Metrics should be updated in real-time

### 4. Health Check Endpoints

**Requirement**: Implement health check endpoints (API, database, worker, etc.).

**Source**: `docs/requirements.md` §8, `docs/technical-specs.md` §3.8

**Required Health Checks**:

#### 4.1 API Health Check
- **Endpoint**: `GET /health` or `GET /api/health`
- **Check**: API is running (simple check, always healthy if endpoint responds)
- **Response**: HTTP 200 OK if healthy, 503 Service Unavailable if unhealthy
- **Response Body**: `{"status": "healthy"|"unhealthy", "checks": {"api": "healthy"}}`

#### 4.2 Database Health Check
- **Check**: Database connectivity
- **Method**: Execute simple query (e.g., `SELECT 1` or `SELECT COUNT(*) FROM tasks LIMIT 1`)
- **Status**: 
  - Healthy if query succeeds
  - Unhealthy if query fails (connection error, timeout)
- **Timeout**: Recommended 5 seconds to avoid hanging
- **Response**: Include database status in health response

#### 4.3 Worker Health Check
- **Check**: Worker status
- **Options**:
  - **Option 1**: Check worker process is running (if worker is separate process)
  - **Option 2**: Check worker last run time (query for last run timestamp, verify it's recent, e.g., within last hour)
  - **Option 3**: Simple check that worker service is accessible (if worker exposes health endpoint)
- **Recommendation**: Check worker last run time (verify worker ran recently)
- **Response**: Include worker status in health response

**Health Check Response Format**:
```json
{
  "status": "healthy" | "unhealthy",
  "checks": {
    "api": "healthy" | "unhealthy",
    "database": "healthy" | "unhealthy",
    "worker": "healthy" | "unhealthy"
  }
}
```

**HTTP Status Codes**:
- `200 OK`: All checks healthy
- `503 Service Unavailable`: One or more checks unhealthy

**Implicit Requirements**:
- Health checks should be fast (avoid slow queries or operations)
- Health checks should have timeouts to avoid hanging
- Health checks should not expose sensitive data
- Optional: Individual check endpoints (e.g., `/health/api`, `/health/database`, `/health/worker`)

## Security Considerations

### Logging Security
- **Do not log**: Passwords, tokens, or other secrets
- **Do not log**: Full request/response bodies (log only necessary context)
- **Use log levels appropriately**: DEBUG for detailed info, INFO for normal operations, ERROR for errors

### Metrics Security
- **Do not expose**: Sensitive data in metric labels (e.g., user IDs, passwords)
- **Use generic labels**: method, endpoint, status_code (not user-specific data)
- **Consider authentication**: Optional but recommended for metrics endpoint in production

### Health Check Security
- **Do not expose**: Database credentials, connection strings, or other secrets
- **Do not expose**: Detailed error messages (generic "unhealthy" status, not specific error details)
- **Consider authentication**: Optional but recommended for health endpoints in production

## Testing Requirements

**Source**: `docs/requirements.md` §11 "Tests", `docs/technical-specs.md` §3.11 "Tests"

### Observability/Health Checks Tests
- Call health endpoints and verify expected responses
- Confirm metrics are exposed for key operations
- Test correlation IDs are generated/extracted per request
- Test correlation IDs are included in all log entries
- Test correlation IDs are preserved across API handlers
- Test worker logs include correlation ID
- Test metrics are updated on API requests
- Test metrics are updated on worker runs
- Test metrics endpoint returns metrics
- Test health endpoint when database is down
- Test health endpoint when worker is down

## Implementation Notes

### Correlation ID Implementation
- Use UUID v4 for correlation IDs (random, unique)
- Store correlation ID in request context (FastAPI `Request.state`)
- Use thread-local storage or request context to access correlation ID in handlers
- Extract from `X-Correlation-ID` header or generate if not present

### Metrics Implementation
- Place metrics middleware in `backend/api/middleware/metrics.py`
- Use dependency injection for metrics registry
- Metrics should be thread-safe (Prometheus client handles this)
- Apply middleware to all API endpoints

### Health Check Implementation
- Place health endpoint in `backend/api/routes/health.py`
- Use dependency injection for database connection
- Use timeout for database check (e.g., 5 seconds)
- Optional: Cache health check results (e.g., cache for 10 seconds)

## Related Documentation

- [Technology Decisions](technology.md) - Library choices and versions
- [Architecture](architecture.md) - System architecture and design patterns
- [Testing Guide](../docs/testing.md) - Testing patterns and best practices
