# Task Tracker

Full stack task management application with authentication, file attachments, search/filtering, background workers, and observability.

## Quick Start

### Docker

```bash
cp .env.example .env  # Set JWT_SECRET_KEY (min 32 chars)
npm run docker:init   # Clean start + auto-setup
```

**Auto-creates:** Test user (`testuser` / `testpassword`) + 50 sample tasks

**Access:** Frontend: <http://localhost:5173> | API: <http://localhost:8000> | Docs: <http://localhost:8000/docs>

### Manual

```bash
# Backend
npm run install:backend
npm run start:backend

# Frontend (new terminal)
npm run install:frontend
npm run start:frontend
```

## Architecture

```mermaid
graph TB
    subgraph Presentation["Presentation Layer"]
        Browser[Web Browser]
        React["React SPA<br/>Vite + Tailwind<br/>:5173"]
        
        Browser -->|HTTPS| React
    end
    
    subgraph Application["Application Layer"]
        Pages["Page Components<br/>Login, Tasks, Detail"]
        Components["UI Components<br/>Layout, Forms"]
        Services["API Client<br/>Axios + JWT"]
        State["State Management<br/>React Context"]
        
        React --> Pages
        Pages --> Components
        Pages --> Services
        Components --> State
    end
    
    subgraph API["API Gateway"]
        FastAPI["FastAPI Server<br/>:8000"]
        Middleware["Middleware<br/>Auth, Rate Limit, CORS"]
        Routes["REST Endpoints<br/>/api/auth, /api/tasks"]
        
        Services -->|REST API<br/>JWT Bearer| FastAPI
        FastAPI --> Middleware
        Middleware --> Routes
    end
    
    subgraph Business["Business Logic Layer"]
        UseCases["Use Cases<br/>Task CRUD, Auth"]
        Domain["Domain Models<br/>Task, User, Attachment"]
        
        Routes --> UseCases
        UseCases --> Domain
    end
    
    subgraph Infrastructure["Infrastructure Layer"]
        Repos["Repositories<br/>SQLAlchemy ORM"]
        Storage["File Storage<br/>Local Filesystem"]
        
        UseCases --> Repos
        UseCases --> Storage
    end
    
    subgraph Data["Data Persistence"]
        PostgreSQL[("PostgreSQL 15<br/>:5432<br/>Relational DB")]
        Redis[("Redis 7<br/>:6379<br/>In-Memory Cache<br/>Rate Limiting")]
        Files[("File System<br/>Docker Volume<br/>Attachments")]
        
        Repos -->|SQL<br/>SQLAlchemy| PostgreSQL
        Middleware -->|Rate Limit Cache| Redis
        Storage -->|File I/O| Files
    end
    
    subgraph Background["Background Processing"]
        Scheduler["APScheduler<br/>Cron Jobs"]
        Worker["Worker Service<br/>Reminder Notifications"]
        
        Scheduler --> Worker
        Worker -->|SQL Queries| PostgreSQL
    end
    
    subgraph Monitoring["Observability"]
        Prometheus["Prometheus<br/>:9090<br/>Metrics Collection"]
        Grafana["Grafana<br/>:3000<br/>Dashboards"]
        
        FastAPI -->|Prometheus Metrics| Prometheus
        Prometheus -->|Query API| Grafana
    end
    
    subgraph Engineering["Engineering Context"]
        AWP["AWP - Agentic Workflow Protocol<br/>Backlog, Context Engineering & MCP"]
        
        AWP -.->|Workflow Context| FastAPI
        AWP -.->|Workflow Context| React
    end
```

**Service Access:**

- **Frontend**: <http://localhost:5173>
- **API**: <http://localhost:8000> | **Docs**: <http://localhost:8000/docs>
- **Prometheus**: <http://localhost:9090>
- **Grafana**: <http://localhost:3000> (admin/admin)

See [Architecture Documentation](docs/architecture.md) for details.

## Scripts

**Docker:**

```bash
npm run docker:init    # Clean start + show credentials
npm run docker:up      # Start services
npm run docker:down    # Stop services
npm run docker:logs    # View logs
npm run docker:creds   # Show test user credentials
```

**Development:**

```bash
npm run start:backend   # Start backend
npm run start:frontend  # Start frontend
npm run install:backend # Setup backend
```

