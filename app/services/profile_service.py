from app.database import db_client
from app.models import ProfileCreate, ProfileUpdate
from typing import Optional
from uuid import UUID


class ProfileService:
    """Profile CRUD operations"""
    
    def __init__(self):
        self.client = db_client
        self.table = "profiles"
    
    def create_profile(self, profile_data: ProfileCreate) -> Optional[dict]:
        """Create new profile"""
        data = profile_data.model_dump(exclude_none=True)
        
        # Convert date to string
        if 'date_of_birth' in data and data['date_of_birth']:
            data['date_of_birth'] = str(data['date_of_birth'])
        
        response = self.client.from_(self.table).insert(data).execute()
        return response.data[0] if response.data else None
    
    def get_profile_by_id(self, profile_id: UUID) -> Optional[dict]:
        """Get profile by ID"""
        response = self.client.from_(self.table)\
            .select("*")\
            .eq("id", str(profile_id))\
            .execute()
        
        return response.data[0] if response.data else None
    
    def get_profile_by_email(self, email: str) -> Optional[dict]:
        """Get profile by email"""
        response = self.client.from_(self.table)\
            .select("*")\
            .eq("email", email)\
            .execute()
        
        return response.data[0] if response.data else None
    
    def get_all_profiles(
        self, 
        page: int = 1, 
        limit: int = 10,
        is_active: Optional[bool] = None
    ) -> tuple[list, int]:
        """Get all profiles with pagination"""
        offset = (page - 1) * limit
        
        query = self.client.from_(self.table).select("*", count="exact")
        
        if is_active is not None:
            query = query.eq("is_active", is_active)
        
        response = query\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        total = response.count if response.count else len(response.data)
        return response.data, total
    
    def update_profile(self, profile_id: UUID, update_data: ProfileUpdate) -> Optional[dict]:
        """Update profile"""
        data = update_data.model_dump(exclude_none=True)
        
        if not data:
            return self.get_profile_by_id(profile_id)
        
        if 'date_of_birth' in data and data['date_of_birth']:
            data['date_of_birth'] = str(data['date_of_birth'])
        
        response = self.client.from_(self.table)\
            .update(data)\
            .eq("id", str(profile_id))\
            .execute()
        
        return response.data[0] if response.data else None
    
    def delete_profile(self, profile_id: UUID) -> bool:
        """Delete profile"""
        response = self.client.from_(self.table)\
            .delete()\
            .eq("id", str(profile_id))\
            .execute()
        
        return len(response.data) > 0
    
    def search_profiles(self, search_term: str, limit: int = 10) -> list:
        """Search profiles by name or email"""
        response = self.client.from_(self.table)\
            .select("*")\
            .or_(f"full_name.ilike.%{search_term}%,email.ilike.%{search_term}%")\
            .limit(limit)\
            .execute()
        
        return response.data


# Singleton instance
profile_service = ProfileService()