from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base


def get_utc_now():
    """Get current UTC time for database defaults."""
    return datetime.now(timezone.utc)


class Step3Data(Base):
    __tablename__ = "step3_data"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    budget_preferences = Column(JSON, nullable=True)
    tech_preferences = Column(JSON, nullable=True)
    analysis_results = Column(JSON, nullable=True)  # Scenariusze, vendorzy, ROI
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    # Relationships
    project = relationship("Project", back_populates="step3_data")
