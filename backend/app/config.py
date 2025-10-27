from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional
import secrets


class Settings(BaseSettings):
    # App
    app_name: str = "BFA Audit App"
    debug: bool = False
    version: str = "1.2.0"
    
    # Database
    database_url: str = "sqlite:///./bfa_audit.db"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_timeout: int = 30
    database_pool_recycle: int = 3600
    
    # Security
    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    password_min_length: int = 8
    
    # API Keys
    claude_api_key: Optional[str] = None
    gamma_api_key: Optional[str] = None
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    ai_rate_limit_requests: int = 10
    ai_rate_limit_window: int = 300
    
    # File Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [".pdf", ".docx", ".txt", ".md", ".xlsx"]
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance
    enable_compression: bool = True
    enable_caching: bool = True
    cache_ttl: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()
