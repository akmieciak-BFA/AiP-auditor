from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # excel, pdf, txt, md, csv
    file_size = Column(BigInteger, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="uploaded_documents")


class DocumentProcessingResult(Base):
    __tablename__ = "document_processing_results"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    extracted_data = Column(JSON, nullable=True)
    confidence_scores = Column(JSON, nullable=True)
    missing_fields = Column(JSON, nullable=True)
    processing_summary = Column(JSON, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    processing_time_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="document_processing_results")
