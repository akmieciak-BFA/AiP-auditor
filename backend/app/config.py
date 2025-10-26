from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "BFA Audit App"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./bfa_audit.db"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # API Keys
    claude_api_key: str = ""
    gamma_api_key: str = ""
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
