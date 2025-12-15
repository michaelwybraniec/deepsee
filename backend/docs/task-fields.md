# Task Field Requirements

This document lists all task fields extracted from the project requirements.

## Source References
- `docs/requirements.md` section "2. Task Management": "Fields: title, description, status, priority, due date, tags."
- `docs/technical-specs.md` section "3.2 Task Management": "Title, Description, Status, Priority, Due date, Tags."

## Required Fields (from Requirements)

### 1. title
- **Type**: string
- **Required**: Yes
- **Description**: Task title
- **Source**: `docs/requirements.md` §2, `docs/technical-specs.md` §3.2

### 2. description
- **Type**: string (text)
- **Required**: No (optional)
- **Description**: Task description
- **Source**: `docs/requirements.md` §2, `docs/technical-specs.md` §3.2

### 3. status
- **Type**: string/enum
- **Required**: No (optional)
- **Description**: Task status (e.g., "todo", "in_progress", "done")
- **Source**: `docs/requirements.md` §2, `docs/technical-specs.md` §3.2
- **Note**: Specific values are design choice (not specified in requirements)

### 4. priority
- **Type**: string/enum
- **Required**: No (optional)
- **Description**: Task priority (e.g., "low", "medium", "high")
- **Source**: `docs/requirements.md` §2, `docs/technical-specs.md` §3.2
- **Note**: Specific values are design choice (not specified in requirements)

### 5. due_date
- **Type**: date/datetime
- **Required**: No (optional)
- **Description**: Task due date
- **Source**: `docs/requirements.md` §2, `docs/technical-specs.md` §3.2

### 6. tags
- **Type**: array of strings
- **Required**: No (optional)
- **Description**: Task tags
- **Source**: `docs/requirements.md` §2, `docs/technical-specs.md` §3.2

## System Fields (Not from Requirements)

These fields are required for system functionality but are not part of the original requirements:

### id
- **Type**: integer (primary key)
- **Required**: Yes (auto-generated)
- **Description**: Unique task identifier
- **Source**: System requirement (not in original requirements)

### owner_user_id
- **Type**: integer (foreign key to users table)
- **Required**: Yes
- **Description**: User who owns the task (for authorization: "modify only own data")
- **Source**: System requirement for authorization (not in original requirements)

### created_at
- **Type**: timestamp
- **Required**: Yes (auto-set)
- **Description**: Task creation timestamp
- **Source**: System requirement (not in original requirements)

### updated_at
- **Type**: timestamp
- **Required**: Yes (auto-updated)
- **Description**: Task last update timestamp
- **Source**: System requirement (not in original requirements)

## Summary

**Required fields from requirements**: title (required), description (optional), status (optional), priority (optional), due_date (optional), tags (optional)

**System fields**: id, owner_user_id, created_at, updated_at

All fields from requirements are accounted for. No missing fields, no extra fields beyond system requirements.
