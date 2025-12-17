# Task Model

**API Schema**: See [API Documentation](api.md) (Swagger UI: `/docs`, ReDoc: `/redoc`)

## Implementation

**Location**: `backend/domain/models/task.py`

**Design Decisions**:

- Tags stored as JSON string (SQLite compatible)
- Status/Priority: String type (not ENUM) for flexibility
- Indexes: `title`, `due_date`, `owner_user_id`, composite `(owner_user_id, due_date)`

**Relationships**:

- `Task.owner_user_id` → `User.id` (CASCADE on delete)
