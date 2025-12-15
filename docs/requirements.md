Hi Michael, it was a pleasure to meet you, this is the assignment.

Full Stack Developer - Technical Assessment
AI-assisted development required
Overview
This assignment is designed to evaluate your ability to design and implement a modern full-stack web application using Python, and React (or similar) using agentic AI development tools (e.g., Cursor, GitHub Copilot, Claude, etc).
Your goal is to deliver a well-structured, functional system based on Clean Architecture, with maintainable code and clearly reasoned design decisions.
 
Assignment: Task Tracker

Description
Create a Task Tracker application that allows users to securely manage their personal tasks.
Each user can log in, create tasks, attach files, receive reminders, and monitor their activity.
The system should include a backend service, a front-end, and basic observability.

Functional Requirements

1. Secure Login
Implement modern authentication (OIDC/OAuth2 or JWT-based).
Each user is allowed to modify only their own data, although they can view all records.

2. Task Management
Create, view, edit, and delete tasks.
Fields: title, description, status, priority, due date, tags.
Client-side validation and user-friendly error handling.

3. Attachments
Allow users to upload files (e.g., screenshots, documents) for each task.
Show file name and size, allow deletion.

4. Search & Filtering
Search tasks by title or description.
Filter by status, priority, tags, and due date.
Sort and paginate results.

5. Notifications
Background worker/service checks for tasks due in the next 24 hours and logs “reminder sent” events.
Idempotent and fault-tolerant (no duplicate reminders).

6. Audit Trail
Record key actions: task creation, update, attachment added/removed, reminder sent.
Include timestamps and user ID.

7. Rate Limiting
Apply basic per-user or per-IP rate limiting on API requests.
Return meaningful error responses when limits are exceeded.

8. Monitoring & Logging
Use structured logging with correlation IDs for each request.
Add basic metrics (e.g., request count, error rate, latency, reminders processed).
Implement health check endpoints (API, database, worker, etc.).

9. Error Handling & Resilience
Centralized exception handling and consistent error responses.
Workers should gracefully handle restarts and retry failed jobs.

10. Front-End
React UI for login and task management.
Views: Task list, task detail, create/edit task, attachments section.
Show toasts or alerts for success/failure.
Change password functionality.

11. Tests
Unit tests
Integration tests (API + DB)
Worker/queue tests
Contract/API documentation tests
Observability/health checks tests
UI smoke tests
 
Deliverables
Source code organized into logical projects (API, Worker, UI).
Docker compose for local run (API, worker, database, frontend).
API documentation (Swagger/OpenAPI).

Tests.
Architecture and rationale document (architecture diagram + brief explanation).
Clear instructions on how to install the application and run it
Self-assessment including:
What was completed and what’s missing.
Design choices and trade-offs.
Where AI assisted you (include example prompts).
 
Evaluation Criteria
Architecture clarity and modularity.
Code organization and readability.
Use of Python/React and modern web best practices.
Thoughtfulness of the self-assessment and documentation.
Proper and effective use of agentic AI tools.
 
Let me know when you have finished it.
Regards 
Loris