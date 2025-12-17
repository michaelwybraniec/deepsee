# Authentication Design

## JWT Implementation

**Method**: JWT (chosen over OIDC/OAuth2 for simplicity and API-first architecture)

**Token Claims**:
- `sub`: User ID (string)
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

## Configuration

**Environment Variables**:
- `JWT_SECRET_KEY` (required): Minimum 32 characters. Generate with: `openssl rand -hex 32`
- `JWT_ALGORITHM` (default: `HS256`): Supported: `HS256`, `RS256`
- `JWT_ACCESS_TOKEN_EXPIRE_HOURS` (default: `24`): Token expiration in hours

## Security Considerations

**Token Revocation Limitation**: JWT tokens cannot be revoked before expiration. Mitigation: User existence checked on every request (deleted users invalidate tokens).

**Secret Key**: Never commit to version control. Rotate periodically (invalidates all tokens).
