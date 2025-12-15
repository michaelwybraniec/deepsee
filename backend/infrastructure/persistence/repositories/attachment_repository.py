"""Attachment repository implementation (SQLAlchemy)."""

from typing import Optional, List
from sqlalchemy.orm import Session

from domain.models.attachment import Attachment
from application.attachments.repository import AttachmentRepository


class SQLAlchemyAttachmentRepository(AttachmentRepository):
    """SQLAlchemy implementation of AttachmentRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, attachment: Attachment) -> Attachment:
        """Create a new attachment."""
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)
        return attachment
    
    def get_by_id(self, attachment_id: int) -> Optional[Attachment]:
        """Get attachment by ID."""
        attachment = self.db.query(Attachment).filter(Attachment.id == attachment_id).first()
        return attachment
    
    def get_by_task_id(self, task_id: int) -> List[Attachment]:
        """Get all attachments for a task."""
        attachments = self.db.query(Attachment).filter(Attachment.task_id == task_id).all()
        return attachments
    
    def delete(self, attachment_id: int) -> bool:
        """Delete an attachment by ID."""
        attachment = self.db.query(Attachment).filter(Attachment.id == attachment_id).first()
        if attachment:
            self.db.delete(attachment)
            self.db.commit()
            return True
        return False
