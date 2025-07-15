"""
Event Bus for async, decoupled agent communication using Redis Streams
"""

import json
import uuid
import structlog
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable, Awaitable
from enum import Enum
import asyncio
import redis.asyncio as redis
from asyncio import sleep
from dataclasses import dataclass

from app.config import settings

logger = structlog.get_logger()


class EventType(str, Enum):
    """Event types for the event bus"""
    # Agent events
    AGENT_REGISTERED = "agent.registered"
    AGENT_HEARTBEAT = "agent.heartbeat"
    AGENT_TRIGGERED = "agent.triggered"
    AGENT_COMPLETED = "agent.completed"
    AGENT_ERROR = "agent.error"
    
    # Git events
    GIT_ISSUE_CREATED = "git.issue.created"
    GIT_ISSUE_UPDATED = "git.issue.updated"
    GIT_PR_CREATED = "git.pr.created"
    GIT_PR_UPDATED = "git.pr.updated"
    GIT_PUSH = "git.push"
    GIT_RELEASE = "git.release"
    
    # Workflow events
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"
    
    # Wellness events
    WELLNESS_CHECKIN = "wellness.checkin"
    WELLNESS_ALERT = "wellness.alert"
    
    # System events
    SYSTEM_HEALTH = "system.health"
    SYSTEM_MAINTENANCE = "system.maintenance"


