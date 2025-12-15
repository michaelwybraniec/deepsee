"""Pagination schemas for task search/filter responses."""

from typing import List
from pydantic import BaseModel, Field
from application.tasks.schemas import TaskResponse


class PaginationMetadata(BaseModel):
    """Pagination metadata."""
    
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")
    total: int = Field(..., description="Total number of tasks matching the query")
    total_pages: int = Field(..., description="Total number of pages")


class PaginatedTaskResponse(BaseModel):
    """Paginated task response."""
    
    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    pagination: PaginationMetadata = Field(..., description="Pagination metadata")
