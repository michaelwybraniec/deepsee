# Authentication

**Files**: `src/pages/LoginPage.jsx`, `src/pages/RegisterPage.jsx`, `src/pages/ChangePasswordPage.jsx`, `src/contexts/AuthContext.jsx`

## Security

- **Token Storage**: JWT tokens stored in `localStorage` (see [Security Considerations](#security-considerations))
- **Protected Routes**: All task management routes require authentication via `ProtectedRoute` component
- **Auto-logout**: Automatic logout on 401 responses (token expired/invalid)

## Key Components

- **AuthContext**: Global authentication state (`src/contexts/AuthContext.jsx`)
- **ProtectedRoute**: Route guard component (`src/components/ProtectedRoute.jsx`)

## Security Considerations

**Token Storage**: Currently uses `localStorage` for JWT tokens. For production with XSS concerns, consider:
- HTTP-only cookies (requires backend changes)
- Token refresh mechanism
- Secure token expiration handling

## Related

- [Backend Auth](../backend/docs/auth-requirements.md)
- [Routing](routing.md) - Protected route implementation
