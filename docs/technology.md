# Technology Stack & Decisions

> **Design Choice**: This document describes technology choices made for the Task Tracker application. These choices are not mandated by `docs/requirements.md` but are design decisions made to implement the requirements effectively.

This document serves as a decision log for all technology choices, including rationale, versions, and alternatives considered.

---

## 1. Core Technology Stack

### Backend Language

**Decision**: Python 3.11+

**Rationale**:

- Required by assignment (`docs/requirements.md` specifies "Python").
- Modern Python (3.11+) provides excellent performance and type hints support.
- Strong ecosystem for web APIs, data processing, and testing.

**Alternatives Considered**:

- Python 3.9/3.10: Older versions, less performance optimizations.
- Other languages: Not considered (Python is required by assignment).

### Frontend Framework

**Decision**: React 18+

**Rationale**:

- Required by assignment (`docs/requirements.md` specifies "React (or similar)").
- React 18+ provides modern features (concurrent rendering, automatic batching).
- Large ecosystem and community support.
- Good for component-based architecture.

**Alternatives Considered**:

- Vue.js, Angular: Not considered (React is preferred/required).
- React 17 or earlier: Not recommended (missing modern features).

---

## 2. Backend Framework & Libraries

### API Framework

**Decision**: FastAPI (recommended) or Flask or Django REST Framework

**Status**: To be decided during implementation (task 2.2, 3.3)

**Options & Rationale**:

**FastAPI** (Recommended):

- **Pros**: Built-in OpenAPI/Swagger support, automatic validation with Pydantic, async support, excellent performance, modern Python features.
- **Cons**: Smaller ecosystem than Django, newer framework.
- **Best for**: API-first applications, when OpenAPI docs are important, performance-critical APIs.
- **Version**: FastAPI 0.104+ (supports Python 3.11+, latest features).

**Flask**:

- **Pros**: Lightweight, flexible, large ecosystem, simple to get started.
- **Cons**: Manual OpenAPI setup needed, less built-in validation.
- **Best for**: Simple APIs, when flexibility is more important than built-in features.
- **Version**: Flask 3.0+ (supports Python 3.11+).

**Django REST Framework**:

- **Pros**: Full-featured, built-in admin, ORM included, excellent documentation.
- **Cons**: Heavier framework, more opinionated, may be overkill for API-only.
- **Best for**: When Django ORM is preferred, need admin interface, full-stack Django apps.
- **Version**: Django 4.2+ with DRF 3.14+ (supports Python 3.11+).

**Recommendation**: FastAPI for this project (API-first, OpenAPI support, performance, modern Python).

### ORM / Database Access

**Decision**: SQLAlchemy 2.0+ (if using FastAPI/Flask) or Django ORM (if using Django)

**Rationale**:

- **SQLAlchemy**: Industry standard, flexible, works with any Python framework, excellent query builder, supports Clean Architecture (can use without framework).
- **Django ORM**: Only if using Django, tightly integrated, less flexible for Clean Architecture.
- **Version**: SQLAlchemy 2.0+ (modern API, better performance) or Django ORM (comes with Django).

**Alternatives Considered**:

- Raw SQL: Too low-level, error-prone, harder to maintain.
- Other ORMs (Peewee, Tortoise ORM): Less mature, smaller ecosystem.

### Database

**Decision**: PostgreSQL 15+ (recommended) or MySQL 8+

**Status**: To be decided during implementation (task 3.2, 11.3)

**Options & Rationale**:

**PostgreSQL** (Recommended):

- **Pros**: Excellent JSON/JSONB support (for tags), full-text search, robust, open-source, excellent performance.
- **Cons**: Slightly more complex setup than MySQL.
- **Best for**: When JSON/JSONB features are needed (tags), full-text search, complex queries.
- **Version**: PostgreSQL 15+ (latest features, performance improvements).

**MySQL 8+**:

- **Pros**: Widely used, simple setup, good performance.
- **Cons**: Less advanced JSON support, no native JSONB.
- **Best for**: When simplicity is preferred, existing MySQL infrastructure.
- **Version**: MySQL 8.0+ (JSON support, modern features).

**Recommendation**: PostgreSQL for this project (better JSON/JSONB support for tags, full-text search capabilities).

---

## 3. Authentication & Security

### Authentication Method

**Decision**: JWT (recommended) or OIDC/OAuth2

