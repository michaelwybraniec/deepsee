# Task ID: 10.3
# Title: Implement auth-related frontend flows
# Status: [x] In Progress
# Priority: high
# Owner: Frontend Dev
# Estimated Effort: 4h

## Description
Implement the login and change-password pages and connect them to the backend authentication endpoints, per `docs/requirements.md` section "10. Front-End" and `docs/technical-specs.md` section "3.10 Front‑End".

**Step-by-step:**
1. Review frontend requirements from task 10.1 (login page, change password page).
2. Create API client for authentication:
   - Create `frontend/src/services/authApi.js`:
     - `login(username, password)` - calls `POST /api/auth/login`, returns token and user info.
     - `changePassword(currentPassword, newPassword)` - calls `POST /api/auth/change-password`.
     - Handle errors (return error message from backend).
3. Implement authentication state management:
   - Create auth context/store (React Context, Redux, or Zustand):
     - Store: `token`, `user`, `isAuthenticated`.
     - Actions: `login(token, user)`, `logout()`, `setUser(user)`.
   - Store token in localStorage or sessionStorage (secure storage).
   - Add auth guard for protected routes (redirect to login if not authenticated).
4. Implement login page:
   - Create `LoginPage.jsx` component:
     - Form with `username` (or email) and `password` fields.
     - Submit handler: call `authApi.login()`, on success: store token, update auth state, redirect to task list.
     - On error: display error message (toast/alert or inline).
     - Client-side validation: required fields, format validation.
5. Implement change-password page:
   - Create `ChangePasswordPage.jsx` component:
     - Form with `currentPassword` and `newPassword` fields (and `confirmPassword` if needed).
     - Submit handler: call `authApi.changePassword()`, on success: show success toast, redirect or clear form.
     - On error: display error message (toast/alert or inline).
     - Client-side validation: required fields, password strength, password match.
6. Add API request interceptor:
   - Add token to request headers (e.g., `Authorization: Bearer {token}`).
   - Handle 401 errors (token expired/invalid): logout user, redirect to login.
7. Write UI smoke tests:
   - Test successful login (enter credentials, submit, verify redirect to task list, token stored).
   - Test failed login (enter invalid credentials, submit, verify error message displayed).
   - Test change password (enter passwords, submit, verify success toast, password changed).
   - Test change password error (enter wrong current password, submit, verify error message).

**Implementation hints:**
- Use React Context or state management library (Redux, Zustand) for auth state.
- Use `axios` or `fetch` for API calls with interceptors for token handling.
- Store token securely (localStorage or httpOnly cookie - localStorage is simpler for SPA).
- Use React Router for navigation (redirect after login, protect routes).

## Dependencies
- [ ] Task ID: 2.3 (Login endpoint must exist)
- [ ] Task ID: 2.4 (Change-password endpoint must exist)
- [ ] Task ID: 10.2 (React project and routing must be set up)

## Testing Instructions
- UI smoke tests:
  - Successful login updates app state (verify token stored, user info stored, isAuthenticated=true, redirect to task list).
  - Change-password flow works end-to-end (enter passwords, submit, verify success toast, password changed, can login with new password).
  - Error messages appear on invalid credentials or invalid password change (verify error message displayed, form not submitted).
- Manual test: Use browser to login and change password, verify behavior.

## Security Review
- Ensure tokens/credentials are handled securely on the client:
  - Store token in localStorage or sessionStorage (not in global variables).
  - Don't log tokens or passwords in console.
  - Use HTTPS for API calls (backend should enforce this).
  - Clear token on logout.

## Risk Assessment
- Broken auth flows will block users from using the app.
- Missing error handling can leave users confused.
- Token storage issues can cause authentication problems.

## Acceptance Criteria
- [ ] Login page calls backend login endpoint and handles success/failure (API call works, token stored on success, error displayed on failure).
- [ ] Change-password page calls backend endpoint and handles success/failure (API call works, success toast on success, error displayed on failure).
- [ ] Authentication state management implemented (token stored, auth state updated, protected routes guarded).
- [ ] Client-side validation implemented (required fields, format validation).
- [ ] Basic UI smoke tests for these flows are passing (all test cases pass).

## Definition of Done
- [ ] Auth-related pages implemented and wired (login page, change-password page, API client, auth state management).
- [ ] Login page implemented (form, API call, token storage, redirect, error handling).
- [ ] Change-password page implemented (form, API call, success/error handling).
- [ ] Authentication state management implemented (context/store, token storage, auth guard).
- [ ] Tests added and passing (login success/failure, change password success/failure).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: UI tests confirm working login and password change flows (all test cases pass).
- **Observable Outcomes**: Login and change password work in browser, token stored, auth state updated, errors displayed.

## Notes
Fulfills the frontend side of "Secure Login" and "Change password functionality". This task implements the UI for authentication flows.

## Strengths
Enables end users to authenticate and manage their credentials. Provides secure authentication UI.

## Sub-tasks (Children)
- [ ] Review frontend requirements from task 10.1 (login page, change password page).
- [ ] Create API client for authentication (login, changePassword methods, error handling).
- [ ] Implement authentication state management (context/store, token storage, auth guard).
- [ ] Implement login page (form, API call, token storage, redirect, error handling, validation).
- [ ] Implement change-password page (form, API call, success/error handling, validation).
- [ ] Add API request interceptor (add token to headers, handle 401 errors).
- [ ] Write UI smoke tests (login success/failure, change password success/failure).
- [ ] Test manually by logging in and changing password in browser.

## Completed
[ ] Pending / [ ] Completed


