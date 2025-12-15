"""Delete task use case."""

from typing import Optional
from domain.models.task import Task
from application.tasks.repository import TaskRepository


def delete_task(
    repository: TaskRepository,
    task_id: int,
    authenticated_user_id: int
) -> bool:
    """
    Delete a task.
    
    Only the task owner can delete the task (ownership check).
    
    Args:
        repository: Task repository interface
        task_id: ID of the task to delete
        authenticated_user_id: ID of the authenticated user
    
    Returns:
        True if task was deleted, False if task not found
    
    Raises:
        PermissionError: If user is not the owner
    """
    # Get task
    task = repository.get_by_id(task_id)
    if not task:
        return False
    
    # Check ownership (defense in depth)
    if task.owner_user_id != authenticated_user_id:
        raise PermissionError("You can only modify your own tasks")
    
    # Delete task
    return repository.delete(task_id)
