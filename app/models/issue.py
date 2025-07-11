"""
Issue models for the Agentic Agile System
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IssueType(str, Enum):
    """Issue type enumeration"""
    BUG = "bug"
    FEATURE = "feature"
    STORY = "story"
    TASK = "task"
    EPIC = "epic"
    SPIKE = "spike"


class IssueStatus(str, Enum):
    """Issue status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    TESTING = "testing"
    DONE = "done"
    CLOSED = "closed"
    BLOCKED = "blocked"


class IssuePriority(str, Enum):
    """Issue priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Issue(Base):
    """SQLAlchemy model for issues"""
    __tablename__ = "issues"
    
    id = Column(String(36), primary_key=True, index=True)
    external_id = Column(String(100), unique=True, index=True)  # Git issue ID
    title = Column(String(200), nullable=False)
    description = Column(Text)
    issue_type = Column(String(20), default=IssueType.TASK)
    status = Column(String(20), default=IssueStatus.OPEN)
    priority = Column(String(20), default=IssuePriority.MEDIUM)
    assignee_id = Column(String(36), ForeignKey("agents.id"), nullable=True)
    created_by = Column(String(36), nullable=False)
    labels = Column(JSON, default=list)
    issue_metadata = Column(JSON, default=dict)  # Renamed from metadata to avoid conflict
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)


class IssueBase(BaseModel):
    """Base Pydantic model for issues"""
    title: str = Field(..., min_length=1, max_length=200, description="Issue title")
    description: Optional[str] = Field(None, description="Issue description")
    issue_type: IssueType = Field(default=IssueType.TASK, description="Type of issue")
    priority: IssuePriority = Field(default=IssuePriority.MEDIUM, description="Issue priority")
    labels: List[str] = Field(default_factory=list, description="Issue labels")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class IssueCreate(IssueBase):
    """Pydantic model for creating issues"""
    external_id: Optional[str] = Field(None, description="External issue ID (e.g., Git issue number)")
    created_by: str = Field(..., description="ID of user/agent creating the issue")


class IssueUpdate(BaseModel):
    """Pydantic model for updating issues"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    issue_type: Optional[IssueType] = None
    status: Optional[IssueStatus] = None
    priority: Optional[IssuePriority] = None
    assignee_id: Optional[str] = None
    labels: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class IssueResponse(IssueBase):
    """Pydantic model for issue responses"""
    id: str
    external_id: Optional[str]
    status: IssueStatus
    assignee_id: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class StoryGeneration(BaseModel):
    """Pydantic model for story generation requests"""
    epic_id: Optional[str] = Field(None, description="Parent epic ID")
    feature_description: str = Field(..., description="Feature description for story generation")
    acceptance_criteria: Optional[List[str]] = Field(default_factory=list)
    story_points: Optional[int] = Field(None, ge=1, le=21, description="Story points estimate")
    priority: IssuePriority = Field(default=IssuePriority.MEDIUM)


class IssueLink(BaseModel):
    """Pydantic model for linking issues"""
    source_issue_id: str = Field(..., description="Source issue ID")
    target_issue_id: str = Field(..., description="Target issue ID")
    link_type: str = Field(default="relates_to", description="Type of link (blocks, relates_to, etc.)")
    description: Optional[str] = Field(None, description="Link description") 