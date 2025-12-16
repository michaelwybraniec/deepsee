"""List tasks use case."""

from typing import List
import json

from domain.models.task import Task
from application.tasks.schemas import TaskResponse
from application.tasks.repository import TaskRepository


def list_tasks(
    repository: TaskRepository
) -> List[TaskResponse]:
    """
    List all tasks.
    
    All authenticated users can view all tasks (no ownership filter for reads).
    Search/filter/sort/pagination will be added in Task 5.
    
    Args:
        repository: Task repository interface
    
    Returns:
        List of TaskResponse objects
    """
    tasks = repository.get_all()
    
    # Convert to response models
    result = []
    for task in tasks:
        # Convert tags JSON string back to list for response
        tags_list = None
        if task.tags:
            try:
                tags_list = json.loads(task.tags)
            except (json.JSONDecodeError, TypeError):
                tags_list = []
        
        result.append(TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            tags=tags_list,
            owner_user_id=task.owner_user_id,
            owner_username=task.owner.username if task.owner else None,
            created_at=task.created_at,
            updated_at=task.updated_at
        ))
    
    return result
