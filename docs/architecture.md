# Architecture – Task Tracker

This document describes the planned architecture for the Task Tracker application, based on:

- The assignment in `docs/requirements.md`
- The structured view in `docs/technical-specs.md`
- Technology choices documented in `docs/technology.md`

Where this document goes beyond those files, items are clearly marked as **Design Choice**. For specific technology, library, and version decisions, see `docs/technology.md`.

---

## Table of Contents

- [Architecture – Task Tracker](#architecture--task-tracker)
  - [Table of Contents](#table-of-contents)
  - [1. Context \& Goals](#1-context--goals)
  - [2. High‑Level System Components](#2-highlevel-system-components)
  - [3. Logical Layering (Clean Architecture)](#3-logical-layering-clean-architecture)
  - [4. Cross‑Cutting Concerns](#4-crosscutting-concerns)
  - [5. Test Strategy (Per Requirements)](#5-test-strategy-per-requirements)
  - [6. Architecture Rationale](#6-architecture-rationale)
    - [6.1 Clean Architecture Approach](#61-clean-architecture-approach)
    - [6.2 Technology Choices](#62-technology-choices)
    - [6.3 Design Patterns Used](#63-design-patterns-used)
    - [6.4 Trade-offs Made](#64-trade-offs-made)
  - [7. Summary](#7-summary)
  - [8. Architecture Charts (Text Diagrams)](#8-architecture-charts-text-diagrams)
    - [8.1 High‑Level Components](#81-highlevel-components)
    - [8.2 Request \& Logging Flow (Example)](#82-request--logging-flow-example)
    - [8.3 Reminder Worker Flow (Example)](#83-reminder-worker-flow-example)

---

## 1. Context & Goals

- Full‑stack Task Tracker application where users:
  - Log in.
  - Create, view, edit, delete tasks.
  - Attach files.
  - Receive reminders for tasks due in the next 24 hours.
  - Monitor their activity.
- System must provide:
  - Backend service.
  - Front‑end.
  - Basic observability (logging, metrics, health checks).
- Non‑functional expectations:
  - Clean Architecture, maintainable code, clear design decisions.
  - AI‑assisted development (Cursor, Copilot, Claude, etc.).

---

## 2. High‑Level System Components

From the requirements, the system will contain at least:

- **Frontend (React UI)**:
  - Handles login and task management.
  - Provides views for:
    - Task list.
    - Task detail.
    - Create/edit task.
    - Attachments section.
  - Displays:
    - Client‑side validation errors.
    - Toasts/alerts for success and failure.
  - Exposes change‑password functionality.
  - See `docs/technology.md` for specific React setup, routing, and library choices.

- **Backend API service (Python)**:
  - Exposes endpoints for:
    - Secure login (OIDC/OAuth2 or JWT‑based).
    - Task management (CRUD with required fields).
    - Attachments (upload, list, delete).
    - Search, filtering, sorting, pagination of tasks.
  - See `docs/technology.md` for specific Python framework, ORM, and library choices.
    - Change password.
  - Enforces:
    - “User can modify only their own data, but can view all records.”
    - Per‑user or per‑IP rate limiting.
  - Provides:
    - Structured logging with correlation IDs.
    - Basic metrics (request count, error rate, latency, reminders processed).
    - Health check endpoints (API, database, worker).
  - Implements centralized exception handling and consistent error responses.

- **Background worker / service**:
  - Periodically checks for tasks due in the next 24 hours.
  - Logs “reminder sent” events.
  - Is idempotent and fault‑tolerant (no duplicate reminders).
  - Retries failed jobs and handles restarts gracefully.

- **Database**:
  - Stores:
    - Users.
    - Tasks with their fields (title, description, status, priority, due date, tags).
    - Attachments metadata (at least name and size, plus any storage reference as a design choice).
    - Audit trail events (task creation, update, attachment added/removed, reminder sent) with timestamps and user IDs.

> **Design Choice**: Exact database technology, schema details, and attachment storage mechanism are not specified in the requirements and can be selected to fit the stack and time constraints.

---

## 3. Logical Layering (Clean Architecture)

To align with the requirement for Clean Architecture, the backend will be organized into logical layers:

- **Domain layer**:
  - Contains core business concepts and rules for:
    - Users.
    - Tasks.
    - Attachments.
    - Audit events.
    - Reminder logic.

- **Application layer (use‑cases)**:
  - Coordinates operations such as:
    - Creating, viewing, updating, deleting tasks.
    - Managing attachments for tasks.
    - Searching and filtering tasks.
    - Running reminder checks and logging “reminder sent” events.
  - Depends on interfaces for persistence, messaging, and external services.

- **Infrastructure layer**:
  - Implements:
    - Data access (database).
    - Attachment storage.
    - Logging, metrics, rate limiting.
    - Background job scheduling and execution.

- **Interface / presentation layer**:
  - Backend HTTP API controllers/routers.
  - Worker entry points.
  - Frontend React components.

> **Design Choice**: The exact folder/module layout and naming inside these layers are not prescribed by the requirements and can follow common Clean Architecture patterns.

---

## 4. Cross‑Cutting Concerns

These concerns apply across multiple components:

- **Authentication & Authorization**:
  - Modern authentication using OIDC/OAuth2 or JWT.
  - Authorization rules to ensure users modify only their own data.

- **Rate Limiting**:
  - Basic per‑user or per‑IP limits applied at the API boundary.
  - Meaningful error responses when limits are exceeded.

- **Logging & Correlation IDs**:
  - Structured logs with a correlation ID generated or propagated per request.
  - Correlation ID propagated into worker operations where applicable.

- **Metrics & Health Checks**:
  - Metrics for:
    - Request count.
    - Error rate.
    - Latency.
    - Reminders processed.
  - Health endpoints to verify:
    - API is reachable.
    - Database connectivity.
    - Worker/queue is operational.

- **Error Handling & Resilience**:
  - Centralized exception handling in the API.
  - Consistent error response shape (as a design choice).
  - Worker retry and restart strategies to avoid duplicate reminders.

> **Design Choice**: The specific logging/metrics libraries, rate limiting strategy, and retry mechanisms are not fixed by the requirements and can be chosen based on familiarity and ecosystem support. See `docs/technology.md` for specific library choices and rationale.

---

## 5. Test Strategy (Per Requirements)

The architecture must support the following test types:

- **Unit tests**:
  - Focused on individual functions, classes, and domain rules.

- **Integration tests (API + DB)**:
  - Exercise API endpoints together with the database.

- **Worker/queue tests**:
  - Cover reminder scheduling/processing and idempotency behavior.

- **Contract/API documentation tests**:
  - Ensure that the implemented API matches the Swagger/OpenAPI documentation.

- **Observability/health checks tests**:
  - Validate health endpoints and presence of basic metrics.

- **UI smoke tests**:
  - Verify that key flows (login, task list, basic CRUD) work end‑to‑end.

> **Design Choice**: Choice of test frameworks and test organization is left open by the requirements.

---

## 6. Architecture Rationale

### 6.1 Clean Architecture Approach

**Why Clean Architecture?**

- **Separation of Concerns**: Business logic is independent of frameworks, databases, and external services
- **Testability**: Domain and application layers can be tested without infrastructure dependencies
- **Maintainability**: Changes to infrastructure (e.g., switching databases) don't affect business logic
- **Flexibility**: Easy to swap implementations (e.g., different storage backends, different ORMs)

**How Layers Are Organized:**

- **Domain Layer** (`domain/`): Pure business logic, no dependencies on external libraries
- **Application Layer** (`application/`): Use cases that orchestrate domain logic, depends on domain interfaces
- **Infrastructure Layer** (`infrastructure/`): Concrete implementations (database, storage, logging)
- **Interface Layer** (`api/`, `worker/`): HTTP routes, worker entry points, depends on application layer

**Trade-offs:**

- **Pros**: High maintainability, testability, flexibility
- **Cons**: More initial setup, more files/abstractions, can feel like overkill for simple features
- **Decision**: Worth it for maintainable, testable codebase that can evolve

### 6.2 Technology Choices

**FastAPI for Backend:**

- **Rationale**: Built-in OpenAPI support, automatic validation, async support, excellent performance
- **Trade-off**: Smaller ecosystem than Django, but sufficient for API-first application
- **Reference**: See `docs/technology.md` for detailed rationale

**React for Frontend:**

- **Rationale**: Required by assignment, modern component-based architecture, large ecosystem
- **Trade-off**: Learning curve for beginners, but widely adopted and well-documented
- **Reference**: See `docs/technology.md` for detailed rationale

**SQLite (Development) / PostgreSQL (Production):**

- **Rationale**: SQLite for simplicity in development, PostgreSQL for production scalability
- **Trade-off**: SQLite limitations (concurrency, JSON support) vs. simplicity
- **Decision**: Support both via `DATABASE_URL` environment variable

**Redis for Rate Limiting:**

- **Rationale**: Fast, distributed, supports per-user and per-IP rate limiting
- **Trade-off**: Additional infrastructure dependency vs. in-memory solution
- **Decision**: Graceful degradation if Redis unavailable (rate limiting disabled)

### 6.3 Design Patterns Used

**Repository Pattern:**

- **Why**: Abstracts data access, enables testing with in-memory implementations
- **Implementation**: `application/tasks/repository.py` defines interface, `infrastructure/persistence/repositories/` implements

**Dependency Injection:**

- **Why**: Loose coupling, easier testing, follows Dependency Inversion Principle
- **Implementation**: FastAPI's `Depends()` for route dependencies, constructor injection for use cases

**Use Case Pattern:**

- **Why**: Encapsulates business logic, single responsibility per use case
- **Implementation**: Each operation (create_task, update_task, etc.) is a separate use case function

**Middleware Pattern:**

- **Why**: Cross-cutting concerns (auth, logging, rate limiting) applied consistently
- **Implementation**: FastAPI middleware for correlation IDs, metrics, rate limiting, CORS

### 6.4 Trade-offs Made

**Simplicity vs. Scalability:**

- **Choice**: Started with SQLite, designed to support PostgreSQL
- **Rationale**: Faster development, easier local setup, can scale when needed

**Development Speed vs. Architecture Purity:**

- **Choice**: Clean Architecture with some pragmatic shortcuts (e.g., SQLAlchemy models in domain layer)
- **Rationale**: Balance between maintainability and development velocity

**Feature Completeness vs. Time:**

- **Choice**: Implemented core features fully, some enhancements deferred (e.g., Prometheus/Grafana dashboards)
- **Rationale**: Focus on working, well-tested core functionality first

## 7. Summary

This architecture description:

- Stays within the scope defined by `docs/requirements.md` and `docs/technical-specs.md`.
- Highlights where concrete implementation decisions are required but not mandated.
- Provides enough structure to implement the backend, worker, and frontend while preserving flexibility for technology and detailed design choices.
- Implements Clean Architecture principles for maintainability and testability.

---

## 8. Architecture Charts (Text Diagrams)

The following diagrams give a visual overview of the system. They are descriptive only and do not add new requirements.

### 8.1 High‑Level Components

```mermaid
flowchart LR
  UserBrowser["User (Browser)"]
  Frontend["Frontend (React UI)"]
  Api["Backend API Service (Python)"]
  Worker["Background Worker"]
  DB["Database"]

  UserBrowser --> Frontend
  Frontend --> Api
  Api --> DB
  Api --> Worker
  Worker --> DB
```

### 8.2 Request & Logging Flow (Example)

```mermaid
sequenceDiagram
  participant U as User
  participant FE as Frontend (React)
  participant API as Backend API
  participant DB as Database

  U->>FE: Click "Create Task"
  FE->>API: POST /tasks (with auth token, correlation ID)
  API->>API: Validate & authorize
  API->>DB: Insert task
  DB-->>API: OK
  API-->>FE: 201 Created + task data
  FE-->>U: Show success toast
```

### 8.3 Reminder Worker Flow (Example)

```mermaid
sequenceDiagram
  participant S as Scheduler
  participant W as Worker
  participant DB as Database

  S->>W: Trigger "Check due tasks"
  W->>DB: Query tasks due in next 24h
  DB-->>W: List of tasks
  loop For each task
    W->>W: Check if reminder already sent (idempotency)
    W->>DB: Log "reminder sent" event (audit)
  end
```
