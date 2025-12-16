# Frontend Features Documentation

This document provides detailed documentation for all frontend features implemented in the Task Tracker application.

## Table of Contents

1. [Authentication](#authentication)
2. [Task Management](#task-management)
3. [Search & Filtering](#search--filtering)
4. [Sorting](#sorting)
5. [Pagination](#pagination)
6. [Attachments](#attachments)
7. [Validation](#validation)
8. [Toasts & Notifications](#toasts--notifications)
9. [Routing](#routing)

---

## Authentication

**Implementation**: `src/pages/LoginPage.jsx`, `src/pages/RegisterPage.jsx`, `src/pages/ChangePasswordPage.jsx`, `src/contexts/AuthContext.jsx`

### Features

- **Login**: User authentication with username and password
- **Registration**: New user account creation
- **Change Password**: Update user password with validation
- **Token Management**: JWT token storage in localStorage
- **Protected Routes**: Automatic redirect to login for unauthenticated users
- **Session Persistence**: User session maintained across page refreshes

### Implementation Details

- **AuthContext**: Global authentication state management
- **ProtectedRoute Component**: Route guard for authenticated pages
- **API Integration**: JWT token included in all API requests
- **Auto-logout**: Automatic logout on 401 responses

### Related Documentation

- [Frontend Requirements - Authentication](frontend-requirements.md#21-login-page)
- [Task 10 Review - Auth Implementation](task-10-review.md#-task-103-implement-auth-related-frontend-flows)
- [Backend Auth Documentation](../backend/docs/auth-requirements.md)

---

## Task Management

**Implementation**: `src/pages/TaskListPage.jsx`, `src/pages/TaskDetailPage.jsx`, `src/pages/CreateTaskPage.jsx`, `src/pages/EditTaskPage.jsx`, `src/services/taskApi.js`

### Features

- **Create Tasks**: Full form with all task fields (title, description, status, priority, due date, tags)
- **View Tasks**: List view with key information and detailed view with all fields
- **Edit Tasks**: Update existing tasks with pre-populated forms
- **Delete Tasks**: Delete with confirmation dialog
- **Task Ownership**: Users can only manage their own tasks (enforced by backend)

### Task Fields

- **Title**: Required, text input
- **Description**: Optional, textarea
- **Status**: Dropdown (pending, in_progress, done)
- **Priority**: Dropdown (low, medium, high)
- **Due Date**: Date picker
- **Tags**: Comma-separated text input

### Implementation Details

- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Real-time Updates**: Task list refreshes after create/update/delete
- **Navigation**: Seamless navigation between list, detail, create, and edit views
- **Error Handling**: User-friendly error messages for all operations

### Related Documentation

- [Frontend Requirements - Task Views](frontend-requirements.md#22-task-list-view)
- [Task 10 Review - Task Management](task-10-review.md#-task-104-implement-task-list-detail-and-edit-views)
- [Backend Task API](../backend/docs/task-model.md)

---

## Search & Filtering

**Implementation**: `src/pages/TaskListPage.jsx` (search and filter state management)

### Features

- **Text Search**: Search by title and description (partial matching)
- **Status Filter**: Filter by task status (pending, in_progress, done)
- **Priority Filter**: Filter by priority (low, medium, high)
- **Tag Filter**: Filter by tags (case-insensitive partial matching)
- **Due Date Range**: Filter by due date range (from/to dates)
- **My Tasks Filter**: Show only tasks owned by current user
- **Clear Filters**: One-click filter reset

### Implementation Details

- **Debounced Search**: 500ms debounce for search and tag filter inputs
- **Combined Filters**: Multiple filters can be applied simultaneously
- **URL State**: Filters persist in component state (can be enhanced with URL params)
- **Real-time Updates**: Task list updates automatically when filters change

### API Integration

- Uses backend search/filter API endpoints
- Supports all backend filter parameters:
  - `q`: Search query (title/description)
  - `status`: Status filter
  - `priority`: Priority filter
  - `tags`: Tag filter (comma-separated)
  - `due_date_from`: Start date
  - `due_date_to`: End date
  - `owner_user_id`: Filter by owner

### Related Documentation

- [Backend Search & Filter API](../backend/docs/search-filter-api-design.md)
- [Backend Tag Filtering](../backend/docs/tag-filtering-partial-match.md)

---

## Sorting

**Implementation**: `src/pages/TaskListPage.jsx` (sortBy state)

### Features

- **Sort Options**: Sort by due date, priority, created date, updated date
- **Sort Direction**: Ascending or descending order
- **Default Sort**: Newest first (created_at:desc)
- **UI Control**: Dropdown selector for sort field and direction

### Sort Fields

- `due_date`: Sort by due date
- `priority`: Sort by priority (low < medium < high)
- `created_at`: Sort by creation date
- `updated_at`: Sort by last update date

### Implementation Details

- **Format**: `field:direction` (e.g., `due_date:asc`, `priority:desc`)
- **Backend Integration**: Uses backend `sort` query parameter
- **State Management**: Sort preference stored in component state

### Related Documentation

- [Backend Search & Filter API](../backend/docs/search-filter-api-design.md#sorting)

---

## Pagination

**Implementation**: `src/pages/TaskListPage.jsx` (pagination state and controls)

### Features

- **Page Navigation**: Navigate between pages with Previous/Next buttons
- **Page Size**: Configurable items per page (default: 20)
- **Page Numbers**: Display current page and total pages
- **Item Count**: Show total number of tasks
- **Top & Bottom Controls**: Pagination controls at both top and bottom of task list

### Implementation Details

- **Backend Integration**: Uses backend pagination API
- **State Management**: Page and pageSize stored in component state
- **Auto-reset**: Page resets to 1 when filters change
- **Pagination Data**: Received from backend API response

### Pagination Response Format

```json
{
  "tasks": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Related Documentation

- [Backend Search & Filter API](../backend/docs/search-filter-api-design.md#pagination)

---

## Attachments

**Implementation**: `src/components/AttachmentsSection.jsx`, `src/services/attachmentApi.js`, `src/pages/CreateTaskPage.jsx`, `src/pages/EditTaskPage.jsx`

### Features

- **Upload Attachments**: Upload files when creating or editing tasks
- **View Attachments**: Display attachment list on task detail page
- **Delete Attachments**: Remove attachments from tasks
- **File Information**: Display file name and size
- **Download**: Download attachment files

### Implementation Details

- **File Size Limit**: 10MB maximum per file
- **Multiple Files**: Support for multiple file uploads
- **Client-side Validation**: File size validation before upload
- **Upload Progress**: Visual feedback during upload
- **File Types**: Accepts all file types (no restriction)

### Attachment Management

- **Create Task**: Attachments can be uploaded during task creation
- **Edit Task**: Attachments can be added when editing tasks
- **Task Detail**: Full attachment management interface
- **Delete Confirmation**: Confirmation dialog before deletion

### Related Documentation

- [Frontend Requirements - Attachments](frontend-requirements.md#26-attachments-section)
- [Task 10 Review - Attachments](task-10-review.md#-task-105-implement-attachments-ui)
- [Backend Attachment API](../backend/docs/attachment-design.md)

---

## Validation

**Implementation**: All form components (`src/pages/*.jsx`)

### Features

- **Required Fields**: Validation for required form fields
- **Field Format**: Validation for email, date, password formats
- **Password Strength**: Minimum length and match validation
- **File Validation**: File size and type validation
- **Inline Errors**: Error messages displayed next to fields
- **Form Submission**: Prevents submission if validation fails

### Validation Rules

#### Authentication Forms
- **Username**: Required, trimmed
- **Password**: Required, minimum 8 characters
- **Email**: Valid email format (for registration)
- **Password Confirmation**: Must match new password
- **New Password**: Must be different from current password

#### Task Forms
- **Title**: Required, non-empty after trim
- **Description**: Optional
- **Status**: Must be valid status value
- **Priority**: Must be valid priority value
- **Due Date**: Valid date format
- **Tags**: Optional, comma-separated

#### Attachment Forms
- **File Size**: Maximum 10MB per file
- **File Selection**: At least one file selected (if uploading)

### Implementation Details

- **Client-side Only**: Validation performed before API calls
- **User-friendly Messages**: Clear, actionable error messages
- **Real-time Feedback**: Validation errors shown as user types/submits
- **Backend Validation**: Backend also validates (double-check)

### Related Documentation

- [Frontend Requirements - Validation](frontend-requirements.md#3-client-side-validation)
- [Task 10 Review - Validation](task-10-review.md#validation-and-error-handling)

---

## Toasts & Notifications

**Implementation**: `src/components/Toaster.jsx` (Sonner library integration)

### Features

- **Success Notifications**: Toast notifications for successful operations
- **Error Notifications**: Toast notifications for errors
- **Auto-dismiss**: Toasts automatically dismiss after a few seconds
- **Manual Dismiss**: Users can manually dismiss toasts
- **Non-blocking**: Toasts don't prevent user interaction
- **Positioning**: Centered at top of screen

### Notification Types

- **Success**: Green toast for successful operations
- **Error**: Red toast for errors and failures
- **Info**: Blue toast for informational messages (if needed)

### Triggered For

- **Authentication**: Login success/failure, registration, password change
- **Task Operations**: Create, update, delete success/failure
- **Attachment Operations**: Upload, delete success/failure
- **API Errors**: Network errors, validation errors, server errors

### Implementation Details

- **Library**: Sonner (react-toast library)
- **Global Component**: Toaster component in root App
- **API Integration**: Toasts triggered from API service functions
- **Error Parsing**: Extracts user-friendly messages from API error responses

### Related Documentation

- [Frontend Requirements - Toasts](frontend-requirements.md#5-toastsalerts)
- [Task 10 Review - Toasts](task-10-review.md#toasts-and-error-handling)

---

## Routing

**Implementation**: `src/App.jsx` (React Router configuration), `src/components/ProtectedRoute.jsx`

### Features

- **Route Configuration**: All application routes defined
- **Protected Routes**: Authentication required for task management routes
- **Public Routes**: Login and registration accessible without authentication
- **Navigation**: Programmatic and link-based navigation
- **Redirects**: Automatic redirects (e.g., root to /tasks, login to /tasks after auth)

### Route Structure

#### Public Routes
- `/login` - Login page
- `/register` - Registration page

#### Protected Routes (require authentication)
- `/` - Root (redirects to `/tasks`)
- `/tasks` - Task list page
- `/tasks/:id` - Task detail page
- `/tasks/new` - Create task page
- `/tasks/:id/edit` - Edit task page
- `/change-password` - Change password page

### Implementation Details

- **Router**: React Router v6 (BrowserRouter)
- **Route Guard**: ProtectedRoute component checks authentication
- **Layout**: Shared Layout component for protected routes
- **Navigation**: useNavigate hook for programmatic navigation
- **Link Components**: Link components for declarative navigation

### Protected Route Logic

1. Check if user is authenticated (via AuthContext)
2. If authenticated: render protected component
3. If not authenticated: redirect to `/login`
4. After login: redirect back to originally requested route (if applicable)

### Related Documentation

- [Frontend Requirements - Routing](frontend-requirements.md#61-routing)
- [Task 10 Review - Routing](task-10-review.md#-task-102-set-up-react-project-and-routing)

---

## Additional Features

### Responsive Design

- **Mobile-first**: Optimized for mobile devices
- **Breakpoints**: Responsive layouts for tablet and desktop
- **Touch-friendly**: Large touch targets for mobile interaction

### Error Handling

- **Network Errors**: Handled gracefully with user-friendly messages
- **API Errors**: Parsed and displayed clearly
- **404 Handling**: Not found pages handled (can be enhanced)
- **Error Recovery**: Retry options for failed operations

### User Experience

- **Loading States**: Loading indicators during API calls
- **Optimistic Updates**: Immediate UI feedback where appropriate
- **Form State**: Form state preserved during navigation (where applicable)
- **Keyboard Navigation**: Accessible keyboard navigation

---

## Important README Sections

The [Frontend README](../README.md) contains important information that complements this features documentation:

- **[Technology Stack](../README.md#technology-stack)** - Complete list of technologies used (React, Vite, Tailwind CSS, etc.)
- **[Project Structure](../README.md#project-structure)** - Directory structure and file organization
- **[Available Scripts](../README.md#available-scripts)** - All npm scripts (dev, build, test, lint)
- **[Configuration](../README.md#configuration)** - Environment variables and API configuration
- **[Testing](../README.md#testing)** - E2E test setup, prerequisites, and test coverage
- **[Quick Reference](../README.md#quick-reference)** - Common commands and access URLs
- **[Development Setup](../README.md#development)** - First-time setup and user creation instructions

## Related Documentation

- [Frontend Requirements](frontend-requirements.md) - Complete frontend requirements
- [Task 10 Review](task-10-review.md) - Implementation review and verification
- [Backend API Documentation](../backend/docs/README.md) - Backend API reference
- [E2E Tests](../tests/e2e/README.md) - End-to-end test documentation
- [Frontend README](../README.md) - Main frontend documentation with setup and usage
