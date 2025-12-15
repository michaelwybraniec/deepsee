## Technical Specification – Task Tracker (Strict Restatement)

This document **restructures** but does not extend or interpret the original assignment in `docs/requirements.md`.  
It is intended as a faithful, sectioned view of the same content.

---

## 1. Overview

- Full Stack Developer – Technical Assessment.
- AI‑assisted development is required (agentic AI tools such as Cursor, GitHub Copilot, Claude, etc.).
- Goal: design and implement a modern full‑stack web application using Python and React (or similar).
- Target: a well‑structured, functional system based on Clean Architecture, with maintainable code and clearly reasoned design decisions.

---

## 2. Assignment Description

- Build a **Task Tracker** application that allows users to securely manage their personal tasks.
- Each user can:
  - Log in.
  - Create tasks.
  - Attach files to tasks.
  - Receive reminders.
  - Monitor their activity.
- The system must include:
  - A backend service.
  - A front‑end.
  - Basic observability.

---

## 3. Functional Requirements

### 3.1 Secure Login
- Implement modern authentication (**OIDC/OAuth2** or **JWT‑based**).
- Each user is allowed to **modify only their own data**, although they can **view all records**.

> _Good practice (optional)_: Keep authentication logic centralized (e.g. middleware/guards) so that permission checks are not duplicated across handlers.

### 3.2 Task Management
- Users can:
  - Create tasks.
  - View tasks.
  - Edit tasks.
  - Delete tasks.
- Task fields:
  - Title.
  - Description.
  - Status.
  - Priority.
  - Due date.
  - Tags.
- The front‑end must provide:
  - Client‑side validation.
  - User‑friendly error handling.

> _Good practice (optional)_: Keep controllers/route handlers thin and move task business rules into dedicated use‑case/services for easier testing and maintenance.

### 3.3 Attachments
- Allow users to upload files (e.g., screenshots, documents) for each task.
- Display:
  - File name.
  - File size.
- Allow deletion of attachments.

### 3.4 Search & Filtering
- Search tasks by:
  - Title.
  - Description.
- Filter tasks by:
  - Status.
  - Priority.
  - Tags.
  - Due date.
- Sort results.
- Paginate results.

### 3.5 Notifications
- A background worker/service:
  - Checks for tasks due in the next 24 hours.
  - Logs “reminder sent” events.
- The notification system must be:
  - Idempotent.
  - Fault‑tolerant (no duplicate reminders).

### 3.6 Audit Trail
- Record key actions:
  - Task creation.
  - Task update.
  - Attachment added.
  - Attachment removed.
  - Reminder sent.
- Include:
  - Timestamps.
  - User ID.

### 3.7 Rate Limiting
- Apply basic per‑user or per‑IP rate limiting on API requests.
- When limits are exceeded:
  - Return meaningful error responses.

### 3.8 Monitoring & Logging
- Use **structured logging** with **correlation IDs** for each request.
- Add basic metrics, for example:
  - Request count.
  - Error rate.
  - Latency.
  - Reminders processed.
- Implement health check endpoints for:
  - API.
  - Database.
  - Worker (etc.).

> _Good practice (optional)_: Use a single correlation ID per request and propagate it through logs and metrics to simplify troubleshooting.

### 3.9 Error Handling & Resilience
- Implement centralized exception handling.
- Ensure consistent error responses.
- Workers should:
  - Gracefully handle restarts.
  - Retry failed jobs.

> _Good practice (optional)_: Define and reuse a single JSON error response shape across all endpoints to keep the API predictable.

### 3.10 Front‑End
- Implement a React UI for:
  - Login.
  - Task management.
- Views:
  - Task list.
  - Task detail.
  - Create/edit task.
  - Attachments section.
- Show toasts or alerts for:
  - Success.
  - Failure.
- Include **change password** functionality.

### 3.11 Tests
- Implement tests of the following kinds:
  - Unit tests.
  - Integration tests (API + DB).
  - Worker/queue tests.
  - Contract/API documentation tests.
  - Observability/health checks tests.
  - UI smoke tests.

> _Good practice (optional)_: Prioritize tests around the core flows first (login, task CRUD, reminders) before adding coverage for edge cases.

---

## 4. Deliverables

- Source code organized into logical projects:
  - API.
  - Worker.
  - UI.
- Docker Compose for local run:
  - API.
  - Worker.
  - Database.
  - Frontend.
- API documentation:
  - Swagger/OpenAPI.
- Tests.
- Architecture and rationale document:
  - Architecture diagram.
  - Brief explanation.
- Clear instructions on:
  - How to install the application.
  - How to run it.
- Self‑assessment including:
  - What was completed and what is missing.
  - Design choices and trade‑offs.
  - Where AI assisted you (with example prompts).

---

## 5. Evaluation Criteria

- Architecture clarity and modularity.
- Code organization and readability.
- Use of Python/React and modern web best practices.
- Thoughtfulness of the self‑assessment and documentation.
- Proper and effective use of agentic AI tools.

---

## 6. Design Decisions & Assumptions (Not in Original Requirements)

The following items are **implementation choices** made during design and are **not explicitly specified** in `docs/requirements.md`.  
They can be changed if needed without violating the original assignment.

- **Domain model details (examples)**:
  - Specific task statuses (e.g. `todo`, `in_progress`, `done`).
  - Specific priority levels (e.g. `low`, `medium`, `high`).
  - Extra entity fields such as internal IDs, owner references, or metadata.

- **API and protocol choices**:
  - Using REST over HTTP with JSON bodies and responses.
  - Exact URL structure and naming conventions for endpoints.
  - Specific HTTP status codes or error response shapes beyond “meaningful error responses”.

- **Pagination, sorting, and filtering mechanics**:
  - Exact query parameters for pagination (e.g. `page`, `page_size`).
  - Default sort order (e.g. by due date or creation date).
  - Any additional filter combinations or operators beyond those named in the requirements.

- **Infrastructure and tooling**:
  - Choice of database and ORM.
  - Choice of job queue/scheduler for background workers.
  - Specific logging/metrics libraries and formats (beyond “structured logging” and “basic metrics”).

- **Frontend UX details**:
  - Visual design, component library, and layout structure.
  - Exact behavior and appearance of toasts/alerts and validation messages.
  - Any additional pages or UI flows that help usability but are not explicitly listed.

Whenever a new design decision is made that goes beyond the strict wording of `docs/requirements.md`, it should be documented here (or in a separate architecture/rationale document) and clearly marked as an assumption or choice.


