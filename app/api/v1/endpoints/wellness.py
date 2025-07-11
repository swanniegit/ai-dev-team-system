"""
Wellness endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import structlog

from app.core.database import get_db
from app.models.wellness import (
    WellnessCheckin, WellnessCheckinCreate, WellnessCheckinResponse,
    WellnessMetrics, MoraleChallenge, WellnessRecommendation,
    MoodLevel
)

logger = structlog.get_logger()
router = APIRouter()


@router.post("/checkin", response_model=WellnessCheckinResponse, status_code=status.HTTP_201_CREATED)
async def create_wellness_checkin(
    checkin: WellnessCheckinCreate,
    db: Session = Depends(get_db)
):
    """Create a wellness check-in"""
    try:
        db_checkin = WellnessCheckin(
            id=str(uuid.uuid4()),
            user_id=checkin.user_id,
            agent_id=checkin.agent_id,
            mood_level=checkin.mood_level,
            energy_level=checkin.energy_level,
            stress_level=checkin.stress_level,
            satisfaction_level=checkin.satisfaction_level,
            engagement_level=checkin.engagement_level,
            workload_level=checkin.workload_level,
            notes=checkin.notes,
            metadata=checkin.metadata
        )
        
        db.add(db_checkin)
        db.commit()
        db.refresh(db_checkin)
        
        return db_checkin
        
    except Exception as e:
        logger.error("Failed to create wellness check-in", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create wellness check-in"
        )


@router.get("/checkin/{checkin_id}", response_model=WellnessCheckinResponse)
async def get_wellness_checkin(
    checkin_id: str,
    db: Session = Depends(get_db)
):
    """Get wellness check-in by ID"""
    checkin = db.query(WellnessCheckin).filter(WellnessCheckin.id == checkin_id).first()
    if not checkin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wellness check-in not found"
        )
    return checkin


@router.get("/checkin/", response_model=List[WellnessCheckinResponse])
async def list_wellness_checkins(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List wellness check-ins with filtering"""
    query = db.query(WellnessCheckin)
    
    if user_id:
        query = query.filter(WellnessCheckin.user_id == user_id)
    
    if agent_id:
        query = query.filter(WellnessCheckin.agent_id == agent_id)
    
    checkins = query.offset(offset).limit(limit).all()
    return checkins


@router.get("/metrics")
async def get_wellness_metrics(
    period: str = "weekly",
    team_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get aggregated wellness metrics"""
    # In a real implementation, this would aggregate data from the database
    # For now, return mock data
    
    return {
        "team_id": team_id,
        "period": period,
        "total_checkins": 42,
        "average_mood": 7.5,
        "average_energy": 6.8,
        "average_stress": 4.2,
        "average_satisfaction": 8.1,
        "average_engagement": 7.9,
        "average_workload": 6.5,
        "mood_distribution": {
            "excellent": 15,
            "good": 20,
            "neutral": 5,
            "poor": 2,
            "terrible": 0
        },
        "trends": {
            "mood": [7.2, 7.5, 7.8, 7.5],
            "energy": [6.5, 6.8, 7.0, 6.8],
            "stress": [4.5, 4.2, 4.0, 4.2]
        }
    }


@router.post("/challenges")
async def create_morale_challenge(
    challenge: MoraleChallenge,
    db: Session = Depends(get_db)
):
    """Create a morale challenge"""
    try:
        # In a real implementation, this would save to database
        # For now, return the challenge with an ID
        
        challenge.id = str(uuid.uuid4())
        
        return {
            "message": "Morale challenge created successfully",
            "challenge": challenge
        }
        
    except Exception as e:
        logger.error("Failed to create morale challenge", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create morale challenge"
        )


@router.post("/recommendations")
async def create_wellness_recommendation(
    recommendation: WellnessRecommendation,
    db: Session = Depends(get_db)
):
    """Create a wellness recommendation"""
    try:
        # In a real implementation, this would save to database
        # For now, return the recommendation
        
        return {
            "message": "Wellness recommendation created successfully",
            "recommendation": recommendation
        }
        
    except Exception as e:
        logger.error("Failed to create wellness recommendation", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create wellness recommendation"
        ) 