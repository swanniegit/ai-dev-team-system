"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import redis.asyncio as redis
from pymongo import MongoClient
from typing import Optional, Iterator
import structlog
import asyncio

from app.config import settings

logger = structlog.get_logger()

# SQLAlchemy setup
engine = None
SessionLocal = None

# Redis setup
redis_client = None

# MongoDB setup
mongo_client = None
mongo_db = None


async def init_db():
    """Initialize database connections"""
    global engine, SessionLocal, redis_client, mongo_client, mongo_db
    
    try:
        # Initialize PostgreSQL with proper connection pooling
        engine = create_engine(
            settings.database_url,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_timeout=30,
            echo=settings.debug
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Initialize Redis with connection pooling
        redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
            retry_on_timeout=True,
            socket_keepalive=True,
            socket_keepalive_options={}
        )
        await redis_client.ping()  # Test connection
        
        # Initialize MongoDB with connection pooling
        mongo_client = MongoClient(
            settings.mongodb_url,
            maxPoolSize=50,
            minPoolSize=10,
            maxIdleTimeMS=30000,
            waitQueueTimeoutMS=5000,
            serverSelectionTimeoutMS=5000
        )
        mongo_db = mongo_client.get_default_database()
        # Test MongoDB connection
        mongo_db.command('ping')
        
        logger.info("Database connections initialized successfully")
        
    except Exception as e:
        logger.error("Failed to initialize database connections", error=str(e))
        raise


async def close_db():
    """Close database connections"""
    global engine, redis_client, mongo_client
    
    try:
        if engine:
            engine.dispose()
        
        if redis_client:
            await redis_client.close()
            
        if mongo_client:
            mongo_client.close()
            
        logger.info("Database connections closed successfully")
        
    except Exception as e:
        logger.error("Error closing database connections", error=str(e))


def get_db() -> Iterator[Session]:
    """Get database session with proper error handling"""
    if not SessionLocal:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error("Database session error", error=str(e))
        raise
    finally:
        db.close()


def get_redis():
    """Get Redis client"""
    if not redis_client:
        raise RuntimeError("Redis not initialized. Call init_db() first.")
    return redis_client


def get_mongo():
    """Get MongoDB database"""
    if not mongo_db:
        raise RuntimeError("MongoDB not initialized. Call init_db() first.")
    return mongo_db


def get_connection_stats():
    """Get database connection pool statistics"""
    if not engine:
        return {"error": "Database not initialized"}
    
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "total_connections": pool.size() + pool.overflow()
    }


async def health_check():
    """Check health of all database connections"""
    health = {
        "postgresql": {"status": "unknown", "details": {}},
        "redis": {"status": "unknown", "details": {}},
        "mongodb": {"status": "unknown", "details": {}}
    }
    
    # Check PostgreSQL
    try:
        if engine:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            health["postgresql"]["status"] = "healthy"
            health["postgresql"]["details"] = get_connection_stats()
        else:
            health["postgresql"]["status"] = "not_initialized"
    except Exception as e:
        health["postgresql"]["status"] = "unhealthy"
        health["postgresql"]["details"] = {"error": str(e)}
    
    # Check Redis
    try:
        if redis_client:
            await redis_client.ping()
            health["redis"]["status"] = "healthy"
        else:
            health["redis"]["status"] = "not_initialized"
    except Exception as e:
        health["redis"]["status"] = "unhealthy"
        health["redis"]["details"] = {"error": str(e)}
    
    # Check MongoDB
    try:
        if mongo_db:
            mongo_db.command('ping')
            health["mongodb"]["status"] = "healthy"
        else:
            health["mongodb"]["status"] = "not_initialized"
    except Exception as e:
        health["mongodb"]["status"] = "unhealthy"
        health["mongodb"]["details"] = {"error": str(e)}
    
    return health


# Base class for SQLAlchemy models
Base = declarative_base() 