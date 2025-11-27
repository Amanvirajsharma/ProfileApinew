from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID


# ============ REQUEST MODELS ============
class ProfileCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, examples=["Rahul Sharma"])
    email: EmailStr = Field(..., examples=["rahul@example.com"])
    phone: Optional[str] = Field(None, max_length=15, examples=["9876543210"])
    bio: Optional[str] = Field(None, examples=["Software Developer"])
    avatar_url: Optional[str] = Field(None, examples=["https://example.com/avatar.jpg"])
    date_of_birth: Optional[date] = Field(None, examples=["1995-05-15"])
    gender: Optional[str] = Field(None, examples=["Male"])
    address: Optional[str] = Field(None, examples=["123, MG Road"])
    city: Optional[str] = Field(None, examples=["Mumbai"])
    country: Optional[str] = Field(None, examples=["India"])


class ProfileUpdate(BaseModel):
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
class ProfileResponse(BaseModel):
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
        from_attributes = True


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict | list] = None


class PaginatedResponse(BaseModel):
    success: bool
    message: str
    data: list
    total: int
    page: int
    limit: int