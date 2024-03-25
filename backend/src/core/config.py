import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the application."""

    debug: bool = False
    environment: str = "production"
    docs_url: str = "/arq/api/docs"
    openapi_url: str = "/arq/api/openapi.json"
    redoc_url: str = "/arq/api/redoc"
    title: str = "Arq UI API"
    version: str = "0.1.0"
    summary: str = "Interface for Arq background jobs."
    description: str = ""

    cors_allowed_hosts: list[str] | None = ["http://localhost:5173"]
    api_prefix: str = "/arq/api"

    timezone: str = "UTC"

    redis_host: str = "redis"
    redis_password: str = ""
    redis_username: str = ""
    redis_port: int = 6379
    redis_ssl: bool = False
    redis_ssl_cert_reqs: str = "none"
    redis_db: int = 0

    max_jobs: int = 50000
    request_semaphore_jobs: int = 5

    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"))


@lru_cache
def get_app_settings() -> Settings:
    """Retrieve the application settings.

    Returns
    -------
        Settings: The application settings.

    """
    return Settings()
