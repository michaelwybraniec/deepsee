"""Attachment API routes."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from io import BytesIO

from infrastructure.database import get_db
from domain.models.user import User
from api.middleware.auth import get_current_user
from application.attachments.schemas import AttachmentResponse
from application.attachments.upload_attachment import upload_attachment
from application.attachments.list_attachments import list_attachments
from application.attachments.delete_attachment import delete_attachment
from application.attachments.repository import AttachmentRepository
from application.tasks.repository import TaskRepository
from infrastructure.persistence.repositories.attachment_repository import SQLAlchemyAttachmentRepository
from infrastructure.persistence.repositories.task_repository import SQLAlchemyTaskRepository
from infrastructure.attachments.storage import LocalFileStorage
from application.audit.audit_logger import AuditLogger
from infrastructure.audit.audit_logger import AuditLoggerImpl
from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository

router = APIRouter(prefix="/api", tags=["attachments"])


def get_attachment_repository(db: Session = Depends(get_db)) -> SQLAlchemyAttachmentRepository:
    """Dependency to get attachment repository."""
    return SQLAlchemyAttachmentRepository(db)


def get_task_repository(db: Session = Depends(get_db)) -> SQLAlchemyTaskRepository:
    """Dependency to get task repository."""
    return SQLAlchemyTaskRepository(db)


def get_storage() -> LocalFileStorage:
    """Dependency to get storage implementation."""
    return LocalFileStorage()


def get_audit_logger(db: Session = Depends(get_db)) -> AuditLogger:
    """Dependency to get audit logger."""
    audit_repository = SQLAlchemyAuditRepository(db)
    return AuditLoggerImpl(audit_repository)


@router.post(
    "/tasks/{task_id}/attachments",
    response_model=AttachmentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Validation error"},
        403: {"description": "Forbidden - not the task owner"},
        404: {"description": "Task not found"},
        401: {"description": "Unauthorized"}
    }
)
async def upload_attachment_endpoint(
    task_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    task_repository: SQLAlchemyTaskRepository = Depends(get_task_repository),
    attachment_repository: SQLAlchemyAttachmentRepository = Depends(get_attachment_repository),
    storage: LocalFileStorage = Depends(get_storage),
    audit_logger: AuditLogger = Depends(get_audit_logger)
):
    """
    Upload an attachment for a task.
    
    Only the task owner can upload attachments. Requires authentication.
    """
    try:
        # Read file content
        file_content = await file.read()
        file_bytes = BytesIO(file_content)
        
        # Upload attachment
        result = upload_attachment(
            task_repository=task_repository,
            attachment_repository=attachment_repository,
            storage=storage,
            task_id=task_id,
            file=file_bytes,
            filename=file.filename or "file",
            content_type=file.content_type,
            authenticated_user_id=current_user.id,
            audit_logger=audit_logger
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task with ID {task_id} not found"
                    }
                }
            )
        
        return result
        
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
    "/tasks/{task_id}/attachments",
    response_model=List[AttachmentResponse],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"}
    }
)
def list_attachments_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    attachment_repository: SQLAlchemyAttachmentRepository = Depends(get_attachment_repository)
):
    """
    List all attachments for a task.
    
    All authenticated users can view attachments (no ownership filter for reads).
    """
    attachments = list_attachments(attachment_repository, task_id)
    return attachments


@router.delete(
    "/attachments/{attachment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        403: {"description": "Forbidden - not the task owner"},
        404: {"description": "Attachment not found"},
        401: {"description": "Unauthorized"}
    }
)
def delete_attachment_endpoint(
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    task_repository: SQLAlchemyTaskRepository = Depends(get_task_repository),
    attachment_repository: SQLAlchemyAttachmentRepository = Depends(get_attachment_repository),
    storage: LocalFileStorage = Depends(get_storage),
    audit_logger: AuditLogger = Depends(get_audit_logger)
):
    """
    Delete an attachment.
    
    Only the task owner can delete attachments. Requires authentication.
    """
    try:
        deleted = delete_attachment(
            task_repository=task_repository,
            attachment_repository=attachment_repository,
            storage=storage,
            attachment_id=attachment_id,
            authenticated_user_id=current_user.id,
            audit_logger=audit_logger
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "ATTACHMENT_NOT_FOUND",
                        "message": f"Attachment with ID {attachment_id} not found"
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
