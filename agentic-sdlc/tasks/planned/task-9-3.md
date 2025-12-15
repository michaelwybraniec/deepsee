# Task ID: 9.3
# Title: Implement basic metrics collection
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement metrics collection for request count, error rate, latency, and reminders processed, and expose them via a metrics endpoint, per `docs/requirements.md` section "8. Monitoring & Logging" and `docs/technical-specs.md` section "3.8 Monitoring & Logging".

**Step-by-step:**
1. Review monitoring/logging requirements from task 9.1 (metrics: request count, error rate, latency, reminders processed).
2. Choose metrics library:
   - **Option 1**: Prometheus client library (e.g., `prometheus-client` for Python) - exposes `/metrics` endpoint in Prometheus format.
   - **Option 2**: Custom metrics endpoint (simple counters/gauges, JSON response).
   - **Recommendation**: Prometheus client (standard format, easy to integrate with monitoring stack).
3. Define required metrics:
   - **Request count**: Counter `http_requests_total` (labels: method, endpoint, status_code).
   - **Error rate**: Counter `http_errors_total` (labels: method, endpoint, error_type) or calculate from request count with status_code >= 400.
   - **Latency**: Histogram `http_request_duration_seconds` (labels: method, endpoint, buckets: [0.1, 0.5, 1.0, 2.0, 5.0]).
   - **Reminders processed**: Counter `reminders_processed_total` (labels: status: success/failure).
4. Instrument API code paths:
   - Create metrics middleware in `backend/api/middleware/metrics.py`:
     - Before request: record start time.
     - After request: increment request count, record latency, increment error count if status >= 400.
   - Apply middleware to all API endpoints.
5. Instrument worker code paths:
   - In reminder worker job (task 6.3):
     - Increment `reminders_processed_total` counter after each reminder processed (success or failure).
6. Expose metrics endpoint:
   - Create `GET /metrics` endpoint (or use Prometheus client's built-in endpoint).
   - Return metrics in Prometheus format (text/plain) or JSON format.
7. Write observability tests:
   - Test metrics are updated on API requests (send requests, verify counters/histograms updated).
   - Test metrics are updated on worker runs (run worker, verify reminders_processed counter updated).
   - Test metrics endpoint returns metrics (call `/metrics`, verify metrics present).

**Implementation hints:**
- See `docs/technology.md` section "6. Observability & Monitoring" → "Metrics" for metrics library version and rationale.
- Use `prometheus-client` 0.19+ (Python) for Prometheus metrics per `docs/technology.md`.
- Place metrics middleware in `backend/api/middleware/metrics.py`.
- Use dependency injection for metrics registry (inject into middleware).
- Metrics should be thread-safe (Prometheus client handles this).

## Dependencies
- [ ] Task ID: 9.1 (Monitoring/logging requirements must be confirmed)
- [ ] Task ID: 6.3 (Reminder worker must exist for reminders_processed metric)

## Testing Instructions
- Observability tests:
  - Send sample traffic and verify metrics are updated as expected (request count incremented, latency recorded, error count incremented on errors).
  - Test metrics endpoint returns metrics (call `/metrics`, verify metrics in response).
  - Test worker metrics (run worker, verify reminders_processed counter updated).
- Manual test: Send API requests, check `/metrics` endpoint, verify metrics values.

## Security Review
- Ensure metrics endpoint does not leak sensitive data or enable enumeration:
  - Don't expose sensitive data in metric labels (e.g., user IDs, passwords).
  - Use generic labels (method, endpoint, status_code, not user-specific data).
  - Consider authentication for metrics endpoint (optional but recommended for production).

## Risk Assessment
- Without metrics it is hard to measure system health and performance.
- Missing metrics instrumentation can leave gaps in observability.
- Incorrect metric definitions can provide misleading data.

## Acceptance Criteria
- [ ] Counters or histograms exist for request count, error rate, latency, and reminders processed (all required metrics defined).
- [ ] Metrics are exposed via an endpoint (e.g., `/metrics` in Prometheus format or JSON).
- [ ] Metrics instrumentation added to API (middleware records request count, latency, errors).
- [ ] Metrics instrumentation added to worker (reminder worker records reminders_processed).
- [ ] Basic tests or manual checks confirm metrics behavior (metrics updated, endpoint returns metrics).

## Definition of Done
- [ ] Metrics instrumentation added to API and worker (middleware and worker instrumentation).
- [ ] Metrics library chosen and configured (Prometheus client or custom).
- [ ] Required metrics defined (request count, error rate, latency, reminders processed).
- [ ] Metrics endpoint implemented (`/metrics` endpoint returns metrics).
- [ ] Basic tests or manual checks confirm metrics behavior (all test cases pass).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Metrics endpoint shows non-zero values under test traffic (counters incremented, histograms updated).
- **Observable Outcomes**: Metrics endpoint returns metrics, metrics values update on requests/worker runs.

## Notes
Completes the "basic metrics" part of the Monitoring & Logging requirement. Metrics enable monitoring system health and performance.

## Strengths
Provides measurable insight into system behavior. Enables monitoring and alerting.

## Sub-tasks (Children)
- [ ] Review monitoring/logging requirements from task 9.1 (metrics: request count, error rate, latency, reminders processed).
- [ ] Choose metrics library (Prometheus client or custom) and configure it.
- [ ] Define required metrics (request count counter, error rate counter, latency histogram, reminders processed counter).
- [ ] Create metrics middleware (record request count, latency, errors on API requests).
- [ ] Instrument API code paths (apply middleware to all endpoints).
- [ ] Instrument worker code paths (increment reminders_processed counter in reminder worker).
- [ ] Expose metrics endpoint (`/metrics` endpoint returns metrics in Prometheus format or JSON).
- [ ] Write observability tests (metrics updated on requests, metrics endpoint returns metrics, worker metrics updated).
- [ ] Test manually by sending requests and checking metrics endpoint.

## Completed
[ ] Pending / [ ] Completed


