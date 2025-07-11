"""
Issue endpoints for the Agentic Agile System API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import structlog

from app.core.database import get_db
from app.models.issue import (
    Issue, IssueCreate, IssueUpdate, IssueResponse, StoryGeneration,
    IssueType, IssueStatus, IssuePriority
)

logger = structlog.get_logger()
router = APIRouter()


@router.post("/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
    issue: IssueCreate,
    db: Session = Depends(get_db)
):
    """Create a new issue"""
    try:
        db_issue = Issue(
            id=str(uuid.uuid4()),
            external_id=issue.external_id,
            title=issue.title,
            description=issue.description,
            issue_type=issue.issue_type,
            priority=issue.priority,
            labels=issue.labels,
            metadata=issue.metadata,
            created_by=issue.created_by
        )
        
        db.add(db_issue)
        db.commit()
        db.refresh(db_issue)
        
        return db_issue
        
    except Exception as e:
        logger.error("Failed to create issue", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create issue"
        )


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
    issue_id: str,
    db: Session = Depends(get_db)
):
    """Get issue by ID"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    return issue


@router.get("/", response_model=List[IssueResponse])
async def list_issues(
    issue_type: Optional[IssueType] = None,
    status: Optional[IssueStatus] = None,
    priority: Optional[IssuePriority] = None,
    assignee_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List issues with filtering and pagination"""
    query = db.query(Issue)
    
    if issue_type:
        query = query.filter(Issue.issue_type == issue_type)
    
    if status:
        query = query.filter(Issue.status == status)
    
    if priority:
        query = query.filter(Issue.priority == priority)
    
    if assignee_id:
        query = query.filter(Issue.assignee_id == assignee_id)
    
    issues = query.offset(offset).limit(limit).all()
    return issues


@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: str,
    issue_update: IssueUpdate,
    db: Session = Depends(get_db)
):
    """Update issue"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Update fields
    update_data = issue_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(issue, field, value)
    
    db.commit()
    db.refresh(issue)
    
    return issue


@router.post("/generate-stories")
async def generate_stories(
    story_request: StoryGeneration,
    db: Session = Depends(get_db)
):
    """Generate user stories from feature description"""
    try:
        # In a real implementation, this would use AI to generate stories
        # For now, we'll create a simple story structure
        
        story = Issue(
            id=str(uuid.uuid4()),
            title=f"Story: {story_request.feature_description[:50]}...",
            description=f"As a user, I want {story_request.feature_description}",
            issue_type=IssueType.STORY,
            priority=story_request.priority,
            labels=["auto-generated", "story"],
            metadata={
                "epic_id": story_request.epic_id,
                "acceptance_criteria": story_request.acceptance_criteria,
                "story_points": story_request.story_points,
                "generated_by": "PO_Agent"
            },
            created_by="PO_Agent"
        )
        
        db.add(story)
        db.commit()
        db.refresh(story)
        
        return {
            "message": "Story generated successfully",
            "story": story,
            "generated_by": "PO_Agent"
        }
        
    except Exception as e:
        logger.error("Failed to generate story", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate story"
        )


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(
    issue_id: str,
    db: Session = Depends(get_db)
):
    """Delete issue"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    db.delete(issue)
    db.commit()
    
    return None 