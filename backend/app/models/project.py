from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class ProjectStatus(str, enum.Enum):
    step1 = "step1"
    step2 = "step2"
    step3 = "step3"
    step4 = "step4"
    completed = "completed"


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.step1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (removed user relationship - internal app without authentication)
    step1_data = relationship("Step1Data", back_populates="project", uselist=False, cascade="all, delete-orphan")
    step2_processes = relationship("Step2Process", back_populates="project", cascade="all, delete-orphan")
    step3_data = relationship("Step3Data", back_populates="project", uselist=False, cascade="all, delete-orphan")
    step4_outputs = relationship("Step4Output", back_populates="project", cascade="all, delete-orphan")
    drafts = relationship("ProjectDraft", back_populates="project", cascade="all, delete-orphan")
    uploaded_documents = relationship("UploadedDocument", back_populates="project", cascade="all, delete-orphan")
    document_processing_results = relationship("DocumentProcessingResult", back_populates="project", cascade="all, delete-orphan")
