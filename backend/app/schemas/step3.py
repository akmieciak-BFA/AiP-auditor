from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class Step3DataInput(BaseModel):
    budget_level: str  # low/medium/high
    tech_preferences: Optional[Dict[str, Any]] = None


class VendorEvaluation(BaseModel):
    name: str
    category: str
    functionality_score: int
    price_tier: str
    references: List[str]
    recommendation: str


class TechnologyResearch(BaseModel):
    categories: List[str]
    vendors: List[VendorEvaluation]


class CostBreakdown(BaseModel):
    licenses: float
    infrastructure: float
    consulting: float
    training: float
    change_management: float
    total: float


class OpexBreakdown(BaseModel):
    licenses: float
    infrastructure: float
    support: float
    continuous_improvement: float
    total: float


class BenefitsBreakdown(BaseModel):
    fte_savings: float
    operational_savings: float
    error_reduction: float
    speed_improvement: float
    total: float


class FinancialAnalysis(BaseModel):
    roi_3years: float
    payback_months: int
    npv: float


class ProcessToBe(BaseModel):
    description: str
    steps: List[str]
    cycle_time_hours: float
    fte_required: float
    bpmn_description: str


class Solution(BaseModel):
    vendor: str
    product: str
    rationale: str


class BudgetScenario(BaseModel):
    name: str
    description: str
    scope: str
    technologies: List[str]
    solutions: List[Solution]
    costs: Dict[str, Any]
    benefits_year1: BenefitsBreakdown
    financial_analysis: FinancialAnalysis
    process_to_be: ProcessToBe


class ScenarioComparison(BaseModel):
    table: List[List[Any]]
    recommendation: str
    rationale: str


class Step3AnalysisResult(BaseModel):
    technology_research: TechnologyResearch
    scenarios: List[BudgetScenario]
    comparison: ScenarioComparison
