# Backend Architecture

## Clean Architecture Layers

```text
┌─────────────────────────────────────┐
│  API Layer (api/)                   │
│  - HTTP routes, middleware          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Application Layer (application/)   │
│  - Use cases, business logic        │
│  - Repository interfaces            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Domain Layer (domain/)             │
│  - Business entities, rules         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Infrastructure Layer               │
│  (infrastructure/)                  │
│  - Database, storage, external      │
└─────────────────────────────────────┘
```

## Request Flow

```text
HTTP Request
    ↓
api/routes/ → extracts HTTP data
    ↓
application/ → business logic (use cases)
    ↓
domain/ → business rules
    ↓
infrastructure/ → database operations
    ↓
Database
```

## Directory Structure

```text
backend/
├── api/              # HTTP interface (FastAPI routes)
├── application/      # Use cases (business logic orchestration)
├── domain/           # Business entities and rules
└── infrastructure/   # Database, storage, external services
```
