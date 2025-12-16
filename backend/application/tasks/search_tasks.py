"""Search and list tasks use case with search, filters, sorting, and pagination."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
import json
import math

from domain.models.task import Task
from application.tasks.schemas import TaskResponse
from application.tasks.repository import TaskRepository


def search_tasks(
    db: Session,
    q: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date: Optional[datetime] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    owner_user_id: Optional[int] = None,
    sort: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
) -> Dict[str, Any]:
    """
    Search and list tasks with filters, sorting, and pagination.
    
    All authenticated users can search/filter all tasks (no ownership filter for reads).
    
    Args:
        db: Database session
        q: Search term (searches in title and description)
        status: Filter by status (exact match)
        priority: Filter by priority (exact match)
        tags: Filter by tags (tasks containing any of the specified tags)
        due_date: Filter by exact due date
        due_date_from: Filter by due date range (start)
        due_date_to: Filter by due date range (end)
        owner_user_id: Filter by task owner user ID
        sort: Sort field and direction (e.g., "due_date:asc", "priority:desc")
        page: Page number (1-indexed)
        page_size: Number of items per page (max 100)
    
    Returns:
        Dictionary with "tasks" and "pagination" keys matching PaginatedTaskResponse schema
    """
    # Validate and limit page_size
    page_size = min(page_size, 100)  # Max 100 to prevent DoS
    page = max(page, 1)  # Min 1
    
    # Start with base query - eager load owner relationship for username
    query = db.query(Task).options(joinedload(Task.owner))
    
    # Apply search (q parameter)
    if q:
        search_term = f"%{q}%"
        # Build OR condition for title and description
        conditions = [Task.title.ilike(search_term)]
        # Add description condition only if description field exists (not None check per row)
        # SQLAlchemy will handle None values in description field
        conditions.append(Task.description.ilike(search_term))
        query = query.filter(or_(*conditions))
    
    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    if owner_user_id is not None:
        # Ensure owner_user_id is an integer for comparison
        # Note: owner_user_id could be 0, so we check for None explicitly
        owner_id = int(owner_user_id)
        # Apply filter directly
        query = query.filter(Task.owner_user_id == owner_id)
    
    # Tags filter will be applied in Python after fetching (for SQLite JSON string storage)
    # Note: This is less efficient but works for SQLite. For PostgreSQL, could use JSONB operators.
    
    if due_date:
        query = query.filter(Task.due_date == due_date)
    
    if due_date_from:
        query = query.filter(Task.due_date >= due_date_from)
    
    if due_date_to:
        query = query.filter(Task.due_date <= due_date_to)
    
    # Apply sorting (before getting count, for consistency)
    if sort:
        # Parse sort parameter (format: "field:direction")
        parts = sort.split(":")
        if len(parts) == 2:
            sort_field, sort_direction = parts[0].strip(), parts[1].strip().lower()
            
            # Validate sort field
            allowed_fields = ["due_date", "priority", "created_at", "updated_at", "title"]
            if sort_field in allowed_fields:
                sort_attr = getattr(Task, sort_field)
                if sort_direction == "desc":
                    query = query.order_by(sort_attr.desc())
                else:
                    query = query.order_by(sort_attr.asc())
            else:
                # Invalid field, use default
                query = query.order_by(Task.created_at.desc())
        else:
            # Invalid format, use default
            query = query.order_by(Task.created_at.desc())
    else:
        # Default sort: newest first
        query = query.order_by(Task.created_at.desc())
    
    # For tags filter with SQLite JSON storage, we need to filter in Python
    # This requires fetching all matching tasks first, then filtering by tags, then paginating
    if tags and len(tags) > 0:
        # Fetch all tasks matching other filters (before tags filter)
        all_tasks = query.all()
        
        # Filter by tags in Python
        filtered_tasks = []
        for task in all_tasks:
            if task.tags:
                try:
                    task_tags = json.loads(task.tags) if isinstance(task.tags, str) else task.tags
                    if isinstance(task_tags, list):
                        # Check if any task tag matches any filter tag
                        if any(tag in task_tags for tag in tags):
                            filtered_tasks.append(task)
                except (json.JSONDecodeError, TypeError):
                    pass
        
        # Get total count after tags filter
        total = len(filtered_tasks)
        
        # Apply sorting to filtered list
        if sort:
            parts = sort.split(":")
            if len(parts) == 2:
                sort_field, sort_direction = parts[0].strip(), parts[1].strip().lower()
                allowed_fields = ["due_date", "priority", "created_at", "updated_at", "title"]
                if sort_field in allowed_fields:
                    reverse = (sort_direction == "desc")
                    filtered_tasks.sort(key=lambda t: getattr(t, sort_field) or "", reverse=reverse)
        else:
            # Default sort: newest first
            filtered_tasks.sort(key=lambda t: t.created_at or "", reverse=True)
        
        # Apply pagination
        offset = (page - 1) * page_size
        tasks = filtered_tasks[offset:offset + page_size]
        
        # Verify and enforce owner filter if it was applied
        if owner_user_id is not None:
            expected_owner = int(owner_user_id)
            # Always re-filter in Python to ensure correctness (safety measure)
            tasks = [t for t in tasks if t.owner_user_id == expected_owner]
    else:
        # No tags filter - can use SQL pagination
        # Get total count (before pagination)
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        tasks = query.offset(offset).limit(page_size).all()
        
        # Verify and enforce owner filter if it was applied
        if owner_user_id is not None:
            expected_owner = int(owner_user_id)
            # Always re-filter in Python to ensure correctness (safety measure)
            tasks = [t for t in tasks if t.owner_user_id == expected_owner]
    
    # Convert to response models
    result = []
    for task in tasks:
        # Convert tags JSON string back to list for response
        tags_list = None
        if task.tags:
            try:
                tags_list = json.loads(task.tags) if isinstance(task.tags, str) else task.tags
            except (json.JSONDecodeError, TypeError):
                tags_list = []
        
        result.append(TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            tags=tags_list,
            owner_user_id=task.owner_user_id,
            owner_username=task.owner.username if task.owner else None,
            created_at=task.created_at,
            updated_at=task.updated_at
        ))
    
    # Return dictionary matching PaginatedTaskResponse schema
    return {
        "tasks": result,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": math.ceil(total / page_size) if page_size > 0 else 0
        }
    }
