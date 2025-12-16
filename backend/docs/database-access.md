# Database Access Guide

## Database Location

**For Docker Compose (PostgreSQL):**
- Database runs in Docker container: `task-tracker-db`
- Host: `localhost` (or `database` from within Docker network)
- Port: `5432`
- Database name: `task_tracker` (default)
- Username: `tasktracker` (default)
- Password: `changeme` (default, set via `POSTGRES_PASSWORD` env var)

**For Manual Setup (SQLite):**
- Database file located at: `backend/task_tracker.db`
- Or relative to the backend directory: `./task_tracker.db`

## Accessing the Database

### Option 1: Using Adminer Web Interface (PostgreSQL - Docker Compose)

**When using Docker Compose**, you can access the database via Adminer web interface:

1. Start services with Docker Compose:
   ```bash
   docker compose up
   ```

2. Open Adminer in your browser:
   - **URL**: http://localhost:8888

3. Login with PostgreSQL credentials:
   - **System**: PostgreSQL
   - **Server**: `database` (or `localhost` if connecting from host)
   - **Username**: `tasktracker` (or value from `POSTGRES_USER` env var)
   - **Password**: `changeme` (or value from `POSTGRES_PASSWORD` env var)
   - **Database**: `task_tracker` (or value from `POSTGRES_DB` env var)

4. Once logged in, you can:
   - Browse tables and data
   - Run SQL queries
   - Export/import data
   - View table structures

**Note**: Adminer is only available when using Docker Compose. For SQLite or manual PostgreSQL setups, use other options below.

### Option 2: Using SQLite Command Line

```bash
cd backend
sqlite3 task_tracker.db
```

Then you can run SQL queries:
```sql
-- List all tables
.tables

-- View users
SELECT * FROM users;

-- View tasks
SELECT * FROM tasks;

-- View attachments
SELECT * FROM attachments;

-- Exit
.quit
```

### Option 3: Using PostgreSQL Command Line (Docker Compose)

**When using Docker Compose with PostgreSQL:**

```bash
# Connect to PostgreSQL container
docker exec -it task-tracker-db psql -U tasktracker -d task_tracker
```

Then you can run SQL queries:
```sql
-- List all tables
\dt

-- View users
SELECT * FROM users;

-- View tasks
SELECT * FROM tasks;

-- View attachments
SELECT * FROM attachments;

-- Exit
\q
```

### Option 4: Using Python Script

```python
from infrastructure.database import SessionLocal
from domain.models.user import User
from domain.models.task import Task

db = SessionLocal()

# Get all users
users = db.query(User).all()
for user in users:
    print(f"User: {user.username} ({user.email})")

# Get all tasks
tasks = db.query(Task).all()
for task in tasks:
    print(f"Task: {task.title} (owner: {task.owner_user_id})")

db.close()
```

### Option 5: Using Database Browser Tools

You can use GUI tools like:
- **DB Browser for SQLite** (https://sqlitebrowser.org/) - For SQLite files
- **TablePlus** (https://tableplus.com/) - Supports both PostgreSQL and SQLite
- **DBeaver** (https://dbeaver.io/) - Universal database tool
- **pgAdmin** (https://www.pgadmin.org/) - PostgreSQL-specific tool

**For SQLite:**
- Open the file: `backend/task_tracker.db`

**For PostgreSQL (Docker Compose):**
- Host: `localhost`
- Port: `5433` (host port; container uses 5432 internally)
- Database: `task_tracker`
- Username: `tasktracker`
- Password: `changeme` (or value from `POSTGRES_PASSWORD` env var)

**Note**: The container uses port 5432 internally, but it's mapped to port 5433 on the host to avoid conflicts with other PostgreSQL instances.

## Common Queries

### View All Users
```sql
SELECT id, username, email, created_at FROM users;
```

### View All Tasks
```sql
SELECT id, title, status, priority, due_date, owner_user_id, created_at 
FROM tasks 
ORDER BY created_at DESC;
```

### View Tasks with Reminders
```sql
SELECT id, title, due_date, reminder_sent_at 
FROM tasks 
WHERE reminder_sent_at IS NOT NULL
ORDER BY reminder_sent_at DESC;
```

### View Attachments
```sql
SELECT id, task_id, filename, file_size, uploaded_at 
FROM attachments 
ORDER BY uploaded_at DESC;
```

### Count Records
```sql
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM tasks) as total_tasks,
    (SELECT COUNT(*) FROM attachments) as total_attachments;
```

## Creating Users

### Method 1: Using Registration API Endpoint

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "email": "myuser@example.com",
    "password": "mypassword123"
  }'
```

### Method 2: Using Python Script

```bash
cd backend
python scripts/create_user.py myuser myuser@example.com mypassword123
```

### Method 3: Direct SQL (Not Recommended)

```sql
-- Hash password first (use Python bcrypt)
-- Then insert:
INSERT INTO users (username, email, hashed_password, created_at, updated_at)
VALUES ('myuser', 'myuser@example.com', '<hashed_password>', datetime('now'), datetime('now'));
```

## Database Schema

### Users Table
- `id` (INTEGER, PRIMARY KEY)
- `username` (VARCHAR, UNIQUE)
- `email` (VARCHAR, UNIQUE)
- `hashed_password` (VARCHAR)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

### Tasks Table
- `id` (INTEGER, PRIMARY KEY)
- `title` (VARCHAR)
- `description` (TEXT)
- `status` (VARCHAR)
- `priority` (VARCHAR)
- `due_date` (DATETIME)
- `tags` (VARCHAR, JSON string)
- `owner_user_id` (INTEGER, FOREIGN KEY)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)
- `reminder_sent_at` (DATETIME)

### Attachments Table
- `id` (INTEGER, PRIMARY KEY)
- `task_id` (INTEGER, FOREIGN KEY)
- `filename` (VARCHAR)
- `file_size` (INTEGER)
- `storage_path` (VARCHAR)
- `content_type` (VARCHAR)
- `uploaded_at` (DATETIME)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

## Backup Database

```bash
# Copy database file
cp backend/task_tracker.db backend/task_tracker.db.backup

# Or use SQLite backup command
sqlite3 backend/task_tracker.db ".backup 'backend/task_tracker.db.backup'"
```

## Reset Database

**Warning**: This will delete all data!

```bash
cd backend
rm task_tracker.db
python -c "from infrastructure.database import init_db; init_db()"
```

Or in Python:
```python
from infrastructure.database import engine, Base
from domain.models import User, Task, Attachment

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Recreate tables
Base.metadata.create_all(bind=engine)
```
