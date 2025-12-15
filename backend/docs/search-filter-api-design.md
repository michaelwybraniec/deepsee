# Search, Filter, Sort, and Pagination API Design

## Overview

This document describes the API design for searching, filtering, sorting, and paginating tasks.

## API Endpoint

**Endpoint**: `GET /api/tasks`

**Method**: GET

**Authentication**: Required (Bearer token)

**Authorization**: All authenticated users can search/filter all tasks (no ownership filter for reads)

## Query Parameters

### Search Parameter

**`q`** (string, optional)
- **Description**: Search term to match in task title or description
- **Behavior**: Case-insensitive partial match (OR logic - matches if title OR description contains term)
- **Example**: `?q=urgent`
- **Implementation**: `(title ILIKE '%q%' OR description ILIKE '%q%')` (SQLite: `LIKE` with case-insensitive collation)

### Filter Parameters

**`status`** (string, optional)
- **Description**: Filter by task status (exact match)
- **Values**: `todo`, `in_progress`, `done` (or other status values)
- **Example**: `?status=todo`
- **Implementation**: `status = 'status_value'`

**`priority`** (string, optional)
- **Description**: Filter by task priority (exact match)
- **Values**: `low`, `medium`, `high` (or other priority values)
- **Example**: `?priority=high`
- **Implementation**: `priority = 'priority_value'`

**`tags`** (string or array, optional)
- **Description**: Filter by tags (tasks containing any of the specified tags)
- **Format**: Comma-separated string (`tags=urgent,important`) or array (`tags[]=urgent&tags[]=important`)
- **Example**: `?tags=urgent,important`
- **Implementation**: For SQLite with JSON string storage: Parse JSON, check if any tag in array matches any specified tag

**`due_date`** (date, optional)
- **Description**: Filter by exact due date
- **Format**: ISO date format (`YYYY-MM-DD`)
- **Example**: `?due_date=2024-12-31`
- **Implementation**: `due_date = 'date'`

**`due_date_from`** (date, optional)
- **Description**: Filter by due date range (start date)
- **Format**: ISO date format (`YYYY-MM-DD`)
- **Example**: `?due_date_from=2024-01-01&due_date_to=2024-12-31`
- **Implementation**: `due_date >= 'from_date'`

**`due_date_to`** (date, optional)
- **Description**: Filter by due date range (end date)
- **Format**: ISO date format (`YYYY-MM-DD`)
- **Example**: `?due_date_from=2024-01-01&due_date_to=2024-12-31`
- **Implementation**: `due_date <= 'to_date'`

### Sort Parameter

**`sort`** (string, optional)
- **Description**: Sort field and direction
- **Format**: `field:direction` (e.g., `due_date:asc`, `priority:desc`)
- **Default**: `created_at:desc` (newest first)
- **Allowed fields**: `due_date`, `priority`, `created_at`, `updated_at`, `title`
- **Allowed directions**: `asc`, `desc`
- **Example**: `?sort=due_date:asc`
- **Implementation**: `ORDER BY field ASC/DESC`

### Pagination Parameters

**`page`** (integer, optional)
- **Description**: Page number (1-indexed)
- **Default**: `1`
- **Example**: `?page=2`
- **Implementation**: `OFFSET (page - 1) * page_size`

**`page_size`** (integer, optional)
- **Description**: Number of items per page
- **Default**: `20`
- **Maximum**: `100` (to prevent DoS)
- **Example**: `?page_size=50`
- **Implementation**: `LIMIT page_size`

## Response Format

### Success Response (200 OK)

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Task description",
      "status": "todo",
      "priority": "high",
      "due_date": "2024-12-31T00:00:00",
      "tags": ["urgent", "important"],
      "owner_user_id": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Pagination Metadata

- **`page`**: Current page number
- **`page_size`**: Number of items per page
- **`total`**: Total number of tasks matching the query (before pagination)
- **`total_pages`**: Total number of pages (`ceil(total / page_size)`)

## Query Building Logic

### Internal Query Construction

1. **Base Query**: Start with all tasks (no ownership filter for reads)
   ```sql
   SELECT * FROM tasks WHERE 1=1
   ```

