"""
Git integration endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import hmac
import hashlib
import json
import structlog

from app.core.database import get_db
from app.core.git_webhook_handler import GitWebhookHandler
from app.models.git_events import GitEvent, GitEventCreate, GitEventResponse

logger = structlog.get_logger()
router = APIRouter()


@router.post("/webhook/github", status_code=status.HTTP_200_OK)
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Handle GitHub webhooks"""
    try:
        # Get the raw body for signature verification
        body = await request.body()
        
        # Verify webhook signature if provided
        if x_hub_signature_256:
            if not verify_github_signature(body, x_hub_signature_256):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid webhook signature"
                )
        
        # Parse the webhook payload
        payload = json.loads(body.decode('utf-8'))
        
        # Create webhook handler
        handler = GitWebhookHandler(db)
        
        # Process the webhook based on event type
        result = await handler.process_github_webhook(x_github_event, payload)
        
        logger.info(
            "GitHub webhook processed",
            event_type=x_github_event,
            repository=payload.get('repository', {}).get('full_name'),
            action=payload.get('action')
        )
        
        return {"status": "processed", "event_type": x_github_event}
        
    except Exception as e:
        logger.error("Failed to process GitHub webhook", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )


@router.post("/webhook/gitlab", status_code=status.HTTP_200_OK)
async def gitlab_webhook(
    request: Request,
    x_gitlab_event: str = Header(None),
    x_gitlab_token: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Handle GitLab webhooks"""
    try:
        # Get the raw body
        body = await request.body()
        payload = json.loads(body.decode('utf-8'))
        
        # Verify webhook token if provided
        if x_gitlab_token:
            if not verify_gitlab_token(x_gitlab_token):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid webhook token"
                )
        
        # Create webhook handler
        handler = GitWebhookHandler(db)
        
        # Process the webhook
        result = await handler.process_gitlab_webhook(x_gitlab_event, payload)
        
        logger.info(
            "GitLab webhook processed",
            event_type=x_gitlab_event,
            project=payload.get('project', {}).get('name'),
            action=payload.get('object_attributes', {}).get('action')
        )
        
        return {"status": "processed", "event_type": x_gitlab_event}
        
    except Exception as e:
        logger.error("Failed to process GitLab webhook", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )


@router.get("/events", response_model=list[GitEventResponse])
async def list_git_events(
    repository: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List Git events with filtering"""
    from app.models.git_events import GitEvent
    
    query = db.query(GitEvent)
    
    if repository:
        query = query.filter(GitEvent.repository == repository)
    
    if event_type:
        query = query.filter(GitEvent.event_type == event_type)
    
    events = query.order_by(GitEvent.timestamp.desc()).offset(offset).limit(limit).all()
    return events


@router.get("/events/{event_id}", response_model=GitEventResponse)
async def get_git_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific Git event by ID"""
    from app.models.git_events import GitEvent
    
    event = db.query(GitEvent).filter(GitEvent.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Git event not found"
        )
    return event


def verify_github_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature"""
    # Get the secret from environment
    import os
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if not secret:
        logger.warning("GitHub webhook secret not configured")
        return True  # Allow if no secret configured
    
    # Verify signature
    expected_signature = f"sha256={hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()}"
    return hmac.compare_digest(signature, expected_signature)


def verify_gitlab_token(token: str) -> bool:
    """Verify GitLab webhook token"""
    import os
    expected_token = os.getenv("GITLAB_WEBHOOK_TOKEN")
    if not expected_token:
        logger.warning("GitLab webhook token not configured")
        return True  # Allow if no token configured
    
    return token == expected_token 