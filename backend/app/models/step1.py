from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base


def get_utc_now():
    """Get current UTC time for database defaults."""
    return datetime.now(timezone.utc)


class Step1Data(Base):
    __tablename__ = "step1_data"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    organization_data = Column(JSON, nullable=True)
    questionnaire_answers = Column(JSON, nullable=True)
    processes_list = Column(JSON, nullable=True)
    analysis_results = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=get_utc_now, index=True)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now, index=True)
    
    # Add constraints and indexes
    __table_args__ = (
        UniqueConstraint("project_id", name="uq_step1_project_id"),
        Index("idx_step1_project_updated", "project_id", "updated_at"),
    )
    
    # Relationships
    project = relationship("Project", back_populates="step1_data")
