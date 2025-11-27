from fastapi import APIRouter, HTTPException, Query
from app.models import (
    ProfileCreate, 
    ProfileUpdate, 
    ProfileResponse,
    APIResponse, 
    PaginatedResponse
)
from app.services.profile_service import profile_service
from uuid import UUID
from typing import Optional

# Router banao
router = APIRouter(prefix="/profiles", tags=["Profiles"])


# ============ CREATE ============
@router.post("/", response_model=APIResponse, status_code=201)
def create_profile(profile: ProfileCreate):
    """
    ✨ Naya profile banao
    
    - **full_name**: Poora naam (required)
    - **email**: Email address (required, unique hona chahiye)
    - **phone**: Phone number (optional)
    - Baaki sab optional hai
    """
    # Check karo email pehle se hai ya nahi
    existing = profile_service.get_profile_by_email(profile.email)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered hai bhai!"
        )
    
    # Profile create karo
    new_profile = profile_service.create_profile(profile)
    
    if not new_profile:
        raise HTTPException(
            status_code=500, 
            detail="Profile create nahi ho paya!"
        )
    
    return APIResponse(
        success=True,
        message="Profile successfully ban gaya! 🎉",
        data=new_profile
    )


# ============ READ ALL ============
@router.get("/", response_model=PaginatedResponse)
def get_all_profiles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Profiles per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    📋 Saare profiles dekho with pagination
    
    - **page**: Konsa page chahiye (default: 1)
    - **limit**: Ek page mein kitne profiles (default: 10, max: 100)
    - **is_active**: Sirf active/inactive profiles filter karo
    """
    profiles, total = profile_service.get_all_profiles(page, limit, is_active)
    
    return PaginatedResponse(
        success=True,
        message=f"{len(profiles)} profiles mil gaye!",
        data=profiles,
        total=total,
        page=page,
        limit=limit
    )


# ============ READ ONE ============
@router.get("/{profile_id}", response_model=APIResponse)
def get_profile(profile_id: UUID):
    """
    👤 Ek specific profile dekho
    
    - **profile_id**: Profile ka UUID
    """
    profile = profile_service.get_profile_by_id(profile_id)
    
    if not profile:
        raise HTTPException(
            status_code=404, 
            detail="Profile nahi mila bhai!"
        )
    
    return APIResponse(
        success=True,
        message="Profile mil gaya!",
        data=profile
    )


# ============ UPDATE ============
@router.put("/{profile_id}", response_model=APIResponse)
def update_profile(profile_id: UUID, profile_update: ProfileUpdate):
    """
    ✏️ Profile update karo
    
    - Sirf wo fields bhejo jo update karni hai
    - Email update nahi hota (security ke liye)
    """
    # Check karo profile exist karta hai
    existing = profile_service.get_profile_by_id(profile_id)
    if not existing:
        raise HTTPException(
            status_code=404, 
            detail="Profile nahi mila bhai!"
        )
    
    # Update karo
    updated_profile = profile_service.update_profile(profile_id, profile_update)
    
    return APIResponse(
        success=True,
        message="Profile update ho gaya! ✅",
        data=updated_profile
    )


# ============ DELETE ============
@router.delete("/{profile_id}", response_model=APIResponse)
def delete_profile(profile_id: UUID):
    """
    🗑️ Profile delete karo
    
    - **Warning**: Ye permanent hai, wapas nahi aayega!
    """
    # Check karo profile exist karta hai
    existing = profile_service.get_profile_by_id(profile_id)
    if not existing:
        raise HTTPException(
            status_code=404, 
            detail="Profile nahi mila bhai!"
        )
    
    # Delete karo
    deleted = profile_service.delete_profile(profile_id)
    
    if not deleted:
        raise HTTPException(
            status_code=500, 
            detail="Delete nahi ho paya!"
        )
    
    return APIResponse(
        success=True,
        message="Profile delete ho gaya! 🗑️",
        data={"deleted_id": str(profile_id)}
    )


# ============ SEARCH ============
@router.get("/search/", response_model=APIResponse)
def search_profiles(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Max results")
):
    """
    🔍 Profile search karo
    
    - Name ya email se search hoga
    - Minimum 2 characters chahiye
    """
    profiles = profile_service.search_profiles(q, limit)
    
    return APIResponse(
        success=True,
        message=f"{len(profiles)} profiles mile search mein!",
        data=profiles
    )