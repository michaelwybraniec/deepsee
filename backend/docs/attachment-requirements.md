# Attachment Requirements

This document summarizes all attachment-related requirements extracted from the project documentation.

## Source References
- `docs/requirements.md` section "3. Attachments"
- `docs/technical-specs.md` section "3.3 Attachments"

## Requirements Summary

### 1. Upload Files
**Requirement**: Allow users to upload files (e.g., screenshots, documents) for each task.

**Source**: 
- `docs/requirements.md` §3: "Allow users to upload files (e.g., screenshots, documents) for each task."
- `docs/technical-specs.md` §3.3: "Allow users to upload files (e.g., screenshots, documents) for each task."

**Details**:
- Users can upload files associated with tasks
- Multiple files per task are supported (implicit from "files" plural)
- File types: screenshots, documents (examples, not restrictions)

### 2. Display File Information
**Requirement**: Show file name and file size.

**Source**:
- `docs/requirements.md` §3: "Show file name and size, allow deletion."
- `docs/technical-specs.md` §3.3: "Display: File name. File size."

**Details**:
- Must display file name (filename)
- Must display file size (in bytes or human-readable format)
- Display is metadata only (not file content preview)

### 3. Delete Attachments
**Requirement**: Allow deletion of attachments.

**Source**:
- `docs/requirements.md` §3: "Show file name and size, allow deletion."
- `docs/technical-specs.md` §3.3: "Allow deletion of attachments."

**Details**:
- Users can delete attachments
- Deletion should remove both file and metadata

## Implicit Requirements

### 4. Attachment-Task Relationship
**Requirement**: Attachments belong to tasks (one-to-many relationship).

**Source**: Implicit from "for each task" in requirements.

**Details**:
- Each attachment is associated with a specific task
- Task can have multiple attachments
- Attachment must reference task (foreign key: `task_id`)

### 5. Authorization Rules
**Requirement**: Only task owner can modify attachments (upload/delete).

**Source**: 
- `docs/requirements.md` §1: "Each user is allowed to modify only their own data"
- Inherits from task ownership (attachments belong to tasks)

**Details**:
- Upload: Only task owner can upload attachments
- Delete: Only task owner can delete attachments
- View: All authenticated users can view attachments (per "view all records" rule from §1)

### 6. Storage Requirement
**Requirement**: Files must be stored somewhere (filesystem, object storage, etc.).

**Source**: Implicit (files must be persisted to support upload/delete).

**Details**:
- Storage backend is a design decision (not specified in requirements)
- Options: local filesystem, object storage (S3, MinIO), database BLOB
- Must support: save file, retrieve file, delete file

## Design Decisions Needed

1. **Storage Backend**: 
   - Local filesystem: Simple for development
   - Object storage (S3/MinIO): Better for production, scalable
   - Decision to be made in Task 4.2 based on project needs

2. **File Size Limits**:
   - Not specified in requirements
   - Should be decided for security (prevent DoS)
   - Recommendation: Max 10MB per file (design decision)

3. **Allowed File Types**:
   - Requirements mention "screenshots, documents" as examples
   - No explicit restrictions
   - Decision: Allow all file types or restrict to specific MIME types (design decision)

4. **File Naming**:
   - Original filename vs. generated unique name
   - Filename sanitization (security requirement)
   - Decision to be made in Task 4.2

## Implementation Tasks

- Task 4.2: Design attachment metadata model and storage approach
- Task 4.3: Implement upload endpoint with validation and authorization
- Task 4.4: Implement list and delete endpoints with authorization

## Security Considerations

1. **Path Traversal Prevention**: Sanitize filenames, validate storage paths
2. **Access Control**: Enforce task ownership for upload/delete operations
3. **File Size Limits**: Prevent DoS attacks (recommend max 10MB)
4. **Content Type Validation**: Optional - restrict to safe types if needed
5. **Storage Path Validation**: Ensure files stored in intended directory only

## Summary

**Required behaviors**:
- ✅ Upload files for each task
- ✅ Display file name and size
- ✅ Delete attachments
- ✅ Owner-only modification (upload/delete)
- ✅ All users can view attachments

**Design decisions needed**:
- Storage backend (filesystem vs object storage)
- File size limits
- Allowed file types
- File naming strategy

All requirements from `docs/requirements.md` §3 and `docs/technical-specs.md` §3.3 are accounted for.
