"""
Git events models for the Agentic Agile System
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GitEventType(str, Enum):
    """Git event types"""
    ISSUES = "issues"
    PULL_REQUEST = "pull_request"
    PUSH = "push"
    COMMIT = "commit"
    COMMENT = "comment"
    MILESTONE = "milestone"
    LABEL = "label"
    RELEASE = "release"
    DEPLOYMENT = "deployment"
    STATUS = "status"


class GitProvider(str, Enum):
    """Git provider types"""
    GITHUB = "github"
    GITLAB = "gitlab"


class GitEvent(Base):
    """SQLAlchemy model for Git events"""
    __tablename__ = "git_events"
    
    id = Column(String(36), primary_key=True, index=True)
    provider = Column(String(20), nullable=False, index=True)  # github, gitlab
    event_type = Column(String(50), nullable=False, index=True)
    repository = Column(String(200), nullable=False, index=True)
    event_id = Column(String(100), nullable=True, index=True)  # External event ID
    action = Column(String(50), nullable=True, index=True)
    payload = Column(JSON, nullable=False)
    processed = Column(Boolean, default=False, index=True)
    processed_at = Column(DateTime, nullable=True)
    agent_triggered = Column(String(50), nullable=True)  # Which agent was triggered
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Composite indexes for performance optimization
    __table_args__ = (
        Index('idx_git_processing', 'processed', 'created_at', 'repository'),
        Index('idx_git_events_by_repo', 'repository', 'event_type', 'created_at'),
        Index('idx_git_provider_events', 'provider', 'event_type', 'processed'),
        Index('idx_git_event_external', 'event_id', 'provider'),
        Index('idx_git_agent_triggered', 'agent_triggered', 'processed_at'),
    )


class GitEventBase(BaseModel):
    """Base Pydantic model for Git events"""
    provider: GitProvider
    event_type: GitEventType
    repository: str
    event_id: Optional[str] = None
    action: Optional[str] = None
    payload: Dict[str, Any]


class GitEventCreate(GitEventBase):
    """Pydantic model for creating Git events"""
    pass


class GitEventResponse(GitEventBase):
    """Pydantic model for Git event responses"""
    id: str
    processed: bool
    processed_at: Optional[datetime]
    agent_triggered: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class GitEventUpdate(BaseModel):
    """Pydantic model for updating Git events"""
    processed: Optional[bool] = None
    processed_at: Optional[datetime] = None
    agent_triggered: Optional[str] = None
    error_message: Optional[str] = None 