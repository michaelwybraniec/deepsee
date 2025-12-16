"""Task schemas (Pydantic models)."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class TaskCreateRequest(BaseModel):
    """Create task request schema."""
    
    title: str = Field(..., min_length=1, description="Task title (required)")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[str] = Field(None, description="Task status (e.g., 'todo', 'in_progress', 'done')")
    priority: Optional[str] = Field(None, description="Task priority (e.g., 'low', 'medium', 'high')")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    tags: Optional[List[str]] = Field(None, description="Task tags")


class TaskResponse(BaseModel):
    """Task response schema."""
    
    model_config = ConfigDict(from_attributes=True)  # For SQLAlchemy model conversion
    
    id: int
    title: str
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    due_date: Optional[datetime]
    tags: Optional[List[str]]
    owner_user_id: int
    owner_username: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TaskUpdateRequest(BaseModel):
    """Update task request schema (all fields optional for PATCH)."""
    
    title: Optional[str] = Field(None, min_length=1, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[str] = Field(None, description="Task status")
    priority: Optional[str] = Field(None, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    tags: Optional[List[str]] = Field(None, description="Task tags")
