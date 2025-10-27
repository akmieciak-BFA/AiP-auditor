#!/usr/bin/env python3
"""
Script to clean up test documents from the database.
"""
import sys
sys.path.insert(0, '/workspace/backend')

from app.database import SessionLocal
from app.models.document import UploadedDocument, DocumentProcessingResult
from app.models.step1 import Step1Data

def cleanup_project_documents(project_id: int = 1):
    """Clean up all documents and analysis data for a project."""
    db = SessionLocal()
    
    try:
        # Count before
        docs_count = db.query(UploadedDocument).filter(
            UploadedDocument.project_id == project_id
        ).count()
        
        results_count = db.query(DocumentProcessingResult).filter(
            DocumentProcessingResult.project_id == project_id
        ).count()
        
        step1_count = db.query(Step1Data).filter(
            Step1Data.project_id == project_id
        ).count()
        
        print(f"Project {project_id} before cleanup:")
        print(f"  - Uploaded documents: {docs_count}")
        print(f"  - Processing results: {results_count}")
        print(f"  - Step1 data: {step1_count}")
        
        # Delete all
        db.query(UploadedDocument).filter(
            UploadedDocument.project_id == project_id
        ).delete()
        
        db.query(DocumentProcessingResult).filter(
            DocumentProcessingResult.project_id == project_id
        ).delete()
        
        db.query(Step1Data).filter(
            Step1Data.project_id == project_id
        ).delete()
        
        db.commit()
        
        print(f"\n✅ Successfully cleaned up project {project_id}")
        print("All uploaded documents, processing results, and Step1 data have been removed.")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    project_id = 1
    if len(sys.argv) > 1:
        project_id = int(sys.argv[1])
    
    cleanup_project_documents(project_id)
