# Tag Filtering

## Implementation

**Location**: `backend/application/tasks/search_tasks.py` (line ~131)

**Behavior**: Case-insensitive partial matching - filter tag "projec" matches task tag "project"

**Function**: `tag_matches()` - checks if filter tag is a substring of any task tag (case-insensitive)
