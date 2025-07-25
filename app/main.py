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
from app.core.middleware import AuditMiddleware, RateLimitMiddleware, SecurityMiddleware, RequestSizeLimitMiddleware
from app.core.database import init_db, close_db, get_redis
from app.core.logging import setup_logging
from app.core.event_bus import event_bus

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
    
    # Initialize event bus
    await event_bus.connect()
    logger.info("Event bus initialized successfully")
    
    # Initialize cache if needed
    try:
        from app.core.cache import cache_manager
        await cache_manager.connect()
        logger.info("Cache manager initialized successfully")
    except Exception as e:
        logger.warning("Cache manager initialization failed", error=str(e))
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agentic Agile System API Hub")
    await event_bus.disconnect()
    
    # Disconnect cache
    try:
        from app.core.cache import cache_manager
        await cache_manager.disconnect()
        logger.info("Cache manager disconnected")
    except Exception as e:
        logger.warning("Cache manager disconnect failed", error=str(e))
    
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


# Add middleware (order matters - last added executes first)
# Remove the default CORS middleware since SecurityMiddleware handles it

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Add our custom middleware stack
async def setup_rate_limiting():
    """Setup rate limiting with Redis client"""
    try:
        redis_client = get_redis()
        return RateLimitMiddleware(app, redis_client)
    except Exception as e:
        logger.warning("Redis not available for rate limiting", error=str(e))
        return RateLimitMiddleware(app, None)

app.add_middleware(AuditMiddleware)
app.add_middleware(RequestSizeLimitMiddleware, max_size=10 * 1024 * 1024)  # 10MB limit
app.add_middleware(SecurityMiddleware)  # Handles CORS and security headers


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
    # Check database connectivity
    try:
        from app.core.database import health_check
        db_health = await health_check()
        
        # Check if all critical services are healthy
        critical_services = ['postgresql', 'redis']
        all_healthy = all(
            db_health.get(service, {}).get('status') == 'healthy' 
            for service in critical_services
        )
        
        return {
            "status": "ready" if all_healthy else "not_ready",
            "service": settings.project_name,
            "version": settings.version,
            "timestamp": time.time(),
            "services": db_health
        }
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        return {
            "status": "not_ready",
            "service": settings.project_name,
            "version": settings.version,
            "timestamp": time.time(),
            "error": str(e)
        }


# Metrics endpoint (for Prometheus)
@app.get("/metrics")
async def metrics():
    """Metrics endpoint for monitoring"""
    try:
        # Get cache statistics
        from app.core.cache import cache_manager
        cache_stats = await cache_manager.get_stats()
        
        # Get database connection stats
        from app.core.database import get_connection_stats
        db_stats = get_connection_stats()
        
        # Get event bus info
        event_stats = await event_bus.get_stream_info() if event_bus.redis_client else {}
        
        return {
            "service": settings.project_name,
            "version": settings.version,
            "timestamp": time.time(),
            "cache": cache_stats,
            "database": db_stats,
            "event_bus": event_stats
        }
    except Exception as e:
        logger.error("Metrics collection failed", error=str(e))
        return {
            "service": settings.project_name,
            "version": settings.version,
            "timestamp": time.time(),
            "error": str(e)
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