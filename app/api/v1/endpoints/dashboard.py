"""
Dashboard endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import structlog

from app.core.database import get_db

logger = structlog.get_logger()
router = APIRouter()


@router.get("/metrics")
async def get_dashboard_metrics(
    db: Session = Depends(get_db)
):
    """Get dashboard metrics"""
    try:
        # In a real implementation, this would aggregate data from the database
        # For now, return mock data
        
        return {
            "agents": {
                "total": 8,
                "active": 6,
                "busy": 2,
                "offline": 0
            },
            "issues": {
                "total": 45,
                "open": 12,
                "in_progress": 8,
                "review": 5,
                "testing": 3,
                "done": 17
            },
            "sprints": {
                "current": "Sprint 3",
                "velocity": 23,
                "burndown": [25, 22, 18, 15, 12, 8, 5, 2],
                "completion_rate": 0.85
            },
            "wellness": {
                "average_mood": 7.5,
                "checkins_today": 12,
                "participation_rate": 0.92,
                "trend": "improving"
            },
            "performance": {
                "cycle_time": 4.2,
                "lead_time": 8.7,
                "throughput": 15,
                "quality_score": 0.94
            }
        }
        
    except Exception as e:
        logger.error("Failed to get dashboard metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard metrics"
        )


@router.get("/analytics")
async def get_analytics(
    period: str = "30d",
    db: Session = Depends(get_db)
):
    """Get analytics data"""
    try:
        # In a real implementation, this would query the database for analytics
        # For now, return mock data
        
        return {
            "period": period,
            "agent_performance": {
                "PM_Agent": {"tasks_completed": 15, "avg_response_time": 2.3},
                "PO_Agent": {"stories_generated": 28, "avg_quality_score": 8.7},
                "DEV_Agent": {"commits": 45, "code_reviews": 12},
                "QA_Agent": {"tests_run": 156, "bugs_found": 8},
                "Morale_Booster": {"checkins_facilitated": 89, "challenges_created": 5}
            },
            "team_velocity": [18, 22, 19, 25, 23, 21, 24, 26],
            "issue_distribution": {
                "bugs": 0.25,
                "features": 0.45,
                "stories": 0.20,
                "tasks": 0.10
            },
            "wellness_trends": {
                "mood": [7.2, 7.5, 7.8, 7.6, 7.9, 8.1, 7.8, 7.5],
                "energy": [6.5, 6.8, 7.0, 6.9, 7.2, 7.1, 6.8, 6.9],
                "stress": [4.5, 4.2, 4.0, 4.1, 3.8, 3.9, 4.2, 4.0]
            }
        }
        
    except Exception as e:
        logger.error("Failed to get analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get analytics"
        )


@router.get("/health")
async def get_system_health(
    db: Session = Depends(get_db)
):
    """Get system health status"""
    try:
        # In a real implementation, this would check various system components
        # For now, return mock data
        
        return {
            "status": "healthy",
            "components": {
                "database": "healthy",
                "redis": "healthy",
                "mongodb": "healthy",
                "agents": "healthy"
            },
            "last_check": "2024-01-15T10:30:00Z",
            "uptime": "7d 14h 23m",
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error("Failed to get system health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system health"
        ) 