# Routing Feature

**Implementation**: `src/App.jsx` (React Router configuration), `src/components/ProtectedRoute.jsx`

## Features

- **Route Configuration**: All application routes defined
- **Protected Routes**: Authentication required for task management routes
- **Public Routes**: Login and registration accessible without authentication
- **Navigation**: Programmatic and link-based navigation
- **Redirects**: Automatic redirects (e.g., root to /tasks, login to /tasks after auth)

## Route Structure

### Public Routes
- `/login` - Login page
- `/register` - Registration page

### Protected Routes (require authentication)
- `/` - Root (redirects to `/tasks`)
- `/tasks` - Task list page
- `/tasks/:id` - Task detail page
- `/tasks/new` - Create task page
- `/tasks/:id/edit` - Edit task page
- `/change-password` - Change password page

## Implementation Details

- **Router**: React Router v6 (BrowserRouter)
- **Route Guard**: ProtectedRoute component checks authentication
- **Layout**: Shared Layout component for protected routes
- **Navigation**: useNavigate hook for programmatic navigation
- **Link Components**: Link components for declarative navigation

## Protected Route Logic

1. Check if user is authenticated (via AuthContext)
2. If authenticated: render protected component
3. If not authenticated: redirect to `/login`
4. After login: redirect back to originally requested route (if applicable)

## Related Documentation

- [Frontend Requirements - Routing](frontend-requirements.md#61-routing)
- [Task 10 Review - Routing](task-10-review.md#-task-102-set-up-react-project-and-routing)
- [All Features](features.md)
