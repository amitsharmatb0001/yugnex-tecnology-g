"""
FILE: settings.py
PATH: yugnex/backend/config/settings.py
PURPOSE: Manages application configuration and environment variables.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the backend directory (parent of config/)
BACKEND_DIR = Path(__file__).parent.parent
ENV_FILE = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "YugNex API"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Database (PostgreSQL)
    # IMPORTANT: Set DATABASE_URL in .env file - never commit credentials to git!
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/yugnex_db"
    
    # Database (Redis)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "supersecretkey_change_me_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Providers (Standard)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    # Model selection is now dynamic based on task requirements
    # Available Claude models: claude-sonnet-4-5, claude-haiku-4-5, claude-opus-4-5, claude-opus-4-1
    # If set, this will override dynamic selection (not recommended - let system choose)
    ANTHROPIC_MODEL: Optional[str] = None  # Optional override (None = use dynamic selection)
    ANTHROPIC_MODEL_MAP: Optional[str] = None  # Optional JSON mapping: {"claude-sonnet-4.5": "actual-model-name"}
    GOOGLE_API_KEY: Optional[str] = None
    
    # AI Providers (Google Extras)
    GOOGLE_AI_STUDIO_KEY: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    GOOGLE_PROJECT_ID: Optional[str] = None
    
    @field_validator('ANTHROPIC_API_KEY', 'GOOGLE_API_KEY', 'GOOGLE_AI_STUDIO_KEY', mode='before')
    @classmethod
    def strip_api_keys(cls, v):
        """Strip whitespace from API keys (common .env file issue)."""
        if isinstance(v, str):
            return v.strip()
        return v
    
    # Feature Flags
    ENABLE_GEMINI_FALLBACK: bool = True
    AUTO_SWITCH_ON_RATE_LIMIT: bool = True
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else ".env",  # Use absolute path if exists, else relative
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()