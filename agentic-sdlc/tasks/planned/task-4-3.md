# Task ID: 4.3
# Title: Implement attachment upload endpoint
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement endpoint(s) to upload attachments for a task, including validation and error handling, per `docs/requirements.md` section "3. Attachments" and `docs/technical-specs.md` section "3.3 Attachments".

**Step-by-step:**
1. Review attachment design from task 4.2 (metadata model, storage interface, security considerations).
2. Create upload use-case (e.g., `backend/application/attachments/upload_attachment.py`):
   - Accept task ID, file (multipart/form-data), and authenticated user ID.
   - Verify task exists and user is owner (authorization check - only task owner can upload).
   - Validate file: size limits (e.g., max 10MB), filename sanitization (remove path separators, limit length).
   - Save file using storage interface (from task 4.2): call `storage.save(file, task_id)` to get storage_path.
   - Create attachment metadata record: task_id, filename, file_size, storage_path, owner_user_id.
   - Persist metadata via repository.
   - Return attachment metadata (id, filename, file_size).
3. Create API endpoint (e.g., `POST /api/tasks/:id/attachments` in `backend/api/routes/attachments.py`):
   - Require authentication (extract user ID from token).
   - Accept multipart/form-data with file field (e.g., `file`).
   - Extract task ID from URL parameter.
   - Call upload use-case with task ID, file, and user ID.
   - Return 201 Created with attachment metadata on success.
   - Return 403 Forbidden if user is not task owner.
   - Return 400 Bad Request for validation errors (file too large, invalid filename, etc.).
4. Implement security measures:
   - Filename sanitization: remove `../`, limit length, allow only safe characters.
   - File size validation: enforce max size (e.g., 10MB) before saving.
   - Path validation: ensure files stored in intended directory only.
   - Content type validation (optional): restrict to specific MIME types if required.
5. Write integration tests:
   - Test successful upload for task owner (verify 201, metadata returned, file stored).
   - Test upload rejection for non-owner (verify 403 Forbidden).
   - Test upload rejection for file too large (verify 400 Bad Request).
   - Test upload rejection for invalid filename (verify 400 Bad Request).
   - Test upload rejection for non-existent task (verify 404 Not Found).

**Implementation hints:**
- Use multipart/form-data for file uploads (standard HTTP file upload).
- Place use-case in `backend/application/attachments/` following Clean Architecture.
- Place endpoint in `backend/api/routes/attachments.py` or `backend/api/routes/tasks.py`.
- Use storage interface from task 4.2 (abstraction allows switching storage backends).
- Response format: `{"id": 1, "filename": "document.pdf", "file_size": 1024, "task_id": 123}`.

## Dependencies
- [ ] Task ID: 4.2 (Attachment model and storage design must be complete)

## Testing Instructions
- Integration tests (API + DB + Storage):
  - Successful upload of a valid file to a task (verify 201, metadata in DB, file in storage).
  - Rejection of invalid uploads (e.g., too large, wrong type if constrained - verify 400).
  - Rejection for non-owner (verify 403 Forbidden).
  - Rejection for non-existent task (verify 404 Not Found).
- Manual test: Use API client (Postman/curl) to upload file, verify response and file storage.

## Security Review
- Check for path traversal and ensure uploaded files are stored in a safe location:
  - Filename sanitization: remove `../`, limit length, validate characters.
  - Storage path validation: ensure files stored in `uploads/{task_id}/` or similar, not outside.
  - File size limits: prevent DoS attacks (e.g., max 10MB per file).
  - Content type validation: restrict to safe types if required (e.g., images, PDFs only).

## Risk Assessment
- Insecure handling may lead to file system or data exposure issues.
- Missing authorization check may allow unauthorized file uploads.
- Missing file size limits may allow DoS attacks.

## Acceptance Criteria
- [ ] Upload endpoint (`POST /api/tasks/:id/attachments`) accepts files for a given task and stores metadata (201 Created).
- [ ] Endpoint enforces task ownership (403 Forbidden if user is not task owner).
- [ ] File validation implemented (size limits, filename sanitization, path validation).
- [ ] Errors for invalid uploads are clear and safe (400 Bad Request with meaningful messages).
- [ ] Tests for successful and failing uploads are passing (success, non-owner, validation errors).

## Definition of Done
- [ ] Endpoint implemented and wired to attachment storage (use-case and API handler).
- [ ] Upload use-case implemented (authorization check, file validation, storage save, metadata persistence).
- [ ] Security measures implemented (filename sanitization, size limits, path validation).
- [ ] Tests added and passing (success, non-owner, validation errors, 404).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Upload tests pass, and files/metadata are stored as expected (file in storage, metadata in DB).
- **Observable Outcomes**: Endpoint responds correctly to valid/invalid uploads, files are stored securely, authorization enforced.

## Notes
Owner-only modification enforcement is handled in this task (authorization check in use-case). Delete behavior is handled in task 4.4.

## Strengths
Implements the "Allow users to upload files for each task" requirement. Provides secure file upload with proper validation and authorization.

## Sub-tasks (Children)
- [ ] Review attachment design from task 4.2 (metadata model, storage interface).
- [ ] Create upload use-case (accept task ID, file, user ID; verify ownership, validate file, save, persist metadata).
- [ ] Create API endpoint handler (`POST /api/tasks/:id/attachments`) with multipart/form-data support.
- [ ] Implement security measures (filename sanitization, size limits, path validation).
- [ ] Write integration tests (successful upload, non-owner 403, validation errors, 404).
- [ ] Test manually with API client to verify file upload and storage.

## Completed
[ ] Pending / [ ] Completed


