"""Delete task use case."""

from typing import Optional
from domain.models.task import Task
from domain.audit.audit_event import AuditActionType
from application.tasks.repository import TaskRepository
from application.attachments.repository import AttachmentRepository
from application.attachments.storage_interface import AttachmentStorage
from application.audit.audit_logger import AuditLogger


def delete_task(
    repository: TaskRepository,
    task_id: int,
    authenticated_user_id: int,
    attachment_repository: Optional[AttachmentRepository] = None,
    storage: Optional[AttachmentStorage] = None,
    audit_logger: Optional[AuditLogger] = None
) -> bool:
    """
    Delete a task.
    
    Only the task owner can delete the task (ownership check).
    Also deletes all attachments associated with the task.
    
    Args:
        repository: Task repository interface
        task_id: ID of the task to delete
        authenticated_user_id: ID of the authenticated user
        attachment_repository: Attachment repository interface (optional, for deleting attachments)
        storage: Attachment storage interface (optional, for deleting files)
        audit_logger: Audit logger (optional, for logging deletion)
    
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
    
    # Delete all attachments for this task first
    if attachment_repository and storage:
        attachments = attachment_repository.get_by_task_id(task_id)
        for attachment in attachments:
            try:
                # Delete file from storage
                storage.delete(attachment.storage_path)
                # Delete attachment metadata
                attachment_repository.delete(attachment.id)
            except Exception:
                # Log error but continue with task deletion
                # (don't fail task deletion if attachment deletion fails)
                pass
    
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
