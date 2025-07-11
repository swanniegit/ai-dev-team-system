"""
Memory endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import structlog
from datetime import datetime

from app.core.database import get_db
from app.models.corporate_memory import (
    CorporateMemory, CorporateMemoryCreate, CorporateMemoryResponse,
    MemorySearch, MemoryUpdate, MemoryType
)

logger = structlog.get_logger()
router = APIRouter()


@router.post("/memory", response_model=CorporateMemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    memory: CorporateMemoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new corporate memory entry"""
    try:
        db_memory = CorporateMemory(
            id=str(uuid.uuid4()),
            memory_type=memory.memory_type,
            category=memory.category,
            title=memory.title,
            description=memory.description,
            context=memory.context,
            agent_id=memory.agent_id,
            user_id=memory.user_id,
            project_id=memory.project_id,
            tags=memory.tags,
            confidence_score=memory.confidence_score,
            metadata=memory.metadata
        )
        
        db.add(db_memory)
        db.commit()
        db.refresh(db_memory)
        
        logger.info("Corporate memory created", memory_id=db_memory.id, type=memory.memory_type)
        return db_memory
        
    except Exception as e:
        logger.error("Failed to create corporate memory", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create corporate memory"
        )


@router.get("/memory/{memory_id}", response_model=CorporateMemoryResponse)
async def get_memory(
    memory_id: str,
    db: Session = Depends(get_db)
):
    """Get corporate memory by ID"""
    memory = db.query(CorporateMemory).filter(CorporateMemory.id == memory_id).first()
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corporate memory not found"
        )
    
    # Update usage count and last accessed
    memory.usage_count += 1
    memory.last_accessed = datetime.utcnow()
    db.commit()
    
    return memory


@router.get("/memory", response_model=List[CorporateMemoryResponse])
async def list_memories(
    memory_type: Optional[MemoryType] = None,
    category: Optional[str] = None,
    agent_id: Optional[str] = None,
    project_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List corporate memories with filtering"""
    query = db.query(CorporateMemory).filter(CorporateMemory.is_active == True)
    
    if memory_type:
        query = query.filter(CorporateMemory.memory_type == memory_type)
    
    if category:
        query = query.filter(CorporateMemory.category == category)
    
    if agent_id:
        query = query.filter(CorporateMemory.agent_id == agent_id)
    
    if project_id:
        query = query.filter(CorporateMemory.project_id == project_id)
    
    memories = query.order_by(CorporateMemory.timestamp.desc()).offset(offset).limit(limit).all()
    return memories


@router.put("/memory/{memory_id}", response_model=CorporateMemoryResponse)
async def update_memory(
    memory_id: str,
    memory_update: MemoryUpdate,
    db: Session = Depends(get_db)
):
    """Update corporate memory"""
    memory = db.query(CorporateMemory).filter(CorporateMemory.id == memory_id).first()
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corporate memory not found"
        )
    
    # Update fields if provided
    if memory_update.title is not None:
        memory.title = memory_update.title
    if memory_update.description is not None:
        memory.description = memory_update.description
    if memory_update.context is not None:
        memory.context = memory_update.context
    if memory_update.tags is not None:
        memory.tags = memory_update.tags
    if memory_update.confidence_score is not None:
        memory.confidence_score = memory_update.confidence_score
    if memory_update.is_active is not None:
        memory.is_active = memory_update.is_active
    if memory_update.metadata is not None:
        memory.metadata = memory_update.metadata
    
    db.commit()
    db.refresh(memory)
    
    logger.info("Corporate memory updated", memory_id=memory_id)
    return memory


@router.delete("/memory/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: str,
    db: Session = Depends(get_db)
):
    """Delete corporate memory (soft delete)"""
    memory = db.query(CorporateMemory).filter(CorporateMemory.id == memory_id).first()
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corporate memory not found"
        )
    
    # Soft delete by setting is_active to False
    memory.is_active = False
    db.commit()
    
    logger.info("Corporate memory deleted", memory_id=memory_id)


@router.post("/memory/search", response_model=List[CorporateMemoryResponse])
async def search_memories(
    search: MemorySearch,
    db: Session = Depends(get_db)
):
    """Search corporate memories with advanced filtering"""
    query = db.query(CorporateMemory).filter(CorporateMemory.is_active == True)
    
    # Apply filters
    if search.memory_types:
        query = query.filter(CorporateMemory.memory_type.in_(search.memory_types))
    
    if search.categories:
        query = query.filter(CorporateMemory.category.in_(search.categories))
    
    if search.tags:
        # Search for memories that contain any of the specified tags
        for tag in search.tags:
            query = query.filter(CorporateMemory.tags.contains([tag]))
    
    if search.agent_id:
        query = query.filter(CorporateMemory.agent_id == search.agent_id)
    
    if search.project_id:
        query = query.filter(CorporateMemory.project_id == search.project_id)
    
    if search.min_confidence:
        query = query.filter(CorporateMemory.confidence_score >= search.min_confidence)
    
    # Full-text search on title and description
    if search.query:
        search_term = f"%{search.query}%"
        query = query.filter(
            (CorporateMemory.title.ilike(search_term)) |
            (CorporateMemory.description.ilike(search_term))
        )
    
    memories = query.order_by(CorporateMemory.confidence_score.desc(), 
                             CorporateMemory.usage_count.desc()).offset(search.offset).limit(search.limit).all()
    
    return memories


@router.get("/memory/stats")
async def get_memory_stats(
    db: Session = Depends(get_db)
):
    """Get corporate memory statistics"""
    total_memories = db.query(CorporateMemory).filter(CorporateMemory.is_active == True).count()
    
    # Count by memory type
    type_counts = {}
    for memory_type in MemoryType:
        count = db.query(CorporateMemory).filter(
            CorporateMemory.memory_type == memory_type,
            CorporateMemory.is_active == True
        ).count()
        type_counts[memory_type.value] = count
    
    # Most used memories
    most_used = db.query(CorporateMemory).filter(
        CorporateMemory.is_active == True
    ).order_by(CorporateMemory.usage_count.desc()).limit(5).all()
    
    return {
        "total_memories": total_memories,
        "memory_types": type_counts,
        "most_used": [
            {
                "id": memory.id,
                "title": memory.title,
                "usage_count": memory.usage_count,
                "memory_type": memory.memory_type
            }
            for memory in most_used
        ]
    } 