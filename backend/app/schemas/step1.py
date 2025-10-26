from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class OrganizationData(BaseModel):
    company_name: str
    industry: str
    size: str
    structure: str
    description: Optional[str] = None


class Step1DataInput(BaseModel):
    organization_data: OrganizationData
    questionnaire_answers: Dict[str, Any]
    processes_list: List[str]


class DigitalMaturity(BaseModel):
    process_maturity: int
    digital_infrastructure: int
    data_quality: int
    organizational_readiness: int
    financial_capacity: int
    strategic_alignment: int
    overall_score: int
    interpretation: str


class ProcessScoring(BaseModel):
    process_name: str
    score: int
    tier: int
    rationale: str


class SystemDependencies(BaseModel):
    systems: List[str]
    matrix: List[List[int]]


class Step1AnalysisResult(BaseModel):
    digital_maturity: DigitalMaturity
    processes_scoring: List[ProcessScoring]
    top_processes: List[str]
    legal_analysis: str
    system_dependencies: SystemDependencies
    recommendations: str
