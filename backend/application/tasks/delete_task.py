"""Delete task use case."""

from typing import Optional
from domain.models.task import Task
from domain.audit.audit_event import AuditActionType
from application.tasks.repository import TaskRepository
from application.audit.audit_logger import AuditLogger


def delete_task(
    repository: TaskRepository,
    task_id: int,
    authenticated_user_id: int,
    audit_logger: Optional[AuditLogger] = None
) -> bool:
    """
    Delete a task.
    
    Only the task owner can delete the task (ownership check).
    
    Args:
        repository: Task repository interface
        task_id: ID of the task to delete
        authenticated_user_id: ID of the authenticated user
    
    Returns:
        True if task was deleted, False if task not found
    
    Raises:
        PermissionError: If user is not the owner
    """
    # Get task
    task = repository.get_by_id(task_id)
    if not task:
        return False
    
    # Check ownership (defense in depth)
    if task.owner_user_id != authenticated_user_id:
        raise PermissionError("You can only modify your own tasks")
    
    # Store task title for audit before deletion
    task_title = task.title
    
    # Delete task
    deleted = repository.delete(task_id)
    
    # Log audit event (only if deletion was successful)
    if deleted and audit_logger:
        audit_logger.log(
            action_type=AuditActionType.TASK_DELETED,
            user_id=authenticated_user_id,
            resource_type="task",
            resource_id=str(task_id),
            metadata={
                "task_id": task_id,
                "title": task_title
            }
        )
    
    return deleted
