"""
Application configuration and settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Agentice"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Database
    DATABASE_URL: str
    REDIS_URL: str
    
    # LLM Providers
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"  # Default to GPT-4o
    ANTHROPIC_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_KEY: Optional[str] = None
    
    # AutoGen
    AUTOGEN_USE_DOCKER: bool = False
    AUTOGEN_MAX_CONSECUTIVE_AUTO_REPLY: int = 10
    AUTOGEN_HUMAN_INPUT_MODE: str = "ALWAYS"
    
    # Google Services
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GMAIL_SCOPES: str
    CALENDAR_SCOPES: str
    
    # Microsoft Services
    MICROSOFT_CLIENT_ID: Optional[str] = None
    MICROSOFT_CLIENT_SECRET: Optional[str] = None
    MICROSOFT_TENANT_ID: Optional[str] = None
    
    # GitHub
    GITHUB_TOKEN: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    
    # LinkedIn
    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None
    LINKEDIN_ACCESS_TOKEN: Optional[str] = None
    
    # Job Board APIs
    INDEED_API_KEY: Optional[str] = None
    LINKEDIN_JOBS_API_KEY: Optional[str] = None
    GLASSDOOR_API_KEY: Optional[str] = None
    
    # Storage
    RESUME_STORAGE_PATH: str = "/data/resumes"
    DOCUMENT_STORAGE_PATH: str = "/data/documents"
    TEMP_FILE_PATH: str = "/tmp/agentice"
    
    # Notifications
    NOTIFICATION_EMAIL_FROM: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_PORT: int = 9090
    
    # Feature Flags
    ENABLE_AUTO_APPLY: bool = False
    ENABLE_VOICE_INTERFACE: bool = False
    REQUIRE_APPROVAL_FOR_EMAILS: bool = True
    REQUIRE_APPROVAL_FOR_APPLICATIONS: bool = True
    ENABLE_PROFILE_AUTO_UPDATE: bool = False
    
    # Rate Limiting
    MAX_APPLICATIONS_PER_DAY: int = 50
    MAX_EMAILS_PER_HOUR: int = 100
    MAX_PROFILE_UPDATES_PER_WEEK: int = 10
    
    # AI Models
    DEFAULT_LLM_MODEL: str = "gpt-4-turbo-preview"
    FAST_LLM_MODEL: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    RESUME_OPTIMIZATION_MODEL: str = "gpt-4-turbo-preview"
    COVER_LETTER_MODEL: str = "gpt-4-turbo-preview"
    
    # Vector Database
    VECTOR_DB_TYPE: str = "pgvector"
    VECTOR_DIMENSION: int = 1536
    SIMILARITY_THRESHOLD: float = 0.75
    
    # Security
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 30
    ENCRYPTION_KEY: str
    
    # Application Tracking
    TRACK_APPLICATION_STATUS: bool = True
    APPLICATION_FOLLOWUP_DAYS: str = "7,14,21"
    
    @property
    def followup_days_list(self) -> List[int]:
        return [int(day.strip()) for day in self.APPLICATION_FOLLOWUP_DAYS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
