"""
Event models for the Agentic Agile System
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class EventCreate(BaseModel):
    """Pydantic model for creating events"""
    event_type: str = Field(..., description="Type of event")
    data: Dict[str, Any] = Field(..., description="Event data")
    priority: Optional[str] = Field("normal", description="Event priority")
    source: Optional[str] = Field(None, description="Event source")
    target: Optional[str] = Field(None, description="Event target")


class EventResponse(BaseModel):
    """Pydantic model for event responses"""
    id: str
    type: str
    data: Dict[str, Any]
    priority: str
    source: Optional[str]
    target: Optional[str]
    timestamp: datetime
    version: str


class EventHistory(BaseModel):
    """Pydantic model for event history"""
    message_id: str
    id: str
    type: str
    data: Dict[str, Any]
    priority: str
    source: Optional[str]
    target: Optional[str]
    timestamp: datetime
    version: str 