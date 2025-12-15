# Task ID: 5.2
# Title: Design search, filter, sort, and pagination API
# Status: [x] Completed
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 2h

## Description
Design API query parameters and internal logic for searching by title/description, filtering by status/priority/tags/due date, sorting, and paginating tasks, based on requirements from task 5.1.

**Step-by-step:**
1. Review search/filter requirements from task 5.1 (search by title/description, filters, sorting, pagination).
2. Design query parameters for `GET /api/tasks`:
   - **Search**: `q` (string, optional) - searches in both title and description (OR logic, case-insensitive partial match).
   - **Filters**:
     - `status` (string/enum, optional) - exact match (e.g., "todo", "in_progress", "done").
     - `priority` (string/enum, optional) - exact match (e.g., "low", "medium", "high").
     - `tags` (string or array, optional) - tasks containing any of the specified tags (e.g., `tags=urgent,important` or `tags[]=urgent&tags[]=important`).
     - `due_date` (date or range, optional) - exact date or range (e.g., `due_date=2024-01-01` or `due_date_from=2024-01-01&due_date_to=2024-12-31`).
   - **Sorting**: `sort` (string, optional) - field and direction (e.g., `sort=due_date:asc`, `sort=priority:desc`, `sort=created_at:desc`). Default: `created_at:desc`.
   - **Pagination**: `page` (integer, optional, default 1), `page_size` (integer, optional, default 20, max 100).
3. Design internal query logic:
   - Build SQL/ORM query with WHERE clauses for filters:
     - `q`: `(title ILIKE '%q%' OR description ILIKE '%q%')` (PostgreSQL) or `(title LIKE '%q%' OR description LIKE '%q%')` (case-insensitive).
     - `status`: `status = 'status_value'`.
     - `priority`: `priority = 'priority_value'`.
     - `tags`: `tags @> ARRAY['tag1', 'tag2']` (PostgreSQL JSONB) or `tags CONTAINS 'tag'` (depending on storage).
     - `due_date`: `due_date = 'date'` or `due_date BETWEEN 'from' AND 'to'`.
   - Apply sorting: `ORDER BY field ASC/DESC` (default: `created_at DESC`).
   - Apply pagination: `LIMIT page_size OFFSET (page - 1) * page_size`.
   - Return total count for pagination metadata: `SELECT COUNT(*) FROM tasks WHERE ...`.
4. Design response format:
   - `{"tasks": [...], "pagination": {"page": 1, "page_size": 20, "total": 100, "total_pages": 5}}`.
5. Document design:
   - Create `backend/docs/search-filter-api-design.md` or add to code comments.
   - Document query parameters, formats, examples, and internal logic.

**Implementation hints:**
- Use query builder pattern (SQLAlchemy query builder, Django ORM queryset) for dynamic filtering.
- Place query logic in repository or use-case (e.g., `backend/application/tasks/search_tasks.py`).
- Use parameterized queries to prevent SQL injection.
- Consider full-text search for better search performance (PostgreSQL `tsvector`, Elasticsearch, etc.) - optional enhancement.

## Dependencies
- [x] Task ID: 5.1 (Search/filter requirements must be confirmed)

## Testing Instructions
- N/A for design task. Verify that the design covers all required combinations and is documented.
- Review design document to ensure all requirements from task 5.1 are addressed.

## Security Review
- Ensure design respects auth rules and does not allow unauthorized data leakage:
  - All authenticated users can search/filter all tasks (no ownership filter for reads).
  - Query parameters are validated (prevent SQL injection, validate enum values, validate date formats).
  - Pagination limits enforced (max page_size to prevent DoS).

## Risk Assessment
- Poor design may make implementation or usage confusing.
- Missing parameter validation can cause errors or security issues.
- Inefficient query design can cause performance problems.

## Acceptance Criteria
- [x] Query parameter scheme is documented (e.g. `q`, `status`, `priority`, `tags`, `due_date`, `sort`, `page`, `page_size`) with formats and examples.
- [x] Internal filter/sort/pagination approach is described (SQL/ORM query building, parameter handling).
- [x] Response format is documented (tasks array, pagination metadata).
- [x] Design is implementable (clear enough to code without guesswork).

## Definition of Done
- [ ] Design documented in code comments or a short note (file committed or documented).
- [ ] Query parameters, formats, and examples documented.
- [ ] Internal query logic described (filtering, sorting, pagination).
- [ ] Response format documented.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Design doc exists and is referenced by implementation (code files reference design doc).
- **Observable Outcomes**: Design document shows complete API contract and internal logic.

## Notes
This decouples deciding the interface from actual coding work. The actual implementation happens in tasks 5.3 and 5.4.

**Completed**: Created `backend/docs/search-filter-api-design.md` documenting:
- Query parameters: `q` (search), `status`, `priority`, `tags`, `due_date`, `due_date_from`, `due_date_to`, `sort`, `page`, `page_size`
- Response format with pagination metadata
- Internal query building logic (SQLAlchemy query builder)
- Parameter validation rules
- Example requests and error responses
- Security considerations (SQL injection prevention, parameter validation, pagination limits)

## Strengths
Provides a clear contract for both backend code and frontend consumers. Ensures consistent API design before implementation.

## Sub-tasks (Children)
- [ ] Review search/filter requirements from task 5.1 (search, filters, sorting, pagination).
- [ ] Decide on query parameter names and formats (`q`, `status`, `priority`, `tags`, `due_date`, `sort`, `page`, `page_size`).
- [ ] Design search logic (title/description partial match, case-insensitive).
- [ ] Design filter logic (status, priority, tags, due date - exact match or range).
- [ ] Design sorting logic (field and direction, default sort).
- [ ] Design pagination logic (page, page_size, total count, total_pages).
- [ ] Design response format (tasks array, pagination metadata).
- [ ] Document design (query parameters, internal logic, examples) in code comments or design doc.

## Completed
[x] Completed


