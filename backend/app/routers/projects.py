from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from ..database import get_db, get_db_context
from ..models.project import Project
from ..schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate
from ..middleware.security import validate_project_name, sanitize_string
from ..middleware.rate_limit import rate_limit
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectSchema])
def get_projects(
    skip: int = Query(0, ge=0, description="Number of projects to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of projects to return"),
    sort_by: str = Query("updated_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get all projects with pagination and sorting."""
    try:
        # Validate sort field
        allowed_sort_fields = ["id", "name", "client_name", "status", "created_at", "updated_at"]
        if sort_by not in allowed_sort_fields:
            sort_by = "updated_at"
        
        # Apply sorting
        order_func = desc if sort_order == "desc" else asc
        query = db.query(Project).order_by(order_func(getattr(Project, sort_by)))
        
        # Apply pagination
        projects = query.offset(skip).limit(limit).all()
        
        logger.info(f"Retrieved {len(projects)} projects (skip={skip}, limit={limit})")
        return projects
    except Exception as e:
        logger.error(f"Error retrieving projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve projects"
        )


@router.post("/", response_model=ProjectSchema)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project."""
    try:
        # Validate and sanitize input
        if not validate_project_name(project_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid project name format"
            )
        
        # Check for duplicate project names
        existing_project = db.query(Project).filter(
            Project.name == project_data.name,
            Project.client_name == project_data.client_name
        ).first()
        
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project with this name and client already exists"
            )
        
        # Sanitize input
        sanitized_name = sanitize_string(project_data.name, max_length=100)
        sanitized_client = sanitize_string(project_data.client_name, max_length=100)
        
        new_project = Project(
            name=sanitized_name,
            client_name=sanitized_client,
            status="step1"
        )
        
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        
        logger.info(f"Created project: {new_project.id} - {new_project.name}")
        return new_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )


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
