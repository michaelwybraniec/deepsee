# API Documentation

## Swagger/OpenAPI Documentation

The Task Tracker API includes comprehensive Swagger/OpenAPI documentation that is automatically generated from the code.

### Access Points

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON Spec**: http://localhost:8000/openapi.json

### Features

- **Auto-generated**: Documentation is automatically generated from FastAPI route definitions and Pydantic models
- **Interactive**: Use Swagger UI's "Try it out" feature to test endpoints directly
- **Complete**: All endpoints, request/response schemas, and authentication requirements are documented
- **Up-to-date**: Documentation stays in sync with code automatically

### Authentication in Swagger UI

To test authenticated endpoints in Swagger UI:

1. Open http://localhost:8000/docs
2. Click the "Authorize" button (top right)
3. Enter your JWT token (without "Bearer " prefix - Swagger adds it automatically)
4. Click "Authorize" to authenticate
5. Now you can test protected endpoints

**Getting a token:**
- Use the `/api/auth/login` endpoint first to get a token
- Copy the token from the response
- Use that token in the Authorize dialog

### Endpoints Documented

All API endpoints are documented, including:

- **Authentication**: `/api/auth/register`, `/api/auth/login`, `/api/auth/change-password`
- **Tasks**: `/api/tasks/` (CRUD operations)
- **Attachments**: `/api/tasks/{task_id}/attachments`, `/api/attachments/{id}`
- **Worker**: `/api/worker/status`, `/api/worker/trigger`, `/api/worker/statistics`
- **Health**: `/api/health`, `/api/health/api`, `/api/health/database`, `/api/health/worker`
- **Metrics**: `/api/metrics`

### Contract Tests

Contract tests verify that the OpenAPI spec matches the actual API implementation. Run with:

```bash
cd backend
pytest tests/contract/
```

These tests ensure:
- All endpoints are documented
- Request/response schemas match implementation
- OpenAPI spec is accessible

### Documentation Quality

The API documentation includes:
- Endpoint descriptions
- Request/response schemas (from Pydantic models)
- Parameter descriptions
- Authentication requirements
- Error response formats
- Example requests/responses (via Swagger UI)

---

**Status**: ✅ Complete - Swagger/OpenAPI documentation is fully integrated and accessible.
