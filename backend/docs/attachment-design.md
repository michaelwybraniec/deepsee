# Attachment Design

## Overview

This document describes the attachment metadata model and storage design for the Task Tracker API.

## Attachment Metadata Model

**Table**: `attachments`

### Schema

| Column | Type | Nullable | Description | Source |
|--------|------|----------|-------------|--------|
| `id` | INTEGER | NO | Primary key, auto-increment | System |
| `task_id` | INTEGER | NO | Foreign key to tasks.id | Requirements |
| `filename` | VARCHAR | NO | Original filename (sanitized) | Requirements |
| `file_size` | INTEGER | NO | File size in bytes | Requirements |
| `storage_path` | VARCHAR | NO | Path to file in storage | System |
| `content_type` | VARCHAR | YES | MIME type (optional) | Design |
| `uploaded_at` | DATETIME | NO | Upload timestamp | System |
| `created_at` | DATETIME | NO | Creation timestamp | System |
| `updated_at` | DATETIME | NO | Last update timestamp | System |

### Relationships

- **Attachment belongs to Task**: `Attachment.task_id` → `Task.id`
- Relationship: `Attachment.task` → `Task` (SQLAlchemy relationship)
- Backref: `Task.attachments` → List of attachments for task

### Indexes

- Primary Key: `id` (automatic)
- `task_id`: For querying attachments by task
- Composite: `(task_id, id)` - For efficient task attachment queries

## Storage Design

### Storage Backend: Local Filesystem

**Decision**: Local filesystem storage for development simplicity.

**Rationale**:
- Simple to implement and test
- No external dependencies (S3, MinIO)
- Sufficient for development and small-scale deployments
- Easy to switch to object storage later via storage interface

**Storage Structure**:
```
backend/uploads/
  {task_id}/
    {filename}
```

**Example**:
```
backend/uploads/
  1/
    document.pdf
    screenshot.png
  2/
    report.docx
```

### Storage Interface (Abstraction Layer)

**Location**: `backend/application/attachments/storage_interface.py`

**Interface**: `AttachmentStorage` (ABC)

**Methods**:
- `save(file, task_id, filename) -> storage_path`: Save file, return storage path
- `get_url(storage_path) -> url`: Get URL/path to access file
- `delete(storage_path) -> bool`: Delete file from storage
- `exists(storage_path) -> bool`: Check if file exists

**Implementation**: `LocalFileStorage` in `backend/infrastructure/attachments/storage.py`

**Benefits**:
- Clean Architecture: business logic doesn't depend on storage implementation
- Easy to swap storage backends (e.g., switch to S3 by implementing new adapter)
- Testable: can mock storage interface in tests

## Security Considerations

### 1. Filename Sanitization
- Remove path separators (`/`, `\`)
- Remove dangerous characters (`..`, `~`)
- Limit filename length (max 255 characters)
- Allow only safe characters (alphanumeric, `-`, `_`, `.`)

### 2. Path Traversal Prevention
- Store files in task-specific directories: `uploads/{task_id}/`
- Validate storage paths don't contain `..`
- Use `pathlib` for safe path operations

### 3. File Size Limits
- **Max file size**: 10MB per file (design decision for security)
- Validate before saving to prevent DoS attacks
- Return 400 Bad Request if file exceeds limit

### 4. Access Control
- Only task owner can upload/delete attachments
- All authenticated users can view attachments (per "view all records" rule)
- Authorization checks in use-case layer (defense in depth)

### 5. Content Type Validation
- Optional: Can restrict to specific MIME types if needed
- Current design: Allow all file types (per requirements - no restrictions specified)
- Can be enhanced later if needed

## File Naming Strategy

**Decision**: Use original filename (sanitized).

**Rationale**:
- User-friendly (users see original filename)
- Simple to implement
- Sanitization prevents security issues

**Sanitization Rules**:
1. Remove path separators (`/`, `\`)
2. Remove dangerous sequences (`..`, `~`)
3. Limit length to 255 characters
4. Replace spaces with underscores (optional)
5. Keep only safe characters: `[a-zA-Z0-9._-]`

## Future Enhancements

### Object Storage (S3/MinIO)
To switch to object storage:
1. Implement new `AttachmentStorage` adapter (e.g., `S3Storage`)
2. Update storage initialization in dependency injection
3. No changes needed to business logic (use-case layer)

### File Versioning
- Store multiple versions of same file
- Add `version` field to attachment model

### File Preview
- Generate thumbnails for images
- Extract text from PDFs
- Store preview metadata

## Implementation Files

- **Domain Model**: `backend/domain/models/attachment.py`
- **Storage Interface**: `backend/application/attachments/storage_interface.py`
- **Storage Implementation**: `backend/infrastructure/attachments/storage.py`
- **Repository**: `backend/application/attachments/repository.py` (to be created in Task 4.3)
