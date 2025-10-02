from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = Field(default="sqlite:///./test.db", alias="DATABASE_URL")

    # Application
    secret_key: str = Field(alias="SECRET_KEY")
    jwt_secret_key: str = Field(default="test-secret-key-for-development", alias="JWT_SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    debug: bool = Field(default=False, alias="DEBUG")

    # Supabase (optional, for reference)
    supabase_url: Optional[str] = Field(default=None, alias="SUPABASE_URL")
    supabase_anon_key: Optional[str] = Field(default=None, alias="SUPABASE_ANON_KEY")
    supabase_service_role_key: Optional[str] = Field(default=None, alias="SUPABASE_SERVICE_ROLE_KEY")

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra='allow'
    )


settings = Settings()
