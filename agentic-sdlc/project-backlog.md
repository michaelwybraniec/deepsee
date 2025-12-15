# Project Backlog – Task Tracker

## How to Use This Backlog

This backlog follows the **Agentic Workflow Protocol (AWP)** for task management. See [AWP.md](AWP.md) for complete workflow instructions.

### Quick Start

1. **Check current status**: Review this backlog to see planned tasks
2. **Find next task**: Look for tasks with all dependencies completed
3. **Read task file**: Open the task file (e.g., `tasks/planned/task-2-1.md`) for detailed instructions
4. **Follow AWP workflow**: Use `awp check`, `awp update`, `awp commit`, `awp next` commands

### Workflow Commands

- **`awp check`**: Determine the current actionable step
- **`awp update`**: Review docs, update documentation, check for blockers
- **`awp commit`**: Commit changes with task references (e.g., `feat(auth): implement login [task-2-3]`)
- **`awp next`**: Move to next task after update and commit
- **`awp handoff`**: Transfer work between human and AI

### Task Structure

Each task file contains:
- **Step-by-step instructions** in the Description section
- **Detailed acceptance criteria** with concrete examples
- **Implementation hints** (file locations, patterns, libraries)
- **Actionable sub-tasks** with clear steps
- **Testing instructions** and **Security review** notes

### Technology Decisions

Technology choices, library versions, and rationale are documented in `docs/technology.md`. Tasks that involve technology decisions should reference this document for specific library choices, versions, and alternatives considered.

### Starting a Task

1. Check that all dependencies are completed
2. Read the full task file for detailed instructions
3. Mark task as `[x] In Progress` in the task file
4. Follow the step-by-step instructions
5. Verify acceptance criteria as you work

### Completing a Task

1. Verify all acceptance criteria are met
2. Run all relevant tests
3. Mark task as `[x] Completed` in the task file
4. Move task from "Planned" to "Completed" below
5. Commit with task reference: `awp commit`

---

## Planned Tasks

- [x] [Task 1: Project environment and documentation](tasks/planned/task-1.md)
  - [x] [Task 1.1: Verify repository structure](tasks/planned/task-1-1.md)
  - [x] [Task 1.2: Verify root README links](tasks/planned/task-1-2.md)
  - [x] [Task 1.3: Verify requirements source document](tasks/planned/task-1-3.md)
  - [x] [Task 1.4: Verify technical spec restatement](tasks/planned/task-1-4.md)
  - [x] [Task 1.5: Verify architecture document alignment](tasks/planned/task-1-5.md)
  - [x] [Task 1.6: Review agentic SDLC backlog coverage](tasks/planned/task-1-6.md)
- [x] [Task 2: Secure login and authorization](tasks/planned/task-2.md)
  - [x] [Task 2.1: Analyze authentication and authorization requirements](tasks/planned/task-2-1.md)
  - [x] [Task 2.2: Choose and configure authentication approach](tasks/planned/task-2-2.md)
  - [x] [Task 2.3: Implement login endpoint](tasks/planned/task-2-3.md)
  - [x] [Task 2.4: Implement change-password endpoint](tasks/planned/task-2-4.md)
  - [x] [Task 2.5: Implement authorization guards](tasks/planned/task-2-5.md)
- [x] [Task 3: Task management API (CRUD)](tasks/planned/task-3.md)
  - [x] [Task 3.1: Confirm task field requirements](tasks/planned/task-3-1.md)
  - [x] [Task 3.2: Design task data model](tasks/planned/task-3-2.md)
  - [x] [Task 3.3: Implement create task endpoint](tasks/planned/task-3-3.md)
  - [x] [Task 3.4: Implement read task endpoints](tasks/planned/task-3-4.md)
  - [x] [Task 3.5: Implement update and delete task endpoints](tasks/planned/task-3-5.md)
- [x] [Task 4: Attachments API](tasks/planned/task-4.md)
  - [x] [Task 4.1: Confirm attachment requirements](tasks/planned/task-4-1.md)
  - [x] [Task 4.2: Design attachment metadata and storage](tasks/planned/task-4-2.md)
  - [x] [Task 4.3: Implement attachment upload endpoint](tasks/planned/task-4-3.md)
  - [x] [Task 4.4: Implement attachment list and delete endpoints](tasks/planned/task-4-4.md)
