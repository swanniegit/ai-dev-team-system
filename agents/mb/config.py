"""
MB Agent Configuration
Handles all configuration settings for the Morale Booster Agent
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class MBAgentConfig:
    """Configuration for MB Agent"""
    
    # Agent Identity
    agent_name: str = "mb_agent"
    agent_version: str = "1.0.0"
    agent_description: str = "Morale Booster Agent for team wellness and motivation"
    
    # Claude Integration
    claude_api_key: str = field(default_factory=lambda: os.getenv("CLAUDE_API_KEY", ""))
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 4000
    claude_temperature: float = 0.7  # Higher temperature for creative responses
    
    # API Hub Integration
    api_hub_url: str = field(default_factory=lambda: os.getenv("API_HUB_URL", "http://localhost:8000"))
    api_hub_timeout: int = 30
    
    # Wellness Configuration
    checkin_frequency: str = "daily"
    mood_threshold: float = 6.0  # 1-10 scale
    stress_threshold: float = 7.0  # 1-10 scale
    
    # Communication Settings
    slack_webhook: str = field(default_factory=lambda: os.getenv("SLACK_WEBHOOK", ""))
    email_enabled: bool = True
    notification_frequency: str = "daily"
    
    # Wellness Categories
    wellness_categories: List[str] = field(default_factory=lambda: [
        "mood", "stress", "work_life_balance", "team_collaboration", "recognition"
    ])
    
    # Monitoring
    health_check_port: int = 8006
    log_level: str = "INFO"
    log_file: str = "mb_agent.log"
    
    # Behavior Configuration
    behaviors: Dict[str, Any] = field(default_factory=lambda: {
        "wellness_monitoring": {
            "enabled": True,
            "frequency": "daily",
            "priority": "high"
        },
        "mood_tracking": {
            "enabled": True,
            "frequency": "daily",
            "priority": "high"
        },
        "stress_detection": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "critical"
        },
        "burnout_prevention": {
            "enabled": True,
            "frequency": "daily",
            "priority": "high"
        },
        "work_life_balance": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "medium"
        },
        "achievement_recognition": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "high"
        },
        "milestone_celebration": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "medium"
        },
        "peer_recognition": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "medium"
        },
        "team_building": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "low"
        },
        "mental_health_support": {
            "enabled": True,
            "frequency": "daily",
            "priority": "critical"
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
        
        if self.mood_threshold < 1 or self.mood_threshold > 10:
            raise ValueError("mood_threshold must be between 1 and 10")
        
        if self.stress_threshold < 1 or self.stress_threshold > 10:
            raise ValueError("stress_threshold must be between 1 and 10")
    
    def _create_directories(self):
        """Create necessary directories"""
        Path("wellness_data").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        Path("activities").mkdir(exist_ok=True)
    
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
            "wellness_categories": self.wellness_categories,
            "mood_threshold": self.mood_threshold,
            "stress_threshold": self.stress_threshold,
            "behaviors": self.behaviors
        }

# Global configuration instance
config = MBAgentConfig() 