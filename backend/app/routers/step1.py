from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging
from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..models.step1 import Step1Data
from ..schemas.step1 import Step1DataInput, Step1AnalysisResult, OrganizationData
from ..services.claude_service import ClaudeService
from ..utils.auth import get_current_user
from ..utils.validators import validate_processes_list, validate_questionnaire_answers
from ..middleware.rate_limit import form_generation_rate_limit, ai_analysis_rate_limit
from ..middleware.security import sanitize_dict, validate_input

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects/{project_id}/step1", tags=["step1"])


@router.post("/generate-form")
def generate_step1_form(
    project_id: int,
    org_data: OrganizationData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _rate_limit: bool = Depends(form_generation_rate_limit)
) -> Dict[str, Any]:
    """Generate dynamic questionnaire form based on organization data."""
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
    
    # Validate and sanitize organization data
    clean_data = sanitize_dict(org_data.dict())
    validate_input(clean_data.get('company_name', ''), 'Nazwa firmy', 100)
    validate_input(clean_data.get('industry', ''), 'Branża', 100)
    
    # Call Claude API to generate form
    claude_service = ClaudeService()
    try:
        form_data = claude_service.generate_step1_form(clean_data)
        return form_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Form generation failed: {str(e)}"
        )


@router.post("/analyze", response_model=Step1AnalysisResult)
def analyze_step1(
    project_id: int,
    data: Step1DataInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _rate_limit: bool = Depends(ai_analysis_rate_limit)
):
    """Analyze Step 1 data using Claude API."""
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
    
    # Validate inputs
    clean_processes = validate_processes_list(data.processes_list)
    validate_questionnaire_answers(data.questionnaire_answers)
    
    # Sanitize data
    clean_org_data = sanitize_dict(data.organization_data.dict())
    clean_answers = sanitize_dict(data.questionnaire_answers)
    
    # Call Claude API
    claude_service = ClaudeService()
    try:
        logger.info(f"Analyzing Step 1 for project {project_id}")
        analysis_results = claude_service.analyze_step1({
            "organization_data": clean_org_data,
            "questionnaire_answers": clean_answers,
            "processes_list": clean_processes
        })
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    
    # Save to database
    step1_data = db.query(Step1Data).filter(Step1Data.project_id == project_id).first()
    
    if step1_data:
        step1_data.organization_data = data.organization_data.dict()
        step1_data.questionnaire_answers = data.questionnaire_answers
        step1_data.processes_list = data.processes_list
        step1_data.analysis_results = analysis_results
    else:
        step1_data = Step1Data(
            project_id=project_id,
            organization_data=data.organization_data.dict(),
            questionnaire_answers=data.questionnaire_answers,
            processes_list=data.processes_list,
            analysis_results=analysis_results
        )
        db.add(step1_data)
    
    # Update project status
    project.status = "step2"
    
    db.commit()
    db.refresh(step1_data)
    
    return Step1AnalysisResult(**analysis_results)


@router.get("/results", response_model=Step1AnalysisResult)
def get_step1_results(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get Step 1 analysis results."""
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
    
    step1_data = db.query(Step1Data).filter(Step1Data.project_id == project_id).first()
    
    if not step1_data or not step1_data.analysis_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step 1 analysis not found"
        )
    
    return Step1AnalysisResult(**step1_data.analysis_results)
