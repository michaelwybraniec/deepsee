# UI Smoke Tests

This directory contains end-to-end smoke tests for critical user flows.

## Required Test Flows

1. Login and change password
2. Viewing task list and detail
3. Creating and editing tasks
4. Managing attachments from the UI
5. Basic validation and error display

## Test Tools

UI smoke tests can be implemented using:
- **Playwright** (recommended for E2E testing)
- **Cypress** (alternative E2E testing framework)
- **React Testing Library** (for component-level testing)

## Status

⚠️ **Not yet implemented** - Tests should be added here to verify critical user flows work end-to-end.

## Running Tests

Once implemented, run with:
```bash
npm test
# or
playwright test
# or
cypress run
```
