# Task Tracker Frontend

React frontend for the Task Tracker application, built with Vite.

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running (default: `http://localhost:8000`)

### Installation

```bash
cd frontend
npm install
```

### Development Server

Start the development server:

```bash
npm run dev
```

The frontend will be available at **http://localhost:5173** (Vite default port).

### Configuration

The frontend connects to the backend API. By default, it expects the API at `http://localhost:8000`.

To change the API base URL, create a `.env` file in the `frontend/` directory:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

Or set it when running:

```bash
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run test:e2e` - Run E2E tests (Playwright)
- `npm run test:e2e:ui` - Run E2E tests with UI mode
- `npm run test:e2e:headed` - Run E2E tests in headed mode

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components (Layout, ProtectedRoute, etc.)
│   ├── contexts/       # React contexts (AuthContext)
│   ├── pages/          # Page components (Login, Register, Tasks, etc.)
│   └── services/       # API clients (api.js, taskApi.js, attachmentApi.js)
├── tests/
│   └── e2e/            # Playwright E2E tests
├── docs/               # Frontend documentation
├── public/             # Static assets (favicon, etc.)
├── dist/               # Production build output
├── tailwind.config.js  # Tailwind CSS configuration
├── vite.config.js      # Vite configuration
└── playwright.config.js # Playwright E2E test configuration
```

## Features

- **Authentication**: Login and change password
- **Task Management**: Create, view, edit, and delete tasks
- **Attachments**: Upload and manage file attachments
- **Validation**: Client-side form validation
- **Toasts**: Success and error notifications
- **Routing**: React Router with protected routes

## Development

### First Time Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Ensure backend is running:
   ```bash
   # In backend directory
   cd ../backend
   source .venv/bin/activate
   uvicorn api.main:app --reload
   ```

3. Start frontend:
   ```bash
   # In frontend directory
   npm run dev
   ```

4. Open browser:
   - Frontend: http://localhost:5173
   - Backend API docs: http://localhost:8000/docs

### Creating a User

Before logging in, create a user account:

```bash
cd ../backend
.venv/bin/python3 scripts/create_user.py
```

## Technology Stack

- **React 19+**: UI framework
- **Vite 7+**: Build tool and dev server
- **React Router 6.20+**: Routing
- **Axios 1.6+**: HTTP client
- **Tailwind CSS 3.4+**: Utility-first CSS framework
- **Sonner 2.0+**: Toast notifications
- **Playwright 1.57+**: E2E testing framework

## Testing

### E2E Tests (Playwright)

**Prerequisites:**
- Backend API running on `http://localhost:8000`
- Test user created: `testuser` / `testpassword`
- Frontend dev server running (or Playwright will start it automatically)

**Run Tests:**
```bash
# Run all E2E tests
npm run test:e2e

# Run with interactive UI mode
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed
```

**Test Coverage:**
- Authentication (login, invalid credentials, registration)
- Task management (list, create, view detail, search, filter)
- Attachments (upload, display)

See [tests/e2e/README.md](tests/e2e/README.md) for detailed test documentation.

## Quick Reference

**Start Development Server:**
```bash
npm run dev
```

**Build for Production:**
```bash
npm run build
```

**Run E2E Tests:**
```bash
npm run test:e2e
```

**Access Application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Related Documentation

- [Frontend Requirements](docs/frontend-requirements.md) - Detailed requirements
- [Task 10 Review](docs/task-10-review.md) - Frontend implementation review
- [E2E Tests README](tests/e2e/README.md) - Playwright E2E test documentation
- [Backend API Documentation](../backend/docs/README.md) - Backend API docs
- [Backend API Endpoints Summary](../backend/docs/api-endpoints-summary.md) - Complete API reference
