from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID

# ============ REQUEST MODELS ============
# Ye models client se data lene ke liye hai

class ProfileCreate(BaseModel):
    """Naya profile banane ke liye"""
    full_name: str = Field(..., min_length=2, max_length=100, example="Rahul Sharma")
    email: EmailStr = Field(..., example="rahul@example.com")
    phone: Optional[str] = Field(None, max_length=15, example="9876543210")
    bio: Optional[str] = Field(None, example="Software Developer")
    avatar_url: Optional[str] = Field(None, example="https://example.com/avatar.jpg")
    date_of_birth: Optional[date] = Field(None, example="1995-05-15")
    gender: Optional[str] = Field(None, example="Male")
    address: Optional[str] = Field(None, example="123, MG Road")
    city: Optional[str] = Field(None, example="Mumbai")
    country: Optional[str] = Field(None, example="India")


class ProfileUpdate(BaseModel):
    """Profile update karne ke liye - sab optional hai"""
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


# ============ RESPONSE MODELS ============
# Ye models client ko data bhejne ke liye hai

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
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ORM mode enable


class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool
    message: str
    data: Optional[dict | list] = None


class PaginatedResponse(BaseModel):
    """Pagination ke saath response"""
    success: bool
    message: str
    data: list
    total: int
    page: int
    limit: int