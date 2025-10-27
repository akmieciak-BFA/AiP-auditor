from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Index, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from ..database import Base


def get_utc_now():
    """Get current UTC time for database defaults."""
    return datetime.now(timezone.utc)


class ProjectStatus(str, enum.Enum):
    step1 = "step1"
    step2 = "step2"
    step3 = "step3"
    step4 = "step4"
    completed = "completed"


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    client_name = Column(String(100), nullable=False, index=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.step1, index=True)
    created_at = Column(DateTime, default=get_utc_now, index=True)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now, index=True)
    
    # Add constraints
    __table_args__ = (
        CheckConstraint("length(name) >= 3", name="check_name_length"),
        CheckConstraint("length(client_name) >= 3", name="check_client_name_length"),
        Index("idx_project_name_client", "name", "client_name"),
        Index("idx_project_status_updated", "status", "updated_at"),
    )
    
    # Relationships (removed user relationship - internal app without authentication)
    step1_data = relationship("Step1Data", back_populates="project", uselist=False, cascade="all, delete-orphan")
    step2_processes = relationship("Step2Process", back_populates="project", cascade="all, delete-orphan")
    step3_data = relationship("Step3Data", back_populates="project", uselist=False, cascade="all, delete-orphan")
    step4_outputs = relationship("Step4Output", back_populates="project", cascade="all, delete-orphan")
    drafts = relationship("ProjectDraft", back_populates="project", cascade="all, delete-orphan")
    uploaded_documents = relationship("UploadedDocument", back_populates="project", cascade="all, delete-orphan")
    document_processing_results = relationship("DocumentProcessingResult", back_populates="project", cascade="all, delete-orphan")
