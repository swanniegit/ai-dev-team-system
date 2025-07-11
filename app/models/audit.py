"""
Audit models for the Agentic Agile System
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuditAction(str, Enum):
    """Audit action enumeration"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    TRIGGER = "trigger"
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"
    HEARTBEAT = "heartbeat"


class AuditLog(Base):
    """SQLAlchemy model for audit logs"""
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(String(36), nullable=True, index=True)
    agent_id = Column(String(36), nullable=True, index=True)
    action = Column(String(50), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(String(36), nullable=True, index=True)
    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    request_data = Column(JSON, nullable=True)
    response_data = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    trace_id = Column(String(36), nullable=True, index=True)
    duration_ms = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)


class AuditLogResponse(BaseModel):
    """Pydantic model for audit log responses"""
    id: str
    timestamp: datetime
    user_id: Optional[str]
    agent_id: Optional[str]
    action: AuditAction
    resource_type: str
    resource_id: Optional[str]
    endpoint: str
    method: str
    status_code: int
    request_data: Optional[Dict[str, Any]]
    response_data: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    user_agent: Optional[str]
    trace_id: Optional[str]
    duration_ms: Optional[int]
    error_message: Optional[str]
    
    class Config:
        from_attributes = True


class AuditFilter(BaseModel):
    """Pydantic model for audit log filtering"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    action: Optional[AuditAction] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    status_code: Optional[int] = None
    limit: int = Field(default=100, le=1000)
    offset: int = Field(default=0, ge=0) 