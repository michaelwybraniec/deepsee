# Validation Feature

**Implementation**: All form components (`src/pages/*.jsx`)

## Features

- **Required Fields**: Validation for required form fields
- **Field Format**: Validation for email, date, password formats
- **Password Strength**: Minimum length and match validation
- **File Validation**: File size and type validation
- **Inline Errors**: Error messages displayed next to fields
- **Form Submission**: Prevents submission if validation fails

## Validation Rules

### Authentication Forms
- **Username**: Required, trimmed
- **Password**: Required, minimum 8 characters
- **Email**: Valid email format (for registration)
- **Password Confirmation**: Must match new password
- **New Password**: Must be different from current password

### Task Forms
- **Title**: Required, non-empty after trim
- **Description**: Optional
- **Status**: Must be valid status value
- **Priority**: Must be valid priority value
- **Due Date**: Valid date format
- **Tags**: Optional, comma-separated

### Attachment Forms
- **File Size**: Maximum 10MB per file
- **File Selection**: At least one file selected (if uploading)

## Implementation Details

- **Client-side Only**: Validation performed before API calls
- **User-friendly Messages**: Clear, actionable error messages
- **Real-time Feedback**: Validation errors shown as user types/submits
- **Backend Validation**: Backend also validates (double-check)

## Related Documentation

- [Frontend Requirements - Validation](frontend-requirements.md#3-client-side-validation)
- [All Features](../README.md#features) - See README for complete feature list