- [x] [Task 5: Search, filtering, sorting, pagination](tasks/planned/task-5.md)
  - [x] [Task 5.1: Confirm search and filter requirements](tasks/planned/task-5-1.md)
  - [x] [Task 5.2: Design search, filter, sort, and pagination API](tasks/planned/task-5-2.md)
  - [x] [Task 5.3: Implement search by title and description](tasks/planned/task-5-3.md)
  - [x] [Task 5.4: Implement filters, sorting, and pagination](tasks/planned/task-5-4.md)
- [ ] [Task 6: Notifications worker for due tasks](tasks/planned/task-6.md)
  - [ ] [Task 6.1: Confirm notification requirements](tasks/planned/task-6-1.md)
  - [ ] [Task 6.2: Design worker schedule and query](tasks/planned/task-6-2.md)
  - [ ] [Task 6.3: Implement reminder worker job](tasks/planned/task-6-3.md)
  - [ ] [Task 6.4: Implement idempotency and retry behavior](tasks/planned/task-6-4.md)
- [ ] [Task 7: Audit trail implementation](tasks/planned/task-7.md)
  - [ ] [Task 7.1: Confirm audit trail requirements](tasks/planned/task-7-1.md)
  - [ ] [Task 7.2: Design audit event schema](tasks/planned/task-7-2.md)
  - [ ] [Task 7.3: Implement audit logging service](tasks/planned/task-7-3.md)
  - [ ] [Task 7.4: Integrate audit logging with tasks, attachments, and reminders](tasks/planned/task-7-4.md)
- [ ] [Task 8: Rate limiting](tasks/planned/task-8.md)
  - [ ] [Task 8.1: Confirm rate limiting requirements](tasks/planned/task-8-1.md)
  - [ ] [Task 8.2: Design rate limiting strategy](tasks/planned/task-8-2.md)
  - [ ] [Task 8.3: Implement rate limiting and tests](tasks/planned/task-8-3.md)
- [ ] [Task 9: Monitoring, logging, health checks](tasks/planned/task-9.md)
  - [ ] [Task 9.1: Confirm monitoring and logging requirements](tasks/planned/task-9-1.md)
  - [ ] [Task 9.2: Implement structured logging and correlation IDs](tasks/planned/task-9-2.md)
  - [ ] [Task 9.3: Implement basic metrics collection](tasks/planned/task-9-3.md)
  - [ ] [Task 9.4: Implement health check endpoints](tasks/planned/task-9-4.md)
- [ ] [Task 10: React frontend](tasks/planned/task-10.md)
  - [ ] [Task 10.1: Confirm frontend requirements](tasks/planned/task-10-1.md)
  - [ ] [Task 10.2: Set up React project and routing](tasks/planned/task-10-2.md)
  - [ ] [Task 10.3: Implement auth-related frontend flows](tasks/planned/task-10-3.md)
  - [ ] [Task 10.4: Implement task list, detail, and edit views](tasks/planned/task-10-4.md)
  - [ ] [Task 10.5: Implement attachments UI](tasks/planned/task-10-5.md)
  - [ ] [Task 10.6: Implement validation, error handling, and toasts/alerts](tasks/planned/task-10-6.md)
- [ ] [Task 11: Testing and self-assessment](tasks/planned/task-11.md)
  - [ ] [Task 11.1: Confirm test and deliverable requirements](tasks/planned/task-11-1.md)
  - [ ] [Task 11.2: Implement required test categories](tasks/planned/task-11-2.md)
  - [ ] [Task 11.3: Add Docker Compose configuration](tasks/planned/task-11-3.md)
  - [ ] [Task 11.4: Integrate Swagger/OpenAPI documentation](tasks/planned/task-11-4.md)
  - [ ] [Task 11.5: Write architecture rationale and self-assessment](tasks/planned/task-11-5.md)

## Unplanned Tasks
- _None yet. Any scope beyond `docs/requirements.md` should be tracked here with `U-` IDs._

## Completed Tasks
- [x] [Task 1: Project environment and documentation](tasks/planned/task-1.md)
- [x] [Task 2: Secure login and authorization](tasks/planned/task-2.md)
- [x] [Task 3: Task management API (CRUD)](tasks/planned/task-3.md)
- [x] [Task 4: Attachments API](tasks/planned/task-4.md)
- [x] [Task 5: Search, filtering, sorting, pagination](tasks/planned/task-5.md)


