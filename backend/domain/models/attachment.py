"""Attachment domain model.

Attachment fields per requirements:
- task_id (integer, required) - Foreign key to tasks table
- filename (string, required) - Original filename (sanitized)
- file_size (integer, required) - File size in bytes
- storage_path (string, required) - Path to file in storage (filesystem path or object storage key)
- content_type (string, optional) - MIME type (e.g., "image/png", "application/pdf")
- uploaded_at (datetime, auto-set) - Upload timestamp

System fields:
- id (integer, auto-generated) - Primary key
- created_at (datetime, auto-set) - Creation timestamp
- updated_at (datetime, auto-updated) - Last update timestamp

Storage: Local filesystem (development) - files stored in backend/uploads/{task_id}/{filename}
"""

from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from domain.models.user import Base


class Attachment(Base):
    """Attachment domain model.
    
    Represents a file attachment for a task with all required fields from 
    docs/requirements.md section "3. Attachments".
    """
    
    __tablename__ = "attachments"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Required fields from requirements
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String, nullable=False)  # Original filename (sanitized)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    
    # Storage reference
    storage_path = Column(String, nullable=False)  # Path to file in storage
    
    # Optional metadata
    content_type = Column(String)  # MIME type (e.g., "image/png", "application/pdf")
    
    # System fields
    uploaded_at = Column(DateTime, default=lambda: datetime.now(UTC))
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relationship
    task = relationship("Task", backref="attachments")
    
    def __repr__(self):
        return f"<Attachment(id={self.id}, filename={self.filename}, task_id={self.task_id})>"
