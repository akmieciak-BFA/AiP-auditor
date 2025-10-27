from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base


def get_utc_now():
    """Get current UTC time for database defaults."""
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    # Relationships
    # Note: User model is kept for authentication endpoints but not used for project ownership
    # Projects are accessible without authentication in the current version
