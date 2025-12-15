"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database import get_db
from application.auth.schemas import (
    LoginRequest, LoginResponse, ErrorResponse,
    ChangePasswordRequest, ChangePasswordResponse
)
from application.auth.login import login_user
from application.auth.change_password import change_user_password
from api.middleware.auth import get_current_user
from domain.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"}
    }
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint.
    
    Authenticates user with username/email and password.
    Returns JWT token and user information on success.
    Returns generic error message on failure (prevents user enumeration).
    """
    result = login_user(db, request.username, request.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid username or password"
                }
            }
        )
    
    return result


@router.post(
    "/change-password",
    response_model=ChangePasswordResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized or invalid current password"},
        400: {"model": ErrorResponse, "description": "Invalid request (weak password)"}
    }
)
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change password endpoint.
    
    Requires authentication. Verifies current password before allowing change.
    """
    result = change_user_password(
        db,
        current_user.id,
        request.current_password,
        request.new_password
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_CURRENT_PASSWORD",
                    "message": "Current password is incorrect"
                }
            }
        )
    
    return result
