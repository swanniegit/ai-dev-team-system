"""
API Client for PM Agent to communicate with the API Hub
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from .config import config

logger = logging.getLogger(__name__)


class APIClient:
    """Client for communicating with the Agentic Agile System API Hub"""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or config.api_base_url
        self.timeout = timeout or config.api_timeout
        self.session = requests.Session()
        self.agent_id = None
        
    def register_agent(self) -> Dict[str, Any]:
        """Register this agent with the API hub"""
        try:
            registration_data = {
                "name": config.name,
                "agent_type": config.agent_type,
                "capabilities": config.capabilities,
                "metadata": {
                    "version": config.version,
                    "started_at": datetime.utcnow().isoformat(),
                    "config": {
                        "heartbeat_interval": config.heartbeat_interval,
                        "issue_check_interval": config.issue_check_interval
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/v1/agents/register",
                json=registration_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            agent_data = response.json()
            self.agent_id = agent_data["id"]
            logger.info(f"Successfully registered agent with ID: {self.agent_id}")
            
            return agent_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to register agent: {e}")
            raise
    
    def send_heartbeat(self, status: str = "active", current_task: str = None) -> bool:
        """Send heartbeat to the API hub"""
        if not self.agent_id:
            logger.error("Agent not registered, cannot send heartbeat")
            return False
            
        try:
            heartbeat_data = {
                "status": status,
                "current_task": current_task,
                "metrics": {
                    "issues_processed": 0,  # TODO: Track actual metrics
                    "last_activity": datetime.utcnow().isoformat()
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/v1/agents/{self.agent_id}/heartbeat",
                json=heartbeat_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.debug("Heartbeat sent successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send heartbeat: {e}")
            return False
    
    def get_issues(self, status: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
        """Get issues from the API hub"""
        try:
            params = {
                "status": status,
                "limit": limit
            }
            
            response = self.session.get(
                f"{self.base_url}/v1/issues/",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get issues: {e}")
            return []
    
    def create_issue(self, issue_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new issue"""
        try:
            response = self.session.post(
                f"{self.base_url}/v1/issues/",
                json=issue_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create issue: {e}")
            return None
    
    def update_issue(self, issue_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing issue"""
        try:
            response = self.session.put(
                f"{self.base_url}/v1/issues/{issue_id}",
                json=update_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update issue: {e}")
            return None
    
    def trigger_agent(self, agent_id: str, action: str, parameters: Dict[str, Any] = None) -> bool:
        """Trigger an action on another agent"""
        try:
            trigger_data = {
                "action": action,
                "parameters": parameters or {},
                "priority": 5
            }
            
            response = self.session.post(
                f"{self.base_url}/v1/agents/{agent_id}/trigger",
                json=trigger_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.info(f"Successfully triggered {action} on agent {agent_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to trigger agent {agent_id}: {e}")
            return False
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of another agent"""
        try:
            response = self.session.get(
                f"{self.base_url}/v1/agents/{agent_id}/status",
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get agent status: {e}")
            return None
    
    def health_check(self) -> bool:
        """Check if the API hub is healthy"""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            response.raise_for_status()
            
            health_data = response.json()
            return health_data.get("status") == "healthy"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return False 