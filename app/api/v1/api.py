"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import agents, issues, wellness, auth, dashboard, git, events

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(issues.router, prefix="/issues", tags=["issues"])
api_router.include_router(wellness.router, prefix="/wellness", tags=["wellness"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(git.router, prefix="/git", tags=["git"])
api_router.include_router(events.router, prefix="/events", tags=["events"]) 