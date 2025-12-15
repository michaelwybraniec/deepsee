## Suggestions – Design & Implementation (Beyond Requirements)

This document lists **optional** suggestions based on SOLID principles, Clean Architecture, and general good practice.  
They are **not part of the assignment requirements** in `docs/requirements.md`.

---

## 1. Architecture & Structure

- **Use explicit layers**:
  - Separate **domain**, **application/use‑cases**, **infrastructure**, and **interface** (API, UI) modules.
  - Define clear interfaces (ports) between layers to keep business logic independent from frameworks.

- **Feature‑oriented modules**:
  - Group code by feature (auth, tasks, attachments, notifications, audit) rather than by technical type only.
  - This often improves cohesion and makes it easier to reason about change impact.

---

## 2. SOLID & Clean Code

- **Single Responsibility Principle (SRP)**:
  - Keep controllers thin (HTTP details only).
  - Move business rules into use‑case or domain services.

- **Open/Closed Principle (OCP)**:
  - Depend on abstractions for persistence and external services so that implementations can change without modifying core logic.

- **Dependency Inversion Principle (DIP)**:
  - Have the domain/application code depend on interfaces, implemented in infrastructure.
  - Wire dependencies in a composition root (e.g., app startup).

- **Small, focused functions and classes**:
  - Prefer small, testable units with descriptive names over large multi‑purpose functions.

---

## 3. API & Error Handling

- **Consistent error format**:
  - Choose a standard JSON error shape and reuse it across all endpoints.

- **Clear validation strategy**:
  - Validate input close to the boundary (API/UI) and pass only valid data into core logic.

---

## 4. Observability

- **Correlation IDs end‑to‑end**:
  - Generate/propagate a correlation ID from the frontend through the API and into the worker logs.

- **Minimal but meaningful metrics**:
  - Start with a small set of metrics (requests, errors, latency, reminders processed) and expand only if needed.

---

## 5. Testing Approach

- **Test the core flows first**:
  - Prioritize tests for login, task CRUD, and reminders before adding coverage for edge cases.

- **Use integration tests to fix boundaries**:
  - Let integration tests validate contracts between API and DB, and worker and DB, to catch wiring/config issues early.


