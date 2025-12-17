# Attachment Design

**API Endpoints & Schemas**: See [API Documentation](api.md) (Swagger UI: `/docs`, ReDoc: `/redoc`)

## Storage

**Location**: `uploads/{task_id}/{filename}`

**Backend**: Local filesystem (abstracted via `AttachmentStorage` interface for easy migration to S3/MinIO)

**Production Storage**: The `AttachmentStorage` interface allows swapping to object storage (S3, MinIO, Azure Blob, etc.) without changing business logic. Simply implement a new storage adapter (e.g., `S3Storage`) and update the dependency injection. The `storage_path` in the database would store the object key (e.g., `"attachments/{task_id}/{filename}"`) instead of a filesystem path.

**Path Resolution**: Uses absolute path based on file location to work consistently in Docker and local environments:
- **Docker**: `/app/uploads/{task_id}/{filename}` (stored in named volume `uploads_data`, not bind mount)
- **Local**: `{backend_dir}/uploads/{task_id}/{filename}` (relative to backend directory)

**Docker Space Optimization**: 
- Uploads stored in named Docker volume (`uploads_data:/app/uploads`) instead of bind mount
- Prevents uploads from syncing to host filesystem, saving disk space
- Improves performance by avoiding file system sync overhead
- Named volumes can be backed up/cleaned independently

## Security

**File Size Limit**: 10MB per file

**Filename Sanitization**:
- Remove path separators (`/`, `\`)
- Remove dangerous sequences (`..`, `~`)
- Max length: 255 characters
- Safe characters only: `[a-zA-Z0-9._-]`

**Path Traversal Prevention**: Files stored in task-specific directories, paths validated

**Access Control**: Only task owner can upload/delete; all authenticated users can view
