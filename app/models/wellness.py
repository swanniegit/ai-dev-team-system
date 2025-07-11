"""
Wellness models for the Agentic Agile System
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MoodLevel(str, Enum):
    """Mood level enumeration"""
    EXCELLENT = "excellent"
    GOOD = "good"
    NEUTRAL = "neutral"
    POOR = "poor"
    TERRIBLE = "terrible"


class WellnessMetric(str, Enum):
    """Wellness metric enumeration"""
    MOOD = "mood"
    ENERGY = "energy"
    STRESS = "stress"
    SATISFACTION = "satisfaction"
    ENGAGEMENT = "engagement"
    WORKLOAD = "workload"


class WellnessCheckin(Base):
    """SQLAlchemy model for wellness check-ins"""
    __tablename__ = "wellness_checkins"
    
    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    agent_id = Column(String(36), nullable=True, index=True)
    mood_level = Column(String(20), nullable=False)
    energy_level = Column(Integer, nullable=True)  # 1-10 scale
    stress_level = Column(Integer, nullable=True)  # 1-10 scale
    satisfaction_level = Column(Integer, nullable=True)  # 1-10 scale
    engagement_level = Column(Integer, nullable=True)  # 1-10 scale
    workload_level = Column(Integer, nullable=True)  # 1-10 scale
    notes = Column(Text, nullable=True)
    wellness_metadata = Column(JSON, default=dict)  # Renamed from metadata to avoid conflict
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class WellnessCheckinBase(BaseModel):
    """Base Pydantic model for wellness check-ins"""
    mood_level: MoodLevel = Field(..., description="Current mood level")
    energy_level: Optional[int] = Field(None, ge=1, le=10, description="Energy level (1-10)")
    stress_level: Optional[int] = Field(None, ge=1, le=10, description="Stress level (1-10)")
    satisfaction_level: Optional[int] = Field(None, ge=1, le=10, description="Job satisfaction (1-10)")
    engagement_level: Optional[int] = Field(None, ge=1, le=10, description="Engagement level (1-10)")
    workload_level: Optional[int] = Field(None, ge=1, le=10, description="Workload level (1-10)")
    notes: Optional[str] = Field(None, description="Additional notes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class WellnessCheckinCreate(WellnessCheckinBase):
    """Pydantic model for creating wellness check-ins"""
    user_id: str = Field(..., description="User ID")
    agent_id: Optional[str] = Field(None, description="Agent ID if submitted by agent")


class WellnessCheckinResponse(WellnessCheckinBase):
    """Pydantic model for wellness check-in responses"""
    id: str
    user_id: str
    agent_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class WellnessMetrics(BaseModel):
    """Pydantic model for aggregated wellness metrics"""
    team_id: Optional[str] = None
    period: str = Field(..., description="Time period (daily, weekly, monthly)")
    start_date: datetime
    end_date: datetime
    total_checkins: int
    average_mood: float
    average_energy: float
    average_stress: float
    average_satisfaction: float
    average_engagement: float
    average_workload: float
    mood_distribution: Dict[str, int]
    trends: Dict[str, List[float]]


class MoraleChallenge(BaseModel):
    """Pydantic model for morale booster challenges"""
    id: str
    title: str = Field(..., description="Challenge title")
    description: str = Field(..., description="Challenge description")
    challenge_type: str = Field(..., description="Type of challenge")
    start_date: datetime
    end_date: datetime
    participants: List[str] = Field(default_factory=list)
    rewards: Optional[Dict[str, Any]] = None
    is_active: bool = True
    created_by: str = Field(..., description="Creator ID (agent or user)")


class WellnessRecommendation(BaseModel):
    """Pydantic model for wellness recommendations"""
    user_id: str = Field(..., description="Target user ID")
    recommendation_type: str = Field(..., description="Type of recommendation")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Recommendation description")
    priority: int = Field(default=1, ge=1, le=5, description="Priority level (1-5)")
    action_items: List[str] = Field(default_factory=list)
    created_by: str = Field(..., description="Creator ID (agent or user)")
    expires_at: Optional[datetime] = None 