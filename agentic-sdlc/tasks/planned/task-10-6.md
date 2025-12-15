# Task ID: 10.6
# Title: Implement validation, error handling, and toasts/alerts
# Status: [ ] Pending
# Priority: high
# Owner: Frontend Dev
# Estimated Effort: 4h

## Description
Implement client-side validation for forms, user-friendly error messages, and toasts/alerts for success and failure of key actions, per `docs/requirements.md` section "10. Front-End" and `docs/technical-specs.md` section "3.10 Front‑End".

**Step-by-step:**
1. Review frontend requirements from task 10.1 (client-side validation, user-friendly error handling, toasts/alerts).
2. Implement global toast/alert component:
   - Create `Toast.jsx` or use toast library (e.g., `react-toastify`, `react-hot-toast`):
     - Toast types: success, error, warning, info.
     - Toast position: top-right, bottom-right, etc.
     - Auto-dismiss after timeout (e.g., 3-5 seconds).
     - Manual dismiss button (optional).
   - Create toast context/store (React Context or state management):
     - Actions: `showSuccess(message)`, `showError(message)`, `showWarning(message)`, `showInfo(message)`.
3. Add validation rules to forms:
   - **Login form**: username/email (required, email format if email), password (required, min length).
   - **Change password form**: current password (required), new password (required, min length, strength), confirm password (required, matches new password).
   - **Task form**: title (required, non-empty), description (optional), status (enum validation), priority (enum validation), due_date (date format), tags (array validation).
   - **Attachment upload**: file (required, size limit, file type if restricted).
4. Implement inline validation messages:
   - Show validation errors below form fields (on blur or on submit).
   - Highlight invalid fields (red border, error icon).
   - Show error messages from backend (API errors) in addition to client-side validation.
5. Integrate toasts/alerts into main flows:
   - **Login**: success toast on login, error toast on failure.
   - **Change password**: success toast on success, error toast on failure.
   - **Task CRUD**: success toast on create/update/delete, error toast on failure.
   - **Attachments**: success toast on upload/delete, error toast on failure.
6. Implement error handling:
   - Parse backend error responses (extract error message from API response).
   - Display user-friendly error messages (not raw API errors, e.g., "Invalid credentials" instead of "401 Unauthorized").
   - Handle network errors (show "Network error. Please try again.").
   - Handle validation errors (show field-specific errors from backend).
7. Write UI tests or manual checks:
   - Test invalid input shows inline validation messages (enter invalid data, verify error messages appear).
   - Test successful operations show success toasts/alerts (perform action, verify success toast appears).
   - Test failed operations show clear error toasts/alerts (trigger error, verify error toast appears with clear message).

**Implementation hints:**
- Use form validation library (React Hook Form with validation, Formik with Yup, or custom validation).
- Use toast library (`react-toastify`, `react-hot-toast`) for toasts/alerts.
- Create reusable validation functions (e.g., `validateEmail`, `validateRequired`, `validateDate`).
- Create error message mapping (map API error codes to user-friendly messages).

## Dependencies
- [ ] Task ID: 10.3 (Auth pages must exist)
- [ ] Task ID: 10.4 (Task views must exist)
- [ ] Task ID: 10.5 (Attachments UI must exist)

## Testing Instructions
- UI tests or manual checks:
  - Invalid input shows inline validation messages (enter invalid data, verify error messages appear below fields).
  - Successful operations show success toasts/alerts (perform action, verify success toast appears and dismisses).
  - Failed operations show clear error toasts/alerts (trigger error, verify error toast appears with clear message).
  - Test validation on different forms (login, change password, task form, attachment upload).
- Manual test: Use browser to test validation and toasts, verify behavior.

## Security Review
- Ensure client-side validation complements, but does not replace, server-side validation:
  - Client-side validation is for UX (immediate feedback), not security.
  - Always validate on backend (never trust client-side validation alone).
  - Don't expose sensitive validation rules in client code.

## Risk Assessment
- Poor validation and feedback can harm user experience and hide issues.
- Missing error handling can leave users confused.
- Inconsistent validation messages can confuse users.

## Acceptance Criteria
- [ ] Client-side validation implemented for main forms (auth, tasks, attachments) with appropriate rules (required fields, format validation, enum validation).
- [ ] Inline error messages and toasts/alerts are shown appropriately (errors below fields, toasts for success/failure).
- [ ] Error messages are user-friendly (not raw API errors, clear and actionable).
- [ ] Basic tests or scripted checks for validation and toast behavior are in place (validation works, toasts appear).

## Definition of Done
- [ ] Validation, error handling, and feedback implemented across main flows (all forms have validation, all actions show toasts).
- [ ] Global toast/alert component implemented (toast library or custom component, context/store).
- [ ] Validation rules added to all forms (login, change password, task form, attachment upload).
- [ ] Inline validation messages implemented (errors below fields, field highlighting).
- [ ] Toasts/alerts integrated into all main flows (login, change password, task CRUD, attachments).
- [ ] Error handling implemented (parse backend errors, show user-friendly messages).
- [ ] Tests/checks added and passing (validation works, toasts appear, error handling works).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: UI tests or manual QA confirm validation and feedback behave as expected (all test cases pass).
- **Observable Outcomes**: Validation works in browser, toasts appear, error messages are clear.

## Notes
Fulfills client-side validation and "Show toasts or alerts for success/failure" requirements. This task enhances UX across all frontend flows.

## Strengths
Provides a modern, user-friendly UX aligned with the assignment brief. Improves user experience with clear feedback.

## Sub-tasks (Children)
- [ ] Review frontend requirements from task 10.1 (validation, error handling, toasts/alerts).
- [ ] Implement global toast/alert component (toast library or custom component, context/store, actions).
- [ ] Add validation rules to forms (login, change password, task form, attachment upload - required fields, format, enum validation).
- [ ] Implement inline validation messages (errors below fields, field highlighting, error icons).
- [ ] Integrate toasts/alerts into main flows (login, change password, task CRUD, attachments - success/error toasts).
- [ ] Implement error handling (parse backend errors, map to user-friendly messages, handle network errors).
- [ ] Write UI tests or manual checks (validation works, toasts appear, error handling works).
- [ ] Test manually by testing validation and toasts in browser.

## Completed
[ ] Pending / [ ] Completed


