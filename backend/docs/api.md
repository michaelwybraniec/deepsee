# API Documentation

## Access Points

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON Spec**: http://localhost:8000/openapi.json

## Authentication in Swagger UI

### Get JWT Token

1. Open Swagger UI: `http://localhost:8000/docs`
2. Use **POST /api/auth/login** with username/password
3. Copy the `token` from the response

### Authorize in Swagger

1. Click **"Authorize"** button (🔒 top right)
2. Paste **only the token** (without "Bearer " prefix)
3. Click **"Authorize"**

**Important**: Don't include "Bearer " prefix - Swagger adds it automatically.

### Troubleshooting

- **401 Unauthorized**: Make sure you authorized and pasted token correctly
- **Token Expired**: Login again to get a new token
- **Can't see Authorize button**: Refresh the page or check browser console

## Contract Tests

Verify OpenAPI spec matches implementation:

```bash
cd backend
pytest tests/contract/
```
