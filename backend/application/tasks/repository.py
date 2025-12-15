"""Task repository interface (Clean Architecture)."""

from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.task import Task


class TaskRepository(ABC):
    """Repository interface for task persistence."""
    
    @abstractmethod
    def create(self, task: Task) -> Task:
        """Create a new task."""
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        """Get all tasks (no ownership filter for reads)."""
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        """Update an existing task."""
        pass
    
    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        pass
