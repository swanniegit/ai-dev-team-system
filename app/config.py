"""
Configuration settings for the Agentic Agile System API Hub
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Settings
    api_v1_str: str = Field(default="/v1", env="API_V1_STR")
    project_name: str = Field(default="Agentic Agile System API", env="PROJECT_NAME")
    version: str = Field(default="1.0.0", env="VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database URLs
    database_url: str = Field(
        default="postgresql://user:pass@localhost/agentic_agile",
        env="DATABASE_URL"
    )
    mongodb_url: str = Field(
        default="mongodb://localhost:27017/agentic_agile",
        env="MONGODB_URL"
    )
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=3600, env="RATE_LIMIT_WINDOW")  # 1 hour
    
    # CORS
    cors_origins: list = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Event Bus
    event_bus_enabled: bool = Field(default=True, env="EVENT_BUS_ENABLED")
    
    # Agent Settings
    max_agents_per_type: int = Field(default=5, env="MAX_AGENTS_PER_TYPE")
    agent_heartbeat_timeout: int = Field(default=300, env="AGENT_HEARTBEAT_TIMEOUT")  # 5 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 