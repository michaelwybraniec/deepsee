# Routing

**Files**: `src/App.jsx`, `src/components/ProtectedRoute.jsx`

## Route Structure

### Public Routes

- `/login` - Login page
- `/register` - Registration page

### Protected Routes (require authentication)

- `/` → redirects to `/tasks`
- `/tasks` - Task list
- `/tasks/:id` - Task detail
- `/tasks/new` - Create task
- `/tasks/:id/edit` - Edit task
- `/change-password` - Change password

## Security

**ProtectedRoute Component**: Checks authentication via `AuthContext`

- If authenticated: renders protected component
- If not authenticated: redirects to `/login`

## Related

- [Authentication](authentication.md) - Auth implementation
