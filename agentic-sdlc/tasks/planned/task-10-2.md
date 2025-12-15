# Task ID: 10.2
# Title: Set up React project and routing
# Status: [ ] Pending
# Priority: high
# Owner: Frontend Dev
# Estimated Effort: 3h

## Description
Set up the React (or similar) frontend project with routing and a basic layout suitable for the required views, per `docs/requirements.md` section "10. Front-End" and `docs/technical-specs.md` section "3.10 Front‑End".

**Step-by-step:**
1. Review requirements: must support views for "Task list, task detail, create/edit task, attachments section" plus "login" and "change password" per `docs/requirements.md`.
2. Review technology decisions: See `docs/technology.md` section "4. Frontend Libraries" for recommended React setup, routing, and library choices.
3. Initialize React project:
   - Use `Vite` (recommended), `create-react-app`, or `Next.js` per `docs/technology.md`.
   - Place in `frontend/` directory.
   - Install dependencies: `react` 18+, `react-router-dom` 6.20+ (or similar for routing) per `docs/technology.md`.
4. Set up project structure:
   - `frontend/src/components/` - Reusable components.
   - `frontend/src/pages/` or `frontend/src/views/` - Page components.
   - `frontend/src/services/` - API client code.
   - `frontend/src/utils/` - Helper functions.
   - `frontend/src/App.jsx` or `App.tsx` - Main app component with routing.
4. Configure routing:
   - Install `react-router-dom` (or use framework routing if using Next.js).
   - Set up routes in `App.jsx`:
     - `/login` - Login page.
     - `/tasks` - Task list page.
     - `/tasks/:id` - Task detail page.
     - `/tasks/new` - Create task page.
     - `/tasks/:id/edit` - Edit task page.
     - `/tasks/:id/attachments` - Attachments section (could be part of detail page).
     - `/change-password` - Change password page.
   - Add route protection (placeholder for now, will be implemented in task 10.3).
5. Create base layout:
   - Create `Layout` component with navigation (if needed) and `<Outlet />` for child routes.
   - Or use simple layout with header/footer if required.
6. Create stub page components:
   - `LoginPage.jsx` - Placeholder with "Login" heading.
   - `TaskListPage.jsx` - Placeholder with "Task List" heading.
   - `TaskDetailPage.jsx` - Placeholder with "Task Detail" heading and task ID from route params.
   - `CreateTaskPage.jsx` - Placeholder with "Create Task" heading.
   - `EditTaskPage.jsx` - Placeholder with "Edit Task" heading and task ID.
   - `ChangePasswordPage.jsx` - Placeholder with "Change Password" heading.
7. Test routing:
   - Start dev server (`npm start` or `npm run dev`).
   - Navigate to each route manually and verify it renders without errors.
   - Verify route parameters work (e.g., `/tasks/123` shows task ID 123).

**Implementation hints:**
- See `docs/technology.md` section "4. Frontend Libraries" for specific library versions and implementation guidance.
- Use `react-router-dom` 6.20+ (latest API with `<Routes>`, `<Route>`, `<Navigate>`) per `docs/technology.md`.
- For TypeScript: use `.tsx` extensions, define route types if needed.
- Keep routes simple for now (no nested routes unless necessary).
- Use `useParams()` hook to get route parameters (e.g., task ID).
- Use `useNavigate()` hook for programmatic navigation (will be needed later).
- Place API client setup in `frontend/src/services/api.js` (will be implemented in task 10.3).

## Dependencies
- [ ] Task ID: 10.1 (Requirements analysis must be complete)

## Testing Instructions
- Run the development server (`npm start` or `npm run dev`) and manually navigate between placeholder routes:
  - `/login` - Should show "Login" placeholder.
  - `/tasks` - Should show "Task List" placeholder.
  - `/tasks/123` - Should show "Task Detail" placeholder with ID 123.
  - `/tasks/new` - Should show "Create Task" placeholder.
  - `/tasks/123/edit` - Should show "Edit Task" placeholder with ID 123.
  - `/change-password` - Should show "Change Password" placeholder.
- Verify no console errors when navigating.
- Verify route parameters are accessible (e.g., task ID in detail/edit pages).

## Security Review
- Ensure initial setup does not include vulnerable demo code or sample secrets.
- Remove any default demo API keys or secrets from template code.
- Ensure `.env` files are in `.gitignore` (if using environment variables).

## Risk Assessment
- Poor initial setup can slow down later UI work.
- Missing routes will require adding them later, disrupting workflow.

## Acceptance Criteria
- [ ] React project created with routing configured (`react-router-dom` installed and set up).
- [ ] Routes exist for all major views: `/login`, `/tasks`, `/tasks/:id`, `/tasks/new`, `/tasks/:id/edit`, `/change-password`.
- [ ] Each route has a corresponding stub page component (placeholder content is fine).
- [ ] Route parameters work (e.g., `/tasks/123` shows task ID 123 in component).
- [ ] Development server starts without errors.
- [ ] Navigation between routes works (no 404 errors).

## Definition of Done
- [ ] Project can be started via a single command (`npm start` or `npm run dev`).
- [ ] Router configured with all required routes.
- [ ] Stub page components created for each route.
- [ ] Base layout component created (if needed).
- [ ] Basic navigation between routes works (manual testing passes).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Navigating to the defined routes is possible without errors (all routes render placeholder content).
- **Observable Outcomes**: Dev server runs, routes are accessible, route parameters work, no console errors.

## Notes
Component content will be added in later tasks (10.4, 10.5, etc.). This task only sets up the routing skeleton.

## Strengths
Provides a skeleton for the entire frontend, making it easy to add component content incrementally.

## Sub-tasks (Children)
- [ ] Review frontend requirements from `docs/requirements.md` (views: login, task list, detail, create/edit, attachments, change password).
- [ ] Initialize React app (create-react-app, Vite, or Next.js) in `frontend/` directory.
- [ ] Install routing library (`react-router-dom` or framework routing).
- [ ] Set up project structure (components/, pages/, services/, utils/ directories).
- [ ] Configure router in `App.jsx` with all required routes.
- [ ] Create base layout component (if needed) with navigation structure.
- [ ] Create stub page components for each route (LoginPage, TaskListPage, TaskDetailPage, CreateTaskPage, EditTaskPage, ChangePasswordPage).
- [ ] Test routing manually (navigate to each route, verify it renders, check route parameters).

## Completed
[ ] Pending / [ ] Completed


