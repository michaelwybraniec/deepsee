# Task ID: 5.3
# Title: Implement search by title and description
# Status: [x] Completed
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 3h

## Description
Implement backend logic to search tasks by title and description according to the designed API from task 5.2, per `docs/requirements.md` section "4. Search & Filtering" and `docs/technical-specs.md` section "3.4 Search & Filtering".

**Step-by-step:**
1. Review API design from task 5.2 (query parameter `q` searches both title and description).
2. Update list tasks use-case (e.g., `backend/application/tasks/search_tasks.py` or extend `list_tasks.py`):
   - Accept query parameters: `q` (search term), plus other filters (from task 5.4).
   - If `q` provided: build query with `(title ILIKE '%q%' OR description ILIKE '%q%')` (case-insensitive partial match).
   - If `q` not provided: return all tasks (no search filter).
   - Combine with other filters (status, priority, tags, due date) if provided.
   - Apply sorting and pagination (from task 5.4).
   - Return matching tasks with pagination metadata.
3. Update API endpoint `GET /api/tasks`:
   - Accept query parameter `q` (string, optional).
   - Pass `q` to search use-case.
   - Return 200 OK with search results (tasks array, pagination metadata).
4. Implement search logic:
   - Use SQL/ORM query builder for dynamic WHERE clause.
   - For PostgreSQL: `(title ILIKE '%term%' OR description ILIKE '%term%')`.
   - For MySQL: `(title LIKE '%term%' OR description LIKE '%term%')` (case-insensitive).
   - Escape special characters in search term to prevent SQL injection (use parameterized queries).
5. Write integration tests:
   - Test search by title (verify tasks with matching title returned).
   - Test search by description (verify tasks with matching description returned).
   - Test search matches both title and description (OR logic - task matches if either field contains term).
   - Test case-insensitive search (verify "Task" matches "task").
   - Test partial match (verify "task" matches "My Task Title").
   - Test empty search term (verify all tasks returned, no filter applied).
   - Test search combined with filters (e.g., search + status filter).

**Implementation hints:**
- Use parameterized queries to prevent SQL injection (never concatenate user input into SQL).
- Place search logic in repository or use-case (e.g., `backend/application/tasks/search_tasks.py`).
- Use query builder pattern (SQLAlchemy `.filter()`, Django ORM `.filter()`) for dynamic queries.
- Consider full-text search for better performance (PostgreSQL `tsvector`, Elasticsearch) - optional enhancement.

## Dependencies
- [x] Task ID: 5.2 (API design must be complete)

## Testing Instructions
- Integration tests (API + DB):
  - Search by title returns matching tasks (verify tasks with matching title in results).
  - Search by description returns matching tasks (verify tasks with matching description in results).
  - Search matches both title and description (OR logic - task appears if either field matches).
  - Test case-insensitive search (verify "Task" matches "task", "TASK").
  - Test partial match (verify "task" matches "My Task Title", "Task Management").
  - Test empty search term (verify all tasks returned, no search filter applied).
  - Test search combined with other filters (e.g., `q=task&status=todo` - verify both conditions applied).
- Manual test: Use API client to search tasks, verify results match search term.

## Security Review
- Ensure search does not bypass auth or expose tasks the user should not see:
  - All authenticated users can search all tasks (no ownership filter for reads per requirements).
  - Query parameters are validated (prevent SQL injection with parameterized queries).
  - Search term is sanitized (escape special characters, limit length if needed).

## Risk Assessment
- Inaccurate search could frustrate users and hide relevant tasks.
- SQL injection vulnerability if search term not properly parameterized.
- Performance issues if search not optimized (full table scan without indexes).

## Acceptance Criteria
- [x] Search parameters for title and description are handled by the list endpoint (`GET /api/tasks?q=term`).
- [x] Search uses OR logic (task matches if title OR description contains search term).
- [x] Search is case-insensitive (e.g., "Task" matches "task").
- [x] Search supports partial matching (e.g., "task" matches "My Task Title").
- [x] Tests confirm correct search behavior for both fields (title, description, combined, case-insensitive, partial match).

## Definition of Done
- [ ] Search logic implemented (query builder with title/description ILIKE conditions).
- [ ] API endpoint accepts `q` parameter and passes to use-case.
- [ ] Search use-case implemented (build query with search conditions, combine with other filters).
- [ ] Parameterized queries used (prevent SQL injection).
- [ ] Tests added and passing (search by title, description, combined, case-insensitive, partial match, empty term).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Search tests pass, with correct matches returned (tasks with matching title/description appear in results).
- **Observable Outcomes**: Endpoint responds correctly to search queries, results match search term, case-insensitive and partial matching work.

## Notes
Forms the base of the "Search tasks by title or description" requirement. Filters, sorting, and pagination are implemented in task 5.4.

**Completed**: 
- Search use case implemented in `backend/application/tasks/search_tasks.py`
- Search logic: OR condition on title and description, case-insensitive partial match using SQLAlchemy `ilike`
- API endpoint updated to accept `q` parameter
- Parameterized queries used (SQLAlchemy handles SQL injection prevention)
- Integrated with filters, sorting, and pagination (all in one use case)

## Strengths
Improves usability of the task list view. Provides foundation for combined search + filter operations.

## Sub-tasks (Children)
- [ ] Review API design from task 5.2 (query parameter `q` for search).
- [ ] Update list tasks use-case to accept `q` parameter and build search query.
- [ ] Implement search logic (title/description ILIKE with OR condition, case-insensitive, partial match).
- [ ] Update API endpoint `GET /api/tasks` to accept `q` query parameter.
- [ ] Use parameterized queries to prevent SQL injection.
- [ ] Write integration tests (search by title, description, combined, case-insensitive, partial match, empty term).
- [ ] Test manually with API client to verify search behavior.

## Completed
[x] Completed


