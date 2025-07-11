"""
Agent models for the Agentic Agile System
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AgentStatus(str, Enum):
    """Agent status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class AgentCapability(str, Enum):
    """Agent capability enumeration"""
    # Core Agile Roles
    PROJECT_MANAGER = "project_manager"
    PRODUCT_OWNER = "product_owner"
    SCRUM_MASTER = "scrum_master"
    SOFTWARE_ARCHITECT = "software_architect"
    SOFTWARE_WRITER = "software_writer"
    DEVELOPER = "developer"
    QA_ENGINEER = "qa_engineer"
    ARCHITECTURE_REVIEWER = "architecture_reviewer"
    APPLICATION_DEVELOPER = "application_developer"
    MORALE_BOOSTER = "morale_booster"
    
    # Additional Capabilities
    ISSUE_TRIAGE = "issue_triage"
    STORY_GENERATION = "story_generation"
    SPRINT_PLANNING = "sprint_planning"
    SPEC_CREATION = "spec_creation"
    CODE_SCAFFOLDING = "code_scaffolding"
    TEST_GENERATION = "test_generation"
    CODE_REVIEW = "code_review"
    DEPLOYMENT = "deployment"
    WELLNESS_TRACKING = "wellness_tracking"


class Agent(Base):
    """SQLAlchemy model for agents"""
    __tablename__ = "agents"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    agent_type = Column(String(50), nullable=False, index=True)
    status = Column(String(20), default=AgentStatus.INACTIVE)
    capabilities = Column(JSON, default=list)
    agent_metadata = Column(JSON, default=dict)  # Renamed from metadata to avoid conflict
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class AgentBase(BaseModel):
    """Base Pydantic model for agents"""
    name: str = Field(..., min_length=1, max_length=100, description="Agent name")
    agent_type: str = Field(..., description="Type of agent (PM, PO, SM, etc.)")
    capabilities: List[AgentCapability] = Field(default_factory=list, description="Agent capabilities")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional agent metadata")


class AgentCreate(AgentBase):
    """Pydantic model for creating agents"""
    pass


class AgentUpdate(BaseModel):
    """Pydantic model for updating agents"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[AgentStatus] = None
    capabilities: Optional[List[AgentCapability]] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentResponse(AgentBase):
    """Pydantic model for agent responses"""
    id: str
    status: AgentStatus
    last_heartbeat: datetime
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class AgentTrigger(BaseModel):
    """Pydantic model for triggering agent actions"""
    action: str = Field(..., description="Action to trigger")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    priority: int = Field(default=1, ge=1, le=10, description="Action priority (1-10)")
    timeout: Optional[int] = Field(None, ge=1, description="Timeout in seconds")


class AgentHeartbeat(BaseModel):
    """Pydantic model for agent heartbeats"""
    status: AgentStatus
    current_task: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None


class AgentRegistration(BaseModel):
    """Pydantic model for agent registration"""
    name: str = Field(..., min_length=1, max_length=100)
    agent_type: str = Field(..., description="Type of agent")
    capabilities: List[AgentCapability] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    endpoint_url: Optional[str] = Field(None, description="Agent's callback endpoint")
    auth_token: Optional[str] = Field(None, description="Agent's authentication token") 