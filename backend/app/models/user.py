from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
