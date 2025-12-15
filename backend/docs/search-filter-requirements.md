# Search & Filtering Requirements

This document summarizes all search, filtering, sorting, and pagination requirements extracted from the project documentation.

## Source References
- `docs/requirements.md` section "4. Search & Filtering"
- `docs/technical-specs.md` section "3.4 Search & Filtering"

## Requirements Summary

### 1. Search Tasks
**Requirement**: Search tasks by title or description.

**Source**: 
- `docs/requirements.md` §4: "Search tasks by title or description."
- `docs/technical-specs.md` §3.4: "Search tasks by: Title. Description."

**Details**:
- Search by title (string matching)
- Search by description (string matching)
- Search should match either title OR description (OR logic)
- Search algorithm: partial match (not exact match only)
- Case sensitivity: case-insensitive (design decision for better UX)

### 2. Filter Tasks
**Requirement**: Filter by status, priority, tags, and due date.

**Source**:
- `docs/requirements.md` §4: "Filter by status, priority, tags, and due date."
- `docs/technical-specs.md` §3.4: "Filter tasks by: Status. Priority. Tags. Due date."

**Details**:
- **Status**: Filter by task status (exact match, e.g., "todo", "in_progress", "done")
- **Priority**: Filter by task priority (exact match, e.g., "low", "medium", "high")
- **Tags**: Filter by tags (tasks containing any of the specified tags)
- **Due date**: Filter by due date (exact date or date range)

### 3. Sort Results
**Requirement**: Sort results.

**Source**:
- `docs/requirements.md` §4: "Sort and paginate results."
- `docs/technical-specs.md` §3.4: "Sort results."

**Details**:
- Sort by chosen field(s) (e.g., due date, priority, created_at, updated_at, title)
- Sort direction: ascending or descending
- Default sort: not specified (design decision - recommend `created_at DESC`)

### 4. Paginate Results
**Requirement**: Paginate results.

**Source**:
- `docs/requirements.md` §4: "Sort and paginate results."
- `docs/technical-specs.md` §3.4: "Paginate results."

**Details**:
- Return paginated results (not all tasks at once)
- Pagination parameters: page number, page size
- Default values: not specified (design decision - recommend page=1, page_size=20)
- Maximum page size: not specified (design decision - recommend max 100 to prevent DoS)

## Implicit Requirements

### 5. Combination of Search and Filters
**Requirement**: Search and filters can be combined.

**Source**: Implicit from requirements (no restriction mentioned).

**Details**:
- Search term can be combined with filters (e.g., search "urgent" AND filter by status "todo")
- Multiple filters can be combined (e.g., status="todo" AND priority="high" AND tags="urgent")
- All query parameters work together (search + filters + sort + pagination)

### 6. Authorization Rules
**Requirement**: All authenticated users can search/filter all tasks.

**Source**: 
- `docs/requirements.md` §1: "Each user is allowed to modify only their own data, although they can view all records."
- Inherits from "view all records" rule

**Details**:
- No ownership filter for search/filter operations
- All authenticated users can search and filter all tasks
- Results include tasks from all users (read-only access)

### 7. Deterministic Results
**Requirement**: Results should be consistent (deterministic sorting when no sort specified).

**Source**: Implicit (good practice for user experience).

**Details**:
- When no sort parameter provided, use default sort (e.g., `created_at DESC`)
- Ensures consistent ordering across requests
- Prevents confusion from random ordering

## Design Decisions Needed

1. **Search Algorithm**:
   - Partial match (contains) vs exact match
   - Decision: Partial match (better UX)
   - Case sensitivity: Case-insensitive (better UX)

2. **Search Implementation**:
   - SQL LIKE/ILIKE vs full-text search
   - Decision: SQL LIKE/ILIKE for simplicity (can enhance with full-text search later)

3. **Tags Filter**:
   - Exact match vs contains any tag
   - Decision: Contains any tag (tasks containing any of the specified tags)

4. **Due Date Filter**:
   - Exact date vs date range
   - Decision: Support both (exact date or range with `due_date_from`/`due_date_to`)

5. **Sort Default**:
   - Default field and direction
   - Decision: `created_at DESC` (newest first)

6. **Pagination Defaults**:
   - Default page: 1
   - Default page_size: 20
   - Maximum page_size: 100 (prevent DoS)

7. **Response Format**:
   - Include pagination metadata (total count, total pages)
   - Decision: Include metadata for frontend pagination UI

## Implementation Tasks

- Task 5.2: Design search, filter, sort, and pagination API (query parameters, response format)
- Task 5.3: Implement search by title and description
- Task 5.4: Implement filters, sorting, and pagination

## Security Considerations

1. **SQL Injection Prevention**: Use parameterized queries (never concatenate user input)
2. **Query Parameter Validation**: Validate enum values (status, priority), date formats, integers
3. **Pagination Limits**: Enforce maximum page_size to prevent DoS attacks
4. **Authorization**: All authenticated users can search/filter all tasks (no ownership filter)

## Summary

**Required behaviors**:
- ✅ Search by title and description (OR logic, partial match, case-insensitive)
- ✅ Filter by status (exact match)
- ✅ Filter by priority (exact match)
- ✅ Filter by tags (contains any tag)
- ✅ Filter by due date (exact or range)
- ✅ Sort results (by field and direction)
- ✅ Paginate results (page, page_size)
- ✅ Combine search + filters + sort + pagination
- ✅ All authenticated users can search/filter all tasks

**Design decisions**:
- Search: Partial match, case-insensitive, SQL LIKE/ILIKE
- Tags: Contains any tag (OR logic)
- Due date: Support exact and range
- Sort default: `created_at DESC`
- Pagination: page=1, page_size=20, max=100
- Response: Include pagination metadata

All requirements from `docs/requirements.md` §4 and `docs/technical-specs.md` §3.4 are accounted for.
