# Validation

**Files**: All form components in `src/pages/*.jsx`

## Validation Rules

### Authentication

- **Username**: Required, trimmed
- **Password**: Required, minimum 8 characters
- **Email**: Valid email format (registration)
- **Password Confirmation**: Must match new password
- **New Password**: Must be different from current password

### Tasks

- **Title**: Required, non-empty after trim
- **Status/Priority**: Valid enum values (enforced by dropdowns)

### Attachments

- **File Size**: Maximum 10MB per file

## Implementation

- **Client-side Only**: Validation before API calls
- **Backend Validation**: Backend also validates (double-check)
- **Error Display**: Inline error messages below form fields
