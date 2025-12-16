"""Task domain model.

Task fields per requirements:
- title (string, required) - Task title
- description (string, optional) - Task description
- status (string, optional) - Task status (e.g., "todo", "in_progress", "done")
- priority (string, optional) - Task priority (e.g., "low", "medium", "high")
- due_date (datetime, optional) - Task due date
- tags (string/JSON, optional) - Task tags (stored as JSON string for SQLite compatibility)

System fields:
- id (integer, auto-generated) - Primary key
- owner_user_id (integer, required) - Foreign key to users table (for authorization)
- created_at (datetime, auto-set) - Creation timestamp
- updated_at (datetime, auto-updated) - Last update timestamp

Indexes:
- owner_user_id: For authorization queries and filtering
- due_date: For filtering and sorting by due date
- Full-text search on title/description: For search functionality (Task 5)
"""

from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from domain.models.user import Base


class Task(Base):
    """Task domain model.
    
    Represents a task with all required fields from docs/requirements.md section "2. Task Management".
    Supports search/filter operations (Task 5) with appropriate indexes.
    """
    
    __tablename__ = "tasks"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Required fields from requirements
    title = Column(String, nullable=False, index=True)  # Indexed for search
    description = Column(Text)  # Text for longer descriptions
    
    # Optional fields from requirements
    status = Column(String)  # e.g., "todo", "in_progress", "done"
    priority = Column(String)  # e.g., "low", "medium", "high"
    due_date = Column(DateTime, index=True)  # Indexed for filtering/sorting
    tags = Column(String)  # JSON string: ["tag1", "tag2"] (SQLite compatible)
    
    # System fields (for authorization and tracking)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    reminder_sent_at = Column(DateTime, nullable=True, index=True)  # For idempotency tracking
    
    # Relationship
    owner = relationship("User", backref="tasks")
    
    # Indexes for search/filter operations (Task 5)
    __table_args__ = (
        Index('idx_task_owner_due_date', 'owner_user_id', 'due_date'),  # Composite index for filtering
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, owner_user_id={self.owner_user_id})>"
