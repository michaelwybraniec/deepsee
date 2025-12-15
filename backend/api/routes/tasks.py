"""Task API routes."""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from infrastructure.database import get_db
from domain.models.user import User
from api.middleware.auth import get_current_user
from application.tasks.schemas import TaskCreateRequest, TaskResponse, TaskUpdateRequest
from application.tasks.pagination_schemas import PaginatedTaskResponse
from application.tasks.create_task import create_task
from application.tasks.get_task import get_task_by_id
from application.tasks.list_tasks import list_tasks
from application.tasks.search_tasks import search_tasks
from application.tasks.update_task import update_task
from application.tasks.delete_task import delete_task
from infrastructure.persistence.repositories.task_repository import SQLAlchemyTaskRepository

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def get_task_repository(db: Session = Depends(get_db)) -> SQLAlchemyTaskRepository:
    """Dependency to get task repository."""
    return SQLAlchemyTaskRepository(db)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Unauthorized"}
    }
)
def create_task_endpoint(
    request: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyTaskRepository = Depends(get_task_repository)
):
    """
    Create a new task.
    
    Requires authentication. Task owner is automatically set to the authenticated user.
    """
    try:
        created_task = create_task(repository, request, current_user.id)
        return created_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e)
                }
            }
        )


@router.get(
    "/",
    response_model=PaginatedTaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Unauthorized"}
    }
)
def list_tasks_endpoint(
    q: Optional[str] = Query(None, description="Search term (searches in title and description)"),
    status: Optional[str] = Query(None, description="Filter by status (exact match)"),
    priority: Optional[str] = Query(None, description="Filter by priority (exact match)"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated, e.g., 'urgent,important')"),
    due_date: Optional[datetime] = Query(None, description="Filter by exact due date (ISO format)"),
    due_date_from: Optional[datetime] = Query(None, description="Filter by due date range (start, ISO format)"),
    due_date_to: Optional[datetime] = Query(None, description="Filter by due date range (end, ISO format)"),
    sort: Optional[str] = Query(None, description="Sort field and direction (e.g., 'due_date:asc', 'priority:desc')"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page (max 100)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List tasks with search, filtering, sorting, and pagination.
    
    All authenticated users can view all tasks (no ownership filter for reads).
    
    **Query Parameters:**
    - `q`: Search term (searches in title and description, case-insensitive partial match)
    - `status`: Filter by status (exact match)
    - `priority`: Filter by priority (exact match)
    - `tags`: Filter by tags (comma-separated, tasks containing any tag)
    - `due_date`: Filter by exact due date
    - `due_date_from`: Filter by due date range (start)
    - `due_date_to`: Filter by due date range (end)
    - `sort`: Sort field and direction (e.g., "due_date:asc", "priority:desc")
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 20, max: 100)
    """
    # Parse tags if provided
    tags_list = None
    if tags:
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    # Validate due_date range
    if due_date_from and due_date_to and due_date_from > due_date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "due_date_from must be less than or equal to due_date_to"
                }
            }
        )
    
    # Call search use case
    result = search_tasks(
        db=db,
        q=q,
        status=status,
        priority=priority,
        tags=tags_list,
        due_date=due_date,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        sort=sort,
        page=page,
        page_size=page_size
    )
    
    return result


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Task not found"},
        401: {"description": "Unauthorized"}
    }
)
def get_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyTaskRepository = Depends(get_task_repository)
):
    """
    Get a single task by ID.
    
    All authenticated users can view all tasks (no ownership filter for reads).
    """
    task = get_task_by_id(repository, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "TASK_NOT_FOUND",
                    "message": f"Task with ID {task_id} not found"
                }
            }
        )
    
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        403: {"description": "Forbidden - not the owner"},
        404: {"description": "Task not found"},
        401: {"description": "Unauthorized"}
    }
)
def update_task_endpoint(
    task_id: int,
    request: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyTaskRepository = Depends(get_task_repository)
):
    """
    Update an existing task.
    
    Only the task owner can update the task. Requires authentication.
    """
    try:
        updated_task = update_task(repository, task_id, request, current_user.id)
        
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with ID {task_id} not found"
                    }
                }
            )
        
        return updated_task
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "FORBIDDEN",
                    "message": str(e)
                }
            }
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        403: {"description": "Forbidden - not the owner"},
        404: {"description": "Task not found"},
        401: {"description": "Unauthorized"}
    }
)
def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyTaskRepository = Depends(get_task_repository)
):
    """
    Delete a task.
    
    Only the task owner can delete the task. Requires authentication.
    """
    try:
        deleted = delete_task(repository, task_id, current_user.id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with ID {task_id} not found"
                    }
                }
            )
        
        return None  # 204 No Content
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "FORBIDDEN",
                    "message": str(e)
                }
            }
        )