**Status**: ✅ Implemented (task 2.2) - JWT chosen

**Options & Rationale**:

**JWT** (Recommended):

- **Library**: `python-jose[cryptography]` 3.3.2+
- **Pros**: Simple for single-tenant, stateless, good for API-first, no external dependencies.
- **Cons**: Token revocation requires additional logic, tokens can't be easily invalidated.
- **Best for**: Single-tenant applications, API-first architecture, when simplicity is preferred.
- **Version**: python-jose 3.3.2+ (supports modern JWT features, cryptography backend for RS256).

**OIDC/OAuth2**:

- **Library**: `authlib` 1.2+ or `python-social-auth`
- **Pros**: Better for multi-tenant, external identity providers, industry standard.
- **Cons**: More complex setup, requires OAuth provider configuration.
- **Best for**: Multi-tenant applications, integration with external identity providers.
- **Version**: authlib 1.2+ (modern OAuth2/OIDC support).

**Recommendation**: JWT for this project (simpler, API-first, single-tenant, faster to implement).

### Password Hashing

**Decision**: bcrypt

**Rationale**:

- Industry standard for password hashing.
- Built-in salt generation, slow by design (resistant to brute force).
- Well-tested and secure.
- **Version**: `bcrypt` 4.1+ (supports Python 3.11+, latest security improvements).

**Alternatives Considered**:

- **argon2**: More modern, better security, but bcrypt is sufficient and more widely used.
- **pbkdf2**: Older standard, less secure than bcrypt/argon2.
- **Plaintext**: Never acceptable (security risk).

---

## 4. Frontend Libraries

### React Setup

**Decision**: Vite (recommended) or create-react-app or Next.js

**Status**: To be decided during implementation (task 10.2)

**Options & Rationale**:

**Vite** (Recommended):

- **Pros**: Fast development server, modern build tool, excellent performance, simple configuration.
- **Cons**: Newer tool, less documentation than CRA.
- **Best for**: Modern React apps, when performance is important.
- **Version**: Vite 5+ (supports React 18+, latest features).

**create-react-app**:

- **Pros**: Well-documented, stable, widely used.
- **Cons**: Slower build times, less modern tooling.
- **Best for**: When simplicity and stability are preferred.
- **Version**: CRA 5+ (supports React 18+).

**Next.js**:

- **Pros**: Full-stack framework, SSR/SSG support, excellent DX.
- **Cons**: May be overkill for SPA, adds complexity.
- **Best for**: When SSR/SSG is needed, full-stack React apps.
- **Version**: Next.js 14+ (supports React 18+, latest features).

**Recommendation**: Vite for this project (fast, modern, simple, good for SPA).

### Routing

**Decision**: react-router-dom 6+

**Rationale**:

- Standard routing library for React.
- Version 6+ has modern API (hooks-based, better TypeScript support).
- **Version**: react-router-dom 6.20+ (latest features, React 18 compatible).

**Alternatives Considered**:

- **Next.js Router**: Only if using Next.js.
- **Reach Router**: Deprecated, merged into react-router.

### HTTP Client

**Decision**: axios 1.6+ or fetch API

**Rationale**:

- **axios**: Better error handling, interceptors, request/response transformation, widely used.
- **fetch**: Native browser API, no dependencies, but less features.
- **Version**: axios 1.6+ (supports modern features, TypeScript).

**Recommendation**: axios for this project (better error handling, interceptors for auth tokens).

### State Management

**Decision**: React Context API or Zustand (if needed)

**Rationale**:

- **React Context**: Built-in, sufficient for auth state and simple state.
- **Zustand**: Lightweight, if more complex state management is needed.
- **Version**: Built-in (React) or Zustand 4.4+.

**Alternatives Considered**:

- **Redux**: Overkill for this project, too much boilerplate.
- **Jotai, Recoil**: More complex than needed.

### Styling & CSS Framework

**Decision**: Tailwind CSS 3.4+ (recommended) or CSS Modules or plain CSS

**Status**: To be decided during implementation (task 10.2)

**Options & Rationale**:

**Tailwind CSS** (Recommended):

- **Pros**: Utility-first CSS, highly maintainable, scalable, excellent developer experience, great for rapid development, consistent design system, small bundle size (purges unused styles).
- **Cons**: Learning curve for utility classes, requires build step.
- **Best for**: Modern React apps, when consistency and maintainability are important, rapid development.
- **Version**: Tailwind CSS 3.4+ (latest features, JIT mode, better performance).

