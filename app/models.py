from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import date, datetime
from uuid import UUID
from enum import Enum
import re


# ============ ENUMS ============
class RoleEnum(str, Enum):
    """User roles - sirf 2 allowed hai"""
    USER = "user"
    INSTITUTION = "institution"


# ============ REQUEST MODELS ============
class ProfileCreate(BaseModel):
    """Naya profile banane ke liye"""
    full_name: str = Field(..., min_length=2, max_length=100, examples=["Rahul Sharma"])
    email: str = Field(..., examples=["rahul@example.com"])
    phone: Optional[str] = Field(None, max_length=15, examples=["9876543210"])
    bio: Optional[str] = Field(None, examples=["Software Developer"])
    avatar_url: Optional[str] = Field(None, examples=["https://example.com/avatar.jpg"])
    date_of_birth: Optional[date] = Field(None, examples=["1995-05-15"])
    gender: Optional[str] = Field(None, examples=["Male"])
    address: Optional[str] = Field(None, examples=["123, MG Road"])
    city: Optional[str] = Field(None, examples=["Mumbai"])
    country: Optional[str] = Field(None, examples=["India"])
    role: RoleEnum = Field(default=RoleEnum.USER, examples=["user", "institution"])  # NEW FIELD
    
    # Email validation
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v.lower()


class ProfileUpdate(BaseModel):
    """Profile update karne ke liye"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=15)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[RoleEnum] = Field(None, examples=["user", "institution"])  # NEW FIELD


# ============ RESPONSE MODELS ============
class ProfileResponse(BaseModel):
    """Single profile response"""
    id: UUID
    full_name: str
    email: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    role: str  # NEW FIELD
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    """Standard API response"""
    success: bool
    message: str
    data: Optional[dict | list] = None


class PaginatedResponse(BaseModel):
    """Paginated response"""
    success: bool
    message: str
    data: list
    total: int
    page: int
    limit: int


# ============ ROLE STATS ============
class RoleStats(BaseModel):
    """Role wise count"""
    total_users: int
    total_institutions: int
    total_profiles: int