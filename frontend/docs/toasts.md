# Toasts & Notifications Feature

**Implementation**: `src/components/Toaster.jsx` (Sonner library integration)

## Features

- **Success Notifications**: Toast notifications for successful operations
- **Error Notifications**: Toast notifications for errors
- **Auto-dismiss**: Toasts automatically dismiss after a few seconds
- **Manual Dismiss**: Users can manually dismiss toasts
- **Non-blocking**: Toasts don't prevent user interaction
- **Positioning**: Centered at top of screen

## Notification Types

- **Success**: Green toast for successful operations
- **Error**: Red toast for errors and failures
- **Info**: Blue toast for informational messages (if needed)

## Triggered For

- **Authentication**: Login success/failure, registration, password change
- **Task Operations**: Create, update, delete success/failure
- **Attachment Operations**: Upload, delete success/failure
- **API Errors**: Network errors, validation errors, server errors

## Implementation Details

- **Library**: Sonner (react-toast library)
- **Global Component**: Toaster component in root App
- **API Integration**: Toasts triggered from API service functions
- **Error Parsing**: Extracts user-friendly messages from API error responses

## Related Documentation

- [Frontend Requirements - Toasts](frontend-requirements.md#5-toastsalerts)
- [All Features](../README.md#features) - See README for complete feature list
