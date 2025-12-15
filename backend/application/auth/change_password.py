"""Change password use case."""

from typing import Optional
from sqlalchemy.orm import Session
import bcrypt

from domain.models.user import User
from infrastructure.auth.config import auth_config
from application.auth.schemas import ChangePasswordResponse
from application.auth.login import verify_password


def change_user_password(
    db: Session,
    user_id: int,
    current_password: str,
    new_password: str
) -> Optional[ChangePasswordResponse]:
    """
    Change user password.
    
    Verifies current password, then updates to new password.
    Returns ChangePasswordResponse on success, None on failure.
    """
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        return None
    
    # Validate new password strength (minimum 8 characters)
    if len(new_password) < 8:
        return None
    
    # Hash new password
    new_password_hash = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt(rounds=auth_config.BCRYPT_ROUNDS)
    ).decode('utf-8')
    
    # Update user password
    user.hashed_password = new_password_hash
    db.commit()
    db.refresh(user)
    
    return ChangePasswordResponse(message="Password changed successfully")
