"""
Authentication endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
import structlog
import uuid

from app.core.database import get_db
from app.models.user import User, UserCreate, UserResponse, UserLogin, Token
from app.core.security import create_access_token, get_current_user, get_password_hash, verify_password

logger = structlog.get_logger()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user.email) | (User.username == user.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
        
        # Create new user with hashed password
        hashed_password = get_password_hash(user.password)
        db_user = User(
            id=str(uuid.uuid4()),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to register user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    try:
        # Find user by username or email
        user = db.query(User).filter(
            (User.username == form_data.username) | (User.email == form_data.username)
        ).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        # Verify password hash
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.username})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,  # 30 minutes
            "user": user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to login user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to login user"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@router.post("/logout")
async def logout_user():
    """Logout user (in a real implementation, this would invalidate the token)"""
    return {"message": "Successfully logged out"} 