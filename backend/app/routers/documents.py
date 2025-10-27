from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging
import time
import os
import re
from datetime import datetime
from pathlib import Path
from ..database import get_db
from ..models.project import Project
from ..models.document import UploadedDocument, DocumentProcessingResult
from ..models.step1 import Step1Data
from ..services.claude_service import ClaudeService
from ..utils.file_parsers import parse_file
from ..middleware.rate_limit import ai_analysis_rate_limit

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects/{project_id}/documents", tags=["documents"])

# Configuration
UPLOAD_DIR = Path("./uploaded_documents")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_TOTAL_SIZE = 200 * 1024 * 1024  # 200MB
MAX_FILES = 10
MAX_FILES_PER_PROJECT = 100  # Increased limit per project
MAX_FILENAME_LENGTH = 255  # Maximum filename length
ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.pdf', '.txt', '.md', '.csv'}


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other security issues.
    """
    path = Path(filename)
    ext = path.suffix.lower()
    name = path.stem
    
    # Remove dangerous characters
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', name)
    safe_name = safe_name[:MAX_FILENAME_LENGTH - len(ext)]
    safe_name = safe_name.strip('. ')
    
    if not safe_name:
        safe_name = f"document_{int(time.time())}"
    
    return f"{safe_name}{ext}"


def cleanup_uploaded_files(file_paths: List[str]):
    """Clean up uploaded files in case of error"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to cleanup file {file_path}: {e}")


def create_step1_data_from_analysis(
    db: Session,
    project_id: int,
    analysis_result: Dict[str, Any]
) -> Step1Data:
    """
    Create or update Step1Data from document analysis.
    """
    existing = db.query(Step1Data).filter(
        Step1Data.project_id == project_id
    ).first()
    
    if existing:
        # Update existing
        existing.analysis_results = analysis_result
        existing.processes_list = analysis_result.get('processes_scoring', [])
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new
    step1_data = Step1Data(
        project_id=project_id,
        organization_data={},
        questionnaire_answers={},
        processes_list=analysis_result.get('processes_scoring', []),
        analysis_results=analysis_result
    )
    
    db.add(step1_data)
    db.commit()
    db.refresh(step1_data)
    return step1_data


