# Task Tracker – Technical Assessment

This repository contains the implementation of the Task Tracker application for the Full Stack Developer technical assessment.

## 📋 Quick Links

### 🚀 Services & Endpoints

**Application Services:**
- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

**Observability Services:**
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (default: `admin` / `admin`)
- **API Metrics**: http://localhost:8000/api/metrics
- **Health Check (API)**: http://localhost:8000/api/health/api
- **Health Check (Database)**: http://localhost:8000/api/health/database
- **Health Check (Worker)**: http://localhost:8000/api/health/worker

**Infrastructure Services:**
- **PostgreSQL Database**: `localhost:5432`
- **Redis**: `localhost:6379`

### 📚 Documentation

#### Core Documentation (`docs/`)
- **[Requirements](docs/requirements.md)** - Original assignment (source of truth)
- **[Technical Specs](docs/technical-specs.md)** - Structured restatement of requirements
- **[Architecture](docs/architecture.md)** - System architecture, design patterns, and rationale
- **[Technology Stack](docs/technology.md)** - Technology decisions and rationale
- **[Self-Assessment](docs/self-assessment.md)** - Completion status, design choices, and trade-offs
- **[Suggestions](docs/suggestions.md)** - Optional best practices
- **[Unplanned Tasks Analysis](docs/unplanned-tasks-analysis.md)** - Analysis of unplanned enhancements

#### Backend Documentation (`backend/docs/`)
- **[API Documentation](backend/docs/api-documentation.md)** - Swagger/OpenAPI usage guide
- **[API Endpoints Summary](backend/docs/api-endpoints-summary.md)** - Complete API reference
- **[Swagger Auth Guide](backend/docs/swagger-auth-guide.md)** - How to authenticate in Swagger UI
- **[Quick Start](backend/docs/quick-start.md)** - Backend setup guide
- **[Database Access](backend/docs/database-access.md)** - Database connection and query examples
- **[Testing](backend/docs/testing.md)** - Backend testing guide

**Feature-Specific Documentation:**
- **[Authentication Requirements](backend/docs/auth-requirements.md)** - Auth design and implementation
- **[Authorization](backend/docs/authorization.md)** - Authorization guards and permissions
- **[Task Model](backend/docs/task-model.md)** - Task data model design
- **[Task Fields](backend/docs/task-fields.md)** - Task field specifications
- **[Attachment Requirements](backend/docs/attachment-requirements.md)** - Attachment feature design
- **[Attachment Design](backend/docs/attachment-design.md)** - Attachment storage and metadata
- **[Search & Filter Requirements](backend/docs/search-filter-requirements.md)** - Search/filter design
- **[Search & Filter API Design](backend/docs/search-filter-api-design.md)** - API design for search/filter
- **[Tag Filtering (Partial Match)](backend/docs/tag-filtering-partial-match.md)** - Tag matching implementation
- **[Audit Trail Requirements](backend/docs/audit-trail-requirements.md)** - Audit logging design
- **[Audit Schema Design](backend/docs/audit-schema-design.md)** - Audit event schema
- **[Audit Trail Usage](backend/docs/audit-trail-usage.md)** - How to query audit events
- **[Rate Limiting Requirements](backend/docs/rate-limiting-requirements.md)** - Rate limiting design
- **[Rate Limiting Design](backend/docs/rate-limiting-design.md)** - Rate limiting implementation
- **[Monitoring & Logging Requirements](backend/docs/monitoring-logging-requirements.md)** - Observability design
- **[Monitoring Usage](backend/docs/monitoring-usage.md)** - How to access logs and metrics
- **[Prometheus & Grafana Usage](backend/docs/prometheus-grafana-usage.md)** - Observability dashboards guide
- **[Notification Requirements](backend/docs/notification-requirements.md)** - Reminder worker design
- **[Worker Design](backend/docs/worker-design.md)** - Background worker architecture
- **[Worker Usage](backend/docs/worker-usage.md)** - How to use and test the worker

#### Frontend Documentation
- **[E2E Tests README](frontend/tests/e2e/README.md)** - Playwright E2E test documentation

