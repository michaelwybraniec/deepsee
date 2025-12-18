# Database Access Guide

## Connection Details

**PostgreSQL (Docker Compose):**

- Host: `database` (from Docker network) or `localhost` (from host)
- Port: `5432`
- Database: `task_tracker`
- Username: `tasktracker`
- Password: `changeme` (set via `POSTGRES_PASSWORD` env var)
- **SSL**: Disabled (`?sslmode=disable`) - Docker PostgreSQL doesn't have SSL enabled by default

**SQLite (Manual Setup):**

- File: `backend/task_tracker.db`

## Access Methods

### pgAdmin Web UI

1. **Access**: <http://localhost:8888>
2. **Login**: `admin`@`example.com` / `admin`
3. **Connect to Database**:
   - Right-click "Servers" → "Register" → "Server"
   - **Connection tab**:
     - Host: `database`
     - Port: `5432`
     - Database: `task_tracker`
     - Username: `tasktracker`
     - Password: `changeme`
4. **View Data**: Right-click table → "View/Edit Data" → "All Rows"
5. **Run Queries**: Right-click database → "Query Tool" → Write SQL → Press `F5`

### Console/Command Line

**Interactive:**

```bash
docker exec -it task-tracker-db psql -U tasktracker -d task_tracker
```

**Single Query:**

```bash
docker exec task-tracker-db psql -U tasktracker -d task_tracker -c "SELECT * FROM users;"
```

**Useful Commands:**

```sql
\dt          -- List tables
\d table     -- Describe table
\q           -- Exit
```

## Maintenance Scripts

**Seed Sample Data:**

```bash
docker exec task-tracker-api python scripts/seed_tasks.py --count 50 --user-id 1
```

**Create User:**

```bash
docker exec task-tracker-api python scripts/create_user.py username email password
```

**Reset Password:**

```bash
docker exec task-tracker-api python scripts/reset_password.py username new_password
```

**Reset Database (Drop all tables and data):**

```bash
# Drop and recreate all tables (with confirmation)
docker exec task-tracker-api python scripts/reset_database.py

# Drop without recreating
docker exec task-tracker-api python scripts/reset_database.py --no-recreate

# Skip confirmation (use with caution!)
docker exec task-tracker-api python scripts/reset_database.py --force
```

## Troubleshooting

### SSL Connection Error

**Error:** `pq: SSL is not enabled on the server`

**Solution:** The Docker PostgreSQL container doesn't have SSL enabled. The connection string in `docker-compose.yml` includes `?sslmode=disable` to handle this.

If you're connecting manually (e.g., from host machine), add `?sslmode=disable` to your connection string:

```bash
# Correct format
DATABASE_URL=postgresql://tasktracker:changeme@localhost:5432/task_tracker?sslmode=disable
```

**Note:** For production environments, you should enable SSL on PostgreSQL and use appropriate SSL mode (`require`, `verify-ca`, or `verify-full`).

### Connection Refused

If you can't connect from the host machine:

1. **Check if database port is exposed:** The database port is not exposed to the host by default (internal Docker network only).
2. **Use pgAdmin:** Access via <http://localhost:8888> instead.
3. **Or use Docker exec:** `docker exec -it task-tracker-db psql -U tasktracker -d task_tracker`

### Database Not Initialized

If tables don't exist:

```bash
# Initialize schema
docker exec task-tracker-api python -c "from infrastructure.database import init_db; init_db()"
```

### Data Persistence

Database data is stored in the `postgres_data` Docker volume and persists across container restarts. To completely remove data:

```bash
docker compose down -v  # Removes volumes
```
