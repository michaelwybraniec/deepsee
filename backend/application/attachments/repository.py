"""Attachment repository interface (Clean Architecture)."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.attachment import Attachment


class AttachmentRepository(ABC):
    """Repository interface for attachment persistence."""
    
    @abstractmethod
    def create(self, attachment: Attachment) -> Attachment:
        """Create a new attachment."""
        pass
    
    @abstractmethod
    def get_by_id(self, attachment_id: int) -> Optional[Attachment]:
        """Get attachment by ID."""
        pass
    
    @abstractmethod
    def get_by_task_id(self, task_id: int) -> List[Attachment]:
        """Get all attachments for a task."""
        pass
    
    @abstractmethod
    def delete(self, attachment_id: int) -> bool:
        """Delete an attachment by ID. Returns True if deleted, False if not found."""
        pass
