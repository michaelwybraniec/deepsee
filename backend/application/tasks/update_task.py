"""Update task use case."""

from typing import Optional
import json

from domain.models.task import Task
from domain.audit.audit_event import AuditActionType
from application.tasks.schemas import TaskUpdateRequest, TaskResponse
from application.tasks.repository import TaskRepository
from application.audit.audit_logger import AuditLogger
from api.middleware.authorization import check_ownership


def update_task(
    repository: TaskRepository,
    task_id: int,
    request: TaskUpdateRequest,
    authenticated_user_id: int,
    audit_logger: Optional[AuditLogger] = None
) -> Optional[TaskResponse]:
    """
    Update an existing task.
    
    Only the task owner can update the task (ownership check).
    
    Args:
        repository: Task repository interface
        task_id: ID of the task to update
        request: Update request data (partial fields)
        authenticated_user_id: ID of the authenticated user
    
    Returns:
        TaskResponse with updated task data, or None if task not found or not owner
    
    Raises:
        PermissionError: If user is not the owner
    """
    # Get task
    task = repository.get_by_id(task_id)
    if not task:
        return None
    
    # Check ownership (defense in depth)
    if task.owner_user_id != authenticated_user_id:
        raise PermissionError("You can only modify your own tasks")
    
    # Store old values for audit metadata
    old_status = task.status
    old_priority = task.priority
    
    # Update fields (only provided fields)
    if request.title is not None:
        task.title = request.title.strip()
    if request.description is not None:
        task.description = request.description.strip() if request.description else None
    if request.status is not None:
        task.status = request.status
    if request.priority is not None:
        task.priority = request.priority
    if request.due_date is not None:
        task.due_date = request.due_date
    if request.tags is not None:
        # Convert tags list to JSON string
        task.tags = json.dumps(request.tags) if request.tags else None
    
    # Update timestamp
    from datetime import datetime, UTC
    task.updated_at = datetime.now(UTC)
    
    # Persist via repository
    updated_task = repository.update(task)
    
    # Log audit event
    if audit_logger:
        # Build changes metadata
        changes = {}
        if request.status is not None and old_status != updated_task.status:
            changes["status"] = {"old": old_status, "new": updated_task.status}
        if request.priority is not None and old_priority != updated_task.priority:
            changes["priority"] = {"old": old_priority, "new": updated_task.priority}
        if request.title is not None:
            changes["title"] = {"new": updated_task.title}
        
        audit_logger.log(
            action_type=AuditActionType.TASK_UPDATED,
            user_id=authenticated_user_id,
            resource_type="task",
            resource_id=str(task_id),
            metadata={
                "task_id": task_id,
                "changes": changes
            }
        )
    
    # Convert tags JSON string back to list for response
    tags_list = None
    if updated_task.tags:
        try:
            tags_list = json.loads(updated_task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_list = []
    
    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        status=updated_task.status,
        priority=updated_task.priority,
        due_date=updated_task.due_date,
        tags=tags_list,
        owner_user_id=updated_task.owner_user_id,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )
