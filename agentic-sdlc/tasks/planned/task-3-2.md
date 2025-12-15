# Task ID: 3.2
# Title: Design task data model
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 2h

## Description
Design the task data model and database representation to store all required fields (title, description, status, priority, due date, tags) and ownership information, based on field list from task 3.1.

**Step-by-step:**
1. Review field list from task 3.1 (title, description, status, priority, due_date, tags, plus system fields).
2. Design database schema (SQL or ORM model):
   - Table: `tasks`
   - Columns:
     - `id` (primary key, auto-increment/UUID)
     - `title` (string/VARCHAR, NOT NULL)
     - `description` (text/VARCHAR, nullable)
     - `status` (string/VARCHAR or ENUM, nullable - e.g., "todo", "in_progress", "done")
     - `priority` (string/VARCHAR or ENUM, nullable - e.g., "low", "medium", "high")
     - `due_date` (date/DATE or timestamp/TIMESTAMP, nullable)
     - `tags` (JSON/JSONB array or separate `task_tags` table, nullable)
     - `owner_user_id` (foreign key to users table, NOT NULL)
     - `created_at` (timestamp/TIMESTAMP, auto-set)
     - `updated_at` (timestamp/TIMESTAMP, auto-updated)
3. Design domain entity (Clean Architecture):
   - Create `Task` entity in `backend/domain/tasks/task.py`:
     - Properties: id, title, description, status, priority, due_date, tags, owner_user_id, created_at, updated_at
     - Methods: validation logic if needed (e.g., validate status enum, validate date format)
4. Design ORM model (if using SQLAlchemy, Django ORM, etc.):
   - Create `Task` model in `backend/infrastructure/persistence/models/task.py`:
     - Map to database table
     - Define relationships (e.g., belongs_to user via owner_user_id)
     - Define indexes (e.g., on owner_user_id, due_date for queries)
5. Consider search/filter requirements (from task 5):
   - Ensure `title` and `description` are searchable (full-text index if needed)
   - Ensure `status`, `priority`, `due_date`, `tags` are filterable (indexes if needed)
   - Ensure `owner_user_id` is indexed (for authorization queries)
6. Document model:
   - Create schema diagram or code comments
   - Document field types, constraints, indexes
   - Document relationships (task belongs to user)

**Implementation hints:**
- See `docs/technology.md` section "2. Backend Framework & Libraries" for ORM and database choices, versions, and rationale.
- Use SQLAlchemy 2.0+ (if using FastAPI/Flask) or Django ORM (if using Django) per `docs/technology.md`.
- Database: PostgreSQL 15+ (recommended) or MySQL 8+ per `docs/technology.md`.
- For tags: Use JSON/JSONB column (PostgreSQL) or separate `task_tags` table (normalized).
- Place domain entity in `backend/domain/tasks/task.py` (pure Python, no ORM dependencies).
- Place ORM model in `backend/infrastructure/persistence/models/task.py` (depends on ORM).
- Use repository pattern: interface in `backend/application/tasks/repository.py`, implementation in `backend/infrastructure/persistence/repositories/task_repository.py`.

## Dependencies
- [ ] Task ID: 3.1 (Field list must be confirmed)

## Testing Instructions
- N/A for design task. Verify by checking that the model includes all fields and an owner reference.
- Review model definition to ensure all fields from task 3.1 are present.

## Security Review
- Ensure no unnecessary sensitive data is stored in the task model.
- Ensure `owner_user_id` is present and indexed (for authorization checks).

## Risk Assessment
- Poor model design may complicate filtering, search, and authorization checks later.
- Missing indexes can cause slow queries for search/filter operations.
- Incorrect data types can cause validation or query issues.

## Acceptance Criteria
- [ ] Task model includes all required fields (title, description, status, priority, due_date, tags) and owner reference (owner_user_id).
- [ ] Model design supports search/filter/sort/pagination requirements (indexes on searchable/filterable fields, owner_user_id indexed).
- [ ] Model is implemented in code (ORM/entity definition exists).
- [ ] Model is documented (schema diagram, code comments, or design doc).

## Definition of Done
- [ ] Model documented and implemented in code (e.g. ORM/entity definition in `backend/domain/tasks/task.py` and `backend/infrastructure/persistence/models/task.py`).
- [ ] Database schema defined (migration file or SQL script).
- [ ] Indexes defined for search/filter operations (owner_user_id, due_date, full-text on title/description if needed).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Model definition matches field list and is committed (code files exist, schema defined).
- **Observable Outcomes**: Model can be used in code, database table can be created, indexes are defined.

## Notes
This forms the basis for CRUD and search/filter operations (tasks 3.3, 3.4, 3.5, 5). Ensure model design supports all these use cases.

## Strengths
Enables consistent handling of tasks across the API and worker. Provides foundation for all task operations.

## Sub-tasks (Children)
- [ ] Review field list from task 3.1 (title, description, status, priority, due_date, tags, plus system fields).
- [ ] Design database schema (table name, columns, types, constraints, indexes).
- [ ] Design domain entity (pure Python class in `backend/domain/tasks/task.py`).
- [ ] Design ORM model (SQLAlchemy/Django model in `backend/infrastructure/persistence/models/task.py`).
- [ ] Define indexes for search/filter operations (owner_user_id, due_date, full-text on title/description if needed).
- [ ] Document model (schema diagram, code comments, or design doc).
- [ ] Create database migration or SQL script to create table.

## Completed
[ ] Pending / [ ] Completed


