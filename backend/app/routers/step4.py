from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
# User import removed (no auth)
from ..models.project import Project
from ..models.step1 import Step1Data
from ..models.step2 import Step2Process
from ..models.step3 import Step3Data
from ..models.step4 import Step4Output
from ..schemas.step4 import Step4GenerateRequest, Step4Output as Step4OutputSchema
from ..services.gamma_service import GammaService
from ..services.analysis_service import AnalysisService
# get_current_user removed (no auth)

router = APIRouter(prefix="/api/projects/{project_id}/step4", tags=["step4"])


@router.post("/generate-presentation")
def generate_presentation(
    project_id: int,
    request_data: Step4GenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate presentation using Gamma API."""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all data from previous steps
    analysis_service = AnalysisService()
    project_summary = analysis_service.get_project_summary(db, project_id)
    
    if not project_summary.get("step1_results"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Step 1 analysis not found"
        )
    
    if not project_summary.get("step2_results"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Step 2 processes not found"
        )
    
    if not project_summary.get("step3_results"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Step 3 analysis not found"
        )
    
    # Filter selected processes
    step2_results = [
        p for p in project_summary["step2_results"]
        if p["process_name"] in request_data.selected_processes
    ]
    
    if not step2_results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected processes not found"
        )
    
    # Generate presentation
    gamma_service = GammaService()
    try:
        gamma_url = gamma_service.generate_presentation(
            client_name=request_data.client_name,
            author_name=request_data.author_name,
            step1_results=project_summary["step1_results"],
            step2_results=step2_results,
            step3_results=project_summary["step3_results"],
            selected_processes=request_data.selected_processes,
            budget_scenario=request_data.budget_scenario
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Presentation generation failed: {str(e)}"
        )
    
    # Save output record
    output = Step4Output(
        project_id=project_id,
        output_type="presentation",
        gamma_url=gamma_url,
        settings=request_data.dict()
    )
    
    db.add(output)
    
    # Update project status
    project.status = "completed"
    
    db.commit()
    db.refresh(output)
    
    return {
        "id": output.id,
        "gamma_url": gamma_url,
        "message": "Presentation generated successfully"
    }


@router.get("/downloads", response_model=List[Step4OutputSchema])
def get_downloads(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get all generated outputs for a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    outputs = db.query(Step4Output).filter(
        Step4Output.project_id == project_id
    ).all()
    
    return outputs
