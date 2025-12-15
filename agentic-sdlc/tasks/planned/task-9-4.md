# Task ID: 9.4
# Title: Implement health check endpoints
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement health check endpoints for the API, database, and worker as required by the assignment, per `docs/requirements.md` section "8. Monitoring & Logging" and `docs/technical-specs.md` section "3.8 Monitoring & Logging".

**Step-by-step:**
1. Review monitoring/logging requirements from task 9.1 (health checks for API, database, worker).
2. Design health check response format:
   - HTTP status: 200 OK if healthy, 503 Service Unavailable if unhealthy.
   - Response body: `{"status": "healthy"|"unhealthy", "checks": {"api": "healthy", "database": "healthy", "worker": "healthy"}}`.
3. Implement API health endpoint:
   - Create `GET /health` or `GET /api/health` endpoint in `backend/api/routes/health.py`:
     - Check API is running (simple check, always healthy if endpoint responds).
     - Return 200 OK with `{"status": "healthy", "checks": {"api": "healthy"}}`.
4. Implement database connectivity check:
   - In health endpoint, add database check:
     - Execute simple query (e.g., `SELECT 1` or `SELECT COUNT(*) FROM tasks LIMIT 1`).
     - If query succeeds: database is healthy.
     - If query fails (connection error, timeout): database is unhealthy.
   - Return database status in health response.
5. Implement worker health check:
   - **Option 1**: Check worker process is running (if worker is separate process, check process status).
   - **Option 2**: Check worker last run time (query reminder_log or worker_status table for last run timestamp, verify it's recent).
   - **Option 3**: Simple check that worker service is accessible (if worker exposes health endpoint, call it).
   - **Recommendation**: Check worker last run time (verify worker ran recently, e.g., within last hour).
   - Return worker status in health response.
6. Implement comprehensive health endpoint:
   - `GET /health` returns overall health (healthy if all checks pass, unhealthy if any check fails).
   - Individual checks: `GET /health/api`, `GET /health/database`, `GET /health/worker` (optional, for detailed checks).
7. Write health-check tests:
   - Test API health endpoint returns success (verify 200 OK, status="healthy").
   - Test database check (verify database connectivity check works, returns healthy/unhealthy correctly).
   - Test worker health check (verify worker status check works, returns healthy/unhealthy correctly).
   - Test health endpoint when database is down (verify 503, database="unhealthy").
   - Test health endpoint when worker is down (verify 503 or worker="unhealthy").

**Implementation hints:**
- Place health endpoint in `backend/api/routes/health.py`.
- Use dependency injection for database connection (inject into health handler).
- Use timeout for database check (e.g., 5 seconds) to avoid hanging.
- Cache health check results (optional, e.g., cache for 10 seconds to avoid excessive database queries).

## Dependencies
- [ ] Task ID: 3.2 (Task model must exist for database check)
- [ ] Task ID: 6.3 (Reminder worker must exist for worker health check)

## Testing Instructions
- Observability/health tests:
  - Call API health endpoint and verify success response (200 OK, status="healthy", all checks="healthy").
  - Verify DB check runs and reports connectivity (test with database up and down, verify correct status).
  - Verify worker/queue health is reported (test with worker running and stopped, verify correct status).
  - Test health endpoint when components are down (verify 503 or individual checks="unhealthy").
- Manual test: Call health endpoint, verify response, stop database/worker, call again, verify unhealthy status.

## Security Review
- Ensure health endpoints do not expose sensitive configuration or data:
  - Don't expose database credentials, connection strings, or other secrets.
  - Don't expose detailed error messages (generic "unhealthy" status, not specific error details).
  - Consider authentication for health endpoints (optional but recommended for production).

## Risk Assessment
- Missing or incorrect health checks make it harder to monitor system status.
- Health checks that are too slow can cause timeouts.
- Missing timeout on database check can cause health endpoint to hang.

## Acceptance Criteria
- [ ] API health endpoint implemented (`GET /health` returns health status).
- [ ] DB connectivity check implemented (database check in health endpoint, returns healthy/unhealthy).
- [ ] Worker/queue health check implemented (worker status check in health endpoint, returns healthy/unhealthy).
- [ ] Health endpoint returns appropriate HTTP status (200 if healthy, 503 if unhealthy).
- [ ] Health tests are passing (all test cases: API healthy, DB healthy/unhealthy, worker healthy/unhealthy).

## Definition of Done
- [ ] Health endpoints integrated and documented (health endpoint implemented, documented in API docs).
- [ ] API health check implemented (simple check, always healthy if endpoint responds).
- [ ] Database connectivity check implemented (query database, return healthy/unhealthy based on result).
- [ ] Worker health check implemented (check worker last run time or process status, return healthy/unhealthy).
- [ ] Tests added and passing (all test cases: healthy, unhealthy scenarios).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Health tests confirm endpoints return expected status (200 when healthy, 503 when unhealthy, correct check statuses).
- **Observable Outcomes**: Health endpoint responds correctly, returns health status, checks work as expected.

## Notes
Essential for operational observability and automated monitoring. Health checks enable monitoring systems to detect component failures.

## Strengths
Directly addresses the "health check endpoints" requirement and related tests. Enables automated monitoring and alerting.

## Sub-tasks (Children)
- [ ] Review monitoring/logging requirements from task 9.1 (health checks for API, database, worker).
- [ ] Design health check response format (HTTP status, response body with status and checks).
- [ ] Implement API health endpoint (`GET /health` with API check).
- [ ] Implement database connectivity check (query database, return healthy/unhealthy).
- [ ] Implement worker health check (check worker last run time or process status, return healthy/unhealthy).
- [ ] Implement comprehensive health endpoint (overall health, individual checks).
- [ ] Add health-check tests (API healthy, DB healthy/unhealthy, worker healthy/unhealthy, overall health).
- [ ] Test manually by calling health endpoint and verifying responses.

## Completed
[ ] Pending / [ ] Completed


