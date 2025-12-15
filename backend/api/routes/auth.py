"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.database import get_db
from application.auth.schemas import LoginRequest, LoginResponse, ErrorResponse
from application.auth.login import login_user

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