@router.post("/upload")
async def upload_documents(
    project_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(ai_analysis_rate_limit)
):
    """Upload and process documents for Step 1 BFA analysis"""
    
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Validate files
    if len(files) > MAX_FILES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Too many files. Maximum {MAX_FILES} files allowed per upload."
        )
    
    # Check project document limit
    existing_docs_count = db.query(UploadedDocument).filter(
        UploadedDocument.project_id == project_id
    ).count()
    
    if existing_docs_count + len(files) > MAX_FILES_PER_PROJECT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project document limit exceeded. Maximum {MAX_FILES_PER_PROJECT} documents per project. Current: {existing_docs_count}"
        )
    
    total_size = sum(file.size or 0 for file in files)
    if total_size > MAX_TOTAL_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Total file size exceeds {MAX_TOTAL_SIZE / 1024 / 1024}MB"
        )
    
    # Process files
    uploaded_docs = []
    parsed_documents = []
    uploaded_file_paths = []
    
    try:
        for file in files:
            # Validate filename length
            if len(file.filename) > MAX_FILENAME_LENGTH:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Filename too long: {file.filename}. Maximum {MAX_FILENAME_LENGTH} characters."
                )
            
            # Validate file size
            if file.size and file.size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} is too large. Maximum {MAX_FILE_SIZE / 1024 / 1024}MB per file."
                )
            
            # Validate file type
            ext = Path(file.filename).suffix.lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
                )
            
            # Read content
            content = await file.read()
            
            # Validate empty file
            if len(content) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} is empty"
                )
            
            # Sanitize filename
            safe_filename = sanitize_filename(file.filename)
            
            # Save file
            project_dir = UPLOAD_DIR / f"project_{project_id}"
            project_dir.mkdir(exist_ok=True)
            
            # Ensure unique filename
            file_path = project_dir / safe_filename
            counter = 1
            original_stem = Path(safe_filename).stem
            original_ext = Path(safe_filename).suffix
            while file_path.exists():
                file_path = project_dir / f"{original_stem}_{counter}{original_ext}"
                counter += 1
            
            with open(file_path, 'wb') as f:
                f.write(content)
            
            uploaded_file_paths.append(str(file_path))
            
            # Save to database
            uploaded_doc = UploadedDocument(
                project_id=project_id,
                filename=file_path.name,
                file_path=str(file_path),
                file_type=ext.lstrip('.'),
                file_size=len(content)
            )
            db.add(uploaded_doc)
            uploaded_docs.append(uploaded_doc)
            
            # Parse file
            try:
                parsed_doc = parse_file(content, file.filename)
                parsed_documents.append(parsed_doc)
                logger.info(f"Parsed file: {file.filename}")
            except Exception as e:
                logger.error(f"Failed to parse {file.filename}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to parse {file.filename}: {str(e)}"
                )
        
        db.commit()
        
        # Step 3: Perform BFA analysis using Claude
        logger.info(f"Starting BFA analysis for project {project_id} with {len(parsed_documents)} documents")
        start_time = time.time()
        
        claude_service = ClaudeService()
        analysis_result = claude_service.extract_data_from_documents(parsed_documents)
        
        processing_time = int(time.time() - start_time)
        
        # Save processing results
        processing_result = DocumentProcessingResult(
            project_id=project_id,
            extracted_data=analysis_result,  # Full BFA analysis here
            confidence_scores=analysis_result.get('confidence_scores', {}),
            missing_fields=analysis_result.get('missing_information', []),
            processing_summary={
                'documents_processed': len(parsed_documents),
                'processing_time_seconds': processing_time,
                'key_findings': analysis_result.get('key_findings', []),
                'overall_confidence': analysis_result.get('confidence_scores', {}).get('overall', 0.0),
                'top_processes': analysis_result.get('top_processes', []),
                'digital_maturity_score': analysis_result.get('digital_maturity', {}).get('overall_score', 0)
            },
            processing_time_seconds=processing_time
        )
        db.add(processing_result)
        db.commit()
        db.refresh(processing_result)
        
        # Step 4: Create Step1Data from analysis
        step1_data = None
        try:
            step1_data = create_step1_data_from_analysis(
                db=db,
                project_id=project_id,
                analysis_result=analysis_result
            )
            logger.info(f"Successfully created Step1Data (id={step1_data.id}) for project {project_id}")
        except Exception as e:
            logger.error(f"Failed to create Step1Data: {e}")
            # Continue - DocumentProcessingResult is saved
        
        logger.info(f"Document processing completed for project {project_id} in {processing_time}s")
        
        return {
            "success": True,
            "project_id": project_id,
            "processing_result_id": processing_result.id,
            "step1_data_id": step1_data.id if step1_data else None,
            "files_uploaded": len(uploaded_docs),
            "files": [{"filename": doc.filename, "id": doc.id} for doc in uploaded_docs],
            "analysis_summary": {
                "top_processes": analysis_result.get('top_processes', []),
                "overall_confidence": analysis_result.get('confidence_scores', {}).get('overall', 0.0),
                "key_findings": analysis_result.get('key_findings', []),
                "missing_information": analysis_result.get('missing_information', [])
            },
            "digital_maturity": analysis_result.get('digital_maturity', {}),
            "processes_scoring": analysis_result.get('processes_scoring', []),
            "processing_time_seconds": processing_time
        }
        
    except HTTPException:
        cleanup_uploaded_files(uploaded_file_paths)
        db.rollback()
        raise
    except Exception as e:
        cleanup_uploaded_files(uploaded_file_paths)
        logger.error(f"Document upload/processing failed: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document processing failed: {str(e)}"
        )


@router.get("/processing-result/{result_id}")
def get_processing_result(
    project_id: int,
    result_id: int,
    db: Session = Depends(get_db)
):
    """Get document processing result"""
    
    result = db.query(DocumentProcessingResult).filter(
        DocumentProcessingResult.id == result_id,
        DocumentProcessingResult.project_id == project_id
    ).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Processing result not found"
        )
    
    return {
        "id": result.id,
        "project_id": result.project_id,
        "extracted_data": result.extracted_data,
        "confidence_scores": result.confidence_scores,
        "missing_fields": result.missing_fields,
        "processing_summary": result.processing_summary,
        "processing_time_seconds": result.processing_time_seconds,
        "created_at": result.created_at
    }


