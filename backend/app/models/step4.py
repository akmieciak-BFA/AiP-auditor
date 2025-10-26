from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Step4Output(Base):
    __tablename__ = "step4_outputs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    output_type = Column(String, nullable=False)  # presentation, report, summary
    gamma_url = Column(String, nullable=True)  # Dla prezentacji
    file_path = Column(String, nullable=True)  # Dla PDF/DOCX
    settings = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="step4_outputs")
