"""
Configuration settings using Pydantic Settings
환경 변수를 관리하는 설정 파일
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application Settings
    APP_NAME: str = "EduGuard AI"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PORT: int = 8000

    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/eduguard_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # JWT & Authentication
    SECRET_KEY: str = "your_secret_key_here_please_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4o"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"

    # Safety Thresholds
    TOXICITY_THRESHOLD: float = 0.7
    PII_DETECTION_ENABLED: bool = True
    CONTENT_FILTER_STRICT_MODE: bool = True
    LLAMA_GUARD_THRESHOLD: float = 0.8

    # Google Perspective API
    GOOGLE_PERSPECTIVE_API_KEY: Optional[str] = None

    # Llama Guard Configuration
    LLAMA_GUARD_MODEL_PATH: str = "meta-llama/Llama-Guard-3-8B"

    # Pinecone Vector DB
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: str = "us-west1-gcp"
    PINECONE_INDEX_NAME: str = "eduguard-knowledge"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 30
    RATE_LIMIT_PER_HOUR: int = 500

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "./logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
