"""Download endpoints for audit reports."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
import logging
from ..database import get_db
from ..models.project import Project
from ..models.step1 import Step1Data
from ..models.step2 import Step2Process
from ..utils.markdown_formatter import MarkdownFormatter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects/{project_id}/download", tags=["downloads"])


@router.get("/markdown")
def download_markdown_report(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Download complete audit report as Markdown file.
    
    Returns:
        Markdown file with complete audit report
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    logger.info(f"Generating Markdown report for project {project_id}")
    
    # Get Step 1 data
    step1_record = db.query(Step1Data).filter(Step1Data.project_id == project_id).first()
    step1_data = step1_record.analysis_results if step1_record else None
    organization_data = step1_record.organization_data if step1_record else None
    
    # Get Step 2 data (all processes)
    step2_processes = db.query(Step2Process).filter(Step2Process.project_id == project_id).all()
    step2_data = {}
    for proc in step2_processes:
        if proc.analysis_results:
            step2_data[proc.process_name] = proc.analysis_results
    
    # Get Step 3 data (would come from step3 table - placeholder)
    # TODO: Implement when Step 3 model is ready
    step3_data = None
    
    # Get Step 4 data (would come from step4 table - placeholder)
    step4_data = None
    
    # Check if we have any data
    if not step1_data and not step2_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No audit data available for this project"
        )
    
    try:
        # Generate Markdown
        markdown_content = MarkdownFormatter.format_complete_audit(
            project_name=project.name,
            client_name=project.client_name,
            step1_data=step1_data,
            step2_data=step2_data if step2_data else None,
            step3_data=step3_data,
            step4_data=step4_data,
            organization_data=organization_data
        )
        
        # Create filename
        safe_project_name = project.name.replace(" ", "_").replace("/", "_")
        safe_client_name = project.client_name.replace(" ", "_").replace("/", "_")
        filename = f"Audyt_BFA_{safe_client_name}_{safe_project_name}.md"
        
        logger.info(f"Generated Markdown report: {len(markdown_content)} characters")
        
        # Return as downloadable file
        return Response(
            content=markdown_content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to generate Markdown report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


@router.get("/preview")
def preview_markdown_report(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Preview Markdown report content (for debugging/testing).
    
    Returns:
        JSON with markdown content and metadata
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all data
    step1_record = db.query(Step1Data).filter(Step1Data.project_id == project_id).first()
    step1_data = step1_record.analysis_results if step1_record else None
    organization_data = step1_record.organization_data if step1_record else None
    
    step2_processes = db.query(Step2Process).filter(Step2Process.project_id == project_id).all()
    step2_data = {}
    for proc in step2_processes:
        if proc.analysis_results:
            step2_data[proc.process_name] = proc.analysis_results
    
    if not step1_data and not step2_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No audit data available for this project"
        )
    
    try:
        # Generate Markdown
        markdown_content = MarkdownFormatter.format_complete_audit(
            project_name=project.name,
            client_name=project.client_name,
            step1_data=step1_data,
            step2_data=step2_data if step2_data else None,
            step3_data=None,
            step4_data=None,
            organization_data=organization_data
        )
        
        # Calculate statistics
        word_count = len(markdown_content.split())
        char_count = len(markdown_content)
        line_count = len(markdown_content.split("\n"))
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "client_name": project.client_name,
            "markdown_content": markdown_content,
            "statistics": {
                "word_count": word_count,
                "character_count": char_count,
                "line_count": line_count,
                "estimated_slides": max(10, int(word_count / 220))
            },
            "has_step1": step1_data is not None,
            "has_step2": len(step2_data) > 0 if step2_data else False,
            "step2_process_count": len(step2_data) if step2_data else 0
        }
        
    except Exception as e:
        logger.error(f"Failed to preview Markdown report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate preview: {str(e)}"
        )
