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

### From Frontend Directory

```bash
cd frontend

# Run all E2E tests
npm run test:e2e

# Run with UI mode (interactive)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed

# Run specific test file
npx playwright test tests/e2e/auth.spec.js
```

### From Project Root

```bash
# Run all E2E tests
npm run test:e2e

# Run with UI mode (interactive)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed
```

**Note**: When running from the project root, use the npm scripts. If running Playwright directly, specify the config:
```bash
node frontend/node_modules/.bin/playwright test --config=frontend/playwright.config.js
```

## Prerequisites

1. Backend API running on `http://localhost:8000`
2. Frontend dev server running on `http://localhost:5173`
3. Test user created: `testuser` / `testpassword`

## Test User Setup

Before running tests, ensure a test user exists. You can use the setup script:

```bash
# From project root
./frontend/tests/e2e/setup-test-user.sh

# Or manually:
cd backend
.venv/bin/python3 scripts/create_user.py testuser test@example.com testpassword
```

**Note**: If the user already exists, the script will show a warning but tests should still work.

## Configuration

Tests are configured in `playwright.config.js`:
- Base URL: `http://localhost:5173` (configurable via `PLAYWRIGHT_BASE_URL` env var)
- Browser: Chromium
- Auto-starts dev server if not running
- Reuses existing dev server if already running on port 5173

### Configuration Details

The Playwright configuration ensures:
- `baseURL` is consistently applied across all test contexts
- The dev server is automatically detected and reused when running
- Tests can use relative URLs (e.g., `/login`, `/tasks`) which are resolved against the baseURL

### Troubleshooting

**Issue**: "Cannot navigate to invalid URL" errors
- **Solution**: Ensure you're running tests from the `frontend` directory or using the npm scripts from the root
- The config file must be found by Playwright - it looks for `playwright.config.js` in the current working directory

**Issue**: Tests fail because dev server isn't running
- **Solution**: The config will auto-start the dev server, but you can also start it manually with `npm run dev` in the frontend directory
