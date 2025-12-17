# Authentication Design

## JWT Process

**1. Login** (`POST /api/auth/login`):
   - User provides username/password
   - Server verifies password (bcrypt)
   - Server creates JWT token with user ID (`sub` claim)
   - Server signs token with `JWT_SECRET_KEY`
   - Server returns token to client

**2. Authenticated Requests**:
   - Client sends token in `Authorization: Bearer <token>` header
   - Server validates token signature using `JWT_SECRET_KEY`
   - Server extracts user ID from token
   - Server verifies user exists in database
   - Request proceeds with authenticated user

**3. Token Expiration**:
   - Tokens expire after configured hours (default: 24)
   - Expired tokens return `401 Unauthorized`
   - Client must login again to get new token

## Implementation

**Method**: JWT (chosen over OIDC/OAuth2 for simplicity and API-first architecture)

**Token Creation**: `backend/application/auth/login.py::create_access_token()`
**Token Validation**: `backend/api/middleware/auth.py::get_current_user()`

**Token Claims**:
- `sub`: User ID (string)
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

## Configuration

**Location**: Set in `backend/.env` file (copy from `.env.example`)

**Environment Variables**:
- `JWT_SECRET_KEY` (required): Used to **sign and verify** JWT tokens. Must be:
  - **Random and unpredictable** (not a placeholder or guessable value)
  - Minimum 32 characters
  - **Secret** (if compromised, attackers can forge tokens and impersonate users)
  
  **Generate secure key:**
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  # Or: openssl rand -hex 32
  ```
  
  **Why generate?** The key is used cryptographically - a weak/placeholder key allows token forgery. Each deployment should have a unique random key.
- `JWT_ALGORITHM` (default: `HS256`): Supported: `HS256`, `RS256`
- `JWT_ACCESS_TOKEN_EXPIRE_HOURS` (default: `24`): Token expiration in hours

## Security Considerations

**Token Revocation Limitation**: JWT tokens cannot be revoked before expiration. Mitigation: User existence checked on every request (deleted users invalidate tokens).

**Secret Key**: Never commit to version control. Rotate periodically (invalidates all tokens).
