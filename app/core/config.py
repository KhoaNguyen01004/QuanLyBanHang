from pydantic import BaseSettings  # type: ignore
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str

    # Application
    secret_key: str
    debug: bool = False

    # Supabase (optional, for reference)
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
