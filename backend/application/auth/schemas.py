"""Authentication schemas (Pydantic models)."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class LoginRequest(BaseModel):
    """Login request schema."""
    
    username: str = Field(..., description="Username or email")
    password: str = Field(..., min_length=1, description="Password")


class LoginResponse(BaseModel):
    """Login response schema."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com"
                }
            }
        }
    )
    
    token: str = Field(..., description="JWT access token")
    user: dict = Field(..., description="User information")


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""
    
    current_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")


class ChangePasswordResponse(BaseModel):
    """Change password response schema."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Password changed successfully"
            }
        }
    )
    
    message: str = Field(..., description="Success message")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid username or password"
                }
            }
        }
    )
    
    error: dict = Field(..., description="Error information")
