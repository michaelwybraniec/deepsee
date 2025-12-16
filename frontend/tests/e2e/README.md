# UI Smoke Tests

This directory contains end-to-end smoke tests for critical user flows using Playwright.

## Test Coverage

### Authentication (`auth.spec.js`)
- ✅ Login with valid credentials
- ✅ Login error handling
- ✅ User registration and auto-login

### Task Management (`tasks.spec.js`)
- ✅ Display task list
- ✅ Create new task
- ✅ View task detail
- ✅ Search tasks
- ✅ Filter tasks by status

### Attachments (`attachments.spec.js`)
- ✅ Display attachments section
- ✅ Attachment upload UI (basic smoke test)

## Running Tests

```bash
# Run all E2E tests
npm run test:e2e

# Run with UI mode (interactive)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed

# Run specific test file
npx playwright test tests/e2e/auth.spec.js
```

## Prerequisites

1. Backend API running on `http://localhost:8000`
2. Frontend dev server running on `http://localhost:5173`
3. Test user created: `testuser` / `testpassword`

## Test User Setup

Before running tests, ensure a test user exists:
```bash
cd backend
.venv/bin/python3 scripts/create_user.py testuser test@example.com testpassword
```

## Configuration

Tests are configured in `playwright.config.js`:
- Base URL: `http://localhost:5173`
- Browser: Chromium
- Auto-starts dev server if not running
