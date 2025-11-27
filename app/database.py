from supabase import create_client, Client
from app.config import get_settings

settings = get_settings()

def get_supabase_client() -> Client:
    """
    Supabase client banata hai
    Ek baar connect karo, baar baar use karo
    """
    supabase: Client = create_client(
        settings.supabase_url,
        settings.supabase_key
    )
    return supabase

# Global client - poore app mein use hoga
supabase_client = get_supabase_client()