"""Authentication and User Pydantic Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class UserRegister(BaseModel):
    """Schema for registering a new user."""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, max_length=128)
    role: UserRole = UserRole.CANDIDATE


class UserLogin(BaseModel):
    """Schema for user credential validation."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT access token response."""
    access_token: str
    token_type: str = "bearer"
    role: UserRole


class TokenPayload(BaseModel):
    """Decoded token payload schema."""
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None


class UserProfile(BaseModel):
    """Public user profile response schema."""
    id: int
    email: EmailStr
    name: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True
