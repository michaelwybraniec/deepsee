"""Task API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database import get_db
from domain.models.user import User
from api.middleware.auth import get_current_user
from application.tasks.schemas import TaskCreateRequest, TaskResponse
from application.tasks.create_task import create_task
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
