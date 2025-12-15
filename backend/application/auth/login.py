"""Login use case."""

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from sqlalchemy.orm import Session
import bcrypt

from domain.models.user import User
from infrastructure.auth.config import auth_config
from application.auth.schemas import LoginResponse


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash using constant-time comparison."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_access_token(user_id: int) -> str:
    """Create JWT access token."""
    expire = datetime.utcnow() + timedelta(hours=auth_config.get_token_expire_hours())
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(
        payload,
        auth_config.get_secret_key(),
        algorithm=auth_config.get_algorithm()
    )
    return token


def login_user(db: Session, username: str, password: str) -> Optional[LoginResponse]:
    """
    Login user with username/email and password.
    
    Returns LoginResponse on success, None on failure.
    Uses generic error message to prevent user enumeration.
    """
    # Try to find user by username or email
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    # Always perform password check (even if user doesn't exist) to prevent timing attacks
    # Use a dummy hash if user doesn't exist
    dummy_hash = bcrypt.hashpw(b"dummy", bcrypt.gensalt()).decode('utf-8')
    password_hash = user.hashed_password if user else dummy_hash
    
    # Constant-time password verification
    if not verify_password(password, password_hash):
        # Generic error - don't reveal if user exists
        return None
    
    # If we get here and user is None, password matched dummy (shouldn't happen, but be safe)
    if not user:
        return None
    
    # Create access token
    token = create_access_token(user.id)
    
    # Return login response
    return LoginResponse(
        token=token,
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    )
