from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ProcessStep(BaseModel):
    name: str
    description: str
    executor: str
    system_used: str
    duration_minutes: int
    frequency: str
    action_type: str  # manual/automatic/semi-automatic


class ProcessBasicInfo(BaseModel):
    name: str
    department: str
    process_owner: str
    objective: str
    scope: str


class ProcessAsIs(BaseModel):
    steps: List[ProcessStep]
    total_cycle_time_hours: float
    execution_frequency: str
    annual_volume: int
    fte_count: float


class ProcessCosts(BaseModel):
    labor_costs: float
    operational_costs: float
    error_costs: float
    delay_costs: float


class ProcessProblem(BaseModel):
    description: str
    impact: str  # Low/Medium/High
    annual_cost: float


class ProcessProblems(BaseModel):
    problems: List[ProcessProblem]


class ProcessSystems(BaseModel):
    systems_used: List[str]
    integrations: List[str]
    data_quality: str
    technical_bottlenecks: List[str]


class Step2ProcessData(BaseModel):
    basic_info: ProcessBasicInfo
    as_is: ProcessAsIs
    costs: ProcessCosts
    problems: ProcessProblems
    systems: ProcessSystems


class MudaItem(BaseModel):
    description: str
    cost_per_year: float


class MudaAnalysis(BaseModel):
    defects: MudaItem
    overproduction: MudaItem
    waiting: MudaItem
    non_utilized_talent: MudaItem
    transportation: MudaItem
    inventory: MudaItem
    motion: MudaItem
    extra_processing: MudaItem
    total_waste_cost: float


class ProcessCostsAnalysis(BaseModel):
    labor_costs: float
    operational_costs: float
    error_costs: float
    delay_costs: float
    total_cost: float


class Bottleneck(BaseModel):
    name: str
    description: str
    impact: str
    cost_per_year: float


class AutomationPotential(BaseModel):
    percentage: int
    automatable_steps: List[str]
    rationale: str


class Step2AnalysisResult(BaseModel):
    muda_analysis: MudaAnalysis
    process_costs: ProcessCostsAnalysis
    bottlenecks: List[Bottleneck]
    automation_potential: AutomationPotential
    bpmn_description: str
