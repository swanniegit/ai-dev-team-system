"""
QA Agent Configuration
Handles all configuration settings for the QA Agent
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class QAAgentConfig:
    """Configuration for QA Agent"""
    
    # Agent Identity
    agent_name: str = "qa_agent"
    agent_version: str = "1.0.0"
    agent_description: str = "Quality Assurance Agent for automated testing and quality control"
    
    # Claude Integration
    claude_api_key: str = field(default_factory=lambda: os.getenv("CLAUDE_API_KEY", ""))
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 4000
    claude_temperature: float = 0.1
    
    # API Hub Integration
    api_hub_url: str = field(default_factory=lambda: os.getenv("API_HUB_URL", "http://localhost:8000"))
    api_hub_timeout: int = 30
    
    # Test Configuration
    test_timeout: int = 300  # 5 minutes
    max_retries: int = 3
    parallel_tests: int = 4
    
    # Test Types
    test_types: List[str] = field(default_factory=lambda: [
        "unit", "integration", "regression", "performance", "security", "accessibility"
    ])
    
    # Quality Gates
    min_test_coverage: float = 80.0
    max_bug_density: float = 5.0  # bugs per 1000 lines
    performance_threshold: float = 2.0  # seconds
    
    # Reporting
    report_format: str = "html"  # html, json, xml
    report_directory: str = "reports"
    enable_notifications: bool = True
    
    # Test Data Management
    test_data_dir: str = "test_data"
    test_environment: str = "staging"
    
    # Integration Settings
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    jira_url: str = field(default_factory=lambda: os.getenv("JIRA_URL", ""))
    jira_username: str = field(default_factory=lambda: os.getenv("JIRA_USERNAME", ""))
    jira_password: str = field(default_factory=lambda: os.getenv("JIRA_PASSWORD", ""))
    
    # Monitoring
    health_check_port: int = 8003
    log_level: str = "INFO"
    log_file: str = "qa_agent.log"
    
    # Behavior Configuration
    behaviors: Dict[str, Any] = field(default_factory=lambda: {
        "test_planning": {
            "enabled": True,
            "frequency": "daily",
            "priority": "high"
        },
        "test_execution": {
            "enabled": True,
            "frequency": "continuous",
            "priority": "critical"
        },
        "bug_tracking": {
            "enabled": True,
            "frequency": "real_time",
            "priority": "high"
        },
        "quality_reporting": {
            "enabled": True,
            "frequency": "daily",
            "priority": "medium"
        },
        "test_automation": {
            "enabled": True,
            "frequency": "continuous",
            "priority": "high"
        },
        "performance_testing": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "medium"
        },
        "security_testing": {
            "enabled": True,
            "frequency": "weekly",
            "priority": "high"
        },
        "accessibility_testing": {
            "enabled": True,
            "frequency": "sprint_end",
            "priority": "medium"
        },
        "regression_testing": {
            "enabled": True,
            "frequency": "pre_deploy",
            "priority": "critical"
        },
        "test_coverage_analysis": {
            "enabled": True,
            "frequency": "daily",
            "priority": "medium"
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
        
        if self.min_test_coverage < 0 or self.min_test_coverage > 100:
            raise ValueError("min_test_coverage must be between 0 and 100")
        
        if self.max_bug_density < 0:
            raise ValueError("max_bug_density must be positive")
    
    def _create_directories(self):
        """Create necessary directories"""
        Path(self.report_directory).mkdir(exist_ok=True)
        Path(self.test_data_dir).mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
    
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
            "test_types": self.test_types,
            "min_test_coverage": self.min_test_coverage,
            "max_bug_density": self.max_bug_density,
            "performance_threshold": self.performance_threshold,
            "behaviors": self.behaviors
        }

# Global configuration instance
config = QAAgentConfig() 