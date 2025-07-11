"""
Main Developer Agent Application
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

class DEVAgent(AgentBase):
    """Developer Agent for the Agentic Agile System"""
    def __init__(self, api_client):
        super().__init__(api_client, config)
        self.claude_client = ClaudeClient()
        self.stats.update({
            "code_scaffolded": 0,
            "features_implemented": 0,
            "code_reviews_completed": 0,
            "tests_written": 0
        })
    def get_current_task(self):
        if self.stats["code_scaffolded"] > 0:
            return "scaffolding_code"
        elif self.stats["features_implemented"] > 0:
            return "implementing_features"
        elif self.stats["code_reviews_completed"] > 0:
            return "reviewing_code"
        else:
            return "monitoring_tasks"
    def run(self):
        while self.running:
            try:
                # Check for new development tasks
                if config.enabled_behaviors["code_scaffolding"]:
                    self._scaffold_code()
                if config.enabled_behaviors["feature_implementation"]:
                    self._implement_features()
                if config.enabled_behaviors["code_review"]:
                    self._review_code()
                if config.enabled_behaviors["unit_testing"]:
                    self._write_tests()
                time.sleep(config.code_check_interval)
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(30)
    def _scaffold_code(self):
        try:
            # Simulate code scaffolding
            feature_desc = "User authentication endpoint"
            code = self.claude_client.scaffold_code(feature_desc)
            logger.info(f"Scaffolded code for: {feature_desc}")
            self.stats["code_scaffolded"] += 1
        except Exception as e:
            logger.error(f"Error scaffolding code: {e}")
    def _implement_features(self):
        try:
            # Simulate feature implementation
            logger.info("Implemented feature (simulated)")
            self.stats["features_implemented"] += 1
        except Exception as e:
            logger.error(f"Error implementing features: {e}")
    def _review_code(self):
        try:
            # Simulate code review
            sample_code = "def hello_world():\n    print('Hello, World!')"
            review = self.claude_client.review_code(sample_code)
            logger.info(f"Code review completed: {review[:100]}...")
            self.stats["code_reviews_completed"] += 1
        except Exception as e:
            logger.error(f"Error reviewing code: {e}")
    def _write_tests(self):
        try:
            # Simulate test writing
            logger.info("Wrote unit tests (simulated)")
            self.stats["tests_written"] += 1
        except Exception as e:
            logger.error(f"Error writing tests: {e}")
    def get_stats(self) -> Dict[str, Any]:
        base_stats = super().get_stats()
        return {
            **base_stats,
            "behaviors_enabled": len([b for b in config.enabled_behaviors.values() if b]),
            "claude_integration": bool(config.claude_api_key),
            "code_scaffolded": self.stats["code_scaffolded"],
            "features_implemented": self.stats["features_implemented"],
            "code_reviews_completed": self.stats["code_reviews_completed"],
            "tests_written": self.stats["tests_written"]
        }
def main():
    pm_agent_path = os.path.join(os.path.dirname(__file__), '..', 'pm_agent')
    sys.path.append(pm_agent_path)
    from api_client import APIClient
    api_client = APIClient()
    agent = DEVAgent(api_client)
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