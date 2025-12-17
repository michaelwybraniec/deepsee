# Pagination

**File**: `src/pages/TaskListPage.jsx`

## Configuration

- **Default Page Size**: 20 items per page
- **Auto-reset**: Page resets to 1 when filters change

## API Response Format

```json
{
  "tasks": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## Related

- [Backend Search & Filter API](../backend/docs/search-filters.md#pagination)
