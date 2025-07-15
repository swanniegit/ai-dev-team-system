"""
Redis-based caching layer for the Agentic Agile System

Provides high-performance caching with TTL, pattern-based invalidation,
and automatic cache warming capabilities.
"""

import json
import hashlib
import structlog
from typing import Any, Optional, Dict, List, Union, Callable
from datetime import datetime, timedelta
from functools import wraps
import redis.asyncio as redis
import asyncio
from dataclasses import dataclass

from app.config import settings

logger = structlog.get_logger()


@dataclass
class CacheConfig:
    """Configuration for cache behavior"""
    default_ttl: int = 3600  # 1 hour
    key_prefix: str = "agentic_agile"
    serializer: str = "json"  # json, pickle
    compression: bool = False
    max_connections: int = 10


class CacheError(Exception):
    """Base exception for cache errors"""
    pass


class CacheConnectionError(CacheError):
    """Cache connection error"""
    pass


class CacheManager:
    """High-performance Redis cache manager"""
    
    def __init__(self, config: CacheConfig = None):
        self.config = config or CacheConfig()
        self.redis_client: Optional[redis.Redis] = None
        self.connection_pool = None
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "errors": 0
        }
    
    async def connect(self):
        """Connect to Redis with connection pooling"""
        try:
            self.connection_pool = redis.ConnectionPool.from_url(
                settings.redis_url,
                max_connections=self.config.max_connections,
                retry_on_timeout=True,
                socket_keepalive=True,
                socket_keepalive_options={}
            )
            
            self.redis_client = redis.Redis(
                connection_pool=self.connection_pool,
                decode_responses=True
            )
            
            await self.redis_client.ping()
            logger.info("Cache manager connected to Redis")
            
        except Exception as e:
            logger.error("Failed to connect cache manager to Redis", error=str(e))
            raise CacheConnectionError(f"Failed to connect to Redis: {e}")
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
        if self.connection_pool:
            await self.connection_pool.disconnect()
        logger.info("Cache manager disconnected from Redis")
    
    def _generate_key(self, key: str) -> str:
        """Generate a properly prefixed cache key"""
        return f"{self.config.key_prefix}:{key}"
    
    def _serialize(self, value: Any) -> str:
        """Serialize value for storage"""
        if self.config.serializer == "json":
            return json.dumps(value, default=str)
        else:
            # Could add pickle support here
            return json.dumps(value, default=str)
    
    def _deserialize(self, value: str) -> Any:
        """Deserialize value from storage"""
        if self.config.serializer == "json":
            return json.loads(value)
        else:
            # Could add pickle support here
            return json.loads(value)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            raise CacheConnectionError("Cache not connected")
        
        try:
            cache_key = self._generate_key(key)
            value = await self.redis_client.get(cache_key)
            
            if value is not None:
                self._stats["hits"] += 1
                return self._deserialize(value)
            else:
                self._stats["misses"] += 1
                return None
                
        except Exception as e:
            self._stats["errors"] += 1
            logger.error("Failed to get from cache", key=key, error=str(e))
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Set value in cache with optional TTL and tags"""
        if not self.redis_client:
            raise CacheConnectionError("Cache not connected")
        
        try:
            cache_key = self._generate_key(key)
            serialized_value = self._serialize(value)
            ttl = ttl or self.config.default_ttl
            
            # Set the main cache entry
            await self.redis_client.setex(cache_key, ttl, serialized_value)
            
            # Add to tag indexes for pattern-based invalidation
            if tags:
                for tag in tags:
                    tag_key = self._generate_key(f"tag:{tag}")
                    await self.redis_client.sadd(tag_key, cache_key)
                    await self.redis_client.expire(tag_key, ttl + 60)  # Slightly longer TTL
            
            self._stats["sets"] += 1
            return True
            
        except Exception as e:
            self._stats["errors"] += 1
            logger.error("Failed to set cache", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.redis_client:
            raise CacheConnectionError("Cache not connected")
        
        try:
            cache_key = self._generate_key(key)
            result = await self.redis_client.delete(cache_key)
            self._stats["deletes"] += 1
            return result > 0
            
        except Exception as e:
            self._stats["errors"] += 1
            logger.error("Failed to delete from cache", key=key, error=str(e))
            return False
    
    async def delete_by_pattern(self, pattern: str) -> int:
        """Delete keys matching a pattern"""
        if not self.redis_client:
            raise CacheConnectionError("Cache not connected")
        
        try:
            full_pattern = self._generate_key(pattern)
            keys = await self.redis_client.keys(full_pattern)
            
            if keys:
                deleted = await self.redis_client.delete(*keys)
                self._stats["deletes"] += deleted
                return deleted
            return 0
            
        except Exception as e:
            self._stats["errors"] += 1
            logger.error("Failed to delete by pattern", pattern=pattern, error=str(e))
            return 0
    
    async def delete_by_tag(self, tag: str) -> int:
        """Delete all keys associated with a tag"""
        if not self.redis_client:
            raise CacheConnectionError("Cache not connected")
        
        try:
            tag_key = self._generate_key(f"tag:{tag}")
            keys = await self.redis_client.smembers(tag_key)
            
            if keys:
                # Delete all tagged keys and the tag itself
                all_keys = list(keys) + [tag_key]
                deleted = await self.redis_client.delete(*all_keys)
                self._stats["deletes"] += deleted
                return deleted
            return 0
            
        except Exception as e:
            self._stats["errors"] += 1
            logger.error("Failed to delete by tag", tag=tag, error=str(e))
            return 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.redis_client:
            return False
        
        try:
            cache_key = self._generate_key(key)
            return await self.redis_client.exists(cache_key) > 0
        except Exception as e:
            logger.error("Failed to check cache existence", key=key, error=str(e))
            return False
    
    async def ttl(self, key: str) -> int:
        """Get TTL for a key (-1 if no expiry, -2 if doesn't exist)"""
        if not self.redis_client:
            return -2
        
        try:
            cache_key = self._generate_key(key)
            return await self.redis_client.ttl(cache_key)
        except Exception as e:
            logger.error("Failed to get TTL", key=key, error=str(e))
            return -2
    
    async def increment(self, key: str, amount: int = 1, ttl: Optional[int] = None) -> int:
        """Increment a numeric value in cache"""
        if not self.redis_client:
            raise CacheConnectionError("Cache not connected")
        
        try:
            cache_key = self._generate_key(key)
            result = await self.redis_client.incr(cache_key, amount)
            
            if ttl:
                await self.redis_client.expire(cache_key, ttl)
            
            return result
            
        except Exception as e:
            self._stats["errors"] += 1
            logger.error("Failed to increment cache value", key=key, error=str(e))
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        stats = self._stats.copy()
        
        if self.redis_client:
            try:
                info = await self.redis_client.info("memory")
                stats.update({
                    "redis_memory_used": info.get("used_memory_human", "unknown"),
                    "redis_memory_peak": info.get("used_memory_peak_human", "unknown"),
                    "connected": True
                })
            except Exception as e:
                stats["redis_error"] = str(e)
                stats["connected"] = False
        else:
            stats["connected"] = False
        
        # Calculate hit rate
        total_requests = stats["hits"] + stats["misses"]
        stats["hit_rate"] = (stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return stats
    
    def cache_result(
        self, 
        ttl: Optional[int] = None, 
        key_func: Optional[Callable] = None,
        tags: Optional[List[str]] = None,
        skip_cache: Optional[Callable] = None
    ):
        """
        Decorator to cache function results
        
        Args:
            ttl: Time to live in seconds
            key_func: Function to generate cache key from args/kwargs
            tags: Tags for cache invalidation
            skip_cache: Function to determine if caching should be skipped
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Check if we should skip cache
                if skip_cache and skip_cache(*args, **kwargs):
                    return await func(*args, **kwargs)
                
                # Generate cache key
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    # Default key generation based on function name and arguments
                    key_parts = [func.__name__]
                    key_parts.extend(str(arg) for arg in args)
                    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                    key_string = "|".join(key_parts)
                    cache_key = hashlib.md5(key_string.encode()).hexdigest()
                
                # Try to get from cache
                try:
                    cached_result = await self.get(cache_key)
                    if cached_result is not None:
                        logger.debug("Cache hit", function=func.__name__, key=cache_key)
                        return cached_result
                except Exception as e:
                    logger.warning("Cache get failed, executing function", error=str(e))
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                
                try:
                    await self.set(cache_key, result, ttl, tags)
                    logger.debug("Cached result", function=func.__name__, key=cache_key)
                except Exception as e:
                    logger.warning("Cache set failed", error=str(e))
                
                return result
            
            return wrapper
        return decorator


# Global cache manager instance
cache_manager = CacheManager()


async def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance"""
    if not cache_manager.redis_client:
        await cache_manager.connect()
    return cache_manager


async def create_cache_manager_with_config(config: CacheConfig) -> CacheManager:
    """Create a new cache manager with custom configuration"""
    manager = CacheManager(config)
    await manager.connect()
    return manager


# Utility functions for common caching patterns
async def cache_api_response(
    key: str, 
    response_data: Any, 
    ttl: int = 300,  # 5 minutes default for API responses
    tags: Optional[List[str]] = None
) -> bool:
    """Cache API response data"""
    manager = await get_cache_manager()
    return await manager.set(key, response_data, ttl, tags)


async def get_cached_api_response(key: str) -> Optional[Any]:
    """Get cached API response data"""
    manager = await get_cache_manager()
    return await manager.get(key)


async def invalidate_user_cache(user_id: str):
    """Invalidate all cache entries for a user"""
    manager = await get_cache_manager()
    await manager.delete_by_tag(f"user:{user_id}")


async def invalidate_agent_cache(agent_id: str):
    """Invalidate all cache entries for an agent"""
    manager = await get_cache_manager()
    await manager.delete_by_tag(f"agent:{agent_id}")


async def warm_cache():
    """Warm up the cache with frequently accessed data"""
    logger.info("Starting cache warming process")
    
    try:
        # Import here to avoid circular imports
        from app.core.database import get_db
        from app.models.agent import Agent
        from app.models.user import User
        
        # This would be called during startup to pre-populate cache
        # with frequently accessed data like active agents, user lists, etc.
        
        manager = await get_cache_manager()
        
        # Example: Cache active agents list
        # db = next(get_db())
        # active_agents = db.query(Agent).filter(Agent.is_active == True).all()
        # await manager.set("active_agents", [agent.id for agent in active_agents], 600)
        
        logger.info("Cache warming completed")
        
    except Exception as e:
        logger.error("Cache warming failed", error=str(e))