"""Audit event ORM model."""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index, JSON
from sqlalchemy.orm import relationship

from domain.models.user import Base


class AuditEvent(Base):
    """Audit event ORM model.
    
    Stores audit log entries for tracking key system actions.
    Events are immutable (append-only, never updated or deleted).
    """
    
    __tablename__ = "audit_events"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Required fields
    action_type = Column(String, nullable=False, index=True)  # e.g., "task_created", "attachment_uploaded"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # NULL for system actions
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Resource identification
    resource_type = Column(String, nullable=False, index=True)  # e.g., "task", "attachment", "reminder"
    resource_id = Column(String, nullable=False)  # ID of the affected resource (as string for flexibility)
    
    # Metadata (JSON for flexibility)
    event_metadata = Column(JSON, nullable=True)  # Additional context (task title, status changes, filename, etc.)
    
    # Relationship
    user = relationship("User", foreign_keys=[user_id])
    
    # Indexes for query performance
    __table_args__ = (
        Index('idx_audit_action_timestamp', 'action_type', 'timestamp'),
        Index('idx_audit_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
    )
    
    def __repr__(self):
        return (
            f"<AuditEvent(id={self.id}, action_type={self.action_type}, "
            f"user_id={self.user_id}, resource_type={self.resource_type}, "
            f"resource_id={self.resource_id}, timestamp={self.timestamp})>"
        )
    
    @property
    def metadata(self):
        """Property to access event_metadata (for compatibility with domain entity)."""
        return self.event_metadata
    
    @metadata.setter
    def metadata(self, value):
        """Setter for event_metadata."""
        self.event_metadata = value
