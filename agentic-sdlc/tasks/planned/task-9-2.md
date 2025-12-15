# Task ID: 9.2
# Title: Implement structured logging and correlation IDs
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement structured logging with a correlation ID for each request and propagate it through API handlers and worker jobs, per `docs/requirements.md` section "8. Monitoring & Logging" and `docs/technical-specs.md` section "3.8 Monitoring & Logging".

**Step-by-step:**
1. Review monitoring/logging requirements from task 9.1 (structured logging, correlation IDs).
2. Configure structured logging library:
   - Install logging library (e.g., `structlog` for Python, `winston` for Node.js, or use standard library with JSON formatter).
   - Configure JSON formatter (output logs as JSON with key-value pairs).
   - Configure log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
3. Implement correlation ID middleware:
   - Create middleware in `backend/api/middleware/correlation_id.py`:
     - Extract correlation ID from request header (e.g., `X-Correlation-ID`) or generate new UUID if not present.
     - Store correlation ID in request context (thread-local storage or request context).
     - Add correlation ID to response header (e.g., `X-Correlation-ID`).
4. Integrate correlation ID into logging:
   - Create logging helper that includes correlation ID in all log entries.
   - Use structured logging: `logger.info("task_created", correlation_id=correlation_id, task_id=task_id, user_id=user_id)`.
   - Ensure all log entries include correlation_id field.
5. Propagate correlation ID to worker:
   - When worker job is triggered, pass correlation ID as parameter.
   - Include correlation ID in worker log entries.
   - For scheduled jobs (reminder worker), generate correlation ID per job run.
6. Write observability tests:
   - Test correlation ID is generated/extracted per request (verify header or generated UUID).
   - Test correlation ID is included in all log entries (verify logs contain correlation_id field).
   - Test correlation ID is preserved across API handlers (verify same correlation_id in multiple log entries for same request).
   - Test worker logs include correlation ID (verify worker log entries contain correlation_id).

**Implementation hints:**
- See `docs/technology.md` section "6. Observability & Monitoring" → "Structured Logging" for logging library version and rationale.
- Use `structlog` 23.2+ (Python) for structured logging per `docs/technology.md`.
- Use UUID v4 for correlation IDs (random, unique).
- Store correlation ID in request context (FastAPI `Request.state`, Flask `g`, Express `req.locals`).
- Use thread-local storage or request context to access correlation ID in handlers.

## Dependencies
- [ ] Task ID: 9.1 (Monitoring/logging requirements must be confirmed)

## Testing Instructions
- Observability tests or manual checks:
  - Logs contain a correlation ID for each request (verify correlation_id field in log entries).
  - Correlation ID is preserved across relevant log entries (verify same correlation_id in multiple log entries for same request).
  - Correlation ID is included in response header (verify `X-Correlation-ID` header in response).
  - Worker logs include correlation ID (verify worker log entries contain correlation_id).
- Manual test: Send API request, check logs, verify correlation ID appears in all log entries.

## Security Review
- Ensure logs do not contain secrets or sensitive payloads:
  - Don't log passwords, tokens, or other secrets.
  - Don't log full request/response bodies (log only necessary context).
  - Use log levels appropriately (DEBUG for detailed info, INFO for normal operations, ERROR for errors).

## Risk Assessment
- Without correlation IDs, tracing multi-step flows becomes difficult.
- Missing correlation ID propagation can break request tracing.
- Unstructured logs can make debugging harder.

## Acceptance Criteria
- [ ] Logging library configured for structured logs (JSON format, key-value pairs).
- [ ] Correlation ID generated or extracted per request and included in logs (correlation_id field in all log entries).
- [ ] Correlation ID middleware implemented (extract/generate, store in context, add to response header).
- [ ] Worker logs include the originating correlation ID when applicable (correlation_id in worker log entries).
- [ ] Correlation ID is preserved across API handlers (same correlation_id in multiple log entries for same request).

## Definition of Done
- [ ] Logging and correlation code integrated into API and worker (middleware, logging helper, worker integration).
- [ ] Structured logging configured (JSON formatter, log levels).
- [ ] Correlation ID middleware implemented (extract/generate, store, propagate).
- [ ] Logging helper created (includes correlation_id in all log entries).
- [ ] Worker integration implemented (correlation ID in worker logs).
- [ ] Basic tests or manual checks confirm correlation IDs appear as expected (all test cases pass).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Sample logs show correlation IDs for related entries (correlation_id field present, same ID across related entries).
- **Observable Outcomes**: Logs are structured (JSON format), correlation IDs appear in all entries, correlation ID in response header.

## Notes
This work underpins effective troubleshooting and tracing. Correlation IDs enable tracking requests across API handlers and worker jobs.

## Strengths
Improves debuggability without changing core business behavior. Enables request tracing and debugging.

## Sub-tasks (Children)
- [ ] Review monitoring/logging requirements from task 9.1 (structured logging, correlation IDs).
- [ ] Configure structured logging library (install library, configure JSON formatter, log levels).
- [ ] Implement correlation ID middleware (extract/generate correlation ID, store in request context, add to response header).
- [ ] Create logging helper (includes correlation_id in all log entries, uses structured logging).
- [ ] Integrate correlation ID into API handlers (use logging helper, correlation_id from context).
- [ ] Propagate correlation IDs into worker logs (pass correlation ID to worker, include in worker log entries).
- [ ] Write observability tests (correlation ID generated, included in logs, preserved across handlers, in worker logs).
- [ ] Test manually by sending requests and verifying correlation IDs in logs.

## Completed
[ ] Pending / [ ] Completed


