"""Upload attachment use case."""

import re
from typing import Optional
from io import BytesIO

from domain.models.attachment import Attachment
from domain.models.task import Task
from application.attachments.schemas import AttachmentResponse
from application.attachments.repository import AttachmentRepository
from application.attachments.storage_interface import AttachmentStorage
from application.tasks.repository import TaskRepository


# Security constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_FILENAME_LENGTH = 255
ALLOWED_FILENAME_CHARS = re.compile(r'^[a-zA-Z0-9._-]+$')


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other security issues.
    
    Rules:
    - Remove path separators (/ and \)
    - Remove dangerous sequences (.., ~)
    - Limit length to 255 characters
    - Allow only safe characters: alphanumeric, dots, underscores, hyphens
    """
    # Remove path separators
    filename = filename.replace('/', '').replace('\\', '')
    
    # Remove dangerous sequences
    filename = filename.replace('..', '').replace('~', '')
    
    # Limit length
    if len(filename) > MAX_FILENAME_LENGTH:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:MAX_FILENAME_LENGTH - len(ext) - 1] + ('.' + ext if ext else '')
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Validate characters (allow only safe chars)
    if not ALLOWED_FILENAME_CHARS.match(filename):
        # Keep only safe characters
        filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
    # Ensure filename is not empty
    if not filename:
        filename = "file"
    
    return filename


def upload_attachment(
    task_repository: TaskRepository,
    attachment_repository: AttachmentRepository,
    storage: AttachmentStorage,
    task_id: int,
    file: BytesIO,
    filename: str,
    content_type: Optional[str],
    authenticated_user_id: int
) -> Optional[AttachmentResponse]:
    """
    Upload an attachment for a task.
    
    Only the task owner can upload attachments.
    
    Args:
        task_repository: Task repository interface
        attachment_repository: Attachment repository interface
        storage: Attachment storage interface
        task_id: ID of the task
        file: File content (BytesIO)
        filename: Original filename
        content_type: MIME type (optional)
        authenticated_user_id: ID of the authenticated user
    
    Returns:
        AttachmentResponse on success, None on failure
    
    Raises:
        ValueError: If validation fails
        PermissionError: If user is not task owner
    """
    # Verify task exists
    task = task_repository.get_by_id(task_id)
    if not task:
        return None
    
    # Check ownership (only task owner can upload)
    if task.owner_user_id != authenticated_user_id:
        raise PermissionError("You can only upload attachments to your own tasks")
    
    # Validate file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB")
    
    if file_size == 0:
        raise ValueError("File is empty")
    
    # Sanitize filename
    sanitized_filename = sanitize_filename(filename)
    
    # Save file to storage
    try:
        storage_path = storage.save(file, task_id, sanitized_filename)
    except Exception as e:
        raise ValueError(f"Failed to save file: {str(e)}")
    
    # Create attachment metadata
    attachment = Attachment(
        task_id=task_id,
        filename=sanitized_filename,
        file_size=file_size,
        storage_path=storage_path,
        content_type=content_type
    )
    
    # Persist metadata
    created_attachment = attachment_repository.create(attachment)
    
    return AttachmentResponse(
        id=created_attachment.id,
        task_id=created_attachment.task_id,
        filename=created_attachment.filename,
        file_size=created_attachment.file_size,
        content_type=created_attachment.content_type,
        uploaded_at=created_attachment.uploaded_at
    )
