from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: str
    client_name: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client_name: Optional[str] = None
    status: Optional[str] = None


class Project(ProjectBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