**Database:**

```bash
npm run seed           # Seed sample tasks
npm run user:create    # Create user (args: username email password)
npm run audit:query    # Query audit events
```

**Testing:**

```bash
npm run test:backend   # Backend tests
npm run test:e2e       # E2E tests
```

## Documentation

**Component READMEs:**

- **[Backend README](backend/README.md)** - Backend setup, scripts, and documentation index
- **[Frontend README](frontend/README.md)** - Frontend setup and development guide

**Core Documentation (`docs/`):**

- **[Architecture](docs/architecture.md)** - System design and Clean Architecture
- **[Docker Setup](docs/docker.md)** - Docker guide
- **[Requirements](docs/requirements.md)** - Original assignment
- **[Technology Stack](docs/technology.md)** - Technology decisions
- **[Self-Assessment](docs/self-assessment.md)** - Project review

**Backend Documentation (`backend/docs/`):**

- **[API Documentation](backend/docs/api.md)** - Swagger/OpenAPI endpoints
- **[Testing](backend/docs/testing.md)** - Testing guide
- **[Database Access](backend/docs/database-access.md)** - Database management
- See [Backend README](backend/README.md) for complete index

**Frontend Documentation (`frontend/docs/`):**

- **[E2E Tests](frontend/tests/e2e/README.md)** - Playwright test documentation
- See [Frontend README](frontend/README.md) for complete index

**Project Management (`agentic-sdlc/`):**

- **[AWP](agentic-sdlc/AWP.md)** - Agentic Workflow Protocol
- **[Project Backlog](agentic-sdlc/project-backlog.md)** - Task backlog

## Services & Endpoints

**Application:**

- Frontend: <http://localhost:5173>
- API: <http://localhost:8000>
- API Docs: <http://localhost:8000/docs>

**Observability:**

- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000> (admin/admin)
  - **Metrics**: Dashboards → Task Tracker - System Metrics
  - **Logs**: Drilldown → Logs (Loki data source)
- Loki: <http://localhost:3100> (log aggregation, internal)
- pgAdmin: <http://localhost:8888> (email: `admin`@`example.com` / password: `admin`)

## Key Features

- ✅ [Authentication & Authorization (JWT)](backend/docs/auth-design.md) - [Backend](backend/docs/auth-design.md) | [Authorization](backend/docs/authorization.md) | [Frontend](frontend/docs/authentication.md)
- ✅ [Task Management (CRUD with ownership)](backend/docs/task-model.md) - [Backend](backend/docs/task-model.md) | [Frontend](frontend/docs/task-management.md)
- ✅ [File Attachments](backend/docs/attachments.md) - [Backend](backend/docs/attachments.md) | [Frontend](frontend/docs/attachments.md)
- ✅ [Search & Filtering](backend/docs/search-filter-api-design.md) (title, status, priority, tags, due date) - [Backend](backend/docs/search-filter-api-design.md) | [Frontend](frontend/docs/search-filtering.md)
- ✅ [Background Worker (reminder notifications)](backend/docs/worker.md) - [Backend](backend/docs/worker.md)
- ✅ [Audit Trail](backend/docs/audit.md) - [Backend](backend/docs/audit.md)
- ✅ [Rate Limiting](backend/docs/rate-limiting-design.md) - [Backend](backend/docs/rate-limiting-design.md)
- ✅ [Monitoring & Observability](backend/docs/monitoring-usage.md) (Prometheus + Grafana + Loki) - [Monitoring](backend/docs/monitoring-usage.md) | [Grafana](backend/docs/grafana.md) | [Logs](backend/docs/loki-logs.md)
- ✅ [Comprehensive Testing](backend/docs/testing.md) (68 backend + 10 E2E tests) - [Backend](backend/docs/testing.md) | [Frontend E2E](frontend/tests/e2e/README.md)

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React 19, Vite, Tailwind CSS
- **Infrastructure**: Docker Compose, Redis, Prometheus, Grafana, Loki
- **Testing**: Pytest, Playwright

See [Technology Stack](docs/technology.md) for detailed decisions.

## Project Status

All 11 core tasks + 3 unplanned enhancements complete. See [Project Backlog](agentic-sdlc/project-backlog.md) for details.
