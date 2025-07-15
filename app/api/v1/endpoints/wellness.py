"""
Wellness endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import structlog
import httpx

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
            wellness_metadata=checkin.metadata
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


@router.post("/poll")
async def send_wellness_poll(
    poll_request: dict,
    db: Session = Depends(get_db)
):
    """Send a wellness poll to all active agents and collect responses"""
    try:
        message = poll_request.get("message", "How are you feeling right now?")
        timeout_seconds = poll_request.get("timeout_seconds", 30)
        
        # Get all active agents
        mock_agents = [
            {"id": "dev-001", "name": "Developer Agent", "type": "dev", "endpoint": "http://dev-agent:9001/respond_wellness_poll"},
            {"id": "qa-001", "name": "QA Agent", "type": "qa"},
            {"id": "pm-001", "name": "PM Agent", "type": "pm"},
            {"id": "po-001", "name": "PO Agent", "type": "po"},
            {"id": "sm-001", "name": "SM Agent", "type": "sm"},
            {"id": "ar-001", "name": "AR Agent", "type": "ar"},
            {"id": "ad-001", "name": "AD Agent", "type": "ad"},
            {"id": "mb-001", "name": "MB Agent", "type": "mb"}
        ]
        
        import random
        from datetime import datetime, timedelta
        agent_responses = []
        total_mood = 0
        total_energy = 0
        total_stress = 0
        total_satisfaction = 0
        total_engagement = 0
        total_workload = 0
        
        for agent in mock_agents:
            if agent["id"] == "dev-001":
                # Call the real dev agent endpoint
                try:
                    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
                        resp = await client.post(agent["endpoint"], json={"message": message})
                        if resp.status_code == 200:
                            response = resp.json()
                        else:
                            response = {
                                "agent_id": agent["id"],
                                "agent_name": agent["name"],
                                "mood_level": 7,
                                "energy_level": 7,
                                "stress_level": 4,
                                "satisfaction_level": 8,
                                "engagement_level": 8,
                                "workload_level": 6,
                                "notes": "(Fallback) Could not reach dev agent.",
                                "response_time": datetime.utcnow().isoformat()
                            }
                except Exception as e:
                    logger.error("Failed to get response from dev agent", error=str(e))
                    response = {
                        "agent_id": agent["id"],
                        "agent_name": agent["name"],
                        "mood_level": 7,
                        "energy_level": 7,
                        "stress_level": 4,
                        "satisfaction_level": 8,
                        "engagement_level": 8,
                        "workload_level": 6,
                        "notes": f"(Fallback) Error: {str(e)}",
                        "response_time": datetime.utcnow().isoformat()
                    }
            else:
                # Simulate realistic wellness responses for other agents
                mood = random.randint(6, 9)
                energy = random.randint(5, 8)
                stress = random.randint(2, 6)
                satisfaction = random.randint(6, 9)
                engagement = random.randint(7, 9)
                workload = random.randint(4, 8)
                response = {
                    "agent_id": agent["id"],
                    "agent_name": agent["name"],
                    "mood_level": mood,
                    "energy_level": energy,
                    "stress_level": stress,
                    "satisfaction_level": satisfaction,
                    "engagement_level": engagement,
                    "workload_level": workload,
                    "notes": f"Feeling {['great', 'good', 'okay', 'productive'][random.randint(0, 3)]} today!",
                    "response_time": (datetime.utcnow() - timedelta(seconds=random.randint(1, 30))).isoformat()
                }
            agent_responses.append(response)
            total_mood += response["mood_level"]
            total_energy += response["energy_level"]
            total_stress += response["stress_level"]
            total_satisfaction += response["satisfaction_level"]
            total_engagement += response["engagement_level"]
            total_workload += response["workload_level"]
        num_responses = len(agent_responses)
        return {
            "total_agents": len(mock_agents),
            "responses_received": num_responses,
            "average_mood": total_mood / num_responses,
            "average_energy": total_energy / num_responses,
            "average_stress": total_stress / num_responses,
            "average_satisfaction": total_satisfaction / num_responses,
            "average_engagement": total_engagement / num_responses,
            "average_workload": total_workload / num_responses,
            "agent_responses": agent_responses,
            "poll_message": message,
            "poll_completed_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("Failed to send wellness poll", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send wellness poll"
        ) 