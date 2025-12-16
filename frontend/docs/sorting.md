# Sorting Feature

**Implementation**: `src/pages/TaskListPage.jsx` (sortBy state)

## Features

- **Sort Options**: Sort by due date, priority, created date, updated date
- **Sort Direction**: Ascending or descending order
- **Default Sort**: Newest first (created_at:desc)
- **UI Control**: Dropdown selector for sort field and direction

## Sort Fields

- `due_date`: Sort by due date
- `priority`: Sort by priority (low < medium < high)
- `created_at`: Sort by creation date
- `updated_at`: Sort by last update date

## Implementation Details

- **Format**: `field:direction` (e.g., `due_date:asc`, `priority:desc`)
- **Backend Integration**: Uses backend `sort` query parameter
- **State Management**: Sort preference stored in component state

## Related Documentation

- [Backend Search & Filter API](../backend/docs/search-filter-api-design.md#sorting)
- [All Features](../README.md#features) - See README for complete feature list
