"""Authentication schemas (Pydantic models)."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request schema."""
    
    username: str = Field(..., description="Username or email")
    password: str = Field(..., min_length=1, description="Password")


class LoginResponse(BaseModel):
    """Login response schema."""
    
    token: str = Field(..., description="JWT access token")
    user: dict = Field(..., description="User information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: dict = Field(..., description="Error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid username or password"
                }
            }
        }
