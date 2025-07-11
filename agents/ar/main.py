"""
AR Agent - Architecture Review Agent
Implements all 10 AR behaviors with Claude 3.7 Sonnet integration
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import requests
from pathlib import Path

from config import config
from claude_client import ARClaudeClient

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/{config.log_file}"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ARAgent:
    """AR Agent implementing all 10 behaviors with Claude 3.7 Sonnet integration"""
    
    def __init__(self):
        self.config = config
        self.claude_client = ARClaudeClient()
        self.agent_status = "initializing"
        self.last_activity = datetime.now()
        self.review_queue = []
        self.review_results = {}
        
        # Initialize behavior tracking
        self.behavior_status = {
            "code_review": {"last_run": None, "status": "idle"},
            "architecture_review": {"last_run": None, "status": "idle"},
            "security_review": {"last_run": None, "status": "idle"},
            "performance_review": {"last_run": None, "status": "idle"},
            "maintainability_review": {"last_run": None, "status": "idle"},
            "testability_review": {"last_run": None, "status": "idle"},
            "documentation_review": {"last_run": None, "status": "idle"},
            "best_practices_review": {"last_run": None, "status": "idle"},
            "dependency_review": {"last_run": None, "status": "idle"},
            "compliance_review": {"last_run": None, "status": "idle"}
        }
        
        logger.info(f"AR Agent initialized: {self.config.agent_name} v{self.config.agent_version}")
    
    async def start(self):
        """Start the AR Agent"""
        try:
            self.agent_status = "running"
            logger.info("AR Agent started successfully")
            
            # Register with API Hub
            await self._register_with_api_hub()
            
            # Start behavior monitoring
            await self._monitor_behaviors()
            
        except Exception as e:
            logger.error(f"Error starting AR Agent: {e}")
            self.agent_status = "error"
    
    async def _register_with_api_hub(self):
        """Register AR Agent with the API Hub"""
        try:
            registration_data = {
                "agent_name": self.config.agent_name,
                "agent_version": self.config.agent_version,
                "agent_description": self.config.agent_description,
                "capabilities": list(self.config.behaviors.keys()),
                "config": self.config.to_dict()
            }
            
            response = requests.post(
                f"{self.config.api_hub_url}/v1/agents/register",
                json=registration_data,
                timeout=self.config.api_hub_timeout
            )
            
            if response.status_code == 200:
                logger.info("Successfully registered with API Hub")
            else:
                logger.warning(f"Failed to register with API Hub: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error registering with API Hub: {e}")
    
    async def _monitor_behaviors(self):
        """Monitor and execute behaviors based on their frequency"""
        while self.agent_status == "running":
            try:
                current_time = datetime.now()
                
                # Check each behavior
                for behavior_name, behavior_config in self.config.behaviors.items():
                    if not behavior_config.get("enabled", False):
                        continue
                    
                    frequency = behavior_config.get("frequency", "daily")
                    last_run = self.behavior_status[behavior_name]["last_run"]
                    
                    if self._should_run_behavior(frequency, last_run, current_time):
                        await self._execute_behavior(behavior_name)
                
                # Update status
                self.last_activity = current_time
                
                # Sleep for a short interval
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in behavior monitoring: {e}")
                await asyncio.sleep(60)
    
    def _should_run_behavior(self, frequency: str, last_run: Optional[datetime], current_time: datetime) -> bool:
        """Determine if a behavior should run based on its frequency"""
        if last_run is None:
            return True
        
        if frequency == "real_time":
            return (current_time - last_run).seconds > 30
        elif frequency == "continuous":
            return True
        elif frequency == "hourly":
            return (current_time - last_run).hours >= 1
        elif frequency == "daily":
            return (current_time - last_run).days >= 1
        elif frequency == "weekly":
            return (current_time - last_run).days >= 7
        
        return False
    
    async def _execute_behavior(self, behavior_name: str):
        """Execute a specific behavior"""
        try:
            logger.info(f"Executing behavior: {behavior_name}")
            self.behavior_status[behavior_name]["status"] = "running"
            
            if behavior_name == "code_review":
                await self._code_review()
            elif behavior_name == "architecture_review":
                await self._architecture_review()
            elif behavior_name == "security_review":
                await self._security_review()
            elif behavior_name == "performance_review":
                await self._performance_review()
            elif behavior_name == "maintainability_review":
                await self._maintainability_review()
            elif behavior_name == "testability_review":
                await self._testability_review()
            elif behavior_name == "documentation_review":
                await self._documentation_review()
            elif behavior_name == "best_practices_review":
                await self._best_practices_review()
            elif behavior_name == "dependency_review":
                await self._dependency_review()
            elif behavior_name == "compliance_review":
                await self._compliance_review()
            
            self.behavior_status[behavior_name]["last_run"] = datetime.now()
            self.behavior_status[behavior_name]["status"] = "completed"
            
        except Exception as e:
            logger.error(f"Error executing behavior {behavior_name}: {e}")
            self.behavior_status[behavior_name]["status"] = "error"
    
    # Behavior implementations
    async def _code_review(self):
        """Perform code review"""
        try:
            # Get code to review from API Hub
            code_changes = await self._get_code_changes()
            
            for change in code_changes:
                review_result = self.claude_client.review_code(
                    change["code"],
                    change["language"],
                    change["context"]
                )
                
                # Store review result
                await self._store_review_result(change["id"], review_result)
                
                logger.info(f"Completed code review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in code review: {e}")
    
    async def _architecture_review(self):
        """Perform architecture review"""
        try:
            # Get architecture changes
            arch_changes = await self._get_architecture_changes()
            
            for change in arch_changes:
                review_result = self.claude_client.review_architecture(
                    change["description"],
                    change["components"]
                )
                
                # Store review result
                await self._store_architecture_review(change["id"], review_result)
                
                logger.info(f"Completed architecture review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in architecture review: {e}")
    
    async def _security_review(self):
        """Perform security review"""
        try:
            # Get code for security review
            security_changes = await self._get_security_changes()
            
            for change in security_changes:
                security_result = self.claude_client.assess_security(
                    change["code"],
                    change["language"],
                    change["context"]
                )
                
                # Store security result
                await self._store_security_review(change["id"], security_result)
                
                logger.info(f"Completed security review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in security review: {e}")
    
    async def _performance_review(self):
        """Perform performance review"""
        try:
            # Get code for performance review
            perf_changes = await self._get_performance_changes()
            
            for change in perf_changes:
                perf_result = self.claude_client.assess_performance(
                    change["code"],
                    change["language"],
                    change["context"]
                )
                
                # Store performance result
                await self._store_performance_review(change["id"], perf_result)
                
                logger.info(f"Completed performance review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in performance review: {e}")
    
    async def _maintainability_review(self):
        """Perform maintainability review"""
        try:
            # Get code for maintainability review
            maint_changes = await self._get_maintainability_changes()
            
            for change in maint_changes:
                maint_result = self.claude_client.review_code(
                    change["code"],
                    change["language"],
                    {**change["context"], "focus": "maintainability"}
                )
                
                # Store maintainability result
                await self._store_maintainability_review(change["id"], maint_result)
                
                logger.info(f"Completed maintainability review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in maintainability review: {e}")
    
    async def _testability_review(self):
        """Perform testability review"""
        try:
            # Get code for testability review
            test_changes = await self._get_testability_changes()
            
            for change in test_changes:
                test_result = self.claude_client.review_code(
                    change["code"],
                    change["language"],
                    {**change["context"], "focus": "testability"}
                )
                
                # Store testability result
                await self._store_testability_review(change["id"], test_result)
                
                logger.info(f"Completed testability review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in testability review: {e}")
    
    async def _documentation_review(self):
        """Perform documentation review"""
        try:
            # Get documentation changes
            doc_changes = await self._get_documentation_changes()
            
            for change in doc_changes:
                doc_result = self.claude_client.review_code(
                    change["content"],
                    "markdown",
                    {**change["context"], "focus": "documentation"}
                )
                
                # Store documentation result
                await self._store_documentation_review(change["id"], doc_result)
                
                logger.info(f"Completed documentation review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in documentation review: {e}")
    
    async def _best_practices_review(self):
        """Perform best practices review"""
        try:
            # Get code for best practices review
            bp_changes = await self._get_best_practices_changes()
            
            for change in bp_changes:
                bp_result = self.claude_client.review_code(
                    change["code"],
                    change["language"],
                    {**change["context"], "focus": "best_practices"}
                )
                
                # Store best practices result
                await self._store_best_practices_review(change["id"], bp_result)
                
                logger.info(f"Completed best practices review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in best practices review: {e}")
    
    async def _dependency_review(self):
        """Perform dependency review"""
        try:
            # Get dependencies to review
            dependencies = await self._get_dependencies()
            
            dep_result = self.claude_client.review_dependencies(dependencies)
            
            # Store dependency result
            await self._store_dependency_review(dep_result)
            
            logger.info("Completed dependency review")
            
        except Exception as e:
            logger.error(f"Error in dependency review: {e}")
    
    async def _compliance_review(self):
        """Perform compliance review"""
        try:
            # Get compliance requirements
            compliance_changes = await self._get_compliance_changes()
            
            for change in compliance_changes:
                comp_result = self.claude_client.review_code(
                    change["code"],
                    change["language"],
                    {**change["context"], "focus": "compliance"}
                )
                
                # Store compliance result
                await self._store_compliance_review(change["id"], comp_result)
                
                logger.info(f"Completed compliance review for {change['id']}")
                
        except Exception as e:
            logger.error(f"Error in compliance review: {e}")
    
    # Helper methods for API interactions
    async def _get_code_changes(self) -> List[Dict[str, Any]]:
        """Get code changes from API Hub"""
        return []
    
    async def _store_review_result(self, change_id: str, result: Dict[str, Any]):
        """Store review result in API Hub"""
        try:
            response = requests.post(
                f"{self.config.api_hub_url}/v1/reviews/code",
                json={"change_id": change_id, "result": result},
                timeout=self.config.api_hub_timeout
            )
            
            if response.status_code != 200:
                logger.warning(f"Failed to store review result: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error storing review result: {e}")
    
    # Placeholder methods for other API interactions
    async def _get_architecture_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_architecture_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    async def _get_security_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_security_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    async def _get_performance_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_performance_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    async def _get_maintainability_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_maintainability_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    async def _get_testability_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_testability_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    async def _get_documentation_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_documentation_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    async def _get_best_practices_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_best_practices_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    async def _get_dependencies(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_dependency_review(self, result: Dict[str, Any]):
        pass
    
    async def _get_compliance_changes(self) -> List[Dict[str, Any]]:
        return []
    
    async def _store_compliance_review(self, change_id: str, result: Dict[str, Any]):
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_name": self.config.agent_name,
            "agent_version": self.config.agent_version,
            "status": self.agent_status,
            "last_activity": self.last_activity.isoformat(),
            "behaviors": self.behavior_status,
            "review_queue_size": len(self.review_queue),
            "completed_reviews": len(self.review_results)
        }
    
    async def stop(self):
        """Stop the AR Agent"""
        self.agent_status = "stopped"
        logger.info("AR Agent stopped")

# Main execution
async def main():
    """Main function to run the AR Agent"""
    agent = ARAgent()
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main()) 