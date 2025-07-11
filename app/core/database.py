"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import redis
from pymongo import MongoClient
from typing import Optional
import structlog

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
        # Initialize PostgreSQL
        engine = create_engine(
            settings.database_url,
            poolclass=StaticPool,
            pool_pre_ping=True,
            echo=settings.debug
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Initialize Redis
        redis_client = redis.from_url(settings.redis_url)
        redis_client.ping()  # Test connection
        
        # Initialize MongoDB
        mongo_client = MongoClient(settings.mongodb_url)
        mongo_db = mongo_client.get_default_database()
        
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
            redis_client.close()
            
        if mongo_client:
            mongo_client.close()
            
        logger.info("Database connections closed successfully")
        
    except Exception as e:
        logger.error("Error closing database connections", error=str(e))


def get_db() -> Session:
    """Get database session"""
    if not SessionLocal:
        raise RuntimeError("Database not initialized")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """Get Redis client"""
    if not redis_client:
        raise RuntimeError("Redis not initialized")
    return redis_client


def get_mongo():
    """Get MongoDB database"""
    if not mongo_db:
        raise RuntimeError("MongoDB not initialized")
    return mongo_db


# Base class for SQLAlchemy models
Base = declarative_base() 