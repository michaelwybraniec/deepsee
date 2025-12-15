"""Delete attachment use case."""

from typing import Optional
from domain.models.task import Task
from domain.audit.audit_event import AuditActionType
from application.attachments.repository import AttachmentRepository
from application.attachments.storage_interface import AttachmentStorage
from application.tasks.repository import TaskRepository
from application.audit.audit_logger import AuditLogger


def delete_attachment(
    task_repository: TaskRepository,
    attachment_repository: AttachmentRepository,
    storage: AttachmentStorage,
    attachment_id: int,
    authenticated_user_id: int,
    audit_logger: Optional[AuditLogger] = None
) -> bool:
    """
    Delete an attachment.
    
    Only the task owner can delete attachments (inherits from task ownership).
    
    Args:
        task_repository: Task repository interface
        attachment_repository: Attachment repository interface
        storage: Attachment storage interface
        attachment_id: ID of the attachment to delete
        authenticated_user_id: ID of the authenticated user
    
    Returns:
        True if attachment was deleted, False if not found
    
    Raises:
        PermissionError: If user is not the task owner
    """
    # Get attachment
    attachment = attachment_repository.get_by_id(attachment_id)
    if not attachment:
        return False
    
    # Get task to check ownership
    task = task_repository.get_by_id(attachment.task_id)
    if not task:
        return False
    
    # Check ownership (only task owner can delete)
    if task.owner_user_id != authenticated_user_id:
        raise PermissionError("You can only delete attachments from your own tasks")
    
    # Store attachment info for audit before deletion
    attachment_filename = attachment.filename
    attachment_task_id = attachment.task_id
    
    # Delete file from storage
    storage.delete(attachment.storage_path)
    
    # Delete metadata from database
    deleted = attachment_repository.delete(attachment_id)
    
    # Log audit event (only if deletion was successful)
    if deleted and audit_logger:
        audit_logger.log(
            action_type=AuditActionType.ATTACHMENT_DELETED,
            user_id=authenticated_user_id,
            resource_type="attachment",
            resource_id=str(attachment_id),
            metadata={
                "attachment_id": attachment_id,
                "task_id": attachment_task_id,
                "filename": attachment_filename
            }
        )
    
    return deleted
