"""
AR Agent Configuration
Handles all configuration settings for the Architecture Review Agent
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ARAgentConfig:
    """Configuration for AR Agent"""
    
    # Agent Identity
    agent_name: str = "ar_agent"
    agent_version: str = "1.0.0"
    agent_description: str = "Architecture Review Agent for code review and architectural decisions"
    
    # Claude Integration
    claude_api_key: str = field(default_factory=lambda: os.getenv("CLAUDE_API_KEY", ""))
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 4000
    claude_temperature: float = 0.1
    
    # API Hub Integration
    api_hub_url: str = field(default_factory=lambda: os.getenv("API_HUB_URL", "http://localhost:8000"))
    api_hub_timeout: int = 30
    
    # Review Configuration
    review_timeout: int = 600  # 10 minutes
    max_file_size: int = 1000000  # 1MB
    supported_languages: List[str] = field(default_factory=lambda: [
        "python", "javascript", "typescript", "java", "csharp", "go", "rust", "php", "ruby", "swift"
    ])
    
    # Quality Standards
    min_code_quality_score: float = 7.0  # 1-10 scale
    max_complexity_threshold: int = 10
    min_test_coverage: float = 80.0
    max_technical_debt: float = 5.0  # hours per 1000 lines
    
    # Review Categories
    review_categories: List[str] = field(default_factory=lambda: [
        "code_quality", "architecture", "security", "performance", "maintainability", "testability"
    ])
    
    # Integration Settings
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    github_api_url: str = "https://api.github.com"
    gitlab_token: str = field(default_factory=lambda: os.getenv("GITLAB_TOKEN", ""))
    gitlab_api_url: str = field(default_factory=lambda: os.getenv("GITLAB_API_URL", ""))
    
    # Monitoring
    health_check_port: int = 8004
    log_level: str = "INFO"
    log_file: str = "ar_agent.log"
    
    # Behavior Configuration
    behaviors: Dict[str, Any] = field(default_factory=lambda: {
        "code_review": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "critical"
        },
        "architecture_review": {
            "enabled": True,
            "frequency": "daily",
            "priority": "high"
        },
        "security_review": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "critical"
        },
        "performance_review": {
            "enabled": True,
            "frequency": "daily",
            "priority": "medium"
        },
        "maintainability_review": {
            "enabled": True,
            "frequency": "daily",
            "priority": "medium"
        },
        "testability_review": {
            "enabled": True,
            "frequency": "daily",
            "priority": "medium"
        },
        "documentation_review": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "low"
        },
        "best_practices_review": {
            "enabled": True,
            "frequency": "daily",
            "priority": "high"
        },
        "dependency_review": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "medium"
        },
        "compliance_review": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "high"
        }
    })
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()
        self._create_directories()
    
    def _validate_config(self):
        """Validate configuration settings"""
        if not self.claude_api_key:
            raise ValueError("CLAUDE_API_KEY environment variable is required")
        
        if not self.api_hub_url:
            raise ValueError("API_HUB_URL environment variable is required")
        
        if self.min_code_quality_score < 1 or self.min_code_quality_score > 10:
            raise ValueError("min_code_quality_score must be between 1 and 10")
        
        if self.max_complexity_threshold < 1:
            raise ValueError("max_complexity_threshold must be positive")
    
    def _create_directories(self):
        """Create necessary directories"""
        Path("reviews").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        Path("temp").mkdir(exist_ok=True)
    
    def get_behavior_config(self, behavior_name: str) -> Dict[str, Any]:
        """Get configuration for a specific behavior"""
        return self.behaviors.get(behavior_name, {})
    
    def is_behavior_enabled(self, behavior_name: str) -> bool:
        """Check if a behavior is enabled"""
        config = self.get_behavior_config(behavior_name)
        return config.get("enabled", False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "agent_name": self.agent_name,
            "agent_version": self.agent_version,
            "agent_description": self.agent_description,
            "claude_model": self.claude_model,
            "api_hub_url": self.api_hub_url,
            "supported_languages": self.supported_languages,
            "review_categories": self.review_categories,
            "min_code_quality_score": self.min_code_quality_score,
            "max_complexity_threshold": self.max_complexity_threshold,
            "min_test_coverage": self.min_test_coverage,
            "behaviors": self.behaviors
        }

# Global configuration instance
config = ARAgentConfig() 