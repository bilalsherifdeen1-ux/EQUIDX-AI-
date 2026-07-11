"""
Centralized application configuration.

Loaded once as a singleton (`get_settings`) and injected wherever needed via
FastAPI's dependency system rather than imported ad hoc — this keeps config
access testable and mockable (Dependency Inversion Principle).
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # General
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "EQUIDX AI"
    API_V1_PREFIX: str = "/api/v1"
    LOG_LEVEL: str = "info"

    # Security
    SECRET_KEY: str = "change-me-in-production-please-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OAuth2
    OAUTH2_GOOGLE_CLIENT_ID: str = ""
    OAUTH2_GOOGLE_CLIENT_SECRET: str = ""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://equidx:equidx_dev_password@postgres:5432/equidx"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Object storage
    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "equidx_minio"
    S3_SECRET_KEY: str = "equidx_minio_secret"
    S3_BUCKET_NAME: str = "equidx-uploads"
    S3_REGION: str = "us-east-1"

    # Downstream services
    AI_ENGINE_URL: str = "http://ai-engine:8100"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8400"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
