# Task ID: 4.4
# Title: Implement attachment list and delete endpoints
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement endpoints to list attachments for a task (showing file name and size) and to delete attachments, enforcing task ownership rules, per `docs/requirements.md` section "3. Attachments" and `docs/technical-specs.md` section "3.3 Attachments".

**Step-by-step:**
1. Review authorization requirements: only task owner can delete attachments (inherits from task ownership per task 2.5).
2. Create list attachments use-case (e.g., `backend/application/attachments/list_attachments.py`):
   - Accept task ID and authenticated user ID (for logging, not filtering - all users can view attachments per "view all records" rule).
   - Query attachments from repository by task_id.
   - Return list of attachments with metadata (id, filename, file_size, task_id).
3. Create delete attachment use-case (e.g., `backend/application/attachments/delete_attachment.py`):
   - Accept attachment ID and authenticated user ID.
   - Query attachment from repository by ID.
   - Query task from repository by attachment.task_id.
   - Verify `task.owner_user_id == authenticated_user_id` (ownership check - only task owner can delete).
   - If not owner: return authorization error.
   - If owner: delete file from storage (call `storage.delete(storage_path)`), delete metadata from repository, return success.
4. Create API endpoints:
   - `GET /api/tasks/:id/attachments` (list attachments):
     - Require authentication (extract user ID from token).
     - Extract task ID from URL parameter.
     - Call list use-case with task ID and user ID.
     - Return 200 OK with array of attachments (filename, file_size).
   - `DELETE /api/attachments/:id` (delete attachment):
     - Require authentication (extract user ID from token).
     - Extract attachment ID from URL parameter.
     - Call delete use-case with attachment ID and user ID.
     - Return 204 No Content on success, 403 Forbidden if not owner, 404 Not Found if attachment doesn't exist.
5. Define response schemas (e.g., Pydantic models):
   - Attachment response: id, filename, file_size, task_id
   - List response: array of attachment objects
6. Write integration tests:
   - Test list attachments for a task (verify 200, array with filename and file_size).
   - Test list attachments for non-existent task (verify 404 or empty array).
   - Test owner can delete attachment (verify 204, file deleted from storage, metadata deleted from DB).
   - Test non-owner cannot delete attachment (verify 403 Forbidden).
   - Test delete non-existent attachment (verify 404 Not Found).

**Implementation hints:**
- Follow Clean Architecture: use-cases in `backend/application/attachments/`, endpoints in `backend/api/routes/attachments.py`.
- Use storage interface from task 4.2 to delete files (abstraction allows switching storage backends).
- Ownership check should happen in use-case (defense in depth, even if middleware checks).
- Response format: `[{"id": 1, "filename": "document.pdf", "file_size": 1024, "task_id": 123}, ...]` for list, 204 No Content for delete.

## Dependencies
- [ ] Task ID: 2.5 (Authorization guards must exist - middleware checks)
- [ ] Task ID: 4.2 (Attachment model and storage design must be complete)

## Testing Instructions
- Integration tests (API + DB + Storage):
  - Listing attachments returns correct metadata (name and size - verify 200, array with filename and file_size).
  - Owner can delete attachments (verify 204, file deleted from storage, metadata deleted from DB).
  - Non-owner cannot delete attachments (verify 403 Forbidden).
  - Test list/delete for non-existent task/attachment (verify 404 or appropriate error).
- Manual test: Use API client to list and delete attachments, verify behavior and file storage.

## Security Review
- Ensure delete operations are authorized and properly audited:
  - Ownership check in use-case (verify task owner before allowing delete).
  - File deletion from storage (ensure file is actually removed, not just metadata).
  - Audit logging (optional but recommended - log deletion events for security).

## Risk Assessment
- Incorrect deletion handling could allow unauthorized removal of files.
- Missing file deletion from storage could leave orphaned files.
- Missing ownership check could allow users to delete others' attachments.

## Acceptance Criteria
- [ ] List endpoint (`GET /api/tasks/:id/attachments`) returns attachments with file name and size for a task (200 OK, array with filename and file_size).
- [ ] Delete endpoint (`DELETE /api/attachments/:id`) allows only the task owner to remove attachments (403 if not owner, 204 if owner).
- [ ] Delete operation removes both file from storage and metadata from database.
- [ ] Both endpoints require authentication (401 if not authenticated).
- [ ] Tests for list and delete operations are passing (list success, delete success/forbidden, 404).

## Definition of Done
- [ ] List and delete endpoints implemented (use-cases and API handlers).
- [ ] List attachments use-case implemented (query by task_id, return metadata).
- [ ] Delete attachment use-case implemented (ownership check, delete file from storage, delete metadata).
- [ ] Ownership checks integrated (verify task owner before allowing delete).
- [ ] Response schemas defined (Pydantic models for attachment response and list response).
- [ ] Tests added and passing (list success, delete success/forbidden, 404).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests confirm correct listing and deletion behavior per ownership rules (list returns metadata, delete enforces ownership, files removed from storage).
- **Observable Outcomes**: Endpoints respond correctly, attachments are listed with filename/size, deletion enforces ownership and removes files.

## Notes
Supports the "Show file name and size, allow deletion" requirement. Authorization middleware from task 2.5 provides additional protection, but use-case checks are required for defense in depth.

## Strengths
Provides complete lifecycle management for attachments. Enforces ownership rules and ensures proper file cleanup.

## Sub-tasks (Children)
- [ ] Review authorization requirements from `docs/requirements.md` (modify only own data, view all records).
- [ ] Create list attachments use-case (accept task ID, query by task_id, return metadata with filename and file_size).
- [ ] Create delete attachment use-case (accept attachment ID, user ID; verify task ownership, delete file from storage, delete metadata).
- [ ] Create API endpoint `GET /api/tasks/:id/attachments` (require auth, call use-case, return 200 with array).
- [ ] Create API endpoint `DELETE /api/attachments/:id` (require auth, call use-case, return 204/403/404).
- [ ] Define response schemas (Pydantic models for attachment response and list response).
- [ ] Write integration tests (list success, delete success/forbidden, 404).
- [ ] Test manually with API client to verify list and delete behavior.

## Completed
[ ] Pending / [ ] Completed


