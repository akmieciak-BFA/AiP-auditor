from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Step3Data(Base):
    __tablename__ = "step3_data"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    budget_preferences = Column(JSON, nullable=True)
    tech_preferences = Column(JSON, nullable=True)
    analysis_results = Column(JSON, nullable=True)  # Scenariusze, vendorzy, ROI
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="step3_data")
