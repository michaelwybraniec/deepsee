# Task ID: 5.4
# Title: Implement filters, sorting, and pagination
# Status: [x] Completed
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement filtering by status, priority, tags, and due date, plus sorting and pagination for task listings, according to the designed API from task 5.2, per `docs/requirements.md` section "4. Search & Filtering" and `docs/technical-specs.md` section "3.4 Search & Filtering".

**Step-by-step:**
1. Review API design from task 5.2 (query parameters: `status`, `priority`, `tags`, `due_date`, `sort`, `page`, `page_size`).
2. Update search/list tasks use-case (e.g., `backend/application/tasks/search_tasks.py`):
   - Accept query parameters: `status`, `priority`, `tags`, `due_date`, `sort`, `page`, `page_size`.
   - Build dynamic WHERE clauses for filters:
     - `status`: `status = 'status_value'` (exact match).
     - `priority`: `priority = 'priority_value'` (exact match).
     - `tags`: `tags @> ARRAY['tag1']` (PostgreSQL JSONB) or `tags CONTAINS 'tag'` (tasks containing any specified tag).
     - `due_date`: `due_date = 'date'` (exact) or `due_date BETWEEN 'from' AND 'to'` (range if `due_date_from`/`due_date_to` provided).
   - Apply sorting: `ORDER BY field ASC/DESC` (default: `created_at DESC`).
   - Apply pagination: `LIMIT page_size OFFSET (page - 1) * page_size`.
   - Get total count: `SELECT COUNT(*) FROM tasks WHERE ...` (for pagination metadata).
   - Return tasks with pagination metadata: `{"tasks": [...], "pagination": {"page": 1, "page_size": 20, "total": 100, "total_pages": 5}}`.
3. Update API endpoint `GET /api/tasks`:
   - Accept query parameters: `status`, `priority`, `tags`, `due_date`, `sort`, `page`, `page_size`.
   - Validate parameters (enum values for status/priority, date format for due_date, integer for page/page_size).
   - Pass parameters to search use-case.
   - Return 200 OK with filtered/sorted/paginated results.
4. Implement filter logic:
   - Use query builder for dynamic WHERE clauses (SQLAlchemy `.filter()`, Django ORM `.filter()`).
   - Validate enum values (status, priority) against allowed values.
   - Validate date formats (due_date, due_date_from, due_date_to).
   - Handle tags as array (parse comma-separated or array format).
5. Implement sorting logic:
   - Parse `sort` parameter (e.g., `sort=due_date:asc`, `sort=priority:desc`).
   - Validate sort field (allow: `due_date`, `priority`, `created_at`, `updated_at`, `title`).
   - Validate sort direction (`asc`, `desc`).
   - Apply `ORDER BY` clause (default: `created_at DESC`).
6. Implement pagination logic:
   - Parse `page` (default 1) and `page_size` (default 20, max 100).
   - Calculate offset: `(page - 1) * page_size`.
   - Apply `LIMIT` and `OFFSET` to query.
   - Get total count (separate query or window function).
   - Calculate total_pages: `ceil(total / page_size)`.
7. Write integration tests:
   - Test filtering by status (verify only tasks with matching status returned).
   - Test filtering by priority (verify only tasks with matching priority returned).
   - Test filtering by tags (verify tasks containing any specified tag returned).
   - Test filtering by due date (verify exact date and range filters work).
   - Test filter combinations (e.g., `status=todo&priority=high` - verify both conditions applied).
   - Test sorting (verify results sorted by specified field and direction).
   - Test pagination (verify correct page returned, total count correct, total_pages calculated).
   - Test search + filters + sort + pagination combined (verify all work together).

**Implementation hints:**
- Use query builder pattern for dynamic filtering (SQLAlchemy query builder, Django ORM queryset).
- Place filter/sort/pagination logic in repository or use-case (e.g., `backend/application/tasks/search_tasks.py`).
- Use parameterized queries to prevent SQL injection.
- Validate all query parameters (enum values, date formats, integers).
- Consider database indexes on filterable fields (status, priority, due_date, tags) for performance.

## Dependencies
- [x] Task ID: 5.2 (API design must be complete)

## Testing Instructions
- Integration tests (API + DB):
  - Filtering by each field and combinations (status, priority, tags, due date, combinations).
  - Sorting in at least one direction (asc, desc, default sort).
  - Pagination over multiple pages (verify correct page, total count, total_pages).
  - Test search + filters + sort + pagination combined (verify all work together).
- Manual test: Use API client to test filters, sorting, and pagination, verify results.

## Security Review
- Ensure filters respect auth rules and only operate on permitted task sets:
  - All authenticated users can filter all tasks (no ownership filter for reads per requirements).
  - Query parameters are validated (prevent SQL injection, validate enum values, validate date formats).
  - Pagination limits enforced (max page_size to prevent DoS).

## Risk Assessment
- Incorrect filter/sort/pagination could misrepresent tasks and confuse users.
- SQL injection vulnerability if parameters not properly validated/parameterized.
- Performance issues if queries not optimized (missing indexes, inefficient pagination).

## Acceptance Criteria
- [x] Filters for status, priority, tags, and due date work as specified (exact match for status/priority, contains for tags, exact/range for due date).
- [x] Sorting is applied consistently based on query parameters (field and direction, default sort).
- [x] Pagination returns correct pages of results (correct page, total count, total_pages calculated).
- [x] All query parameters are validated (enum values, date formats, integers).
- [x] Tests for filters, sorting, and pagination are passing (individual and combined).

## Definition of Done
- [ ] Filter/sort/pagination logic implemented in list endpoint (use-case and API handler).
- [ ] Filter logic implemented (status, priority, tags, due date - dynamic WHERE clauses).
- [ ] Sorting logic implemented (parse sort parameter, validate field/direction, apply ORDER BY).
- [ ] Pagination logic implemented (parse page/page_size, apply LIMIT/OFFSET, calculate total/total_pages).
- [ ] Query parameters validated (enum values, date formats, integers, max page_size).
- [ ] Tests covering common combinations implemented and passing (filters, sorting, pagination, combined).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Integration tests validate correct filtering, sorting, and pagination (all test cases pass).
- **Observable Outcomes**: Endpoint responds correctly to filter/sort/pagination parameters, results are correct, pagination metadata is accurate.

## Notes
Completes the "Search & Filtering" requirement from the assignment. This task builds on task 5.3 (search) and combines all query parameters.

**Completed**: 
- All filters implemented: status, priority, tags, due_date (exact and range)
- Sorting implemented with field and direction validation, default sort (created_at DESC)
- Pagination implemented with page, page_size, total count, and total_pages calculation
- Query parameter validation (FastAPI Query with constraints)
- Tags filter works with SQLite JSON string storage (Python filtering)
- All features work together (search + filters + sort + pagination)

## Strengths
Provides a robust and user-friendly way to explore the task list. Enables efficient task discovery and management.

## Sub-tasks (Children)
- [ ] Review API design from task 5.2 (query parameters: status, priority, tags, due_date, sort, page, page_size).
- [ ] Implement filter logic for status, priority, tags, due date (dynamic WHERE clauses, parameterized queries).
- [ ] Implement sorting logic (parse sort parameter, validate field/direction, apply ORDER BY with default).
- [ ] Implement pagination logic (parse page/page_size, apply LIMIT/OFFSET, calculate total/total_pages).
- [ ] Update API endpoint `GET /api/tasks` to accept all query parameters and validate them.
- [ ] Write integration tests (filters individually, combinations, sorting, pagination, all combined).
- [ ] Test manually with API client to verify filter/sort/pagination behavior.

## Completed
[x] Completed