**CSS Modules**:

- **Pros**: Built-in CSS scoping, no dependencies, simple, works with any build tool.
- **Cons**: Less powerful than Tailwind, requires writing more CSS, no design system.
- **Best for**: When minimal dependencies are preferred, simple styling needs.
- **Version**: Built-in with most React build tools.

**Plain CSS**:

- **Pros**: No dependencies, full control, no build step needed.
- **Cons**: Harder to maintain at scale, no design system, potential for style conflicts.
- **Best for**: Very simple projects, when minimal tooling is required.

**Recommendation**: Tailwind CSS for this project (best practice, maintainable, scalable, free, excellent DX).

### UI Component Library

**Decision**: shadcn/ui (recommended) or Chakra UI or MUI or none (custom components)

**Status**: To be decided during implementation (task 10.2)

**Options & Rationale**:

**shadcn/ui** (Recommended):

- **Pros**: Free, open-source, components copied into your project (full control), built on Radix UI (accessible), uses Tailwind CSS, beautiful design, easy to customize, no dependency bloat, excellent for maintainability.
- **Cons**: Requires Tailwind CSS, components are copied (not installed), newer library.
- **Best for**: Modern React apps with Tailwind, when you want full control over components, maintainable codebase.
- **Version**: Latest (components are copied, not versioned as dependency).

**ChakraUI**:

- **Pros**: Free, open-source, comprehensive component library, excellent accessibility, built-in theming, dark mode support, good documentation, composable components.
- **Cons**: Adds dependency, less control over component code, larger bundle size.
- **Best for**: When you want a complete component library without writing custom components.
- **Version**: Chakra UI 2.0+ (React 18+ support).

**MUI (Material-UI)**:

- **Pros**: Free, open-source, very comprehensive, widely used, excellent documentation, Material Design, extensive component library.
- **Cons**: Larger bundle size, Material Design may not fit all projects, more opinionated styling.
- **Best for**: When Material Design is acceptable, enterprise applications.
- **Version**: MUI 5.15+ (React 18+ support).

**None (Custom Components)**:

- **Pros**: Full control, no dependencies, custom design.
- **Cons**: More development time, need to handle accessibility, testing, and edge cases.
- **Best for**: When specific design requirements or minimal dependencies are needed.

**Recommendation**: shadcn/ui for this project (best practice, free, maintainable, scalable, full control, works with Tailwind CSS).

### Form Library

**Decision**: React Hook Form 7.49+ (recommended) or Formik or native HTML forms

**Status**: To be decided during implementation (task 10.4)

**Options & Rationale**:

**React Hook Form** (Recommended):

- **Pros**: Lightweight, performant (uncontrolled components), excellent validation, minimal re-renders, great TypeScript support, easy to integrate with UI libraries, small bundle size.
- **Cons**: Different mental model (uncontrolled vs controlled), requires validation library (zod, yup).
- **Best for**: Performance-critical forms, when you want minimal re-renders, modern React apps.
- **Version**: React Hook Form 7.49+ (latest features, React 18+ support).

**Formik**:

- **Pros**: Popular, controlled components, good documentation, validation built-in.
- **Cons**: Heavier bundle, more re-renders, less performant for large forms.
- **Best for**: When controlled components are preferred, simpler mental model.
- **Version**: Formik 2.4+ (React 18+ support).

**Native HTML Forms**:

- **Pros**: No dependencies, simple, works everywhere.
- **Cons**: More manual work, less validation features, harder to maintain.
- **Best for**: Very simple forms, when minimal dependencies are required.

**Recommendation**: React Hook Form for this project (best practice, performant, maintainable, works well with shadcn/ui).

### Toast/Notification Library

**Decision**: sonner 1.3+ (recommended) or react-hot-toast or react-toastify

**Status**: To be decided during implementation (task 10.6)

**Options & Rationale**:

**sonner** (Recommended):

- **Pros**: Lightweight, modern, beautiful design, works with shadcn/ui, TypeScript support, accessible, customizable, small bundle size.
- **Cons**: Newer library, smaller community than react-toastify.
- **Best for**: Modern React apps, when using shadcn/ui or Tailwind CSS.
- **Version**: sonner 1.3+ (latest features).

**react-hot-toast**:

