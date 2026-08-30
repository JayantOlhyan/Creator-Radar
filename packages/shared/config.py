"""Typed Application Configuration Management."""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App General
    APP_NAME: str = "CreatorRadar"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True

    # Server Ports
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    WEB_PORT: int = 3000

    # PostgreSQL Database
    POSTGRES_USER: str = "creatorradar"
    POSTGRES_PASSWORD: str = "creatorradar_dev_pass"
    POSTGRES_DB: str = "creatorradar_db"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = "postgresql+asyncpg://creatorradar:creatorradar_dev_pass@postgres:5432/creatorradar_db"

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379/0"

    # AI Provider Setup (openai, gemini, anthropic, local, mock)
    AI_PROVIDER: str = "mock"
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    LOCAL_AI_ENDPOINT: str = "http://localhost:11434"

    # Notifications
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
