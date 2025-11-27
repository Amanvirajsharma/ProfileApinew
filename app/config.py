from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Configuration settings - .env file se values load hoti hai
    """
    supabase_url: str
    supabase_key: str
    
    class Config:
        env_file = ".env"

@lru_cache()  # Cache karta hai taaki baar baar load na ho
def get_settings():
    return Settings()