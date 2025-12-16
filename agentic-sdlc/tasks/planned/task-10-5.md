# Task ID: 10.5
# Title: Implement attachments UI
# Status: [x] In Progress
# Priority: high
# Owner: Frontend Dev
# Estimated Effort: 4h

## Description
Implement the attachments section in the task views, allowing users to upload, list, and delete attachments via the backend Attachments API, per `docs/requirements.md` section "10. Front-End" and `docs/technical-specs.md` section "3.10 Front‑End".

**Step-by-step:**
1. Review frontend requirements from task 10.1 (attachments section in task views).
2. Create API client for attachments:
   - Create `frontend/src/services/attachmentApi.js`:
     - `uploadAttachment(taskId, file)` - calls `POST /api/tasks/:id/attachments` with multipart/form-data, returns attachment.
     - `listAttachments(taskId)` - calls `GET /api/tasks/:id/attachments`, returns attachment list.
     - `deleteAttachment(attachmentId)` - calls `DELETE /api/attachments/:id`.
     - Handle errors (return error message from backend).
3. Implement attachments section component:
   - Create `AttachmentsSection.jsx` component (used in task detail view):
     - Display list of attachments (file name, file size) - call `attachmentApi.listAttachments(taskId)`.
     - Add "Upload" button with file input (hidden input, trigger on button click).
     - Add "Delete" button for each attachment (only if user is task owner).
     - Handle loading state (show loading spinner while fetching/uploading).
     - Handle error state (show error message if operation fails).
4. Implement attachment upload:
   - File input handler: on file select, call `attachmentApi.uploadAttachment(taskId, file)`.
   - Show upload progress (optional: progress bar or loading indicator).
   - On success: show success toast, refresh attachment list.
   - On error: show error message (file too large, invalid type, etc.).
   - Client-side validation: file size limit (e.g., max 10MB), file type validation (optional).
5. Implement attachment list and delete:
   - Display attachments: map over attachment list, show file name and size.
   - Delete handler: call `attachmentApi.deleteAttachment(attachmentId)`, show confirmation dialog.
   - On success: show success toast, remove attachment from list (optimistic update or refresh list).
   - On error: show error message.
6. Integrate into task detail view:
   - Add `AttachmentsSection` component to `TaskDetailPage.jsx`.
   - Pass task ID to attachments section.
   - Show attachments section below task details.
7. Write UI smoke tests:
   - Test uploading attachment (select file, upload, verify success toast, attachment appears in list with name and size).
   - Test deleting attachment (click delete, confirm, verify success toast, attachment removed from list).
   - Test attachment list (verify file name and size displayed correctly).
   - Test error handling (upload too large file, verify error message).

**Implementation hints:**
- Use `FormData` for file uploads (multipart/form-data).
- Use React state to manage attachment list (add/remove optimistically or refresh after operations).
- Show file size in human-readable format (e.g., "1.5 MB" instead of bytes).
- Use file input with accept attribute to restrict file types (optional).

## Dependencies
- [ ] Task ID: 4.3 (Attachment upload endpoint must exist)
- [ ] Task ID: 4.4 (Attachment list/delete endpoints must exist)
- [ ] Task ID: 10.4 (Task detail view must exist)

## Testing Instructions
- UI smoke tests:
  - Uploading an attachment and seeing it appear in the list with file name and size (verify upload works, attachment displayed, name and size correct).
  - Deleting an attachment and verifying it disappears from the list (verify delete works, attachment removed, list updated).
  - Test error handling (upload too large file, verify error message displayed).
- Manual test: Use browser to upload and delete attachments, verify behavior.

## Security Review
- Ensure the UI does not expose raw file paths or sensitive metadata:
  - Display only file name and size (not storage path, internal IDs).
  - Don't expose user IDs or other sensitive data in attachment list.

## Risk Assessment
- Broken attachments UI may confuse users about the state of their uploaded files.
- Missing error handling can leave users confused.
- File upload issues (size, type) can cause errors.

## Acceptance Criteria
- [ ] Attachments section shows file name and size for each attachment (list displayed, name and size visible).
- [ ] Users can upload attachments tied to a task (file input works, upload succeeds, attachment appears in list).
- [ ] Users can delete attachments, with the UI updated accordingly (delete button works, confirmation shown, attachment removed from list).
- [ ] Client-side validation implemented (file size limit, file type validation if applicable).
- [ ] UI smoke tests for attachment flows are passing (all test cases pass).

## Definition of Done
- [ ] Attachments UI integrated with backend API (attachments section component, API client).
- [ ] Attachment upload UI implemented (file input, upload handler, progress, success/error handling).
- [ ] Attachment list and delete UI implemented (list display, delete button, confirmation, success/error handling).
- [ ] Attachments section integrated into task detail view.
- [ ] Tests added and passing (upload, delete, list, error handling).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: UI tests confirm attachments can be managed end-to-end (all test cases pass).
- **Observable Outcomes**: Attachments section works in browser, upload/delete work, file name and size displayed.

## Notes
Supports the "Attachments" requirement at the UI layer. This task implements the frontend for attachment management.

## Strengths
Gives users clear feedback on files associated with their tasks. Provides complete attachment management UI.

## Sub-tasks (Children)
- [ ] Review frontend requirements from task 10.1 (attachments section).
- [ ] Create API client for attachments (uploadAttachment, listAttachments, deleteAttachment methods, error handling).
- [ ] Implement attachments section component (list display, upload button, delete buttons).
- [ ] Implement attachment upload (file input, upload handler, progress, success/error handling, validation).
- [ ] Implement attachment list and delete (list display, delete handler, confirmation, success/error handling).
- [ ] Integrate attachments section into task detail view.
- [ ] Write UI smoke tests (upload, delete, list, error handling).
- [ ] Test manually by uploading and deleting attachments in browser.

## Completed
[x] Completed


