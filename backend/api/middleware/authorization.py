"""Authorization middleware for enforcing ownership rules."""

from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.models.user import User


def check_ownership(
    db: Session,
    resource_owner_id: Optional[int],
    current_user_id: int,
    resource_type: str = "resource"
) -> None:
    """
    Check if current user owns the resource.
    
    Raises HTTPException if user is not the owner.
    """
    if resource_owner_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": f"{resource_type.capitalize()} not found"
                }
            }
        )
    
    if resource_owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "FORBIDDEN",
                    "message": "You can only modify your own resources"
                }
            }
        )


def require_ownership_for_modification(
    resource_owner_id: Optional[int],
    current_user_id: int,
    resource_type: str = "resource"
) -> None:
    """
    Require ownership for modification operations (create, update, delete).
    
    For create operations, ownership is set in the use-case (not checked here).
    For update/delete operations, verifies user owns the resource.
    """
    if resource_owner_id is not None:
        # For update/delete: check ownership
        check_ownership(None, resource_owner_id, current_user_id, resource_type)


def allow_read_for_all(current_user_id: int) -> None:
    """
    Allow read access for all authenticated users.
    
    This is a no-op function that can be used to document that
    read endpoints allow all authenticated users.
    """
    # All authenticated users can read all resources
    # No ownership check needed for read operations
    pass
