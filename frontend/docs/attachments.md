# Attachments

**Files**: `src/components/AttachmentsSection.jsx`, `src/services/attachmentApi.js`

## Limits

- **File Size**: 10MB maximum per file (client-side validation)
- **File Types**: All file types accepted

## Security

- **Client-side Validation**: File size checked before upload (10MB limit)
- **Backend Validation**: Backend also enforces limits (double-check)

## Usage

Attachments can be uploaded:
- During task creation (`CreateTaskPage`)
- When editing tasks (`EditTaskPage`)
- From task detail page (`AttachmentsSection` component)

## Related

- [Backend Attachment API](../backend/docs/attachments.md)
