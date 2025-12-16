# Pagination Feature

**Implementation**: `src/pages/TaskListPage.jsx` (pagination state and controls)

## Features

- **Page Navigation**: Navigate between pages with Previous/Next buttons
- **Page Size**: Configurable items per page (default: 20)
- **Page Numbers**: Display current page and total pages
- **Item Count**: Show total number of tasks
- **Top & Bottom Controls**: Pagination controls at both top and bottom of task list

## Implementation Details

- **Backend Integration**: Uses backend pagination API
- **State Management**: Page and pageSize stored in component state
- **Auto-reset**: Page resets to 1 when filters change
- **Pagination Data**: Received from backend API response

## Pagination Response Format

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

## Related Documentation

- [Backend Search & Filter API](../backend/docs/search-filter-api-design.md#pagination)
- [All Features](features.md)
