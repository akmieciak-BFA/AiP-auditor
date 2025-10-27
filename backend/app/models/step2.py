from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Index, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base


def get_utc_now():
    """Get current UTC time for database defaults."""
    return datetime.now(timezone.utc)


class Step2Process(Base):
    __tablename__ = "step2_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    process_name = Column(String(200), nullable=False, index=True)
    process_data = Column(JSON, nullable=True)  # Sekcje A-E
    analysis_results = Column(JSON, nullable=True)  # Wyniki Claude
    created_at = Column(DateTime, default=get_utc_now, index=True)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now, index=True)
    
    # Add constraints and indexes
    __table_args__ = (
        CheckConstraint("length(process_name) >= 3", name="check_process_name_length"),
        Index("idx_step2_project_name", "project_id", "process_name"),
        Index("idx_step2_project_updated", "project_id", "updated_at"),
    )
    
    # Relationships
    project = relationship("Project", back_populates="step2_processes")