class EventPriority(str, Enum):
    """Event priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RetryConfig:
    """Configuration for retry logic"""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    

class EventBusError(Exception):
    """Base exception for event bus errors"""
    pass


class EventPublishError(EventBusError):
    """Error publishing an event"""
    pass


class EventProcessingError(EventBusError):
    """Error processing an event"""
    pass


class EventBus:
    """Event bus for async agent communication using Redis Streams"""
    
    def __init__(self, retry_config: RetryConfig = None):
        self.redis_client: Optional[redis.Redis] = None
        self.subscribers: Dict[str, List[Callable]] = {}
        self.running = False
        self.consumer_group = "agentic_agile_consumers"
        self.stream_name = "agentic_agile_events"
        self.retry_config = retry_config or RetryConfig()
        self.failed_events_stream = "agentic_agile_failed_events"
        self.connection_pool = None
    
    async def connect(self):
        """Connect to Redis and initialize the event bus with connection pooling"""
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                # Create connection pool for better performance
                self.connection_pool = redis.ConnectionPool.from_url(
                    settings.redis_url,
                    max_connections=20,
                    retry_on_timeout=True,
                    socket_keepalive=True,
                    socket_keepalive_options={}
                )
                
                self.redis_client = redis.Redis(
                    connection_pool=self.connection_pool,
                    decode_responses=True
                )
                
                await self.redis_client.ping()
                
                # Create consumer group if it doesn't exist
                try:
                    await self.redis_client.xgroup_create(
                        self.stream_name, 
                        self.consumer_group, 
                        id="0", 
                        mkstream=True
                    )
                except redis.ResponseError as e:
                    if "BUSYGROUP" not in str(e):
                        raise
                
                # Create failed events stream
                try:
                    await self.redis_client.xgroup_create(
                        self.failed_events_stream,
                        f"{self.consumer_group}_failed",
                        id="0",
                        mkstream=True
                    )
                except redis.ResponseError as e:
                    if "BUSYGROUP" not in str(e):
                        raise
                
                logger.info("Event bus connected to Redis", attempt=attempt + 1)
                return
                
            except Exception as e:
                logger.warning(
                    "Failed to connect event bus to Redis", 
                    error=str(e), 
                    attempt=attempt + 1,
                    max_retries=max_retries
                )
                
                if attempt == max_retries - 1:
                    logger.error("Failed to connect to Redis after all retries")
                    raise EventBusError(f"Failed to connect to Redis: {e}")
                
                await sleep(retry_delay * (2 ** attempt))
    
    async def disconnect(self):
        """Disconnect from Redis"""
        self.running = False
        
        if self.redis_client:
            try:
                await self.redis_client.close()
            except Exception as e:
                logger.warning("Error closing Redis client", error=str(e))
                
        if self.connection_pool:
            try:
                await self.connection_pool.disconnect()
            except Exception as e:
                logger.warning("Error closing connection pool", error=str(e))
                
        logger.info("Event bus disconnected from Redis")
    
    async def publish(
        self, 
        event_type: EventType, 
        data: Dict[str, Any], 
        priority: EventPriority = EventPriority.NORMAL,
        source: Optional[str] = None,
        target: Optional[str] = None
    ) -> str:
        """Publish an event to the event bus"""
        if not self.redis_client:
            raise RuntimeError("Event bus not connected")
        
        event_id = str(uuid.uuid4())
        event = {
            "id": event_id,
            "type": event_type,
            "data": data,
            "priority": priority,
            "source": source,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0"
        }
        
        attempt = 0
        while attempt < self.retry_config.max_attempts:
            try:
                # Add event to Redis stream
                stream_id = await self.redis_client.xadd(
                    self.stream_name,
                    {
                        "event": json.dumps(event),
                        "type": event_type,
                        "priority": priority,
                        "source": source or "",
                        "target": target or "",
                        "attempt": str(attempt + 1)
                    }
                )
                
                logger.info(
                    "Event published",
                    event_id=event_id,
                    event_type=event_type,
                    priority=priority,
                    source=source,
                    target=target,
                    stream_id=stream_id
                )
                
                return event_id
                
            except Exception as e:
                attempt += 1
                logger.warning(
                    "Failed to publish event", 
                    error=str(e), 
                    event_id=event_id,
                    attempt=attempt,
                    max_attempts=self.retry_config.max_attempts
                )
                
                if attempt >= self.retry_config.max_attempts:
                    # Store in failed events stream
                    try:
                        await self._store_failed_event(event, str(e))
                    except Exception as store_error:
                        logger.error(
                            "Failed to store failed event",
                            error=str(store_error),
                            original_error=str(e),
                            event_id=event_id
                        )
                    
                    raise EventPublishError(f"Failed to publish event after {self.retry_config.max_attempts} attempts: {e}")
                
                # Exponential backoff
                delay = min(
                    self.retry_config.base_delay * (self.retry_config.exponential_base ** (attempt - 1)),
                    self.retry_config.max_delay
                )
                await sleep(delay)
    
    async def subscribe(
        self, 
        event_types: List[EventType], 
        callback: Callable[[Dict[str, Any]], Awaitable[None]],
        consumer_name: str = None
    ):
        """Subscribe to specific event types"""
        if not consumer_name:
            consumer_name = f"consumer_{uuid.uuid4().hex[:8]}"
        
        for event_type in event_types:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)
        
        logger.info(
            "Subscribed to events",
            consumer_name=consumer_name,
            event_types=[et.value for et in event_types]
        )
        
        return consumer_name
    
    async def unsubscribe(self, event_type: EventType, callback: Callable):
        """Unsubscribe from an event type"""
        if event_type in self.subscribers:
            if callback in self.subscribers[event_type]:
                self.subscribers[event_type].remove(callback)
                logger.info("Unsubscribed from event", event_type=event_type)
    
    async def start_consuming(self):
        """Start consuming events from the stream"""
        if not self.redis_client:
            raise RuntimeError("Event bus not connected")
        
        self.running = True
        logger.info("Starting event bus consumer")
        
        worker_id = f"worker_{uuid.uuid4().hex[:8]}"
        
        while self.running:
            try:
                # Read events from the stream
                messages = await self.redis_client.xreadgroup(
                    self.consumer_group,
                    worker_id,
                    {self.stream_name: ">"},
                    count=10,
                    block=1000
                )
                
                for stream, stream_messages in messages:
                    for message_id, fields in stream_messages:
                        success = await self._process_message_with_retry(message_id, fields)
                        
                        if success:
                            # Acknowledge the message only if processed successfully
                            await self.redis_client.xack(self.stream_name, self.consumer_group, message_id)
                        else:
                            logger.error(
                                "Failed to process message after retries",
                                message_id=message_id
                            )
                
            except redis.ConnectionError as e:
                logger.error("Redis connection error in consumer", error=str(e))
                await self._handle_connection_error()
            except Exception as e:
                logger.error("Error in event bus consumer", error=str(e))
                await sleep(1)  # Wait before retrying
    
    async def stop_consuming(self):
        """Stop consuming events"""
        self.running = False
        logger.info("Stopping event bus consumer")
    
    async def _process_message_with_retry(self, message_id: str, fields: Dict[str, Any]) -> bool:
        """Process a message with retry logic"""
        for attempt in range(self.retry_config.max_attempts):
            try:
                success = await self._process_message(message_id, fields)
                if success:
                    return True
                    
            except Exception as e:
                logger.warning(
                    "Error processing message",
                    error=str(e),
                    message_id=message_id,
                    attempt=attempt + 1
                )
                
            if attempt < self.retry_config.max_attempts - 1:
                delay = self.retry_config.base_delay * (self.retry_config.exponential_base ** attempt)
                await sleep(min(delay, self.retry_config.max_delay))
        
        # Store failed message
        try:
            await self._store_failed_message(message_id, fields)
        except Exception as e:
            logger.error("Failed to store failed message", error=str(e), message_id=message_id)
            
        return False
    
    async def _process_message(self, message_id: str, fields: Dict[str, Any]) -> bool:
        """Process a single message from the stream"""
        try:
            # Handle both bytes and string keys for compatibility
            event_json = fields.get("event") or fields.get(b"event", b"{}")
            if isinstance(event_json, bytes):
                event_json = event_json.decode()
                
            event_data = json.loads(event_json)
            
            event_type_str = fields.get("type") or fields.get(b"type", b"").decode()
            if not event_type_str:
                raise EventProcessingError("Missing event type")
                
            event_type = EventType(event_type_str)
            
            # Call registered callbacks
            callbacks_executed = 0
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    try:
                        await callback(event_data)
                        callbacks_executed += 1
                    except Exception as e:
                        logger.error(
                            "Error in event callback",
                            error=str(e),
                            event_type=event_type,
                            message_id=message_id,
                            callback=str(callback)
                        )
                        # Don't fail the entire message for callback errors
            
            logger.debug(
                "Processed event message",
                message_id=message_id,
                event_type=event_type,
                callbacks_executed=callbacks_executed
            )
            
            return True
            
        except json.JSONDecodeError as e:
            logger.error(
                "Invalid JSON in message",
                error=str(e),
                message_id=message_id
            )
            return False
        except ValueError as e:
            logger.error(
                "Invalid event type",
                error=str(e),
                message_id=message_id
            )
            return False
        except Exception as e:
            logger.error(
                "Failed to process message",
                error=str(e),
                message_id=message_id
            )
            return False
    
    async def get_event_history(
        self, 
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent event history"""
        if not self.redis_client:
            return []
        
        try:
            # Get recent events from the stream
            messages = await self.redis_client.xrevrange(
                self.stream_name,
                count=limit
            )
            
            events = []
            for message_id, fields in messages:
                event_data = json.loads(fields.get(b"event", "{}"))
                
                # Filter by event type if specified
                if event_type and event_data.get("type") != event_type:
                    continue
                
                events.append({
                    "message_id": message_id,
                    **event_data
                })
            
            return events
            
        except Exception as e:
            logger.error("Failed to get event history", error=str(e))
            return []
    
    async def get_stream_info(self) -> Dict[str, Any]:
        """Get information about the event stream"""
        if not self.redis_client:
            return {}
        
        try:
            info = await self.redis_client.xinfo_stream(self.stream_name)
            groups = await self.redis_client.xinfo_groups(self.stream_name)
            
            return {
                "stream_name": self.stream_name,
                "length": info.get("length", 0),
                "groups": len(groups),
                "consumers": sum(len(g.get("consumers", [])) for g in groups)
            }
            
        except Exception as e:
            logger.error("Failed to get stream info", error=str(e))
            return {}


    async def _store_failed_event(self, event: Dict[str, Any], error: str):
        """Store a failed event for later analysis"""
        failed_event = {
            **event,
            "failed_at": datetime.utcnow().isoformat(),
            "error": error,
            "retry_count": self.retry_config.max_attempts
        }
        
        await self.redis_client.xadd(
            self.failed_events_stream,
            {"failed_event": json.dumps(failed_event)}
        )
    
    async def _store_failed_message(self, message_id: str, fields: Dict[str, Any]):
        """Store a failed message for later analysis"""
        failed_message = {
            "message_id": message_id,
            "fields": {k.decode() if isinstance(k, bytes) else k: 
                      v.decode() if isinstance(v, bytes) else v 
                      for k, v in fields.items()},
            "failed_at": datetime.utcnow().isoformat(),
            "retry_count": self.retry_config.max_attempts
        }
        
        await self.redis_client.xadd(
            self.failed_events_stream,
            {"failed_message": json.dumps(failed_message)}
        )
    
    async def _handle_connection_error(self):
        """Handle Redis connection errors"""
        logger.warning("Attempting to reconnect to Redis...")
        try:
            await self.disconnect()
            await sleep(5)  # Wait before reconnecting
            await self.connect()
            logger.info("Successfully reconnected to Redis")
        except Exception as e:
            logger.error("Failed to reconnect to Redis", error=str(e))
            await sleep(10)  # Wait longer before next attempt
    
    async def get_failed_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get failed events for analysis"""
        if not self.redis_client:
            return []
        
        try:
            messages = await self.redis_client.xrevrange(
                self.failed_events_stream,
                count=limit
            )
            
            failed_events = []
            for message_id, fields in messages:
                if "failed_event" in fields:
                    event_data = json.loads(fields["failed_event"])
                    failed_events.append({
                        "message_id": message_id,
                        **event_data
                    })
                elif "failed_message" in fields:
                    message_data = json.loads(fields["failed_message"])
                    failed_events.append({
                        "message_id": message_id,
                        **message_data
                    })
            
            return failed_events
            
        except Exception as e:
            logger.error("Failed to get failed events", error=str(e))
            return []


# Global event bus instance
event_bus = EventBus()


async def get_event_bus() -> EventBus:
    """Get the global event bus instance with health check"""
    if not event_bus.redis_client:
        await event_bus.connect()
    else:
        # Health check
        try:
            await event_bus.redis_client.ping()
        except Exception as e:
            logger.warning("Event bus health check failed, reconnecting", error=str(e))
            await event_bus.connect()
    
    return event_bus


async def create_event_bus_with_config(retry_config: RetryConfig = None) -> EventBus:
    """Create a new event bus instance with custom configuration"""
    bus = EventBus(retry_config)
    await bus.connect()
    return bus 