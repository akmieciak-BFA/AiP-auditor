from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..models.draft import ProjectDraft
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/projects/{project_id}/drafts", tags=["drafts"])


@router.post("/save")
def save_draft(
    project_id: int,
    step: str,
    draft_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save draft data for a project step (auto-save)."""
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if draft exists
    draft = db.query(ProjectDraft).filter(
        ProjectDraft.project_id == project_id,
        ProjectDraft.step == step
    ).first()
    
    if draft:
        # Update existing draft
        draft.draft_data = draft_data
        draft.updated_at = datetime.utcnow()
    else:
        # Create new draft
        draft = ProjectDraft(
            project_id=project_id,
            step=step,
            draft_data=draft_data
        )
        db.add(draft)
    
    db.commit()
    db.refresh(draft)
    
    return {
        "success": True,
        "message": "Draft saved successfully",
        "draft_id": draft.id,
        "updated_at": draft.updated_at
    }


@router.get("/load")
def load_draft(
    project_id: int,
    step: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Load draft data for a project step."""
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get draft
    draft = db.query(ProjectDraft).filter(
        ProjectDraft.project_id == project_id,
        ProjectDraft.step == step
    ).first()
    
    if not draft:
        return {
            "success": True,
            "has_draft": False,
            "draft_data": None
        }
    
    return {
        "success": True,
        "has_draft": True,
        "draft_data": draft.draft_data,
        "updated_at": draft.updated_at
    }


@router.delete("/clear")
def clear_draft(
    project_id: int,
    step: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clear draft data for a project step."""
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Delete draft
    draft = db.query(ProjectDraft).filter(
        ProjectDraft.project_id == project_id,
        ProjectDraft.step == step
    ).first()
    
    if draft:
        db.delete(draft)
        db.commit()
    
    return {
        "success": True,
        "message": "Draft cleared successfully"
    }


@router.get("/all")
def get_all_drafts(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all drafts for a project."""
    # Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all drafts
    drafts = db.query(ProjectDraft).filter(
        ProjectDraft.project_id == project_id
    ).all()
    
    return {
        "success": True,
        "drafts": [
            {
                "step": d.step,
                "has_data": bool(d.draft_data),
                "updated_at": d.updated_at
            }
            for d in drafts
        ]
    }
