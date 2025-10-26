from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class ProjectDraft(Base):
    """Store draft data for projects to enable auto-save."""
    __tablename__ = "project_drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    step = Column(String, nullable=False, index=True)  # step1, step2, step3, step4
    draft_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="drafts")


class ActivityLog(Base):
    """Log user activities for audit trail."""
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String, nullable=False, index=True)  # created, updated, analyzed, generated, etc.
    details = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="activity_logs")
    project = relationship("Project", back_populates="activity_logs")
