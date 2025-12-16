# Authentication Feature

**Implementation**: `src/pages/LoginPage.jsx`, `src/pages/RegisterPage.jsx`, `src/pages/ChangePasswordPage.jsx`, `src/contexts/AuthContext.jsx`

## Features

- **Login**: User authentication with username and password
- **Registration**: New user account creation
- **Change Password**: Update user password with validation
- **Token Management**: JWT token storage in localStorage
- **Protected Routes**: Automatic redirect to login for unauthenticated users
- **Session Persistence**: User session maintained across page refreshes

## Implementation Details

- **AuthContext**: Global authentication state management
- **ProtectedRoute Component**: Route guard for authenticated pages
- **API Integration**: JWT token included in all API requests
- **Auto-logout**: Automatic logout on 401 responses

## Related Documentation

- [Frontend Requirements - Authentication](frontend-requirements.md#21-login-page)
- [Backend Auth Documentation](../backend/docs/auth-requirements.md)
- [All Features](../README.md#features) - See README for complete feature list
