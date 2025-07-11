"""
Main PM Agent Application
"""

import time
import threading
import signal
import sys
import logging
from datetime import datetime
from typing import Dict, Any

from .config import config
from .api_client import APIClient
from .issue_triage import triage_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PMAgent:
    """Project Manager Agent for the Agentic Agile System"""
    
    def __init__(self):
        self.api_client = APIClient()
        self.running = False
        self.agent_id = None
        self.stats = {
            "issues_processed": 0,
            "heartbeats_sent": 0,
            "started_at": datetime.utcnow()
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def start(self):
        """Start the PM Agent"""
        logger.info(f"Starting {config.name} v{config.version}")
        
        try:
            # Check API health
            if not self.api_client.health_check():
                logger.error("API hub is not healthy. Cannot start agent.")
                return False
            
            # Register with API hub
            agent_data = self.api_client.register_agent()
            self.agent_id = agent_data["id"]
            logger.info(f"Successfully registered with API hub. Agent ID: {self.agent_id}")
            
            self.running = True
            
            # Start background threads
            self._start_heartbeat_thread()
            self._start_issue_monitoring_thread()
            
            logger.info("PM Agent is now running. Press Ctrl+C to stop.")
            
            # Main loop
            while self.running:
                time.sleep(1)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start PM Agent: {e}")
            return False
    
    def stop(self):
        """Stop the PM Agent"""
        logger.info("Stopping PM Agent...")
        self.running = False
        
        # Send final heartbeat
        if self.agent_id:
            self.api_client.send_heartbeat(status="inactive", current_task="shutting_down")
        
        logger.info("PM Agent stopped.")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}. Shutting down...")
        self.stop()
        sys.exit(0)
    
    def _start_heartbeat_thread(self):
        """Start the heartbeat thread"""
        def heartbeat_loop():
            while self.running:
                try:
                    current_task = "monitoring_issues" if self.stats["issues_processed"] > 0 else "idle"
                    success = self.api_client.send_heartbeat(
                        status="active", 
                        current_task=current_task
                    )
                    
                    if success:
                        self.stats["heartbeats_sent"] += 1
                    
                    time.sleep(config.heartbeat_interval)
                    
                except Exception as e:
                    logger.error(f"Heartbeat error: {e}")
                    time.sleep(10)  # Wait before retrying
        
        thread = threading.Thread(target=heartbeat_loop, daemon=True)
        thread.start()
        logger.info("Heartbeat thread started")
    
    def _start_issue_monitoring_thread(self):
        """Start the issue monitoring thread"""
        def monitoring_loop():
            while self.running:
                try:
                    self._process_new_issues()
                    time.sleep(config.issue_check_interval)
                    
                except Exception as e:
                    logger.error(f"Issue monitoring error: {e}")
                    time.sleep(30)  # Wait before retrying
        
        thread = threading.Thread(target=monitoring_loop, daemon=True)
        thread.start()
        logger.info("Issue monitoring thread started")
    
    def _process_new_issues(self):
        """Process new issues that need triage"""
        try:
            # Get open issues
            issues = self.api_client.get_issues(status="open", limit=config.max_issues_per_batch)
            
            if not issues:
                logger.debug("No new issues to process")
                return
            
            logger.info(f"Processing {len(issues)} issues")
            
            # Triage issues
            triaged_issues = triage_engine.triage_issues(issues)
            
            # Update issues with triage results
            for issue in triaged_issues:
                analysis = issue.get("triage_analysis", {})
                
                update_data = {
                    "priority": analysis.get("priority", "medium"),
                    "labels": analysis.get("labels", []),
                    "metadata": {
                        "triage_analysis": analysis,
                        "triaged_at": issue.get("triaged_at"),
                        "triaged_by": issue.get("triaged_by")
                    }
                }
                
                # Update the issue
                updated_issue = self.api_client.update_issue(issue["id"], update_data)
                
                if updated_issue:
                    self.stats["issues_processed"] += 1
                    logger.info(f"Updated issue {issue['id']}: {analysis.get('priority')} priority, {analysis.get('issue_type')} type")
                
                # TODO: Trigger appropriate agent based on assignment
                # assignee_type = analysis.get("assignee_type")
                # if assignee_type:
                #     self._trigger_agent_assignment(issue, assignee_type)
            
            logger.info(f"Processed {len(triaged_issues)} issues")
            
        except Exception as e:
            logger.error(f"Error processing issues: {e}")
    
    def _trigger_agent_assignment(self, issue: Dict[str, Any], agent_type: str):
        """Trigger an agent to handle the issue"""
        # TODO: Implement agent triggering logic
        # This would involve:
        # 1. Finding an available agent of the specified type
        # 2. Triggering the agent with the issue details
        # 3. Updating the issue with the assignment
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            **self.stats,
            "uptime_seconds": (datetime.utcnow() - self.stats["started_at"]).total_seconds(),
            "agent_id": self.agent_id,
            "status": "running" if self.running else "stopped"
        }


def main():
    """Main entry point"""
    agent = PMAgent()
    
    try:
        success = agent.start()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        agent.stop()


if __name__ == "__main__":
    main() 