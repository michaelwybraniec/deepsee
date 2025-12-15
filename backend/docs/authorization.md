# Authorization Implementation

## Overview

Authorization guards enforce the requirement: "Each user is allowed to modify only their own data, although they can view all records."

## Authorization Rules

### Rule 1: Modify Own Data Only
- Users can **create, update, delete** only their own tasks and attachments
- Ownership is verified by checking `owner_user_id` matches authenticated user ID
- Returns `403 Forbidden` if user attempts to modify another user's resource

### Rule 2: View All Records
- Users can **read/list** all tasks and attachments (no ownership filter)
- All authenticated users have read access to all resources
- Read endpoints return all resources regardless of ownership

## Implementation

### Ownership Model

**Tasks**:
- `Task.owner_user_id` field (foreign key to `users.id`)
- Set automatically on creation from authenticated user ID
- Never set from request body (security)

**Attachments**:
- Inherit ownership from parent task
- Or have direct `owner_user_id` field
- Ownership checked via task ownership

### Authorization Middleware

Location: `backend/api/middleware/authorization.py`

Functions:
- `check_ownership()`: Verifies user owns resource, raises 403 if not
- `require_ownership_for_modification()`: Checks ownership for update/delete operations
- `allow_read_for_all()`: Documents that read operations allow all authenticated users

### Application to Endpoints

**Task Modification Endpoints** (to be implemented in Task 3):
- `POST /api/tasks` (create): Set `owner_user_id` from authenticated user
- `PUT /api/tasks/:id` (update): Check `task.owner_user_id == current_user.id`
- `DELETE /api/tasks/:id` (delete): Check `task.owner_user_id == current_user.id`

**Task Read Endpoints** (to be implemented in Task 3):
- `GET /api/tasks` (list): No ownership filter, return all tasks
- `GET /api/tasks/:id` (detail): No ownership check, return task if exists

**Attachment Endpoints** (to be implemented in Task 4):
- Similar pattern: modify requires ownership, read allows all

## Defense in Depth

Authorization checks are implemented at two levels:
1. **Middleware level**: Early rejection (FastAPI dependencies)
2. **Use-case level**: Business logic verification (defense in depth)

This ensures no bypass paths exist.

## Testing

See `backend/tests/test_authorization.py` for authorization test cases.
