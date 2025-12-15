"""Attachment schemas (Pydantic models)."""

from datetime import datetime
from pydantic import BaseModel, Field


class AttachmentResponse(BaseModel):
    """Attachment response schema."""
    
    id: int
    task_id: int
    filename: str
    file_size: int
    content_type: str | None
    uploaded_at: datetime
    
    class Config:
        from_attributes = True  # For SQLAlchemy model conversion


class AttachmentListResponse(BaseModel):
    """List of attachments response schema."""
    
    attachments: list[AttachmentResponse]
