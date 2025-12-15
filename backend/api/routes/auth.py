"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from infrastructure.database import get_db
from application.auth.schemas import (
    LoginRequest, LoginResponse, ErrorResponse,
    ChangePasswordRequest, ChangePasswordResponse
)
from application.auth.login import login_user
from application.auth.change_password import change_user_password
from api.middleware.auth import get_current_user
from domain.models.user import User
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    """User registration request schema."""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class RegisterResponse(BaseModel):
    """User registration response schema."""
    message: str
    user: dict


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error or user already exists"},
        409: {"model": ErrorResponse, "description": "User already exists"}
    }
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Creates a new user account with username, email, and password.
    Password is hashed using bcrypt before storage.
    """
    # Check if user already exists
    existing = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "USER_ALREADY_EXISTS",
                    "message": "Username or email already exists"
                }
            }
        )
    
    # Hash password
    hashed_password = bcrypt.hashpw(
        request.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Create user
    user = User(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return RegisterResponse(
            message="User registered successfully",
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "REGISTRATION_ERROR",
                    "message": f"Failed to register user: {str(e)}"
                }
            }
        )


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
