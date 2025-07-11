"""
User models for the Agentic Agile System
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"
    QA = "qa"
    VIEWER = "viewer"


class User(Base):
    """SQLAlchemy model for users"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200))
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    user_metadata = Column(JSON, default=dict)  # Renamed from metadata to avoid conflict
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)


class UserBase(BaseModel):
    """Base Pydantic model for users"""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    full_name: Optional[str] = Field(None, max_length=200, description="Full name")
    role: UserRole = Field(default=UserRole.VIEWER, description="User role")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class UserCreate(UserBase):
    """Pydantic model for creating users"""
    password: str = Field(..., min_length=8, description="Password")


class UserUpdate(BaseModel):
    """Pydantic model for updating users"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    """Pydantic model for user responses"""
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Pydantic model for user login"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")


class Token(BaseModel):
    """Pydantic model for authentication tokens"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponse = Field(..., description="User information")


class TokenData(BaseModel):
    """Pydantic model for token data"""
    username: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[UserRole] = None 