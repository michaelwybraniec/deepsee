# Search & Filtering Feature

**Implementation**: `src/pages/TaskListPage.jsx` (search and filter state management)

## Features

- **Text Search**: Search by title and description (partial matching)
- **Status Filter**: Filter by task status (pending, in_progress, done)
- **Priority Filter**: Filter by priority (low, medium, high)
- **Tag Filter**: Filter by tags (case-insensitive partial matching)
- **Due Date Range**: Filter by due date range (from/to dates)
- **My Tasks Filter**: Show only tasks owned by current user
- **Clear Filters**: One-click filter reset

## Implementation Details

- **Debounced Search**: 500ms debounce for search and tag filter inputs
- **Combined Filters**: Multiple filters can be applied simultaneously
- **URL State**: Filters persist in component state (can be enhanced with URL params)
- **Real-time Updates**: Task list updates automatically when filters change

## API Integration

- Uses backend search/filter API endpoints
- Supports all backend filter parameters:
  - `q`: Search query (title/description)
  - `status`: Status filter
  - `priority`: Priority filter
  - `tags`: Tag filter (comma-separated)
  - `due_date_from`: Start date
  - `due_date_to`: End date
  - `owner_user_id`: Filter by owner

## Related Documentation

- [Backend Search & Filter API](../backend/docs/search-filter-api-design.md)
- [Backend Tag Filtering](../backend/docs/tag-filtering-partial-match.md)
- [All Features](../README.md#features) - See README for complete feature list
