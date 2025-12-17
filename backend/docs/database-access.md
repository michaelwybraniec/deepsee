# Database Access Guide

## Connection Details

**PostgreSQL (Docker Compose):**
- Host: `database` (from Docker network) or `localhost` (from host)
- Port: `5432`
- Database: `task_tracker`
- Username: `tasktracker`
- Password: `changeme` (set via `POSTGRES_PASSWORD` env var)

**SQLite (Manual Setup):**
- File: `backend/task_tracker.db`

## Access Methods

### pgAdmin Web UI

1. **Access**: http://localhost:8888
2. **Login**: `admin@example.com` / `admin`
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