@router.get("/uploaded")
def get_uploaded_documents(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get list of uploaded documents for project"""
    
    documents = db.query(UploadedDocument).filter(
        UploadedDocument.project_id == project_id
    ).all()
    
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "file_size": doc.file_size,
            "uploaded_at": doc.uploaded_at
        }
        for doc in documents
    ]


@router.get("/latest-analysis")
def get_latest_analysis(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get latest document analysis result for project"""
    
    # Get latest processing result
    processing_result = db.query(DocumentProcessingResult).filter(
        DocumentProcessingResult.project_id == project_id
    ).order_by(DocumentProcessingResult.created_at.desc()).first()
    
    if not processing_result:
        return {
            "has_analysis": False,
            "step1_data_available": False
        }
    
    # Check if Step1Data exists
    step1_data = db.query(Step1Data).filter(
        Step1Data.project_id == project_id
    ).first()
    
    return {
        "has_analysis": True,
        "step1_data_available": step1_data is not None,
        "processing_result_id": processing_result.id,
        "step1_data_id": step1_data.id if step1_data else None,
        "extracted_data": processing_result.extracted_data,
        "confidence_scores": processing_result.confidence_scores,
        "missing_fields": processing_result.missing_fields,
        "processing_summary": processing_result.processing_summary,
        "created_at": processing_result.created_at
    }


@router.post("/reanalyze")
async def reanalyze_all_documents(
    project_id: int,
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(ai_analysis_rate_limit)
):
    """Re-analyze all uploaded documents for a project"""
    
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all uploaded documents
    documents = db.query(UploadedDocument).filter(
        UploadedDocument.project_id == project_id
    ).all()
    
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No documents found for this project"
        )
    
    # Parse all documents
    parsed_documents = []
    for doc in documents:
        try:
            with open(doc.file_path, 'rb') as f:
                content = f.read()
            parsed_doc = parse_file(content, doc.filename)
            parsed_documents.append(parsed_doc)
            logger.info(f"Re-parsed file: {doc.filename}")
        except Exception as e:
            logger.error(f"Failed to re-parse {doc.filename}: {e}")
            # Continue with other files
    
    if not parsed_documents:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse any documents"
        )
    
    # Perform BFA analysis
    logger.info(f"Re-analyzing {len(parsed_documents)} documents for project {project_id}")
    start_time = time.time()
    
    try:
        claude_service = ClaudeService()
        analysis_result = claude_service.extract_data_from_documents(parsed_documents)
        
        processing_time = int(time.time() - start_time)
        
        # Save new processing result
        processing_result = DocumentProcessingResult(
            project_id=project_id,
            extracted_data=analysis_result,
            confidence_scores=analysis_result.get('confidence_scores', {}),
            missing_fields=analysis_result.get('missing_information', []),
            processing_summary={
                'documents_processed': len(parsed_documents),
                'processing_time_seconds': processing_time,
                'key_findings': analysis_result.get('key_findings', []),
                'overall_confidence': analysis_result.get('confidence_scores', {}).get('overall', 0.0),
                'top_processes': analysis_result.get('top_processes', []),
                'digital_maturity_score': analysis_result.get('digital_maturity', {}).get('overall_score', 0)
            },
            processing_time_seconds=processing_time
        )
        db.add(processing_result)
        db.commit()
        db.refresh(processing_result)
        
        # Update Step1Data
        step1_data = create_step1_data_from_analysis(
            db=db,
            project_id=project_id,
            analysis_result=analysis_result
        )
        
        logger.info(f"Re-analysis completed for project {project_id} in {processing_time}s")
        
        return {
            "success": True,
            "project_id": project_id,
            "processing_result_id": processing_result.id,
            "step1_data_id": step1_data.id,
            "documents_analyzed": len(parsed_documents),
            "analysis_summary": {
                "top_processes": analysis_result.get('top_processes', []),
                "overall_confidence": analysis_result.get('confidence_scores', {}).get('overall', 0.0),
                "key_findings": analysis_result.get('key_findings', []),
                "missing_information": analysis_result.get('missing_information', [])
            },
            "digital_maturity": analysis_result.get('digital_maturity', {}),
            "processing_time_seconds": processing_time
        }
        
    except Exception as e:
        logger.error(f"Re-analysis failed: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Re-analysis failed: {str(e)}"
        )


@router.delete("/{document_id}")
def delete_document(
    project_id: int,
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete uploaded document"""
    
    document = db.query(UploadedDocument).filter(
        UploadedDocument.id == document_id,
        UploadedDocument.project_id == project_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file from filesystem
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        logger.error(f"Failed to delete file {document.file_path}: {e}")
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
