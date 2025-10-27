from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.project import Project
from ..schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectSchema])
def get_projects(db: Session = Depends(get_db)):
    """Get all projects."""
    projects = db.query(Project).all()
    return projects


@router.post("/", response_model=ProjectSchema)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project."""
    new_project = Project(
        name=project_data.name,
        client_name=project_data.client_name,
        status="step1"
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update fields
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.client_name is not None:
        project.client_name = project_data.client_name
    if project_data.status is not None:
        project.status = project_data.status
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}
