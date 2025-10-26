from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..models.step2 import Step2Process
from ..models.step3 import Step3Data
from ..schemas.step3 import Step3DataInput, Step3AnalysisResult
from ..services.claude_service import ClaudeService
from ..utils.auth import get_current_user
from ..middleware.rate_limit import ai_analysis_rate_limit

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects/{project_id}/step3", tags=["step3"])


@router.post("/analyze")
def analyze_step3(
    project_id: int,
    data: Step3DataInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _rate_limit: bool = Depends(ai_analysis_rate_limit)
):
    """Analyze Step 3 - research technologies and create budget scenarios."""
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
    
    # Get all Step 2 processes
    processes = db.query(Step2Process).filter(
        Step2Process.project_id == project_id
    ).all()
    
    if not processes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No processes found from Step 2"
        )
    
    # Aggregate Step 2 results
    step2_results = {
        "processes": [
            {
                "process_name": p.process_name,
                "process_data": p.process_data,
                "analysis_results": p.analysis_results
            }
            for p in processes if p.analysis_results
        ]
    }
    
    if not step2_results["processes"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No analyzed processes found from Step 2"
        )
    
    # Prepare preferences
    preferences = {
        "budget_level": data.budget_level,
        "tech_preferences": data.tech_preferences or {}
    }
    
    # Call Claude API for each process
    claude_service = ClaudeService()
    all_scenarios = []
    
    try:
        for process_data in step2_results["processes"]:
            process_scenarios = claude_service.analyze_step3(process_data, preferences)
            all_scenarios.append({
                "process_name": process_data["process_name"],
                "scenarios": process_scenarios
            })
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    
    # Aggregate results
    analysis_results = {
        "process_scenarios": all_scenarios,
        "budget_level": data.budget_level
    }
    
    # Save to database
    step3_data = db.query(Step3Data).filter(Step3Data.project_id == project_id).first()
    
    if step3_data:
        step3_data.budget_preferences = {"budget_level": data.budget_level}
        step3_data.tech_preferences = data.tech_preferences or {}
        step3_data.analysis_results = analysis_results
    else:
        step3_data = Step3Data(
            project_id=project_id,
            budget_preferences={"budget_level": data.budget_level},
            tech_preferences=data.tech_preferences or {},
            analysis_results=analysis_results
        )
        db.add(step3_data)
    
    # Update project status
    project.status = "step3"
    
    db.commit()
    db.refresh(step3_data)
    
    return analysis_results


@router.get("/results")
def get_step3_results(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get Step 3 analysis results."""
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
    
    step3_data = db.query(Step3Data).filter(Step3Data.project_id == project_id).first()
    
    if not step3_data or not step3_data.analysis_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step 3 analysis not found"
        )
    
    return step3_data.analysis_results