2. **Apply Search** (if `q` provided):
   ```sql
   AND (title LIKE '%q%' OR description LIKE '%q%')
   ```

3. **Apply Filters** (if provided):
   ```sql
   AND status = 'status_value'  -- if status provided
   AND priority = 'priority_value'  -- if priority provided
   AND tags CONTAINS 'tag'  -- if tags provided (JSON parsing for SQLite)
   AND due_date = 'date'  -- if due_date provided
   AND due_date >= 'from_date'  -- if due_date_from provided
   AND due_date <= 'to_date'  -- if due_date_to provided
   ```

4. **Apply Sorting**:
   ```sql
   ORDER BY field ASC/DESC  -- default: created_at DESC
   ```

5. **Apply Pagination**:
   ```sql
   LIMIT page_size OFFSET (page - 1) * page_size
   ```

6. **Get Total Count** (separate query):
   ```sql
   SELECT COUNT(*) FROM tasks WHERE ... (same filters, no pagination)
   ```

## Parameter Validation

### Validation Rules

1. **`status`**: Must be one of allowed status values (validate against enum)
2. **`priority`**: Must be one of allowed priority values (validate against enum)
3. **`tags`**: Must be valid string or array format
4. **`due_date`**: Must be valid ISO date format (`YYYY-MM-DD`)
5. **`due_date_from`**: Must be valid ISO date format
6. **`due_date_to`**: Must be valid ISO date format, must be >= `due_date_from` if both provided
7. **`sort`**: Must match format `field:direction`, field must be allowed, direction must be `asc` or `desc`
8. **`page`**: Must be positive integer (>= 1)
9. **`page_size`**: Must be positive integer (>= 1, <= 100)

### Error Responses

**400 Bad Request**: Invalid parameter format or value
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid sort parameter format. Expected: field:direction",
    "field": "sort"
  }
}
```

## Example Requests

### Search Only
```
GET /api/tasks?q=urgent
```

### Filter by Status
```
GET /api/tasks?status=todo
```

### Filter by Multiple Criteria
```
GET /api/tasks?status=todo&priority=high&tags=urgent
```

### Search + Filter
```
GET /api/tasks?q=important&status=in_progress&priority=high
```

### Sort by Due Date
```
GET /api/tasks?sort=due_date:asc
```

### Pagination
```
GET /api/tasks?page=2&page_size=50
```

### Complete Example
```
GET /api/tasks?q=urgent&status=todo&priority=high&tags=important&due_date_from=2024-01-01&due_date_to=2024-12-31&sort=due_date:asc&page=1&page_size=20
```

## Implementation Notes

### SQLAlchemy Query Builder

Use SQLAlchemy query builder for dynamic filtering:

```python
query = db.query(Task)

# Search
if q:
    query = query.filter(
        or_(
            Task.title.ilike(f'%{q}%'),
            Task.description.ilike(f'%{q}%')
        )
    )

# Filters
if status:
    query = query.filter(Task.status == status)
if priority:
    query = query.filter(Task.priority == priority)
# ... etc

# Sort
if sort_field and sort_direction:
    query = query.order_by(getattr(Task, sort_field).desc() if sort_direction == 'desc' else getattr(Task, sort_field).asc())
else:
    query = query.order_by(Task.created_at.desc())

# Pagination
total = query.count()
tasks = query.offset((page - 1) * page_size).limit(page_size).all()
```

### Tags Filtering (SQLite JSON)

For SQLite with JSON string storage:
- Parse tags JSON string
- Check if any tag in task's tags array matches any specified filter tag
- Use Python logic (not SQL) for JSON parsing

### Performance Considerations

- Indexes on filterable fields: `status`, `priority`, `due_date`, `title` (already defined in Task model)
- Consider full-text search index for title/description if performance becomes an issue
- Limit page_size to prevent DoS (max 100)

## Security

1. **SQL Injection Prevention**: Use parameterized queries (SQLAlchemy handles this)
2. **Parameter Validation**: Validate all query parameters before use
3. **Pagination Limits**: Enforce maximum page_size (100)
4. **Authorization**: No ownership filter (all authenticated users can search/filter all tasks)
