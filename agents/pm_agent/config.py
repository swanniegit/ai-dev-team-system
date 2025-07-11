"""
Configuration for the PM Agent
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class PMAgentConfig:
    """PM Agent configuration"""
    
    # Agent Identity
    name: str = "PM Agent Alpha"
    agent_type: str = "project_manager"
    version: str = "1.0.0"
    
    # API Connection
    api_base_url: str = "http://localhost:8000"
    api_timeout: int = 30
    
    # Capabilities
    capabilities: List[str] = None
    
    # Behavior Settings
    heartbeat_interval: int = 60  # seconds
    issue_check_interval: int = 300  # seconds
    max_issues_per_batch: int = 10
    
    # Issue Triage Rules
    priority_keywords: Dict[str, List[str]] = None
    auto_assign_rules: Dict[str, str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = [
                "issue_triage",
                "sprint_planning", 
                "project_monitoring",
                "stakeholder_communication"
            ]
        
        if self.priority_keywords is None:
            self.priority_keywords = {
                "critical": ["urgent", "blocker", "production", "security", "hotfix"],
                "high": ["important", "deadline", "customer", "feature"],
                "medium": ["enhancement", "improvement", "nice-to-have"],
                "low": ["documentation", "cleanup", "refactor"]
            }
        
        if self.auto_assign_rules is None:
            self.auto_assign_rules = {
                "bug": "qa_engineer",
                "feature": "product_owner", 
                "story": "product_owner",
                "task": "developer",
                "epic": "product_owner"
            }
    
    @classmethod
    def from_env(cls):
        """Create config from environment variables"""
        return cls(
            name=os.getenv("PM_AGENT_NAME", "PM Agent Alpha"),
            api_base_url=os.getenv("API_BASE_URL", "http://localhost:8000"),
            heartbeat_interval=int(os.getenv("HEARTBEAT_INTERVAL", "60")),
            issue_check_interval=int(os.getenv("ISSUE_CHECK_INTERVAL", "300"))
        )


# Global config instance
config = PMAgentConfig.from_env() 