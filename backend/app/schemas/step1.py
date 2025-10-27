from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class InitialAssessmentData(BaseModel):
    """Comprehensive initial assessment data with 20 questions in 5 sections"""
    
    # SEKCJA A: INFORMACJE ORGANIZACYJNE (Pytania 1-5)
    organization_name: str
    industry: str
    company_size: str
    annual_revenue: Optional[float] = None
    headquarters_location: str
    number_of_locations: int
    functional_areas: List[str]
    critical_areas: List[str]
    
    # Digital maturity scores (0-10 for each)
    digital_maturity_erp: int
    digital_maturity_crm: int
    digital_maturity_production: int
    digital_maturity_rpa: int
    digital_maturity_analytics: int
    digital_maturity_iot: int
    digital_maturity_ai: int
    digital_maturity_communication: int
    digital_maturity_workflow: int
    digital_maturity_cloud: int
    
    # IT Systems
    it_systems: Dict[str, str]  # system_type: system_name
    systems_integrated: str  # Tak/Częściowo/Nie
    
    # Budget
    budget_range: str
    budget_sources: List[str]
    expected_payback_months: int
    
    # SEKCJA B: IDENTYFIKACJA PROBLEMÓW (Pytania 6-10)
    main_challenges_ranked: List[str]  # Top 12 challenges ranked
    challenges_description: str
    
    # Time consuming processes with estimated hours/week
    time_consuming_processes: Dict[str, float]
    
    # Error prone processes with frequency and error rate
    error_prone_processes: Dict[str, Dict[str, Any]]
    
    # Bottlenecks with impact rating (1-5)
    bottlenecks: Dict[str, Dict[str, Any]]
    
    # Process maturity ratings (1-5 for repeatability, standardization, documentation)
    process_maturity: Dict[str, Dict[str, int]]
    
    # SEKCJA C: CELE I OCZEKIWANIA (Pytania 11-15)
    automation_goals_ranked: List[str]
    automation_goals_weights: Dict[str, int]  # Sum = 100%
    
    expected_cost_reduction_percent: float
    expected_revenue_increase_percent: float
    expected_roi_percent: float
    acceptable_payback_months: int
    specific_savings_goal: Optional[float] = None
    savings_sources_description: str
    
    operational_targets: Dict[str, float]  # Various operational improvement targets
    
    employee_expectations: Dict[str, Any]
    change_management_readiness: str
    
    # Timeline
    preferred_start_date: str
    preferred_phase1_end_date: str
    phased_approach: str  # Tak/Nie
    number_of_phases: Optional[int] = None
    preferred_approach: str  # Quick wins/Kompleksowa/Hybrydowa
    business_deadlines: Optional[str] = None
    
    # SEKCJA D: ZASOBY I OGRANICZENIA (Pytania 16-18)
    has_it_team: str
    it_team_size: Optional[int] = None
    has_bpm_department: str
    bpm_team_size: Optional[int] = None
    automation_experience: str
    has_project_manager: str
    has_change_manager: str
    stakeholder_availability: str
    
    constraints_and_risks: Dict[str, int]  # Risk with impact rating 1-5
    special_requirements: List[str]
    
    # SEKCJA E: KONTEKST STRATEGICZNY (Pytania 19-20)
    business_strategy_description: str
    strategic_initiatives: List[str]
    additional_notes: Optional[str] = None


class Step1AnalysisResult(BaseModel):
    digital_maturity: Dict[str, Any]
    processes_scoring: List[Dict[str, Any]]
    top_processes: List[str]
    legal_analysis: str
    system_dependencies: Dict[str, Any]
    recommendations: str
    bfa_scoring: Dict[str, Any]  # 6-dimensional framework scores


# Alias for compatibility
Step1DataInput = InitialAssessmentData
