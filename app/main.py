"""
Main FastAPI application for the Agentic Agile System API Hub
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import time
import uuid
import structlog
from contextlib import asynccontextmanager
from typing import Dict, Any

from app.config import settings
from app.api.v1.api import api_router
from app.core.middleware import AuditMiddleware, RateLimitMiddleware
from app.core.database import init_db, close_db
from app.core.logging import setup_logging

# Setup structured logging
setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Agentic Agile System API Hub", version=settings.version)
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agentic Agile System API Hub")
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="A central, extensible API hub for agent-driven agile development",
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.debug
)


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.project_name,
        version=settings.version,
        description="A central, extensible API hub that orchestrates all agent and system interactions for the Agentic Agile System",
        routes=app.routes,
    )
    
    # Add custom info
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with structured logging"""
    trace_id = str(uuid.uuid4())
    
    logger.error(
        "Unhandled exception",
        trace_id=trace_id,
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "trace_id": trace_id,
            "message": "An unexpected error occurred. Please try again later.",
            "remediation_hint": "Check the logs for more details or contact support."
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": settings.project_name,
        "version": settings.version,
        "timestamp": time.time()
    }


# Readiness check endpoint
@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint for orchestration"""
    # Add database connectivity check here
    return {
        "status": "ready",
        "service": settings.project_name,
        "version": settings.version,
        "timestamp": time.time()
    }


# Metrics endpoint (for Prometheus)
@app.get("/metrics")
async def metrics():
    """Metrics endpoint for monitoring"""
    # Add actual metrics collection here
    return {
        "requests_total": 0,
        "requests_duration_seconds": 0.0,
        "active_agents": 0,
        "total_issues": 0,
        "wellness_checkins_today": 0
    }


# Include API router
app.include_router(api_router, prefix=settings.api_v1_str)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to the Agentic Agile System API Hub",
        "service": settings.project_name,
        "version": settings.version,
        "docs": "/docs",
        "health": "/health",
        "ready": "/ready",
        "metrics": "/metrics"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 