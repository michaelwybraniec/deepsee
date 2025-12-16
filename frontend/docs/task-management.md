# Task Management

**Files**: `src/pages/TaskListPage.jsx`, `src/pages/TaskDetailPage.jsx`, `src/pages/CreateTaskPage.jsx`, `src/pages/EditTaskPage.jsx`, `src/services/taskApi.js`

## Task Fields

- **Title**: Required
- **Description**: Optional
- **Status**: `pending`, `in_progress`, `done`
- **Priority**: `low`, `medium`, `high`
- **Due Date**: Date picker
- **Tags**: Comma-separated string

## Security

- **Ownership**: Users can only edit/delete their own tasks (enforced by backend)
- Frontend shows edit/delete buttons only for owned tasks

## API Service

All task operations use `src/services/taskApi.js`:
- `getTasks(params)` - List with search/filter/sort/pagination
- `getTask(id)` - Get single task
- `createTask(data)` - Create new task
- `updateTask(id, data)` - Update task
- `deleteTask(id)` - Delete task

## Related

- [Backend Task API](../backend/docs/task-model.md)
