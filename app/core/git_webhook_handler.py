"""
Git webhook handler for processing GitHub and GitLab events
"""

import uuid
import structlog
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import httpx

from app.models.git_events import GitEvent, GitEventType, GitProvider
from app.config import settings

logger = structlog.get_logger()


class GitWebhookHandler:
    """Handles Git webhook events and triggers appropriate agents"""
    
    def __init__(self, db: Session):
        self.db = db
        self.api_base_url = settings.api_base_url or "http://localhost:8000"
    
    async def process_github_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process GitHub webhook events"""
        try:
            # Extract repository information
            repository = payload.get('repository', {}).get('full_name', 'unknown')
            action = payload.get('action')
            
            # Create Git event record
            git_event = GitEvent(
                id=str(uuid.uuid4()),
                provider=GitProvider.GITHUB,
                event_type=event_type,
                repository=repository,
                event_id=payload.get('id'),
                action=action,
                payload=payload
            )
            
            self.db.add(git_event)
            self.db.commit()
            
            # Process based on event type
            result = await self._process_event(git_event)
            
            # Update event as processed
            git_event.processed = True
            git_event.processed_at = datetime.utcnow()
            git_event.agent_triggered = result.get('agent_triggered')
            self.db.commit()
            
            return result
            
        except Exception as e:
            logger.error("Failed to process GitHub webhook", error=str(e))
            if git_event:
                git_event.error_message = str(e)
                self.db.commit()
            raise
    
    async def process_gitlab_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process GitLab webhook events"""
        try:
            # Extract repository information
            repository = payload.get('project', {}).get('path_with_namespace', 'unknown')
            action = payload.get('object_attributes', {}).get('action')
            
            # Create Git event record
            git_event = GitEvent(
                id=str(uuid.uuid4()),
                provider=GitProvider.GITLAB,
                event_type=event_type,
                repository=repository,
                event_id=payload.get('object_attributes', {}).get('id'),
                action=action,
                payload=payload
            )
            
            self.db.add(git_event)
            self.db.commit()
            
            # Process based on event type
            result = await self._process_event(git_event)
            
            # Update event as processed
            git_event.processed = True
            git_event.processed_at = datetime.utcnow()
            git_event.agent_triggered = result.get('agent_triggered')
            self.db.commit()
            
            return result
            
        except Exception as e:
            logger.error("Failed to process GitLab webhook", error=str(e))
            if git_event:
                git_event.error_message = str(e)
                self.db.commit()
            raise
    
    async def _process_event(self, git_event: GitEvent) -> Dict[str, Any]:
        """Process Git event and trigger appropriate agents"""
        event_type = git_event.event_type
        action = git_event.action
        payload = git_event.payload
        
        logger.info(
            "Processing Git event",
            event_type=event_type,
            action=action,
            repository=git_event.repository
        )
        
        # Route events to appropriate agents
        if event_type == "issues":
            return await self._handle_issue_event(git_event)
        elif event_type == "pull_request":
            return await self._handle_pull_request_event(git_event)
        elif event_type == "push":
            return await self._handle_push_event(git_event)
        elif event_type == "release":
            return await self._handle_release_event(git_event)
        else:
            logger.info(f"Unhandled event type: {event_type}")
            return {"status": "unhandled", "event_type": event_type}
    
    async def _handle_issue_event(self, git_event: GitEvent) -> Dict[str, Any]:
        """Handle issue events (created, updated, closed, etc.)"""
        action = git_event.action
        payload = git_event.payload
        
        if action == "opened":
            # New issue - trigger PM agent for triage
            await self._trigger_agent("pm", "triage_issue", {
                "issue_id": payload.get('issue', {}).get('id'),
                "title": payload.get('issue', {}).get('title'),
                "body": payload.get('issue', {}).get('body'),
                "repository": git_event.repository,
                "user": payload.get('issue', {}).get('user', {}).get('login')
            })
            return {"agent_triggered": "pm", "action": "triage_issue"}
        
        elif action == "labeled":
            # Issue labeled - trigger appropriate agent based on label
            labels = [label['name'] for label in payload.get('issue', {}).get('labels', [])]
            if 'bug' in labels:
                await self._trigger_agent("qa", "analyze_bug", {
                    "issue_id": payload.get('issue', {}).get('id'),
                    "labels": labels
                })
                return {"agent_triggered": "qa", "action": "analyze_bug"}
            elif 'feature' in labels:
                await self._trigger_agent("po", "create_story", {
                    "issue_id": payload.get('issue', {}).get('id'),
                    "labels": labels
                })
                return {"agent_triggered": "po", "action": "create_story"}
        
        return {"status": "processed", "event_type": "issue", "action": action}
    
    async def _handle_pull_request_event(self, git_event: GitEvent) -> Dict[str, Any]:
        """Handle pull request events"""
        action = git_event.action
        payload = git_event.payload
        
        if action == "opened":
            # New PR - trigger AR agent for review
            await self._trigger_agent("ar", "review_code", {
                "pr_id": payload.get('pull_request', {}).get('id'),
                "title": payload.get('pull_request', {}).get('title'),
                "repository": git_event.repository
            })
            return {"agent_triggered": "ar", "action": "review_code"}
        
        elif action == "synchronize":
            # PR updated - trigger QA agent for testing
            await self._trigger_agent("qa", "run_tests", {
                "pr_id": payload.get('pull_request', {}).get('id'),
                "repository": git_event.repository
            })
            return {"agent_triggered": "qa", "action": "run_tests"}
        
        return {"status": "processed", "event_type": "pull_request", "action": action}
    
    async def _handle_push_event(self, git_event: GitEvent) -> Dict[str, Any]:
        """Handle push events"""
        payload = git_event.payload
        
        # Trigger DEV agent for code analysis
        await self._trigger_agent("dev", "analyze_code", {
            "repository": git_event.repository,
            "branch": payload.get('ref', '').replace('refs/heads/', ''),
            "commits": len(payload.get('commits', []))
        })
        
        return {"agent_triggered": "dev", "action": "analyze_code"}
    
    async def _handle_release_event(self, git_event: GitEvent) -> Dict[str, Any]:
        """Handle release events"""
        payload = git_event.payload
        
        # Trigger AD agent for deployment
        await self._trigger_agent("ad", "deploy_release", {
            "release_id": payload.get('release', {}).get('id'),
            "tag_name": payload.get('release', {}).get('tag_name'),
            "repository": git_event.repository
        })
        
        return {"agent_triggered": "ad", "action": "deploy_release"}
    
    async def _trigger_agent(self, agent_type: str, action: str, data: Dict[str, Any]) -> None:
        """Trigger an agent with specific action and data"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/v1/agents/{agent_type}/trigger",
                    json={
                        "action": action,
                        "data": data,
                        "source": "git_webhook",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    logger.info(
                        f"Successfully triggered {agent_type} agent",
                        action=action,
                        agent_type=agent_type
                    )
                else:
                    logger.error(
                        f"Failed to trigger {agent_type} agent",
                        status_code=response.status_code,
                        response=response.text
                    )
                    
        except Exception as e:
            logger.error(
                f"Error triggering {agent_type} agent",
                error=str(e),
                action=action
            ) 