from app.database import db_client
from app.models import ProfileCreate, ProfileUpdate
from typing import Optional
from uuid import UUID

class ProfileService:
    """
    Profile ke saare database operations yahan hai
    PostgREST client use kar raha hai
    """
    
    def __init__(self):
        self.client = db_client
        self.table = "profiles"
    
    # ============ CREATE ============
    def create_profile(self, profile_data: ProfileCreate) -> dict:
        """
        Naya profile banata hai
        """
        # Pydantic model ko dictionary mein convert karo
        data = profile_data.model_dump(exclude_none=True)
        
        # Date ko string mein convert karo
        if 'date_of_birth' in data and data['date_of_birth']:
            data['date_of_birth'] = str(data['date_of_birth'])
        
        # Database mein insert karo
        response = self.client.from_(self.table).insert(data).execute()
        
        return response.data[0] if response.data else None
    
    # ============ READ (Single) ============
    def get_profile_by_id(self, profile_id: UUID) -> Optional[dict]:
        """
        ID se profile dhundta hai
        """
        response = self.client.from_(self.table)\
            .select("*")\
            .eq("id", str(profile_id))\
            .execute()
        
        return response.data[0] if response.data else None
    
    def get_profile_by_email(self, email: str) -> Optional[dict]:
        """
        Email se profile dhundta hai
        """
        response = self.client.from_(self.table)\
            .select("*")\
            .eq("email", email)\
            .execute()
        
        return response.data[0] if response.data else None
    
    # ============ READ (Multiple) ============
    def get_all_profiles(
        self, 
        page: int = 1, 
        limit: int = 10,
        is_active: Optional[bool] = None
    ) -> tuple[list, int]:
        """
        Saare profiles laata hai with pagination
        Returns: (profiles_list, total_count)
        """
        # Offset calculate karo
        offset = (page - 1) * limit
        
        # Base query
        query = self.client.from_(self.table).select("*", count="exact")
        
        # Filter lagao agar chahiye
        if is_active is not None:
            query = query.eq("is_active", is_active)
        
        # Pagination aur sorting
        response = query\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        total = response.count if response.count else len(response.data)
        return response.data, total
    
    # ============ UPDATE ============
    def update_profile(self, profile_id: UUID, update_data: ProfileUpdate) -> Optional[dict]:
        """
        Profile update karta hai
        """
        # Sirf non-None values lo
        data = update_data.model_dump(exclude_none=True)
        
        # Agar kuch update karne ko nahi hai
        if not data:
            return self.get_profile_by_id(profile_id)
        
        # Date convert karo
        if 'date_of_birth' in data and data['date_of_birth']:
            data['date_of_birth'] = str(data['date_of_birth'])
        
        # Update karo
        response = self.client.from_(self.table)\
            .update(data)\
            .eq("id", str(profile_id))\
            .execute()
        
        return response.data[0] if response.data else None
    
    # ============ DELETE ============
    def delete_profile(self, profile_id: UUID) -> bool:
        """
        Profile delete karta hai
        """
        response = self.client.from_(self.table)\
            .delete()\
            .eq("id", str(profile_id))\
            .execute()
        
        return len(response.data) > 0
    
    # ============ SEARCH ============
    def search_profiles(self, search_term: str, limit: int = 10) -> list:
        """
        Name ya email se search karta hai
        """
        # PostgREST mein ilike search
        response = self.client.from_(self.table)\
            .select("*")\
            .or_(f"full_name.ilike.%{search_term}%,email.ilike.%{search_term}%")\
            .limit(limit)\
            .execute()
        
        return response.data


# Singleton instance
profile_service = ProfileService()