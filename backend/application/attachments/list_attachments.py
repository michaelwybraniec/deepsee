"""List attachments use case."""

from typing import List
from application.attachments.schemas import AttachmentResponse
from application.attachments.repository import AttachmentRepository


def list_attachments(
    repository: AttachmentRepository,
    task_id: int
) -> List[AttachmentResponse]:
    """
    List all attachments for a task.
    
    All authenticated users can view attachments (no ownership filter for reads).
    
    Args:
        repository: Attachment repository interface
        task_id: ID of the task
    
    Returns:
        List of AttachmentResponse objects
    """
    attachments = repository.get_by_task_id(task_id)
    
    return [
        AttachmentResponse(
            id=att.id,
            task_id=att.task_id,
            filename=att.filename,
            file_size=att.file_size,
            content_type=att.content_type,
            uploaded_at=att.uploaded_at
        )
        for att in attachments
    ]
