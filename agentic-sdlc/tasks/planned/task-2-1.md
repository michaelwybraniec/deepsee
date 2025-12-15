# Task ID: 2.1
# Title: Analyze authentication and authorization requirements
# Status: [x] Completed
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 1h

## Description
Review `docs/requirements.md` and `docs/technical-specs.md` to extract all authentication and authorization-related requirements, including modern auth, modify-own-data, view-all-records, and change password.

**Step-by-step:**
1. Open `docs/requirements.md` and locate section "1. Secure Login":
   - Note: "Implement modern authentication (OIDC/OAuth2 or JWT-based)."
   - Note: "Each user is allowed to modify only their own data, although they can view all records."
2. Open `docs/technical-specs.md` and locate section "3.1 Secure Login":
   - Verify it matches requirements.md (should be a restatement).
   - Note any additional clarifications.
3. Check for change password requirement:
   - In `docs/requirements.md` section "10. Front-End": "Change password functionality."
   - In `docs/technical-specs.md` section "3.10 Front‑End": "Include **change password** functionality."
4. Extract key requirements into a structured list:
   - **Authentication**: Must support OIDC/OAuth2 OR JWT (choose one, not both required).
   - **Authorization rule 1**: Users can modify only their own data (tasks, attachments).
   - **Authorization rule 2**: Users can view all records (read-only access to others' tasks).
   - **Change password**: Must be supported (backend endpoint + frontend UI).
5. Document findings in a summary file:
   - Create `backend/docs/auth-requirements.md` or add to architecture notes.
   - List each requirement with source reference (e.g., "req.md §1", "tech-specs.md §3.1").
   - Note any ambiguities or design decisions needed (e.g., which auth method to choose).

**Implementation hints:**
- Use a simple markdown file or code comments in auth module.
- Keep summary concise but complete (1-2 pages max).
- Reference exact section numbers from docs for traceability.

## Dependencies
- [x] Task ID: 1 (Documentation must exist)

## Testing Instructions
- N/A (documentation/analysis task). Verify outcomes by checking that the summary list covers all relevant bullets in the docs.
- Cross-check: Every auth-related bullet in `docs/requirements.md` and `docs/technical-specs.md` should appear in the summary.

## Security Review
- Ensure no requirement that affects security (e.g. password change, modify-own-data rule) is overlooked.
- Verify that authorization rules are clearly understood (modify own vs view all).

## Risk Assessment
- Missing or misinterpreted auth requirements could lead to an incorrect implementation later.
- Unclear authorization rules could cause security vulnerabilities.

## Acceptance Criteria
- [x] A short written summary (in code comments, `backend/docs/auth-requirements.md`, or architecture notes) lists all auth-related requirements from the docs.
- [x] The summary explicitly mentions: modern auth (OIDC/OAuth2 or JWT), modify-own-data, view-all-records, and change password.
- [x] Each requirement includes a source reference (which doc section it came from).
- [x] Summary is stored in a location accessible during implementation (e.g., `backend/docs/` or code comments).

## Definition of Done
- [x] Requirements have been reviewed and summarized.
- [x] The summary is stored alongside backend auth code or architecture notes (file committed or documented).
- [x] Summary covers all auth-related bullets from both docs.
- [x] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Every auth-related bullet in the docs is accounted for in the summary (cross-check complete).
- **Observable Outcomes**: Summary file/comments exist and are readable, requirements are clearly listed.

## Notes
This task prepares for choosing and implementing the auth mechanism. The summary will guide decisions in tasks 2.2, 2.3, 2.4, and 2.5.

**Completed**: Created `backend/docs/auth-requirements.md` with all authentication and authorization requirements extracted from documentation. Summary includes:
- Authentication method requirement (OIDC/OAuth2 or JWT)
- Authorization rule 1: Modify own data only
- Authorization rule 2: View all records
- Change password functionality requirement
- All requirements include source references (doc sections)

## Strengths
Reduces risk of missing or misreading security-sensitive requirements. Provides a single source of truth for auth requirements during implementation.

## Sub-tasks (Children)
- [x] Open `docs/requirements.md` and locate section "1. Secure Login".
- [x] Open `docs/technical-specs.md` and locate section "3.1 Secure Login".
- [x] Check `docs/requirements.md` section "10. Front-End" for change password requirement.
- [x] Extract key requirements: auth method (OIDC/OAuth2 or JWT), modify-own-data, view-all-records, change password.
- [x] Create summary file (e.g., `backend/docs/auth-requirements.md`) or add to architecture notes.
- [x] Document each requirement with source reference (doc section numbers).
- [x] Verify summary covers all auth-related bullets (cross-check against both docs).

## Completed
[x] Completed


