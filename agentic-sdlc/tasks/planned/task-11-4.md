# Task ID: 11.4
# Title: Integrate Swagger/OpenAPI documentation
# Status: [ ] Pending
# Priority: high
# Owner: Full Stack Dev
# Estimated Effort: 3h

## Description
Integrate Swagger/OpenAPI documentation for the API so that endpoints are documented and browsable as required, per `docs/requirements.md` section "Deliverables".

**Step-by-step:**
1. Review deliverable requirements from task 11.1 (API documentation: Swagger/OpenAPI).
2. Choose OpenAPI integration approach:
   - **Option 1**: Auto-generate from code annotations (FastAPI, Flask-RESTX, Django REST Framework).
   - **Option 2**: Write OpenAPI spec manually (YAML/JSON file).
   - **Recommendation**: Auto-generate from code (easier to maintain, stays in sync with code).
3. Review technology decisions: See `docs/technology.md` section "6. Observability & Monitoring" → "API Documentation" for recommended OpenAPI/Swagger library choices.
4. Install OpenAPI/Swagger library:
   - For FastAPI: `fastapi` includes OpenAPI support, `swagger-ui` for UI (recommended per `docs/technology.md`).
   - For Flask: `flask-swagger-ui` or `flasgger`.
   - For Django: `drf-yasg` or `drf-spectacular`.
4. Add OpenAPI annotations to API endpoints:
   - Add endpoint descriptions, request/response schemas, parameter descriptions.
   - Add tags for grouping endpoints (e.g., "Tasks", "Attachments", "Auth").
   - Add example requests/responses.
   - Add authentication requirements (Bearer token, etc.).
5. Configure OpenAPI/Swagger UI:
   - Set OpenAPI metadata (title, version, description, contact info).
   - Configure Swagger UI endpoint (e.g., `/docs` or `/swagger`).
   - Configure ReDoc endpoint (optional, e.g., `/redoc`).
6. Serve API docs:
   - Create route for OpenAPI JSON spec (e.g., `/openapi.json`).
   - Create route for Swagger UI (e.g., `/docs`).
   - Ensure docs are accessible (no authentication required for docs, or document auth in Swagger UI).
7. Write contract/API documentation tests:
   - Test that OpenAPI spec matches actual API implementation:
     - All endpoints in code are documented in OpenAPI spec.
     - Request/response schemas in spec match actual API behavior.
     - Parameter types, required fields, enums match.
   - Use tools like `schemathesis` or custom tests comparing spec to routes.
8. Test API docs:
   - Access Swagger UI endpoint (e.g., `http://localhost:8000/docs`).
   - Verify all endpoints are listed and documented.
   - Test "Try it out" feature in Swagger UI (can execute requests from docs).
   - Verify request/response schemas are correct.

**Implementation hints:**
- Use FastAPI's built-in OpenAPI support (auto-generates from Pydantic models and route decorators).
- Use `@router.get(..., response_model=TaskResponse, summary="Get task", description="...")` for endpoint documentation.
- Use Pydantic models for request/response schemas (auto-documented in OpenAPI).
- Place contract tests in `backend/tests/contract/` or `backend/tests/contract_tests/`.

## Dependencies
- [ ] Task ID: 3.3 (Create task endpoint must exist)
- [ ] Task ID: 3.4 (Read task endpoints must exist)
- [ ] Task ID: 3.5 (Update/delete task endpoints must exist)

## Testing Instructions
- Access the API docs endpoint and verify that it lists all implemented endpoints correctly:
  - Open Swagger UI (e.g., `http://localhost:8000/docs`).
  - Verify all endpoints are listed (tasks, attachments, auth, health, etc.).
  - Verify request/response schemas are documented.
  - Test "Try it out" feature (execute request from Swagger UI, verify response).
- Contract/API documentation tests ensure the docs match the implementation:
  - Run contract tests: `pytest backend/tests/contract/` (verify all pass).
  - Verify spec matches implementation (all endpoints documented, schemas match).

## Security Review
- Ensure sensitive internal endpoints are not accidentally documented if they should not be public:
  - Exclude internal endpoints from OpenAPI spec (if any).
  - Document authentication requirements in Swagger UI (how to authenticate, token format).

## Risk Assessment
- Missing or inaccurate API docs can reduce clarity for reviewers and consumers.
- Out-of-sync docs can mislead API consumers.
- Missing contract tests can allow docs to drift from implementation.

## Acceptance Criteria
- [ ] Swagger/OpenAPI definition exists and is served by the API (OpenAPI spec generated/served, Swagger UI accessible).
- [ ] All API endpoints are documented (tasks, attachments, auth, health, etc.).
- [ ] Request/response schemas are documented (Pydantic models or manual schemas).
- [ ] Contract/API documentation tests are passing (spec matches implementation, all endpoints documented).

## Definition of Done
- [ ] API docs integrated with the running API (OpenAPI library installed, endpoints annotated, Swagger UI configured).
- [ ] OpenAPI spec generated/served (JSON spec available, Swagger UI accessible).
- [ ] All endpoints documented (descriptions, schemas, examples).
- [ ] Tests verifying doc/API alignment are in place (contract tests implemented, passing).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: API docs endpoint is reachable and matches implemented routes (Swagger UI accessible, all endpoints listed, schemas correct, contract tests pass).
- **Observable Outcomes**: API docs are accessible, endpoints are documented, Swagger UI works, contract tests pass.

## Notes
Supports both documentation and contract-testing requirements. This task provides browsable API documentation for reviewers and consumers.

## Strengths
Provides a clear, machine-readable description of the API surface. Enables API exploration and testing via Swagger UI.

## Sub-tasks (Children)
- [ ] Review deliverable requirements from task 11.1 (API documentation: Swagger/OpenAPI).
- [ ] Choose OpenAPI integration approach (auto-generate from code or manual spec).
- [ ] Install OpenAPI/Swagger library (FastAPI built-in, flask-swagger-ui, drf-yasg, etc.).
- [ ] Add OpenAPI annotations to API endpoints (descriptions, schemas, examples, tags, auth requirements).
- [ ] Configure OpenAPI/Swagger UI (metadata, endpoints: `/docs`, `/openapi.json`, `/redoc`).
- [ ] Serve API docs (OpenAPI JSON spec, Swagger UI, ReDoc).
- [ ] Write contract/API documentation tests (spec matches implementation, all endpoints documented, schemas match).
- [ ] Test API docs (access Swagger UI, verify endpoints listed, test "Try it out", verify schemas).

## Completed
[ ] Pending / [ ] Completed


