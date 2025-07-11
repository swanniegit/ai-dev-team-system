"""
Main Scrum Master Agent Application
"""

import time
import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from base.agent_base import AgentBase
from .config import config
from .claude_client import ClaudeClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SMAgent(AgentBase):
    """Scrum Master Agent for the Agentic Agile System"""
    def __init__(self, api_client):
        super().__init__(api_client, config)
        self.claude_client = ClaudeClient()
        self.stats.update({
            "ceremonies_facilitated": 0,
            "impediments_removed": 0,
            "velocity_tracked": 0,
            "retrospectives_led": 0
        })
    def get_current_task(self):
        if self.stats["ceremonies_facilitated"] > 0:
            return "facilitating_ceremonies"
        elif self.stats["impediments_removed"] > 0:
            return "removing_impediments"
        else:
            return "monitoring_team"
    def run(self):
        while self.running:
            try:
                # Facilitate ceremonies
                if config.enabled_behaviors["sprint_planning_facilitation"]:
                    self._facilitate_ceremony("Sprint Planning")
                if config.enabled_behaviors["daily_standup_coordination"]:
                    self._facilitate_ceremony("Daily Standup")
                if config.enabled_behaviors["sprint_review_organization"]:
                    self._facilitate_ceremony("Sprint Review")
                if config.enabled_behaviors["retrospective_facilitation"]:
                    self._facilitate_ceremony("Retrospective")
                # Remove impediments
                if config.enabled_behaviors["impediment_removal"]:
                    self._remove_impediments()
                # Track velocity
                if config.enabled_behaviors["velocity_tracking"]:
                    self._track_velocity()
                time.sleep(config.ceremony_check_interval)
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(30)
    def _facilitate_ceremony(self, ceremony_type: str):
        try:
            context = {"team": "Agile Team", "date": datetime.utcnow().isoformat()}
            agenda = self.claude_client.facilitate_ceremony(ceremony_type, context)
            logger.info(f"Facilitated {ceremony_type}: {agenda}")
            self.stats["ceremonies_facilitated"] += 1
        except Exception as e:
            logger.error(f"Error facilitating {ceremony_type}: {e}")
    def _remove_impediments(self):
        try:
            # Simulate impediment removal
            logger.info("Checked for and removed team impediments (simulated)")
            self.stats["impediments_removed"] += 1
        except Exception as e:
            logger.error(f"Error removing impediments: {e}")
    def _track_velocity(self):
        try:
            # Simulate velocity tracking
            logger.info("Tracked team velocity (simulated)")
            self.stats["velocity_tracked"] += 1
        except Exception as e:
            logger.error(f"Error tracking velocity: {e}")
    def get_stats(self) -> Dict[str, Any]:
        base_stats = super().get_stats()
        return {
            **base_stats,
            "behaviors_enabled": len([b for b in config.enabled_behaviors.values() if b]),
            "claude_integration": bool(config.claude_api_key),
            "ceremonies_facilitated": self.stats["ceremonies_facilitated"],
            "impediments_removed": self.stats["impediments_removed"],
            "velocity_tracked": self.stats["velocity_tracked"],
            "retrospectives_led": self.stats["retrospectives_led"]
        }
def main():
    pm_agent_path = os.path.join(os.path.dirname(__file__), '..', 'pm_agent')
    sys.path.append(pm_agent_path)
    from api_client import APIClient
    api_client = APIClient()
    agent = SMAgent(api_client)
    try:
        success = agent.start()
        if not success:
            import sys
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import sys
        sys.exit(1)
    finally:
        agent.stop()
if __name__ == "__main__":
    main() 