# Search & Filter API

**API Endpoints & Schemas**: See [API Documentation](api.md) (Swagger UI: `/docs`, ReDoc: `/redoc`)

## Implementation Notes

**Tags Filtering**: Tags stored as JSON string in SQLite. Filtering uses Python logic to parse JSON and match tags.

**Performance**: Indexes on `status`, `priority`, `due_date`, `title`. Max `page_size` is 100 to prevent DoS.

**Security**: Parameterized queries (SQLAlchemy), parameter validation, no ownership filter (all authenticated users can search/filter all tasks).
