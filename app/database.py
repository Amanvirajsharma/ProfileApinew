from postgrest import SyncPostgrestClient
from app.config import get_settings

settings = get_settings()

def get_database_client() -> SyncPostgrestClient:
    """
    PostgREST client banata hai - Direct Supabase REST API use karta hai
    """
    # Supabase REST endpoint
    rest_url = f"{settings.supabase_url}/rest/v1"
    
    client = SyncPostgrestClient(
        base_url=rest_url,
        headers={
            "apikey": settings.supabase_key,
            "Authorization": f"Bearer {settings.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    )
    return client

# Global client
db_client = get_database_client()