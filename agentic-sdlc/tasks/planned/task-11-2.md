# Task ID: 11.2
# Title: Implement required test categories
# Status: [ ] Pending
# Priority: high
# Owner: Full Stack Dev
# Estimated Effort: 6h

## Description
Implement and run all required test categories: unit, integration (API + DB), worker/queue, contract/API documentation, observability/health checks, and UI smoke tests, per `docs/requirements.md` section "11. Tests" and `docs/technical-specs.md` section "3.11 Tests".

**Step-by-step:**
1. Review test requirements from task 11.1 (6 test categories: unit, integration API+DB, worker/queue, contract/API docs, observability/health checks, UI smoke tests).
2. Set up test infrastructure:
   - Install test frameworks (e.g., `pytest` for Python backend, `jest`/`vitest` for React frontend).
   - Configure test databases (separate test DB, fixtures, migrations).
   - Configure test environment variables.
3. Implement unit tests:
   - Test core business logic (use-cases, domain entities, utilities).
   - Test validation logic, error handling, edge cases.
   - Place in `backend/tests/unit/` or `backend/tests/unit_tests/`.
   - Run: `pytest backend/tests/unit/` or similar.
4. Implement integration tests (API + DB):
   - Test API endpoints with real database (create test DB, run migrations, test endpoints).
   - Test full request/response cycles (authentication, authorization, CRUD operations).
   - Place in `backend/tests/integration/` or `backend/tests/integration_tests/`.
   - Run: `pytest backend/tests/integration/` or similar.
5. Implement worker/queue tests:
   - Test reminder worker job (query tasks, log reminders, idempotency, retry logic).
   - Test worker scheduling, error handling, fault tolerance.
   - Place in `backend/tests/worker/` or `backend/tests/worker_tests/`.
   - Run: `pytest backend/tests/worker/` or similar.
6. Implement contract/API documentation tests:
   - Test that Swagger/OpenAPI spec matches actual API implementation.
   - Test that all endpoints are documented, request/response schemas match.
   - Use tools like `schemathesis` or custom tests comparing OpenAPI spec to actual routes.
   - Place in `backend/tests/contract/` or `backend/tests/contract_tests/`.
   - Run: `pytest backend/tests/contract/` or similar.
7. Implement observability/health checks tests:
   - Test health check endpoints (API, database, worker).
   - Test metrics collection (request count, error rate, latency, reminders processed).
   - Test structured logging and correlation IDs.
   - Place in `backend/tests/observability/` or `backend/tests/observability_tests/`.
   - Run: `pytest backend/tests/observability/` or similar.
8. Implement UI smoke tests:
   - Test critical user flows (login, create task, view task, upload attachment, change password).
   - Use tools like Playwright, Cypress, or React Testing Library.
   - Place in `frontend/tests/` or `frontend/tests/e2e/`.
   - Run: `npm test` or `playwright test` or similar.
9. Create test runner script:
   - Create `run_tests.sh` or `pytest.ini` to run all test categories.
   - Ensure tests can run in CI/CD pipeline.
10. Run full test suite:
    - Execute all test categories.
    - Fix any failing tests.
    - Document any missing tests with rationale.

**Implementation hints:**
- Use `pytest` for Python backend tests (unit, integration, worker, contract, observability).
- Use `jest`/`vitest` or Playwright for frontend tests (UI smoke tests).
- Use test databases (separate from development, cleaned between tests).
- Use fixtures for test data (users, tasks, attachments).
- Use mocking for external dependencies (Redis, external APIs).

## Dependencies
- [ ] Task ID: 3.3 (Create task endpoint must exist)
- [ ] Task ID: 3.4 (Read task endpoints must exist)
- [ ] Task ID: 3.5 (Update/delete task endpoints must exist)
- [ ] Task ID: 4.3 (Attachment upload endpoint must exist)
- [ ] Task ID: 4.4 (Attachment list/delete endpoints must exist)
- [ ] Task ID: 5.3 (Search functionality must exist)
- [ ] Task ID: 5.4 (Filter/sort/pagination must exist)
- [ ] Task ID: 6.4 (Reminder worker must exist)
- [ ] Task ID: 7.4 (Audit logging must exist)
- [ ] Task ID: 8.3 (Rate limiting must exist)
- [ ] Task ID: 9.4 (Health checks must exist)
- [ ] Task ID: 10.6 (Frontend UI must exist)

