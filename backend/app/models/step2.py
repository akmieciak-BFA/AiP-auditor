from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base


def get_utc_now():
    """Get current UTC time for database defaults."""
    return datetime.now(timezone.utc)


class Step2Process(Base):
    __tablename__ = "step2_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    process_name = Column(String, nullable=False)
    process_data = Column(JSON, nullable=True)  # Sekcje A-E
    analysis_results = Column(JSON, nullable=True)  # Wyniki Claude
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    # Relationships
    project = relationship("Project", back_populates="step2_processes")
