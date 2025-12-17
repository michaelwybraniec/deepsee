# Search & Filtering

**File**: `src/pages/TaskListPage.jsx`

## Performance

- **Debounce**: 500ms debounce for search and tag filter inputs (reduces API calls)

## Filter Options

- **Text Search**: `q` parameter (searches title and description)
- **Status**: `status` parameter
- **Priority**: `priority` parameter
- **Tags**: `tags` parameter (comma-separated, case-insensitive partial match)
- **Due Date Range**: `due_date_from`, `due_date_to` parameters
- **My Tasks**: `owner_user_id` parameter

## API Parameters

All filters are passed as query parameters to `GET /api/tasks`:
```
?q=search&status=in_progress&priority=high&tags=urgent&due_date_from=2024-01-01&owner_user_id=1
```

## Related

- [Backend Search & Filter API](../backend/docs/search-filters.md)
