"""
AD Agent Configuration
Handles all configuration settings for the Application Deployment Agent
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ADAgentConfig:
    """Configuration for AD Agent"""
    
    # Agent Identity
    agent_name: str = "ad_agent"
    agent_version: str = "1.0.0"
    agent_description: str = "Application Deployment Agent for automated deployment and infrastructure management"
    
    # Claude Integration
    claude_api_key: str = field(default_factory=lambda: os.getenv("CLAUDE_API_KEY", ""))
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 4000
    claude_temperature: float = 0.1
    
    # API Hub Integration
    api_hub_url: str = field(default_factory=lambda: os.getenv("API_HUB_URL", "http://localhost:8000"))
    api_hub_timeout: int = 30
    
    # Deployment Configuration
    deployment_timeout: int = 1800  # 30 minutes
    max_retries: int = 3
    rollback_enabled: bool = True
    
    # Environment Configuration
    environments: List[str] = field(default_factory=lambda: [
        "development", "staging", "production"
    ])
    
    # Infrastructure Settings
    cloud_provider: str = field(default_factory=lambda: os.getenv("CLOUD_PROVIDER", "aws"))
    kubernetes_enabled: bool = True
    docker_enabled: bool = True
    
    # Integration Settings
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    aws_access_key: str = field(default_factory=lambda: os.getenv("AWS_ACCESS_KEY_ID", ""))
    aws_secret_key: str = field(default_factory=lambda: os.getenv("AWS_SECRET_ACCESS_KEY", ""))
    gcp_credentials: str = field(default_factory=lambda: os.getenv("GCP_CREDENTIALS", ""))
    azure_credentials: str = field(default_factory=lambda: os.getenv("AZURE_CREDENTIALS", ""))
    
    # Monitoring
    health_check_port: int = 8005
    log_level: str = "INFO"
    log_file: str = "ad_agent.log"
    
    # Behavior Configuration
    behaviors: Dict[str, Any] = field(default_factory=lambda: {
        "deployment_planning": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "critical"
        },
        "infrastructure_provisioning": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "critical"
        },
        "deployment_execution": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "critical"
        },
        "health_monitoring": {
            "enabled": True,
            "frequency": "continuous",
            "priority": "high"
        },
        "rollback_management": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "critical"
        },
        "scaling_management": {
            "enabled": True,
            "frequency": "continuous",
            "priority": "medium"
        },
        "security_compliance": {
            "enabled": True,
            "frequency": "daily",
            "priority": "high"
        },
        "backup_management": {
            "enabled": True,
            "frequency": "daily",
            "priority": "medium"
        },
        "cost_optimization": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "low"
        },
        "disaster_recovery": {
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
        
        if self.deployment_timeout < 300:
            raise ValueError("deployment_timeout must be at least 300 seconds")
    
    def _create_directories(self):
        """Create necessary directories"""
        Path("deployments").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        Path("configs").mkdir(exist_ok=True)
    
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
            "environments": self.environments,
            "cloud_provider": self.cloud_provider,
            "kubernetes_enabled": self.kubernetes_enabled,
            "docker_enabled": self.docker_enabled,
            "behaviors": self.behaviors
        }

# Global configuration instance
config = ADAgentConfig() 