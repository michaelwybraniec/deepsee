"""Attachment schemas (Pydantic models)."""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class AttachmentResponse(BaseModel):
    """Attachment response schema."""
    
    model_config = ConfigDict(from_attributes=True)  # For SQLAlchemy model conversion
    
    id: int
    task_id: int
    filename: str
    file_size: int
    content_type: str | None
    uploaded_at: datetime


class AttachmentListResponse(BaseModel):
    """List of attachments response schema."""
    
    attachments: list[AttachmentResponse]