- **Pros**: Lightweight, popular, simple API, good performance, customizable.
- **Cons**: Less features than sonner, different design.
- **Best for**: Simple toast notifications, when lightweight is important.
- **Version**: react-hot-toast 2.4+ (React 18+ support).

**react-toastify**:

- **Pros**: Very popular, comprehensive features, good documentation, many options.
- **Cons**: Larger bundle size, more features than needed for simple use cases.
- **Best for**: When you need advanced toast features, animations.
- **Version**: react-toastify 9.1+ (React 18+ support).

**Recommendation**: sonner for this project (best practice, modern, works well with shadcn/ui, lightweight).

### Icon Library

**Decision**: lucide-react 0.300+ (recommended) or react-icons

**Status**: To be decided during implementation (task 10.2)

**Options & Rationale**:

**lucide-react** (Recommended):

- **Pros**: Free, open-source, consistent design, tree-shakeable, TypeScript support, works well with shadcn/ui, modern, lightweight, beautiful icons.
- **Cons**: Smaller icon set than react-icons.
- **Best for**: Modern React apps, when consistency is important, using shadcn/ui.
- **Version**: lucide-react 0.300+ (latest icons, React 18+ support).

**react-icons**:

- **Pros**: Free, open-source, massive icon collection (Font Awesome, Material Design, Feather, etc.), widely used, good documentation.
- **Cons**: Larger bundle size if importing many icons, less consistent design across icon sets.
- **Best for**: When you need a wide variety of icons from different icon sets.
- **Version**: react-icons 5.0+ (React 18+ support).

**Recommendation**: lucide-react for this project (best practice, consistent, works with shadcn/ui, tree-shakeable).

---

## 5. Infrastructure & Services

### Rate Limiting Storage

**Decision**: Redis 7+

**Rationale**:

- Fast, in-memory storage perfect for rate limiting.
- Supports TTL (time-to-live) for automatic expiration.
- Scalable, can be shared across multiple API instances.
- **Version**: Redis 7+ (latest features, better performance).

**Alternatives Considered**:

- **In-memory (Python dict)**: Not scalable across instances, lost on restart.
- **Database**: Too slow for rate limiting, adds database load.
- **Memcached**: Similar to Redis but less features, Redis preferred.

### Worker Scheduling

**Decision**: APScheduler 3.10+ (recommended) or celery 5.3+ with celery beat

**Status**: To be decided during implementation (task 6.2)

**Options & Rationale**:

**APScheduler** (Recommended):

- **Pros**: Simple, no external dependencies, easy to integrate, good for single-worker scenarios.
- **Cons**: Not distributed (single process), no built-in job queue.
- **Best for**: Simple reminder worker, single-worker deployment.
- **Version**: APScheduler 3.10+ (Python 3.11+ support, latest features).

**celery with celery beat**:

- **Pros**: Distributed, job queue, retry mechanisms, better for production at scale.
- **Cons**: More complex setup, requires message broker (Redis/RabbitMQ).
- **Best for**: Distributed workers, production at scale, complex job processing.
- **Version**: celery 5.3+ (Python 3.11+ support, latest features).

**Recommendation**: APScheduler for this project (simpler, sufficient for reminder worker, no external dependencies).

---

## 6. Observability & Monitoring

### Structured Logging

**Decision**: structlog 23.2+

**Rationale**:

- Excellent structured logging for Python.
- JSON output support, context propagation, correlation IDs.
- Better than standard library logging for structured logs.
- **Version**: structlog 23.2+ (Python 3.11+ support, latest features).

**Alternatives Considered**:

- **Standard library logging**: Less structured, harder to parse, no built-in JSON formatter.
- **loguru**: Good alternative, but structlog is more widely used in production.

### Metrics

**Decision**: prometheus-client 0.19+

**Rationale**:

- Industry standard for metrics.
- Prometheus format is widely supported.
- Easy to integrate with monitoring stacks.
- **Version**: prometheus-client 0.19+ (Python 3.11+ support, latest features).

**Alternatives Considered**:

- **Custom metrics endpoint**: More work, less standard.
- **StatsD**: Different format, requires StatsD server.

### API Documentation

**Decision**: FastAPI built-in (if using FastAPI) or flask-swagger-ui/flasgger (if using Flask) or drf-yasg/drf-spectacular (if using Django)

**Rationale**:

