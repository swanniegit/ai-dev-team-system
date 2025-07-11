"""
Configuration for Developer Agent
"""

import os
from typing import List, Dict, Any

class DEVConfig:
    """Configuration for Developer Agent"""
    # Agent Identity
    name = "Developer Agent"
    version = "1.0.0"
    agent_type = "dev"
    # API Configuration
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    api_timeout = int(os.getenv("API_TIMEOUT", "30"))
    # Agent Behavior Configuration
    heartbeat_interval = int(os.getenv("HEARTBEAT_INTERVAL", "60"))
    code_check_interval = int(os.getenv("CODE_CHECK_INTERVAL", "300"))
    # Claude 3.7 Sonnet Integration
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    claude_model = "claude-3-5-sonnet-20241022"
    claude_max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "4000"))
    claude_temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
    # Enabled Behaviors (from 20-behavior checklist)
    enabled_behaviors = {
        # Code Development
        "code_scaffolding": True,
        "feature_implementation": True,
        "code_review": True,
        "refactoring": True,
        "technical_design": True,
        # Quality Assurance
        "unit_testing": True,
        "integration_testing": True,
        "code_quality": True,
        "performance_optimization": True,
        "security_implementation": True,
        # DevOps & Deployment
        "ci_cd_pipeline": True,
        "environment_management": True,
        "deployment_automation": True,
        "monitoring_setup": True,
        "infrastructure_management": True,
        # Collaboration & Communication
        "technical_documentation": True,
        "knowledge_sharing": True,
        "mentoring": False,
        "cross_functional_collaboration": True,
        "estimation": True
    }
    # Capabilities (for API registration)
    capabilities = [
        "code_scaffolding",
        "feature_implementation",
        "code_review",
        "unit_testing",
        "technical_design",
        "deployment_automation"
    ]
    # Metadata for API registration
    metadata = {
        "version": version,
        "behaviors_enabled": len([b for b in enabled_behaviors.values() if b]),
        "claude_integration": True,
        "configurable_behaviors": True
    }

# Global config instance
config = DEVConfig() 