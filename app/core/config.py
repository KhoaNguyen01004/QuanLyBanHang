from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./test.db"

    # Application
    secret_key: str = "test-secret-key-for-development"
    debug: bool = False

    # Supabase (optional, for reference)
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()
