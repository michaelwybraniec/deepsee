# Attachment Design

**API Endpoints & Schemas**: See [API Documentation](api.md) (Swagger UI: `/docs`, ReDoc: `/redoc`)

## Storage

**Location**: `backend/uploads/{task_id}/{filename}`

**Backend**: Local filesystem (abstracted via `AttachmentStorage` interface for easy migration to S3/MinIO)

## Security

**File Size Limit**: 10MB per file

**Filename Sanitization**:
- Remove path separators (`/`, `\`)
- Remove dangerous sequences (`..`, `~`)
- Max length: 255 characters
- Safe characters only: `[a-zA-Z0-9._-]`

**Path Traversal Prevention**: Files stored in task-specific directories, paths validated

**Access Control**: Only task owner can upload/delete; all authenticated users can view
