"""
Configuration for Product Owner Agent
"""

import os
from typing import List, Dict, Any

class POConfig:
    """Configuration for Product Owner Agent"""
    
    # Agent Identity
    name = "Product Owner Agent"
    version = "1.0.0"
    agent_type = "po"
    
    # API Configuration
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    api_timeout = int(os.getenv("API_TIMEOUT", "30"))
    
    # Agent Behavior Configuration
    heartbeat_interval = int(os.getenv("HEARTBEAT_INTERVAL", "60"))
    story_check_interval = int(os.getenv("STORY_CHECK_INTERVAL", "300"))
    
    # Claude 3.7 Sonnet Integration
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    claude_model = "claude-3-5-sonnet-20241022"
    claude_max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "4000"))
    claude_temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
    
    # Enabled Behaviors (from 20-behavior checklist)
    enabled_behaviors = {
        # Core Story Management
        "story_creation": True,
        "acceptance_criteria": True,
        "story_pointing": True,
        "priority_ranking": True,
        "dependency_mapping": True,
        
        # Planning & Strategy
        "sprint_planning": True,
        "backlog_grooming": True,
        "release_planning": False,
        "roadmap_creation": False,
        "capacity_planning": False,
        
        # Business Intelligence
        "business_value_scoring": True,
        "roi_calculation": False,
        "market_analysis": False,
        "competitive_analysis": False,
        "customer_feedback_integration": False,
        
        # Quality & Compliance
        "definition_of_ready": True,
        "definition_of_done": True,
        "risk_assessment": True,
        "technical_debt_tracking": False,
        "compliance_checking": False
    }
    
    # Behavior Parameters
    behavior_params = {
        "story_creation": {
            "max_stories_per_batch": 10,
            "story_template": "user_story_template.md",
            "claude_prompt_template": "po_story_creation_prompt.txt"
        },
        "acceptance_criteria": {
            "criteria_template": "acceptance_criteria_template.md",
            "max_criteria_per_story": 8
        },
        "story_pointing": {
            "fibonacci_sequence": [1, 2, 3, 5, 8, 13, 21],
            "complexity_factors": ["effort", "uncertainty", "dependencies"]
        },
        "priority_ranking": {
            "ranking_factors": ["business_value", "urgency", "dependencies", "effort"],
            "scoring_scale": 1-10
        }
    }
    
    # Capabilities (for API registration)
    capabilities = [
        "story_creation",
        "acceptance_criteria_writing", 
        "story_pointing",
        "priority_ranking",
        "backlog_management",
        "sprint_planning",
        "business_value_analysis"
    ]
    
    # Metadata for API registration
    metadata = {
        "version": version,
        "behaviors_enabled": len([b for b in enabled_behaviors.values() if b]),
        "claude_integration": True,
        "configurable_behaviors": True
    }

# Global config instance
config = POConfig() 