#### Project Management (`agentic-sdlc/`)
- **[AWP (Agentic Workflow Protocol)](agentic-sdlc/AWP.md)** - Workflow protocol for task management
- **[Project Backlog](agentic-sdlc/project-backlog.md)** - Main backlog index with all tasks
- **[Backlog README](agentic-sdlc/README.md)** - Backlog structure and usage guide

## 🚀 Getting Started

### Option 1: Docker Compose (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed

**Steps:**
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and set your values (especially `JWT_SECRET_KEY` with at least 32 characters)
3. Start all services:
   ```bash
   docker compose up
   ```
4. Access the application:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs (Swagger UI)
   - **ReDoc**: http://localhost:8000/redoc
   - **Prometheus**: http://localhost:9090
   - **Grafana**: http://localhost:3000 (default: `admin` / `admin`)

**Services:**
- `api` - Backend API (port 8000)
- `worker` - Background worker for reminders
- `database` - PostgreSQL database (port 5432)
- `redis` - Redis for rate limiting (port 6379)
- `frontend` - React frontend (port 5173)
- `prometheus` - Metrics collection (port 9090)
- `grafana` - Metrics visualization (port 3000)

**Stop services:**
```bash
docker compose down
```

**Stop and remove volumes (clean slate):**
```bash
docker compose down -v
```

### Option 2: Manual Setup

**Start Backend:**
```bash
npm run start:backend
```
Or manually:
```bash
cd backend
source .venv/bin/activate  # On macOS/Linux
uvicorn api.main:app --reload
```

**Start Frontend:**
```bash
npm run start:frontend
```
Or manually:
```bash
cd frontend
npm run dev
```

**Start Both (requires two terminals):**
```bash
# Terminal 1 - Backend
npm run start:backend

# Terminal 2 - Frontend  
npm run start:frontend
```

The backend will be available at **http://localhost:8000** and the frontend at **http://localhost:5173**.

## 🧪 Running Tests

**Backend Tests:**
```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

**E2E Tests (Playwright):**
```bash
# Run all E2E tests
npm run test:e2e

# Run with UI mode (interactive)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed
```

**Prerequisites for E2E tests:**
- Backend API running on `http://localhost:8000`
- Test user created: `testuser` / `testpassword`
- See [frontend/tests/e2e/README.md](frontend/tests/e2e/README.md) for detailed test documentation

## 📖 Documentation Structure

### Core Documentation (`docs/`)
```text
docs/
├── requirements.md              # Original assignment (source of truth)
├── technical-specs.md           # Structured restatement of requirements
├── architecture.md              # System architecture & design
├── technology.md                # Technology decisions & rationale
├── self-assessment.md           # Completion status & design choices
├── unplanned-tasks-analysis.md  # Unplanned enhancements analysis
└── suggestions.md               # Optional best practices
```

### Backend Documentation (`backend/docs/`)
```text
backend/docs/
├── README.md                    # Backend documentation index
├── api-documentation.md         # Swagger/OpenAPI usage
├── api-endpoints-summary.md     # Complete API reference
├── quick-start.md               # Backend setup guide
├── database-access.md           # Database connection examples
├── testing.md                   # Backend testing guide
├── auth-requirements.md         # Authentication design
├── authorization.md             # Authorization implementation
├── task-model.md                # Task data model
├── attachment-requirements.md   # Attachment design
├── search-filter-requirements.md # Search/filter design
├── audit-trail-requirements.md  # Audit logging design
├── rate-limiting-requirements.md # Rate limiting design
├── monitoring-usage.md          # Logs and metrics access
├── prometheus-grafana-usage.md  # Observability dashboards
└── worker-usage.md              # Background worker usage
```

### Project Management (`agentic-sdlc/`)
```text
agentic-sdlc/
├── AWP.md                       # Agentic Workflow Protocol
├── project-backlog.md           # Main backlog index
├── README.md                    # Backlog structure guide
└── tasks/
    ├── planned/                 # Planned task files
    └── unplanned/               # Unplanned task files
```

