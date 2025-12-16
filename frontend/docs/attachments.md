# Attachments Feature

**Implementation**: `src/components/AttachmentsSection.jsx`, `src/services/attachmentApi.js`, `src/pages/CreateTaskPage.jsx`, `src/pages/EditTaskPage.jsx`

## Features

- **Upload Attachments**: Upload files when creating or editing tasks
- **View Attachments**: Display attachment list on task detail page
- **Delete Attachments**: Remove attachments from tasks
- **File Information**: Display file name and size
- **Download**: Download attachment files

## Implementation Details

- **File Size Limit**: 10MB maximum per file
- **Multiple Files**: Support for multiple file uploads
- **Client-side Validation**: File size validation before upload
- **Upload Progress**: Visual feedback during upload
- **File Types**: Accepts all file types (no restriction)

## Attachment Management

- **Create Task**: Attachments can be uploaded during task creation
- **Edit Task**: Attachments can be added when editing tasks
- **Task Detail**: Full attachment management interface
- **Delete Confirmation**: Confirmation dialog before deletion

## Related Documentation

- [Frontend Requirements - Attachments](frontend-requirements.md#26-attachments-section)
- [Backend Attachment API](../backend/docs/attachment-design.md)
- [All Features](../README.md#features) - See README for complete feature list
