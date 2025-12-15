"""Task domain model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from domain.models import Base


class Task(Base):
    """Task domain model."""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String)
    priority = Column(String)
    due_date = Column(DateTime)
    tags = Column(String)  # JSON string or comma-separated
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    owner = relationship("User", backref="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, owner_user_id={self.owner_user_id})>"
