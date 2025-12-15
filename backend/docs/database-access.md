# Database Access Guide

## Database Location

The database is a SQLite file located at:
```
backend/task_tracker.db
```

Or relative to the backend directory:
```
./task_tracker.db
```

## Accessing the Database

### Option 1: Using SQLite Command Line

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

### Option 2: Using Python Script

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

### Option 3: Using Database Browser Tools

You can use GUI tools like:
- **DB Browser for SQLite** (https://sqlitebrowser.org/)
- **TablePlus** (https://tableplus.com/)
- **DBeaver** (https://dbeaver.io/)

Open the file: `backend/task_tracker.db`

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
