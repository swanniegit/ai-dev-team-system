"""
Configuration for Scrum Master Agent
"""

import os
from typing import List, Dict, Any

class SMConfig:
    """Configuration for Scrum Master Agent"""
    # Agent Identity
    name = "Scrum Master Agent"
    version = "1.0.0"
    agent_type = "sm"
    # API Configuration
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    api_timeout = int(os.getenv("API_TIMEOUT", "30"))
    # Agent Behavior Configuration
    heartbeat_interval = int(os.getenv("HEARTBEAT_INTERVAL", "60"))
    ceremony_check_interval = int(os.getenv("CEREMONY_CHECK_INTERVAL", "300"))
    # Claude 3.7 Sonnet Integration
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    claude_model = "claude-3-5-sonnet-20241022"
    claude_max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "4000"))
    claude_temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
    # Enabled Behaviors (from 20-behavior checklist)
    enabled_behaviors = {
        # Ceremony Management
        "sprint_planning_facilitation": True,
        "daily_standup_coordination": True,
        "sprint_review_organization": True,
        "retrospective_facilitation": True,
        "backlog_refinement": True,
        # Team Coaching
        "agile_coaching": True,
        "team_building": True,
        "conflict_resolution": True,
        "skill_development": False,
        "mentoring": False,
        # Process Optimization
        "velocity_tracking": True,
        "burndown_monitoring": True,
        "impediment_removal": True,
        "process_improvement": True,
        "metrics_analysis": True,
        # Communication & Coordination
        "stakeholder_communication": True,
        "cross_team_coordination": False,
        "escalation_management": False,
        "documentation": True,
        "training_coordination": False
    }
    # Capabilities (for API registration)
    capabilities = [
        "sprint_planning_facilitation",
        "daily_standup_coordination",
        "retrospective_facilitation",
        "impediment_removal",
        "velocity_tracking",
        "metrics_analysis",
        "agile_coaching"
    ]
    # Metadata for API registration
    metadata = {
        "version": version,
        "behaviors_enabled": len([b for b in enabled_behaviors.values() if b]),
        "claude_integration": True,
        "configurable_behaviors": True
    }

# Global config instance
config = SMConfig() 