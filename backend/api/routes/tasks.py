"""Task API routes."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database import get_db
from domain.models.user import User
from api.middleware.auth import get_current_user
from application.tasks.schemas import TaskCreateRequest, TaskResponse, TaskUpdateRequest
from application.tasks.create_task import create_task
from application.tasks.get_task import get_task_by_id
from application.tasks.list_tasks import list_tasks
from application.tasks.update_task import update_task
from application.tasks.delete_task import delete_task
from application.tasks.schemas import TaskUpdateRequest
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
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"}
    }
)
def list_tasks_endpoint(
    current_user: User = Depends(get_current_user),
    repository: SQLAlchemyTaskRepository = Depends(get_task_repository)
):
    """
    List all tasks.
    
    All authenticated users can view all tasks (no ownership filter for reads).
    Search/filter/sort/pagination will be added in Task 5.
    """
    tasks = list_tasks(repository)
    return tasks


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
