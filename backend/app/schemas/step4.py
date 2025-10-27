from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


class Step4GenerateRequest(BaseModel):
    client_name: str
    author_name: str
    logo_url: Optional[str] = None
    selected_processes: List[str]
    budget_scenario: str  # low/medium/high
    include_reports: Optional[bool] = False


class Step4Output(BaseModel):
    id: int
    project_id: int
    output_type: str
    gamma_url: Optional[str] = None
    file_path: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
