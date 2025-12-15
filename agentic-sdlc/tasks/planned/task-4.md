# Task ID: 4
# Title: Attachments API
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 8h

## Description
Implement attachment handling for tasks, allowing users to upload files per task, display file name and size, and delete attachments.

## Dependencies
- [ ] Task ID: 3

## Testing Instructions
- Integration tests for upload, list, and delete operations.
- Verify that only the owner of a task can manage its attachments.

## Security Review
- Check for secure file handling (no path traversal, restricted types/size as appropriate).
- Ensure file storage configuration does not expose sensitive paths.

## Risk Assessment
- Poor file handling could lead to security or storage issues.

## Acceptance Criteria
- [ ] Endpoint(s) to upload attachments for a task.
- [ ] Endpoint(s) to list attachments for a task including file name and size.
- [ ] Endpoint(s) to delete attachments.
- [ ] Owner-only modification of attachments enforced.
- [ ] Tests for success and common failure cases are passing.

## Definition of Done
- [ ] Attachment metadata model and storage mechanism implemented.
- [ ] Attachment API integrated with task ownership rules.
- [ ] Tests implemented and passing.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Attachments can be added, listed, and deleted in tests.

## Notes
Actual storage backend choice is a design decision; the requirement is to support upload/list/delete and show name and size.

## Strengths
Fulfills the “Attachments” requirement while respecting security and ownership rules.

## Sub-tasks (Children)
- [ ] [Task 4.1: Confirm attachment requirements](task-4-1.md)
- [ ] [Task 4.2: Design attachment metadata and storage](task-4-2.md)
- [ ] [Task 4.3: Implement attachment upload endpoint](task-4-3.md)
- [ ] [Task 4.4: Implement attachment list and delete endpoints](task-4-4.md)

## Completed
[ ] Pending / [ ] Completed


