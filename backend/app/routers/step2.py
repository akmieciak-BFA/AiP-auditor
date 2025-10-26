from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from ..database import get_db
from ..models.project import Project
from ..models.step2 import Step2Process
from ..schemas.step2 import Step2ProcessData, Step2AnalysisResult
from ..services.claude_service import ClaudeService
from ..middleware.rate_limit import ai_analysis_rate_limit
from ..middleware.security import sanitize_dict, validate_input

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects/{project_id}/step2", tags=["step2"])


@router.post("/processes")
def add_process(
    project_id: int,
    process_name: str,
    db: Session = Depends(get_db)
):
    """Add a new process to analyze in Step 2."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create new process entry
    new_process = Step2Process(
        project_id=project_id,
        process_name=process_name,
        process_data={},
        analysis_results={}
    )
    
    db.add(new_process)
    db.commit()
    db.refresh(new_process)
    
    return {"id": new_process.id, "process_name": new_process.process_name}


@router.put("/processes/{process_id}")
def update_process(
    project_id: int,
    process_id: int,
    data: Step2ProcessData,
    db: Session = Depends(get_db)
):
    """Update process data."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get process
    process = db.query(Step2Process).filter(
        Step2Process.id == process_id,
        Step2Process.project_id == project_id
    ).first()
    
    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found"
        )
    
    # Validate process data
    from ..utils.validators import validate_process_steps, validate_costs
    
    process_dict = data.dict()
    
    # Validate steps
    if 'as_is' in process_dict and 'steps' in process_dict['as_is']:
        validate_process_steps(process_dict['as_is']['steps'])
    
    # Validate costs
    if 'costs' in process_dict:
        validate_costs(process_dict['costs'])
    
    # Sanitize and update process data
    clean_data = sanitize_dict(process_dict)
    process.process_data = clean_data
    
    db.commit()
    db.refresh(process)
    
    logger.info(f"Process {process_id} data updated for project {project_id}")
    return {"message": "Process data updated successfully", "process_id": process_id}


@router.post("/processes/{process_id}/analyze", response_model=Step2AnalysisResult)
def analyze_process(
    project_id: int,
    process_id: int,
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(ai_analysis_rate_limit)
):
    """Analyze a process using Claude API."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get process
    process = db.query(Step2Process).filter(
        Step2Process.id == process_id,
        Step2Process.project_id == project_id
    ).first()
    
    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found"
        )
    
    if not process.process_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Process data not provided"
        )
    
    # Call Claude API
    claude_service = ClaudeService()
    try:
        analysis_results = claude_service.analyze_step2(process.process_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    
    # Save results
    process.analysis_results = analysis_results
    db.commit()
    db.refresh(process)
    
    # Update project status
    project.status = "step2"
    db.commit()
    
    return Step2AnalysisResult(**analysis_results)


@router.get("/results")
def get_step2_results(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get all Step 2 process results."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    processes = db.query(Step2Process).filter(
        Step2Process.project_id == project_id
    ).all()
    
    return {
        "processes": [
            {
                "id": p.id,
                "process_name": p.process_name,
                "process_data": p.process_data,
                "analysis_results": p.analysis_results
            }
            for p in processes
        ]
    }
