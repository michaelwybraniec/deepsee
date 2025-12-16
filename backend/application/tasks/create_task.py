"""Create task use case."""

from datetime import datetime, UTC
from typing import Optional
import json

from domain.models.task import Task
from domain.audit.audit_event import AuditActionType
from application.tasks.schemas import TaskCreateRequest, TaskResponse
from application.tasks.repository import TaskRepository
from application.audit.audit_logger import AuditLogger


def create_task(
    repository: TaskRepository,
    request: TaskCreateRequest,
    owner_user_id: int,
    audit_logger: Optional[AuditLogger] = None
) -> TaskResponse:
    """
    Create a new task.
    
    Args:
        repository: Task repository interface
        request: Task creation request data
        owner_user_id: ID of the authenticated user (set as owner)
    
    Returns:
        TaskResponse with created task data
    
    Raises:
        ValueError: If validation fails
    """
    # Validate title is not empty (Pydantic should handle this, but double-check)
    if not request.title or not request.title.strip():
        raise ValueError("Title is required and cannot be empty")
    
    # Convert tags list to JSON string for storage
    tags_json = None
    if request.tags:
        tags_json = json.dumps(request.tags)
    
    # Create task entity
    task = Task(
        title=request.title.strip(),
        description=request.description.strip() if request.description else None,
        status=request.status,
        priority=request.priority,
        due_date=request.due_date,
        tags=tags_json,
        owner_user_id=owner_user_id,  # Set from authenticated user, never from request
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    
    # Persist via repository
    created_task = repository.create(task)
    
    # Log audit event
    if audit_logger:
        audit_logger.log(
            action_type=AuditActionType.TASK_CREATED,
            user_id=owner_user_id,
            resource_type="task",
            resource_id=str(created_task.id),
            metadata={
                "title": created_task.title,
                "status": created_task.status,
                "priority": created_task.priority
            }
        )
    
    # Convert tags JSON string back to list for response
    tags_list = None
    if created_task.tags:
        try:
            tags_list = json.loads(created_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_list = []
    
    # Return response
    return TaskResponse(
        id=created_task.id,
        title=created_task.title,
        description=created_task.description,
        status=created_task.status,
        priority=created_task.priority,
        due_date=created_task.due_date,
        tags=tags_list,
        owner_user_id=created_task.owner_user_id,
        created_at=created_task.created_at,
        updated_at=created_task.updated_at
    )