## Testing Instructions
- Run the full test suite and ensure all categories execute and pass:
  - Run unit tests: `pytest backend/tests/unit/` (verify all pass).
  - Run integration tests: `pytest backend/tests/integration/` (verify all pass).
  - Run worker tests: `pytest backend/tests/worker/` (verify all pass).
  - Run contract tests: `pytest backend/tests/contract/` (verify all pass).
  - Run observability tests: `pytest backend/tests/observability/` (verify all pass).
  - Run UI smoke tests: `npm test` or `playwright test` (verify all pass).
- Verify test coverage (optional but recommended: aim for >80% coverage).

## Security Review
- Ensure tests do not leave sensitive data or test credentials exposed:
  - Use test environment variables (not production secrets).
  - Don't commit test credentials to repository.
  - Clean up test data after tests (teardown, database cleanup).

## Risk Assessment
- Missing or failing tests reduce confidence in system correctness and robustness.
- Incomplete test coverage can miss bugs.
- Flaky tests can cause false negatives.

## Acceptance Criteria
- [ ] Unit tests exist for core logic and pass (use-cases, domain entities, utilities tested).
- [ ] Integration tests (API + DB) exist and pass (endpoints tested with real database).
- [ ] Worker/queue tests exist and pass (reminder worker tested, idempotency, retry logic tested).
- [ ] Contract/API documentation tests ensure Swagger/OpenAPI matches implementation (spec matches routes, schemas match).
- [ ] Observability/health checks tests exist and pass (health endpoints tested, metrics tested, logging tested).
- [ ] UI smoke tests exist and pass (critical user flows tested).
- [ ] Test suite runs cleanly (all tests pass, no flaky tests).

## Definition of Done
- [ ] All required test categories implemented (unit, integration, worker, contract, observability, UI smoke tests).
- [ ] Test infrastructure set up (test frameworks, test databases, fixtures).
- [ ] Test runner script created (can run all test categories).
- [ ] Test suite runs cleanly (all tests pass).
- [ ] Test coverage documented (optional: coverage report generated).
- [ ] All acceptance criteria met, or any missing tests explicitly documented.

## Measurable Outcomes
- **Verification Criteria**: Test reports show all categories executed with success (all test suites pass, coverage acceptable).
- **Observable Outcomes**: Test suite runs successfully, all test categories execute, tests provide confidence in system.

## Notes
Central to meeting the testing requirements of the assignment. This task ensures all required test categories are implemented and passing.

## Strengths
Provides end-to-end validation of the system. Ensures system correctness and robustness.

## Sub-tasks (Children)
- [ ] Review test requirements from task 11.1 (6 test categories).
- [ ] Set up test infrastructure (test frameworks, test databases, fixtures, environment variables).
- [ ] Add and run unit tests (core logic, validation, error handling, edge cases).
- [ ] Add and run integration tests (API + DB, full request/response cycles, authentication, authorization, CRUD).
- [ ] Add and run worker/queue tests (reminder worker, scheduling, idempotency, retry logic, fault tolerance).
- [ ] Add and run contract/API documentation tests (Swagger/OpenAPI matches implementation, all endpoints documented).
- [ ] Add and run observability/health checks tests (health endpoints, metrics, logging, correlation IDs).
- [ ] Add and run UI smoke tests (critical user flows: login, create task, view task, upload attachment, change password).
- [ ] Create test runner script (run all test categories, CI/CD compatible).
- [ ] Run full test suite and fix any failing tests.

## Completed
[ ] Pending / [ ] Completed


