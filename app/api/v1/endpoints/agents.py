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
from app.core.logging import log_agent_action

logger = structlog.get_logger()
router = APIRouter()


@router.post("/register", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def register_agent(
    registration: AgentRegistration,
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
):
    """Get agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    agent_type: Optional[str] = None,
    status: Optional[AgentStatus] = None,
    db: Session = Depends(get_db)
):
    """List all agents with optional filtering"""
    query = db.query(Agent)
    
    if agent_type:
        query = query.filter(Agent.agent_type == agent_type)
    
    if status:
        query = query.filter(Agent.status == status)
    
    agents = query.all()
    return agents


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
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
    """Get agent status"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    return {
        "agent_id": agent.id,
        "name": agent.name,
        "status": agent.status,
        "last_heartbeat": agent.last_heartbeat,
        "current_task": agent.metadata.get("current_task"),
        "capabilities": agent.capabilities
    }


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db)
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
    
    log_agent_action(
        agent_id=agent_id,
        action="delete"
    )
    
    return None 