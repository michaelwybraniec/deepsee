# Task Data Model Design

## Overview

The Task model implements all required fields from `docs/requirements.md` section "2. Task Management" and supports search, filtering, and authorization requirements.

## Database Schema

**Table**: `tasks`

### Columns

| Column | Type | Nullable | Description | Source |
|--------|------|----------|-------------|--------|
| `id` | INTEGER | NO | Primary key, auto-increment | System |
| `title` | VARCHAR | NO | Task title (required) | Requirements |
| `description` | TEXT | YES | Task description | Requirements |
| `status` | VARCHAR | YES | Task status (e.g., "todo", "in_progress", "done") | Requirements |
| `priority` | VARCHAR | YES | Task priority (e.g., "low", "medium", "high") | Requirements |
| `due_date` | DATETIME | YES | Task due date | Requirements |
| `tags` | VARCHAR | YES | JSON string array of tags | Requirements |
| `owner_user_id` | INTEGER | NO | Foreign key to users.id | System (authorization) |
| `created_at` | DATETIME | NO | Creation timestamp | System |
| `updated_at` | DATETIME | NO | Last update timestamp | System |

### Indexes

1. **Primary Key**: `id` (automatic)
2. **owner_user_id**: For authorization queries and filtering by owner
3. **title**: For search by title (Task 5)
4. **due_date**: For filtering and sorting by due date (Task 5)
5. **Composite**: `(owner_user_id, due_date)` - For efficient filtering by owner and due date

### Foreign Keys

- `owner_user_id` → `users.id` (CASCADE on delete - if user deleted, tasks deleted)

## Domain Entity

Location: `backend/domain/models/task.py`

The Task model is implemented as a SQLAlchemy ORM model following Clean Architecture:
- Domain model in `domain/models/` (no infrastructure dependencies)
- Uses SQLAlchemy Base for database mapping
- Includes relationships and indexes

## Relationships

- **Task belongs to User**: `Task.owner_user_id` → `User.id`
- Relationship: `Task.owner` → `User` (SQLAlchemy relationship)
- Backref: `User.tasks` → List of tasks owned by user

## Design Decisions

1. **Tags Storage**: Stored as JSON string (SQLite compatible). For PostgreSQL, could use JSONB.
2. **Status/Priority**: String type (not ENUM) for flexibility. Values are design choice.
3. **Indexes**: Optimized for search (title), filtering (due_date, owner_user_id), and composite queries.
4. **Timestamps**: Auto-set on create, auto-updated on modify.

## Search/Filter Support

The model is designed to support Task 5 requirements:
- **Search**: `title` and `description` fields (indexed for performance)
- **Filter**: `status`, `priority`, `due_date`, `tags` (indexed where needed)
- **Sort**: `due_date`, `created_at`, `updated_at` (indexed)
- **Authorization**: `owner_user_id` (indexed for ownership checks)

## Migration

Database tables are created automatically via SQLAlchemy `Base.metadata.create_all()` in `infrastructure/database/__init__.py`.

For production, consider using Alembic migrations (not required for this assignment).
