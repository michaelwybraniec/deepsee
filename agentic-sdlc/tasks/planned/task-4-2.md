# Task ID: 4.2
# Title: Design attachment metadata and storage
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 2h

## Description
Design the attachment metadata model and choose a storage approach (e.g. filesystem, object storage) consistent with requirements from `docs/requirements.md` section "3. Attachments" and `docs/technical-specs.md` section "3.3 Attachments".

**Step-by-step:**
1. Review requirements: must support upload, display (filename and size), and deletion per `docs/requirements.md`.
2. Design attachment metadata model (database schema or domain entity):
   - Required fields: `id`, `task_id` (foreign key to task), `filename` (string), `file_size` (integer, bytes).
   - Optional: `content_type` (MIME type), `uploaded_at` (timestamp), `storage_path` or `storage_url` (where file is stored).
   - Consider: file size limits, allowed file types (if any restrictions).
3. Choose storage approach:
   - **Local filesystem**: Simple for development, store in `backend/uploads/` or similar. Use relative paths in DB.
   - **Object storage (S3, MinIO)**: Better for production, scalable. Store bucket/key in DB.
   - **Database BLOB**: Not recommended for large files, but possible for small attachments.
4. Design storage interface (abstraction layer):
   - Define interface (e.g., `AttachmentStorage` with methods: `save(file, task_id) -> storage_path`, `get_url(storage_path) -> url`, `delete(storage_path) -> bool`).
   - This allows switching storage backends without changing business logic (Clean Architecture).
5. Document security considerations:
   - Path traversal prevention (sanitize filenames, validate paths).
   - Access control (only task owner can upload/delete attachments).
   - File size limits (prevent DoS).
   - File type validation (if restricting to specific types).
6. Create design document or code comments:
   - Model schema (fields, types, constraints).
   - Storage choice and rationale.
   - Storage interface definition.
   - Security measures.

**Implementation hints:**
- Place domain entity in `backend/domain/attachments/attachment.py`.
- Place storage interface in `backend/application/attachments/storage_interface.py` (port).
- Place storage implementation in `backend/infrastructure/attachments/storage.py` (adapter).
- For local filesystem: use `pathlib`, store files in `backend/uploads/{task_id}/{filename}`.
- For S3: use `boto3`, store files in `{bucket}/attachments/{task_id}/{filename}`.
- Always validate filename (remove path separators, limit length).

## Dependencies
- [ ] Task ID: 4.1 (Requirements analysis must be complete)

## Testing Instructions
- N/A for design task. Verify that the model includes task reference, filename, size, and storage reference.
- Review design document/code to ensure all required fields are present.

## Security Review
- Consider security implications of the chosen storage (path traversal, public access).
- Filename sanitization: remove `../`, limit length, allow only safe characters.
- Access control: only task owner can upload/delete (enforce in API layer).
- File size limits: prevent DoS attacks (e.g., max 10MB per file).
- Storage path validation: ensure files are stored in intended directory only.

## Risk Assessment
- Poor storage design can lead to security issues (path traversal, unauthorized access) or operational complexity.
- Choosing wrong storage backend may require refactoring later.

## Acceptance Criteria
- [ ] Attachment metadata model defined with at least: `id`, `task_id`, `filename`, `file_size`, `storage_reference` (path or URL).
- [ ] Storage approach decided and documented (filesystem, S3, or other) with rationale.
- [ ] Storage interface (abstraction) defined with methods: save, get_url, delete.
- [ ] Security considerations documented (path traversal prevention, access control, file size limits).
- [ ] Design is implementable (clear enough to code without guesswork).

## Definition of Done
- [ ] Model schema documented (fields, types, constraints) in code or design doc.
- [ ] Storage choice documented with rationale.
- [ ] Storage interface defined (methods and signatures).
- [ ] Security measures documented.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Metadata model and storage configuration are committed (design doc or code comments exist).
- **Observable Outcomes**: Design document/code shows complete model schema, storage choice, and interface definition.

## Notes
The actual storage backend is a design decision; the requirement is to support upload, list, and delete. Choose based on project constraints (time, infrastructure, scalability needs).

## Strengths
Provides a solid base for implementing attachment operations with clear separation of concerns (domain model vs storage implementation).

## Sub-tasks (Children)
- [ ] Review attachment requirements from `docs/requirements.md` (upload, show filename/size, delete).
- [ ] Draft attachment metadata schema (id, task_id, filename, file_size, storage_reference, timestamps).
- [ ] Evaluate storage options (local filesystem vs object storage) based on project needs.
- [ ] Decide on storage backend and document rationale.
- [ ] Design storage interface (abstraction layer) with save/get_url/delete methods.
- [ ] Document security considerations (path traversal, access control, file size limits).
- [ ] Create design document or code comments summarizing model, storage choice, and interface.

## Completed
[ ] Pending / [ ] Completed


