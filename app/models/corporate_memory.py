"""
Corporate Memory models for the Agentic Agile System
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MemoryType(str, Enum):
    """Memory type enumeration"""
    DECISION = "decision"
    LEARNING = "learning"
    PATTERN = "pattern"
    KNOWLEDGE = "knowledge"
    EXPERIENCE = "experience"
    BEST_PRACTICE = "best_practice"
    LESSON_LEARNED = "lesson_learned"


class CorporateMemory(Base):
    """SQLAlchemy model for corporate memory"""
    __tablename__ = "corporate_memory"
    
    id = Column(String(36), primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    memory_type = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    context = Column(JSON, nullable=True)
    agent_id = Column(String(36), nullable=True, index=True)
    user_id = Column(String(36), nullable=True, index=True)
    project_id = Column(String(36), nullable=True, index=True)
    tags = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    usage_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)


class CorporateMemoryCreate(BaseModel):
    """Pydantic model for creating corporate memory"""
    memory_type: MemoryType
    category: str
    title: str
    description: str
    context: Optional[Dict[str, Any]] = None
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    tags: Optional[List[str]] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


class CorporateMemoryResponse(BaseModel):
    """Pydantic model for corporate memory responses"""
    id: str
    timestamp: datetime
    memory_type: MemoryType
    category: str
    title: str
    description: str
    context: Optional[Dict[str, Any]]
    agent_id: Optional[str]
    user_id: Optional[str]
    project_id: Optional[str]
    tags: Optional[List[str]]
    confidence_score: Optional[float]
    usage_count: int
    last_accessed: Optional[datetime]
    is_active: bool
    metadata: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class MemorySearch(BaseModel):
    """Pydantic model for memory search"""
    query: str
    memory_types: Optional[List[MemoryType]] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    agent_id: Optional[str] = None
    project_id: Optional[str] = None
    min_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    limit: int = Field(default=20, le=100)
    offset: int = Field(default=0, ge=0)


class MemoryUpdate(BaseModel):
    """Pydantic model for updating corporate memory"""
    title: Optional[str] = None
    description: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None 