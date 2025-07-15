"""
Agent endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import structlog

from app.core.database import get_db
from app.models.agent import (
    Agent, AgentCreate, AgentUpdate, AgentResponse, AgentTrigger,
    AgentHeartbeat, AgentRegistration, AgentStatus, AgentCapability
)
from app.models.user import User
from app.core.logging import log_agent_action
from app.core.cache import get_cache_manager, invalidate_agent_cache
from app.core.authorization import (
    Permission, check_user_permission, require_authenticated_user,
    require_manager_or_admin, log_access_attempt
)
from app.core.security import get_current_active_user

logger = structlog.get_logger()
router = APIRouter()


@router.post("/register", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def register_agent(
    registration: AgentRegistration,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_permission(Permission.AGENT_REGISTER))
):
    """Register a new agent"""
    try:
        # Create agent
        agent = Agent(
            id=str(uuid.uuid4()),
            name=registration.name,
            agent_type=registration.agent_type,
            capabilities=registration.capabilities,
            metadata=registration.metadata,
            status=AgentStatus.ACTIVE
        )
        
        db.add(agent)
        db.commit()
        db.refresh(agent)
        
        log_agent_action(
            agent_id=agent.id,
            action="register",
            agent_type=registration.agent_type,
            capabilities=registration.capabilities
        )
        
        return agent
        
    except Exception as e:
        logger.error("Failed to register agent", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register agent"
        )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_permission(Permission.AGENT_READ))
):
    """Get agent by ID with caching"""
    # Log access attempt
    log_access_attempt(current_user, "agent", agent_id, "read")
    
    # Try cache first
    cache = await get_cache_manager()
    cache_key = f"agent:{agent_id}"
    
    cached_agent = await cache.get(cache_key)
    if cached_agent:
        return AgentResponse(**cached_agent)
    
    # Get from database
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Cache the result
    agent_dict = {
        "id": agent.id,
        "name": agent.name,
        "agent_type": agent.agent_type,
        "status": agent.status,
        "capabilities": agent.capabilities,
        "metadata": agent.agent_metadata,
        "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
        "created_at": agent.created_at.isoformat(),
        "updated_at": agent.updated_at.isoformat(),
        "is_active": agent.is_active
    }
    await cache.set(cache_key, agent_dict, ttl=300, tags=[f"agent:{agent_id}"])
    
    return agent


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    agent_type: Optional[str] = None,
    status: Optional[AgentStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_permission(Permission.AGENT_LIST))
):
    """List all agents with optional filtering and caching"""
    # Generate cache key based on filters
    cache = await get_cache_manager()
    cache_key_parts = ["agents_list"]
    if agent_type:
        cache_key_parts.append(f"type_{agent_type}")
    if status:
        cache_key_parts.append(f"status_{status}")
    cache_key = ":".join(cache_key_parts)
    
    # Try cache first
    cached_agents = await cache.get(cache_key)
    if cached_agents:
        return [AgentResponse(**agent) for agent in cached_agents]
    
    # Get from database
    query = db.query(Agent)
    
    if agent_type:
        query = query.filter(Agent.agent_type == agent_type)
    
    if status:
        query = query.filter(Agent.status == status)
    
    agents = query.all()
    
    # Cache the result
    agents_dict = [{
        "id": agent.id,
        "name": agent.name,
        "agent_type": agent.agent_type,
        "status": agent.status,
        "capabilities": agent.capabilities,
        "metadata": agent.agent_metadata,
        "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
        "created_at": agent.created_at.isoformat(),
        "updated_at": agent.updated_at.isoformat(),
        "is_active": agent.is_active
    } for agent in agents]
    
    await cache.set(cache_key, agents_dict, ttl=180, tags=["agents_list"])
    
    return agents


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_permission(Permission.AGENT_UPDATE))
):
    """Update agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Update fields
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    
    # Invalidate cache
    await invalidate_agent_cache(agent_id)
    cache = await get_cache_manager()
    await cache.delete_by_tag("agents_list")
    
    log_agent_action(
        agent_id=agent_id,
        action="update",
        updated_fields=list(update_data.keys())
    )
    
    return agent


@router.post("/{agent_id}/trigger")
async def trigger_agent(
    agent_id: str,
    trigger: AgentTrigger,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_permission(Permission.AGENT_TRIGGER))
):
    """Trigger an agent action"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    if agent.status == AgentStatus.OFFLINE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agent is offline"
        )
    
    # In a real implementation, this would send the action to the agent
    # For now, we'll just log it and return a success response
    
    log_agent_action(
        agent_id=agent_id,
        action="trigger",
        triggered_action=trigger.action,
        parameters=trigger.parameters,
        priority=trigger.priority
    )
    
    return {
        "message": "Agent action triggered successfully",
        "agent_id": agent_id,
        "action": trigger.action,
        "status": "queued"
    }


@router.post("/{agent_id}/heartbeat")
async def agent_heartbeat(
    agent_id: str,
    heartbeat: AgentHeartbeat,
    db: Session = Depends(get_db)
):
    """Update agent heartbeat"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Update agent status and heartbeat
    agent.status = heartbeat.status
    agent.last_heartbeat = heartbeat.timestamp if hasattr(heartbeat, 'timestamp') else None
    agent.metadata = {**agent.metadata, "current_task": heartbeat.current_task}
    
    db.commit()
    db.refresh(agent)
    
    log_agent_action(
        agent_id=agent_id,
        action="heartbeat",
        status=heartbeat.status,
        current_task=heartbeat.current_task
    )
    
    return {"message": "Heartbeat received", "agent_id": agent_id}


@router.get("/{agent_id}/status")
async def get_agent_status(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get agent status with short-term caching"""
    # Try cache first (short TTL for status)
    cache = await get_cache_manager()
    cache_key = f"agent_status:{agent_id}"
    
    cached_status = await cache.get(cache_key)
    if cached_status:
        return cached_status
    
    # Get from database
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    status_data = {
        "agent_id": agent.id,
        "name": agent.name,
        "status": agent.status,
        "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
        "current_task": agent.agent_metadata.get("current_task"),
        "capabilities": agent.capabilities
    }
    
    # Cache with short TTL since status changes frequently
    await cache.set(cache_key, status_data, ttl=30, tags=[f"agent:{agent_id}"])
    
    return status_data


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager_or_admin)
):
    """Delete agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    db.delete(agent)
    db.commit()
    
    # Invalidate all cache entries for this agent
    await invalidate_agent_cache(agent_id)
    cache = await get_cache_manager()
    await cache.delete_by_tag("agents_list")
    
    log_agent_action(
        agent_id=agent_id,
        action="delete"
    )
    
    return None 