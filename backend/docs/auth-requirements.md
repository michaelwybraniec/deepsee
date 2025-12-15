# Authentication and Authorization Requirements

This document summarizes all authentication and authorization requirements extracted from the project documentation.

## Source References
- `docs/requirements.md` section "1. Secure Login"
- `docs/technical-specs.md` section "3.1 Secure Login"
- `docs/requirements.md` section "10. Front-End" (change password)
- `docs/technical-specs.md` section "3.10 Front‑End" (change password)

## Requirements Summary

### 1. Authentication Method
**Requirement**: Implement modern authentication (OIDC/OAuth2 or JWT-based).

**Source**: 
- `docs/requirements.md` §1: "Implement modern authentication (OIDC/OAuth2 or JWT-based)."
- `docs/technical-specs.md` §3.1: "Implement modern authentication (**OIDC/OAuth2** or **JWT‑based**)."

**Notes**: 
- Must choose one method (OIDC/OAuth2 OR JWT, not both required)
- Decision needed: which method to implement based on project context

### 2. Authorization Rule 1: Modify Own Data
**Requirement**: Each user is allowed to modify only their own data.

**Source**:
- `docs/requirements.md` §1: "Each user is allowed to modify only their own data, although they can view all records."
- `docs/technical-specs.md` §3.1: "Each user is allowed to **modify only their own data**, although they can **view all records**."

**Applies to**:
- Tasks: create, update, delete (only own tasks)
- Attachments: create, delete (only for own tasks)

### 3. Authorization Rule 2: View All Records
**Requirement**: Users can view all records (read-only access to others' data).

**Source**:
- `docs/requirements.md` §1: "Each user is allowed to modify only their own data, although they can view all records."
- `docs/technical-specs.md` §3.1: "Each user is allowed to **modify only their own data**, although they can **view all records**."

**Applies to**:
- Tasks: list all tasks, view detail of any task (read-only)
- Attachments: view attachments for any task (read-only)

### 4. Change Password Functionality
**Requirement**: Change password functionality must be supported.

**Source**:
- `docs/requirements.md` §10: "Change password functionality."
- `docs/technical-specs.md` §3.10: "Include **change password** functionality."

**Notes**:
- Requires backend endpoint for password change
- Requires frontend UI for password change (Task 10.6)

## Design Decisions Needed

1. **Authentication Method Choice**: 
   - JWT: Simpler, stateless, good for API-first applications
   - OIDC/OAuth2: Better for multi-tenant, external identity providers, adds complexity
   - Decision to be made in Task 2.2 based on project context and `docs/technology.md` recommendations

2. **Ownership Model**:
   - Tasks must have `owner_user_id` field
   - Attachments inherit ownership from tasks (or have direct `owner_user_id`)
   - User ID extracted from auth token for authorization checks

## Good Practices (Optional)

From `docs/technical-specs.md` §3.1:
> _Good practice (optional)_: Keep authentication logic centralized (e.g. middleware/guards) so that permission checks are not duplicated across handlers.

## Implementation Tasks

- Task 2.2: Choose and configure authentication approach
- Task 2.3: Implement login endpoint
- Task 2.4: Implement change-password endpoint
- Task 2.5: Implement authorization guards