**Documentation Flow**:
```text
requirements.md (source)
    ↓
technical-specs.md (structured)
    ↓
architecture.md (design)
    ↓
technology.md (decisions)
    ↓
tasks/ (implementation)
```

## 🔍 Key Features

- ✅ **Authentication & Authorization**: JWT-based auth with password hashing
- ✅ **Task Management**: Full CRUD operations with ownership
- ✅ **Attachments**: File upload/download with metadata
- ✅ **Search & Filtering**: Title/description search, status/priority/tags/due date filters
- ✅ **Sorting & Pagination**: Multiple sort options with pagination
- ✅ **Background Worker**: Automated reminder notifications for due tasks
- ✅ **Audit Trail**: Complete audit logging for all operations
- ✅ **Rate Limiting**: Redis-based rate limiting
- ✅ **Monitoring**: Structured logging, metrics, health checks
- ✅ **Observability**: Prometheus + Grafana dashboards
- ✅ **Testing**: Unit, integration, worker, contract, observability, and E2E tests

## 🏗️ Architecture

The application follows **Clean Architecture** principles:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and business rules
- **Infrastructure Layer**: Database, storage, external services
- **API Layer**: FastAPI routes and middleware

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL/SQLite
- **Frontend**: React 19, Vite, Tailwind CSS, React Router
- **Worker**: Python background scheduler
- **Database**: PostgreSQL (production) / SQLite (development)
- **Cache/Rate Limiting**: Redis
- **Observability**: Prometheus, Grafana
- **Testing**: Pytest, Playwright

See [docs/technology.md](docs/technology.md) for detailed technology decisions.

## 📊 Project Status

**All Tasks Complete:**
- ✅ Task 1: Project environment and documentation
- ✅ Task 2: Secure login and authorization
- ✅ Task 3: Task management API (CRUD)
- ✅ Task 4: Attachments API
- ✅ Task 5: Search, filtering, sorting, pagination
- ✅ Task 6: Notifications worker for due tasks
- ✅ Task 7: Audit trail implementation
- ✅ Task 8: Rate limiting
- ✅ Task 9: Monitoring, logging, health checks
- ✅ Task 10: React frontend
- ✅ Task 11: Testing and self-assessment

**Unplanned Enhancements:**
- ✅ U-1: Prometheus + Grafana observability dashboards
- ✅ U-2: Partial/substring tag matching in search
- ✅ U-3: UI smoke tests (E2E tests)

**Test Coverage:**
- ✅ 68 backend tests (unit, integration, worker, contract, observability)
- ✅ 10 frontend E2E tests (Playwright)

See [agentic-sdlc/project-backlog.md](agentic-sdlc/project-backlog.md) for complete task list.

## 📝 Project Backlog & Workflow

This project uses an **Agentic SDLC** approach with a structured backlog and workflow protocol:

- **Backlog**: See [agentic-sdlc/project-backlog.md](agentic-sdlc/project-backlog.md) for all planned tasks
- **Workflow**: See [agentic-sdlc/AWP.md](agentic-sdlc/AWP.md) for the Agentic Workflow Protocol (AWP)
- **Task details**: Individual task files in `agentic-sdlc/tasks/planned/` contain step-by-step implementation instructions

Tasks are organized hierarchically and follow the AWP workflow (`awp check`, `awp update`, `awp commit`, `awp next`, `awp handoff`) for consistent progress tracking and structured task management.

## 🔐 Default Credentials

**Grafana:**
- Username: `admin`
- Password: `admin` (change in production via `GRAFANA_PASSWORD` env var)

**Test User (for E2E tests):**
- Username: `testuser`
- Password: `testpassword`

Create test user:
```bash
cd backend
.venv/bin/python3 scripts/create_user.py testuser test@example.com testpassword
```

## 📞 Support & Resources

- **API Documentation**: http://localhost:8000/docs (when API is running)
- **Backend README**: [backend/README.md](backend/README.md)
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **Self-Assessment**: [docs/self-assessment.md](docs/self-assessment.md) - Complete project review
