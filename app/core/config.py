from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = Field("sqlite:///./test.db")

    # Application
    secret_key: str = Field(..., env="SECRET_KEY")
    jwt_secret_key: str = Field("test-secret-key-for-development", env="JWT_SECRET_KEY")
    algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    debug: bool = Field(False, env="DEBUG")

    # Supabase (optional, for reference)
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra='allow'
    )


settings = Settings()