- **FastAPI**: Built-in OpenAPI/Swagger support, auto-generates from code.
- **Flask**: flask-swagger-ui or flasgger for Swagger UI.
- **Django**: drf-yasg or drf-spectacular for OpenAPI.
- **Version**: Framework-specific (comes with framework or latest version).

**Recommendation**: FastAPI's built-in support (easiest, stays in sync with code).

---

## 7. Testing

### Backend Testing

**Decision**: pytest 7.4+

**Rationale**:

- Industry standard for Python testing.
- Excellent fixtures, plugins, async support.
- Great for unit, integration, and worker tests.
- **Version**: pytest 7.4+ (Python 3.11+ support, latest features).

**Alternatives Considered**:

- **unittest**: Standard library, but pytest is more powerful and easier to use.
- **nose2**: Less maintained, pytest is preferred.

### Frontend Testing

**Decision**: jest/vitest 1.0+ or Playwright 1.40+

**Rationale**:

- **jest/vitest**: For unit and component tests, fast, good React support.
- **Playwright**: For E2E/smoke tests, modern, reliable, cross-browser.
- **Version**: jest 29+ or vitest 1.0+ (React 18+ support), Playwright 1.40+ (latest features).

**Alternatives Considered**:

- **Cypress**: Good alternative to Playwright, but Playwright is more modern and faster.
- **React Testing Library**: Good for component tests, can be used with jest/vitest.

**Recommendation**: vitest for unit tests (faster, modern), Playwright for E2E tests (reliable, cross-browser).

---

## 8. Development Tools

### Containerization

**Decision**: Docker & Docker Compose

**Rationale**:

- Required by assignment (`docs/requirements.md` specifies "Docker compose for local run").
- Standard for local development and deployment.
- **Version**: Docker 24+ and Docker Compose v2+ (latest features, better performance).

### Package Management

**Backend**:

- **Decision**: pip with requirements.txt or poetry or pipenv
- **Recommendation**: pip with requirements.txt (simple, standard) or poetry (better dependency resolution).
- **Version**: pip 23+ or poetry 1.7+.

**Frontend**:

- **Decision**: npm or yarn or pnpm
- **Recommendation**: npm (comes with Node.js) or pnpm (faster, better disk usage).
- **Version**: npm 10+ or pnpm 8+.

---

## 9. Version Compatibility Matrix

| Component | Minimum Version | Recommended Version | Python/Node Requirement |
|-----------|----------------|---------------------|------------------------|
| Python | 3.11 | 3.11+ | - |
| Node.js | 18 | 20 LTS | - |
| FastAPI | 0.104 | Latest | Python 3.11+ |
| Flask | 3.0 | Latest | Python 3.11+ |
| Django | 4.2 | Latest | Python 3.11+ |
| SQLAlchemy | 2.0 | Latest | Python 3.11+ |
| React | 18 | 18+ | Node.js 18+ |
| react-router-dom | 6.20 | Latest | React 18+ |
| Tailwind CSS | 3.4 | Latest | Node.js 18+ |
| shadcn/ui | Latest | Latest | React 18+, Tailwind CSS |
| React Hook Form | 7.49 | Latest | React 18+ |
| sonner | 1.3 | Latest | React 18+ |
| lucide-react | 0.300 | Latest | React 18+ |
| PostgreSQL | 15 | Latest | - |
| MySQL | 8.0 | Latest | - |
| Redis | 7 | Latest | - |
| pytest | 7.4 | Latest | Python 3.11+ |
| Playwright | 1.40 | Latest | Node.js 18+ |

---

## 10. Decision Log

### 2024 - Initial Technology Decisions

**Date**: [To be filled during implementation]

**Decision**: [Technology choice]

- **Rationale**: [Why this choice]
- **Alternatives Considered**: [What else was considered]
- **Impact**: [How this affects the project]
- **Status**: Implemented / Pending / Reconsidered

---

## 11. References

- **Requirements**: See `docs/requirements.md` for assignment requirements
- **Technical Specs**: See `docs/technical-specs.md` for structured requirements
- **Architecture**: See `docs/architecture.md` for system architecture
- **Task Files**: See `agentic-sdlc/tasks/planned/` for implementation-specific technology hints

---

## Notes

- All technology choices are **Design Choices** (not required by assignment).
- Choices should be documented here as they are made during implementation.
- If better alternatives are discovered, they should be discussed and this document updated.
- Version numbers should be updated as dependencies are installed and locked.
