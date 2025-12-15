# Task ID: 10.4
# Title: Implement task list, detail, and edit views
# Status: [ ] Pending
# Priority: high
# Owner: Frontend Dev
# Estimated Effort: 5h

## Description
Implement frontend views for task list, task detail, and create/edit task, integrating with the backend Task API, per `docs/requirements.md` section "10. Front-End" and `docs/technical-specs.md` section "3.10 Front‑End".

**Step-by-step:**
1. Review frontend requirements from task 10.1 (task list, detail, create/edit views).
2. Create API client for tasks:
   - Create `frontend/src/services/taskApi.js`:
     - `getTasks()` - calls `GET /api/tasks`, returns task list.
     - `getTask(id)` - calls `GET /api/tasks/:id`, returns task.
     - `createTask(taskData)` - calls `POST /api/tasks`, returns created task.
     - `updateTask(id, taskData)` - calls `PUT /api/tasks/:id`, returns updated task.
     - `deleteTask(id)` - calls `DELETE /api/tasks/:id`.
     - Handle errors (return error message from backend).
3. Implement task list view:
   - Create `TaskListPage.jsx` component:
     - Fetch tasks on mount: call `taskApi.getTasks()`.
     - Display tasks in list/table (title, status, priority, due date, tags).
     - Add navigation to task detail (click task → navigate to `/tasks/:id`).
     - Add "Create Task" button (navigate to `/tasks/new`).
     - Handle loading state (show loading spinner while fetching).
     - Handle error state (show error message if fetch fails).
4. Implement task detail view:
   - Create `TaskDetailPage.jsx` component:
     - Fetch task on mount: call `taskApi.getTask(id)` with task ID from route params.
     - Display full task information (title, description, status, priority, due date, tags, attachments section).
     - Add "Edit" button (navigate to `/tasks/:id/edit`) - only if user is owner.
     - Add "Delete" button (call `taskApi.deleteTask()`, show confirmation, redirect to list) - only if user is owner.
     - Handle loading and error states.
5. Implement create task view:
   - Create `CreateTaskPage.jsx` component:
     - Form with fields: title (required), description, status, priority, due_date, tags.
     - Submit handler: call `taskApi.createTask()`, on success: show success toast, redirect to task detail or list.
     - On error: display error message (toast/alert or inline).
     - Client-side validation: required fields, date format, enum values.
6. Implement edit task view:
   - Create `EditTaskPage.jsx` component:
     - Fetch task on mount: call `taskApi.getTask(id)`.
     - Form with fields pre-filled from task data.
     - Submit handler: call `taskApi.updateTask()`, on success: show success toast, redirect to task detail.
     - On error: display error message (toast/alert or inline).
     - Client-side validation: same as create task.
7. Write UI smoke tests:
   - Test viewing task list (verify tasks displayed, navigation works).
   - Test viewing task detail (verify task information displayed, edit/delete buttons shown for owner).
   - Test creating task (fill form, submit, verify success toast, redirect, task appears in list).
   - Test editing task (fill form, submit, verify success toast, redirect, task updated).
   - Test deleting task (click delete, confirm, verify success toast, redirect, task removed from list).

**Implementation hints:**
- Use React Router for navigation (`useNavigate`, `useParams` hooks).
- Use React Query or SWR for data fetching (caching, refetching, loading states).
- Use form library (React Hook Form, Formik) for form handling and validation.
- Check task ownership for edit/delete buttons (from task.owner_user_id vs authenticated user ID).

## Dependencies
- [ ] Task ID: 3.3 (Create task endpoint must exist)
- [ ] Task ID: 3.4 (Read task endpoints must exist)
- [ ] Task ID: 3.5 (Update/delete task endpoints must exist)
- [ ] Task ID: 10.2 (React project and routing must be set up)

## Testing Instructions
- UI smoke tests:
  - Viewing the task list and individual task details (verify tasks displayed, navigation works, task info correct).
  - Creating and editing tasks via the UI (fill form, submit, verify success, task created/updated).
  - Deleting tasks (click delete, confirm, verify task deleted).
- Manual test: Use browser to view, create, edit, and delete tasks, verify behavior.

## Security Review
- Ensure UI does not allow editing/deleting tasks that backend will reject, and handles errors gracefully:
  - Check task ownership before showing edit/delete buttons (UI check, backend will also enforce).
  - Handle 403 Forbidden errors gracefully (show error message, don't crash).
  - Don't expose sensitive data in UI (e.g., user IDs, internal IDs).

## Risk Assessment
- Poor task views may expose confusing or incomplete information to users.
- Missing error handling can leave users confused.
- Missing loading states can make UI feel unresponsive.

## Acceptance Criteria
- [ ] Task list view shows tasks and supports basic navigation (tasks displayed, click to detail, create button works).
- [ ] Task detail view shows full task information (all fields displayed, edit/delete buttons for owner).
- [ ] Create/edit views allow users to submit task data to backend and handle responses (form works, API call succeeds, success/error handling).
- [ ] Client-side validation implemented (required fields, date format, enum values).
- [ ] UI smoke tests for these flows are passing (all test cases pass).

## Definition of Done
- [ ] Views implemented and wired to API (task list, detail, create, edit pages, API client).
- [ ] Task list view implemented (fetch tasks, display list, navigation).
- [ ] Task detail view implemented (fetch task, display info, edit/delete buttons for owner).
- [ ] Create/edit task views implemented (forms, API calls, validation, success/error handling).
- [ ] Tests added and passing (list, detail, create, edit, delete flows).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: UI tests show successful task CRUD via the frontend (all test cases pass).
- **Observable Outcomes**: Task views work in browser, tasks displayed, create/edit/delete work, errors handled.

## Notes
Search, filter, sort, and pagination UI refinements may be handled incrementally (can be added later as enhancements). This task implements core task management UI.

## Strengths
Delivers the core task management UI required by the assignment. Provides complete task CRUD functionality.

## Sub-tasks (Children)
- [ ] Review frontend requirements from task 10.1 (task list, detail, create/edit views).
- [ ] Create API client for tasks (getTasks, getTask, createTask, updateTask, deleteTask methods, error handling).
- [ ] Implement task list view (fetch tasks, display list, navigation to detail, create button, loading/error states).
- [ ] Implement task detail view (fetch task, display info, edit/delete buttons for owner, loading/error states).
- [ ] Implement create task view (form, API call, validation, success/error handling, redirect).
- [ ] Implement edit task view (fetch task, form pre-filled, API call, validation, success/error handling, redirect).
- [ ] Write UI smoke tests (list, detail, create, edit, delete flows).
- [ ] Test manually by viewing, creating, editing, and deleting tasks in browser.

## Completed
[ ] Pending / [ ] Completed


