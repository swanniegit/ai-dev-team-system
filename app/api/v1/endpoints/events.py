"""
Event bus endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import structlog

from app.core.database import get_db
from app.core.event_bus import get_event_bus, EventType, EventPriority
from app.models.events import EventCreate, EventResponse, EventHistory

logger = structlog.get_logger()
router = APIRouter()


@router.post("/publish", response_model=Dict[str, str])
async def publish_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    """Publish an event to the event bus"""
    try:
        event_bus = await get_event_bus()
        
        event_id = await event_bus.publish(
            event_type=EventType(event.event_type),
            data=event.data,
            priority=EventPriority(event.priority) if event.priority else EventPriority.NORMAL,
            source=event.source,
            target=event.target
        )
        
        return {"event_id": event_id, "status": "published"}
        
    except Exception as e:
        logger.error("Failed to publish event", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish event"
        )


@router.get("/history", response_model=List[EventHistory])
async def get_event_history(
    event_type: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get event history from the event bus"""
    try:
        event_bus = await get_event_bus()
        
        # Convert event_type string to EventType enum if provided
        event_type_enum = None
        if event_type:
            try:
                event_type_enum = EventType(event_type)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid event type: {event_type}"
                )
        
        events = await event_bus.get_event_history(
            event_type=event_type_enum,
            limit=limit
        )
        
        return events
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get event history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get event history"
        )


@router.get("/stream-info", response_model=Dict[str, Any])
async def get_stream_info(
    db: Session = Depends(get_db)
):
    """Get information about the event stream"""
    try:
        event_bus = await get_event_bus()
        info = await event_bus.get_stream_info()
        return info
        
    except Exception as e:
        logger.error("Failed to get stream info", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get stream info"
        )


@router.get("/types", response_model=List[str])
async def get_event_types():
    """Get all available event types"""
    return [event_type.value for event_type in EventType]


@router.get("/priorities", response_model=List[str])
async def get_event_priorities():
    """Get all available event priorities"""
    return [priority.value for priority in EventPriority] 