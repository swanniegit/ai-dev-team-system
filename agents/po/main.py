"""
Main Product Owner Agent Application
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

class POAgent(AgentBase):
    """Product Owner Agent for the Agentic Agile System"""
    
    def __init__(self, api_client):
        super().__init__(api_client, config)
        self.claude_client = ClaudeClient()
        self.stats.update({
            "stories_created": 0,
            "acceptance_criteria_written": 0,
            "story_points_estimated": 0,
            "stories_prioritized": 0,
            "backlog_items_processed": 0
        })
        
    def get_current_task(self):
        """Override to report current task based on enabled behaviors"""
        if self.stats["stories_created"] > 0:
            return "creating_user_stories"
        elif self.stats["backlog_items_processed"] > 0:
            return "managing_backlog"
        else:
            return "monitoring_feature_requests"
    
    def run(self):
        """Main agent loop - override from base class"""
        while self.running:
            try:
                # Check for new feature requests
                if config.enabled_behaviors["story_creation"]:
                    self._process_feature_requests()
                
                # Manage backlog
                if config.enabled_behaviors["backlog_grooming"]:
                    self._groom_backlog()
                
                # Sprint planning
                if config.enabled_behaviors["sprint_planning"]:
                    self._plan_sprint()
                
                time.sleep(config.story_check_interval)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(30)
    
    def _process_feature_requests(self):
        """Process new feature requests and create user stories"""
        try:
            # Get new feature requests (simulated for now)
            feature_requests = self._get_feature_requests()
            
            if not feature_requests:
                logger.debug("No new feature requests to process")
                return
            
            logger.info(f"Processing {len(feature_requests)} feature requests")
            
            for request in feature_requests:
                # Create user story using Claude
                story = self.claude_client.create_story(
                    request["description"],
                    context=request.get("context", {})
                )
                
                if story:
                    # Create issue in API
                    issue_data = {
                        "title": story["title"],
                        "description": story["description"],
                        "priority": story["priority"],
                        "labels": story["labels"],
                        "metadata": {
                            "story_points": story["story_points"],
                            "business_value": story["business_value"],
                            "risk_level": story["risk_level"],
                            "acceptance_criteria": story["acceptance_criteria"],
                            "created_by": "po_agent",
                            "created_at": datetime.utcnow().isoformat()
                        }
                    }
                    
                    created_issue = self.api_client.create_issue(issue_data)
                    if created_issue:
                        self.stats["stories_created"] += 1
                        logger.info(f"Created story: {story['title']} ({story['story_points']} points)")
                
        except Exception as e:
            logger.error(f"Error processing feature requests: {e}")
    
    def _groom_backlog(self):
        """Groom and prioritize the backlog"""
        try:
            # Get backlog items
            backlog_items = self.api_client.get_issues(status="open", limit=20)
            
            if not backlog_items:
                return
            
            # Prioritize using Claude
            if config.enabled_behaviors["priority_ranking"]:
                prioritized_items = self.claude_client.rank_priority(backlog_items)
                
                # Update priorities in API
                for item in prioritized_items:
                    update_data = {
                        "priority": item.get("priority", "Medium"),
                        "metadata": {
                            **item.get("metadata", {}),
                            "priority_score": item.get("priority_score", 5),
                            "prioritized_by": "po_agent",
                            "prioritized_at": datetime.utcnow().isoformat()
                        }
                    }
                    
                    self.api_client.update_issue(item["id"], update_data)
                    self.stats["stories_prioritized"] += 1
            
            self.stats["backlog_items_processed"] += len(backlog_items)
            logger.info(f"Groomed {len(backlog_items)} backlog items")
            
        except Exception as e:
            logger.error(f"Error grooming backlog: {e}")
    
    def _plan_sprint(self):
        """Plan next sprint"""
        try:
            # Get high-priority stories
            high_priority_stories = self.api_client.get_issues(
                status="open", 
                limit=10
            )
            
            if not high_priority_stories:
                return
            
            # Estimate capacity (simplified)
            team_capacity = 40  # story points per sprint
            
            # Select stories for sprint
            selected_stories = []
            total_points = 0
            
            for story in high_priority_stories:
                story_points = story.get("metadata", {}).get("story_points", 5)
                if total_points + story_points <= team_capacity:
                    selected_stories.append(story)
                    total_points += story_points
                else:
                    break
            
            if selected_stories:
                logger.info(f"Sprint planned with {len(selected_stories)} stories ({total_points} points)")
                
                # Update stories with sprint assignment
                for story in selected_stories:
                    update_data = {
                        "metadata": {
                            **story.get("metadata", {}),
                            "sprint_assigned": True,
                            "planned_by": "po_agent",
                            "planned_at": datetime.utcnow().isoformat()
                        }
                    }
                    self.api_client.update_issue(story["id"], update_data)
            
        except Exception as e:
            logger.error(f"Error planning sprint: {e}")
    
    def _get_feature_requests(self) -> List[Dict[str, Any]]:
        """Get feature requests (simulated for now)"""
        # In a real implementation, this would poll external systems
        # like Jira, GitHub Issues, or customer feedback systems
        
        # Simulated feature requests
        return [
            {
                "id": f"fr_{int(time.time())}",
                "description": "Add user authentication with OAuth2",
                "context": {
                    "source": "customer_feedback",
                    "priority": "high",
                    "requested_by": "customer@example.com"
                }
            },
            {
                "id": f"fr_{int(time.time()) + 1}",
                "description": "Implement real-time notifications",
                "context": {
                    "source": "product_roadmap",
                    "priority": "medium",
                    "requested_by": "product_manager"
                }
            }
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics with PO-specific metrics"""
        base_stats = super().get_stats()
        return {
            **base_stats,
            "behaviors_enabled": len([b for b in config.enabled_behaviors.values() if b]),
            "claude_integration": bool(config.claude_api_key),
            "stories_created": self.stats["stories_created"],
            "acceptance_criteria_written": self.stats["acceptance_criteria_written"],
            "story_points_estimated": self.stats["story_points_estimated"],
            "stories_prioritized": self.stats["stories_prioritized"],
            "backlog_items_processed": self.stats["backlog_items_processed"]
        }


def main():
    """Main entry point"""
    # Import here to avoid circular imports
    pm_agent_path = os.path.join(os.path.dirname(__file__), '..', 'pm_agent')
    sys.path.append(pm_agent_path)
    from api_client import APIClient
    
    api_client = APIClient()
    agent = POAgent(api_client)
    
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