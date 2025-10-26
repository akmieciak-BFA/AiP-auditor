from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Step2Process(Base):
    __tablename__ = "step2_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    process_name = Column(String, nullable=False)
    process_data = Column(JSON, nullable=True)  # Sekcje A-E
    analysis_results = Column(JSON, nullable=True)  # Wyniki Claude
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="step2_processes")
