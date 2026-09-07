"""Application Configuration Module."""
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    PROJECT_NAME: str = "Resume Master AI Screening & Job Matching"
    API_V1_STR: str = "/api"
    DEBUG: bool = True

    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/resume_matcher_db"

    # Security Settings
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS Settings
    ALLOWED_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173"

    # Uploads
    MAX_UPLOAD_SIZE_MB: int = 5
    UPLOAD_DIR: str = "./uploads"

    @property
    def cors_origins(self) -> List[str]:
        """Convert comma-separated origins string to a list."""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        return self.ALLOWED_ORIGINS

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
