from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging
import time
import os
from pathlib import Path
from ..database import get_db
from ..models.project import Project
from ..models.document import UploadedDocument, DocumentProcessingResult
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
ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.pdf', '.txt', '.md', '.csv'}


@router.post("/upload")
async def upload_documents(
    project_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(ai_analysis_rate_limit)
):
    """Upload and process documents for Step 1 data extraction"""
    
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
            detail=f"Too many files. Maximum {MAX_FILES} files allowed."
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
    
    try:
        for file in files:
            # Validate file
            if file.size and file.size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} is too large. Maximum {MAX_FILE_SIZE / 1024 / 1024}MB per file."
                )
            
            ext = Path(file.filename).suffix.lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
                )
            
            # Save file
            project_dir = UPLOAD_DIR / f"project_{project_id}"
            project_dir.mkdir(exist_ok=True)
            
            file_path = project_dir / file.filename
            content = await file.read()
            
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Save to database
            uploaded_doc = UploadedDocument(
                project_id=project_id,
                filename=file.filename,
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
        
        # Extract data using Claude
        logger.info(f"Starting Claude data extraction for project {project_id} with {len(parsed_documents)} documents")
        start_time = time.time()
        
        claude_service = ClaudeService()
        extraction_result = claude_service.extract_data_from_documents(parsed_documents)
        
        processing_time = int(time.time() - start_time)
        
        # Save processing results
        processing_result = DocumentProcessingResult(
            project_id=project_id,
            extracted_data=extraction_result.get('extracted_data'),
            confidence_scores=extraction_result.get('confidence_scores'),
            missing_fields=extraction_result.get('missing_fields'),
            processing_summary=extraction_result.get('processing_summary'),
            processing_time_seconds=processing_time
        )
        db.add(processing_result)
        db.commit()
        db.refresh(processing_result)
        
        logger.info(f"Document processing completed for project {project_id} in {processing_time}s")
        
        return {
            "project_id": project_id,
            "processing_result_id": processing_result.id,
            "files_uploaded": len(uploaded_docs),
            "extracted_data": extraction_result.get('extracted_data'),
            "confidence_scores": extraction_result.get('confidence_scores'),
            "missing_fields": extraction_result.get('missing_fields'),
            "processing_summary": extraction_result.get('processing_summary'),
            "processing_time_seconds": processing_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
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
