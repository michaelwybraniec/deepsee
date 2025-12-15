"""
Authentication configuration module.

This module handles JWT authentication configuration following Clean Architecture.
Uses python-jose for JWT token generation and validation.

Design Choice: JWT was chosen over OIDC/OAuth2 for simplicity, API-first architecture,
and single-tenant requirements. See docs/technology.md section 3.1 for rationale.
"""

import os
from typing import Optional
from jose import jwt
from jose.constants import ALGORITHMS


class AuthConfig:
    """Authentication configuration."""
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_HOURS", "24"))
    
    # Password Hashing
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", "12"))
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY environment variable is required")
        
        if len(cls.JWT_SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long for security")
        
        if cls.JWT_ALGORITHM not in ["HS256", "RS256"]:
            raise ValueError(f"JWT_ALGORITHM must be one of: HS256, RS256")
    
    @classmethod
    def get_secret_key(cls) -> str:
        """Get JWT secret key."""
        return cls.JWT_SECRET_KEY
    
    @classmethod
    def get_algorithm(cls) -> str:
        """Get JWT algorithm."""
        return cls.JWT_ALGORITHM
    
    @classmethod
    def get_token_expire_hours(cls) -> int:
        """Get token expiration time in hours."""
        return cls.JWT_ACCESS_TOKEN_EXPIRE_HOURS


# Global auth config instance
auth_config = AuthConfig()
