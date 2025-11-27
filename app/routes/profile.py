from fastapi import APIRouter, HTTPException, Query
from app.models import (
    ProfileCreate, 
    ProfileUpdate, 
    APIResponse, 
    PaginatedResponse
)
from app.services.profile_service import profile_service
from uuid import UUID
from typing import Optional

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=APIResponse, status_code=201)
def create_profile(profile: ProfileCreate):
    """Create new profile"""
    existing = profile_service.get_profile_by_email(profile.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists!")
    
    new_profile = profile_service.create_profile(profile)
    
    if not new_profile:
        raise HTTPException(status_code=500, detail="Failed to create profile")
    
    return APIResponse(
        success=True,
        message="Profile created successfully!",
        data=new_profile
    )


@router.get("/", response_model=PaginatedResponse)
def get_all_profiles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None
):
    """Get all profiles with pagination"""
    profiles, total = profile_service.get_all_profiles(page, limit, is_active)
    
    return PaginatedResponse(
        success=True,
        message=f"Found {len(profiles)} profiles",
        data=profiles,
        total=total,
        page=page,
        limit=limit
    )


@router.get("/search/", response_model=APIResponse)
def search_profiles(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50)
):
    """Search profiles"""
    profiles = profile_service.search_profiles(q, limit)
    
    return APIResponse(
        success=True,
        message=f"Found {len(profiles)} profiles",
        data=profiles
    )


@router.get("/{profile_id}", response_model=APIResponse)
def get_profile(profile_id: UUID):
    """Get single profile"""
    profile = profile_service.get_profile_by_id(profile_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found!")
    
    return APIResponse(
        success=True,
        message="Profile found!",
        data=profile
    )


@router.put("/{profile_id}", response_model=APIResponse)
def update_profile(profile_id: UUID, profile_update: ProfileUpdate):
    """Update profile"""
    existing = profile_service.get_profile_by_id(profile_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found!")
    
    updated_profile = profile_service.update_profile(profile_id, profile_update)
    
    return APIResponse(
        success=True,
        message="Profile updated!",
        data=updated_profile
    )


@router.delete("/{profile_id}", response_model=APIResponse)
def delete_profile(profile_id: UUID):
    """Delete profile"""
    existing = profile_service.get_profile_by_id(profile_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found!")
    
    deleted = profile_service.delete_profile(profile_id)
    
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete!")
    
    return APIResponse(
        success=True,
        message="Profile deleted!",
        data={"deleted_id": str(profile_id)}
    )