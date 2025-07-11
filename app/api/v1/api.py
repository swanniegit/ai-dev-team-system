"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import agents, issues, wellness, auth, dashboard

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(issues.router, prefix="/issues", tags=["issues"])
api_router.include_router(wellness.router, prefix="/wellness", tags=["wellness"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"]) 