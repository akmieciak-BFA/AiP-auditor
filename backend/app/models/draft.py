from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base


def get_utc_now():
    """Get current UTC time for database defaults."""
    return datetime.now(timezone.utc)


class ProjectDraft(Base):
    """Store draft data for projects to enable auto-save."""
    __tablename__ = "project_drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    step = Column(String, nullable=False, index=True)  # step1, step2, step3, step4
    draft_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=get_utc_now, index=True)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    # Relationships
    project = relationship("Project", back_populates="drafts")
