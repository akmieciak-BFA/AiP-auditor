"""
Pydantic Models for Calculator Inputs/Outputs
=============================================

All request and response models for the calculator API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


# ============================================================================
# MODULE 1: Financial Impact Calculator Models
# ============================================================================


class FinancialImpactInput(BaseModel):
    """Input model for Financial Impact Calculator"""

    # Capital
    project_capital: float = Field(..., ge=0, description="Initial project capital")
    commissioning_cost: float = Field(..., ge=0, description="Commissioning costs")
    fixed_assets: float = Field(..., ge=0, description="Fixed assets")
    inventory: float = Field(..., ge=0, description="Inventory costs")
    operating_cash: float = Field(..., ge=0, description="Operating cash")
    financial_wc: float = Field(..., ge=0, description="Financial working capital")

    # Cost reductions (baseline and reduction %)
    cost_reductions: Dict[str, Dict[str, float]] = Field(
        ...,
        description="Cost reductions by category: {category: {baseline, reduction_pct}}",
    )

    # Revenue enhancements
    current_revenue: float = Field(..., ge=0, description="Current annual revenue")
    quality_premium_pct: float = Field(
        default=0, ge=0, description="Quality premium percentage"
    )
    production_increase_pct: float = Field(
        default=0, ge=0, description="Production increase percentage"
    )

    # Life cycle costs
    capex_breakdown: Dict[str, float] = Field(
        ..., description="CapEx breakdown by category"
    )
    opex_yearly: Dict[str, float] = Field(..., description="Annual OpEx breakdown")

    # Financial parameters
    discount_rate: float = Field(
        default=0.10, ge=0, le=1, description="Discount rate (e.g., 0.10 for 10%)"
    )
    tax_rate: float = Field(
        default=0.21, ge=0, le=1, description="Tax rate (e.g., 0.21 for 21%)"
    )
    project_years: int = Field(
        default=5, ge=1, le=10, description="Number of years to evaluate"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "project_capital": 500000,
                "commissioning_cost": 50000,
                "fixed_assets": 100000,
                "inventory": 20000,
                "operating_cash": 10000,
                "financial_wc": 5000,
                "cost_reductions": {
                    "feedstocks_energy": {"baseline": 100000, "reduction_pct": 15},
                    "maintenance_scheduled": {"baseline": 50000, "reduction_pct": 20},
                },
                "current_revenue": 1000000,
                "quality_premium_pct": 5,
                "production_increase_pct": 10,
                "capex_breakdown": {
                    "hardware": 200000,
                    "installation": 100000,
                    "software_licenses": 50000,
                },
                "opex_yearly": {
                    "maintenance_contracts": 30000,
                    "spare_parts": 10000,
                },
                "discount_rate": 0.10,
                "tax_rate": 0.21,
                "project_years": 5,
            }
        }


# ============================================================================
# MODULE 2: TDABC Models
# ============================================================================


class ActivityInput(BaseModel):
    """Activity input for TDABC"""

    name: str = Field(..., description="Activity name")
    unit_time: float = Field(..., gt=0, description="Time per unit in minutes")
    volume: int = Field(..., ge=0, description="Number of units")


class TDABCInput(BaseModel):
    """Input model for TDABC Calculator"""

    total_cost: float = Field(..., gt=0, description="Total cost of resources")
    theoretical_capacity_minutes: float = Field(
        ..., gt=0, description="Theoretical capacity in minutes"
    )
    resource_type: str = Field(
        default="people", description="Resource type: 'people' or 'machines'"
    )
    activities: List[ActivityInput] = Field(
        ..., description="List of activities with time and volume"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "total_cost": 560000,
                "theoretical_capacity_minutes": 876000,
                "resource_type": "people",
                "activities": [
                    {"name": "Process Orders", "unit_time": 8, "volume": 1000},
                    {"name": "Handle Inquiries", "unit_time": 5, "volume": 2000},
                ],
            }
        }


# ============================================================================
# MODULE 3: Digital ROI Framework Models
# ============================================================================


class DigitalROIInput(BaseModel):
    """Input model for Digital ROI Framework"""

    current_metrics: Dict[str, Dict[str, float]] = Field(
        ..., description="Current metrics by dimension"
    )
    target_metrics: Dict[str, Dict[str, float]] = Field(
        ..., description="Target metrics by dimension"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "current_metrics": {
                    "customers": {"nps_score": 30, "csat_score": 75},
                    "employees": {"engagement_score": 65, "turnover_rate": 15},
                },
                "target_metrics": {
                    "customers": {"nps_score": 50, "csat_score": 85},
                    "employees": {"engagement_score": 80, "turnover_rate": 10},
                },
            }
        }


# ============================================================================
# MODULE 4: IoT Metrics Models
# ============================================================================


class IoTMetricsInput(BaseModel):
    """Input model for IoT Automation Metrics"""

    connectivity_params: Dict[str, Any] = Field(
        ..., description="Connectivity value parameters"
    )
    oee_params: Dict[str, float] = Field(..., description="OEE improvement parameters")
    predictive_maintenance_params: Dict[str, float] = Field(
        ..., description="Predictive maintenance parameters"
    )
    energy_params: Dict[str, float] = Field(
        ..., description="Energy optimization parameters"
    )
    quality_params: Optional[Dict[str, float]] = Field(
        default=None, description="Optional quality improvement parameters"
    )


# ============================================================================
# MODULE 5: RPA Metrics Models
# ============================================================================


class RPAMetricsInput(BaseModel):
    """Input model for RPA Automation Metrics"""

    fte_savings_params: Dict[str, Any] = Field(..., description="FTE savings parameters")
    accuracy_params: Dict[str, float] = Field(
        ..., description="Accuracy improvement parameters"
    )
    velocity_params: Dict[str, float] = Field(
        ..., description="Velocity improvement parameters"
    )
    bot_utilization_params: Optional[Dict[str, float]] = Field(
        default=None, description="Optional bot utilization parameters"
    )
    cycle_time_params: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional cycle time parameters"
    )


# ============================================================================
# MODULE 6: Benchmarking Models
# ============================================================================


class BenchmarkingInput(BaseModel):
    """Input model for Industry Benchmarking"""

    industry: str = Field(
        ...,
        description="Industry name (manufacturing, financial_services, healthcare, etc.)",
    )
    calculated_roi: float = Field(..., description="Calculated ROI percentage")
    calculated_payback_months: float = Field(
        ..., description="Calculated payback period in months"
    )
    capex: Optional[float] = Field(default=None, description="Optional CapEx")
    opex: Optional[float] = Field(default=None, description="Optional OpEx")


class MaturityAssessmentInput(BaseModel):
    """Input model for Maturity Assessment"""

    assessment_scores: Dict[str, float] = Field(
        ...,
        description="Dimension scores (0-100): strategy_governance, technology_infrastructure, etc.",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "assessment_scores": {
                    "strategy_governance": 75,
                    "technology_infrastructure": 60,
                    "process_operations": 70,
                    "people_culture": 55,
                    "measurement_optimization": 65,
                }
            }
        }


# ============================================================================
# MODULE 7: Scenario Planning Models
# ============================================================================


class ScenarioComparisonInput(BaseModel):
    """Input model for Scenario Comparison"""

    base_capex: float = Field(..., ge=0, description="Base CapEx amount")
    base_opex: float = Field(..., ge=0, description="Base annual OpEx")
    base_annual_benefits: float = Field(..., ge=0, description="Base annual benefits")
    project_years: int = Field(default=5, ge=1, le=10, description="Project years")
    discount_rate: float = Field(
        default=0.10, ge=0, le=1, description="Discount rate"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "base_capex": 500000,
                "base_opex": 50000,
                "base_annual_benefits": 200000,
                "project_years": 5,
                "discount_rate": 0.10,
            }
        }


class SensitivityAnalysisInput(BaseModel):
    """Input model for Sensitivity Analysis"""

    base_npv: float = Field(..., description="Base case NPV")
    parameters: Dict[str, Dict[str, Any]] = Field(
        ..., description="Parameters to analyze with base values and calculation functions"
    )
    variation_pct: float = Field(
        default=20, ge=0, le=100, description="Percentage variation to test"
    )


class MonteCarloInput(BaseModel):
    """Input model for Monte Carlo Simulation"""

    parameters_distributions: Dict[str, Dict[str, Any]] = Field(
        ..., description="Parameter distributions (normal, uniform, triangular, etc.)"
    )
    iterations: int = Field(
        default=1000, ge=100, le=10000, description="Number of iterations"
    )
    random_seed: Optional[int] = Field(default=None, description="Optional random seed")


# ============================================================================
# Common Response Models
# ============================================================================


class CalculationResult(BaseModel):
    """Base calculation result model"""

    calculation_id: Optional[str] = None
    module_name: str
    timestamp: datetime = Field(default_factory=datetime.now)
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    status: str = "success"
    error: Optional[str] = None


class ComprehensiveAnalysisInput(BaseModel):
    """Input for comprehensive multi-module analysis"""

    project_id: Optional[int] = None
    project_name: str = Field(..., description="Project name")
    industry: str = Field(..., description="Industry")

    # Financial inputs
    financial_impact: FinancialImpactInput

    # Optional additional analyses
    tdabc: Optional[TDABCInput] = None
    digital_roi: Optional[DigitalROIInput] = None
    iot_metrics: Optional[IoTMetricsInput] = None
    rpa_metrics: Optional[RPAMetricsInput] = None
    maturity_assessment: Optional[MaturityAssessmentInput] = None

    # Scenario planning
    include_scenario_planning: bool = Field(
        default=True, description="Include scenario planning analysis"
    )


class ComprehensiveAnalysisOutput(BaseModel):
    """Output for comprehensive multi-module analysis"""

    project_name: str
    industry: str
    analysis_date: datetime = Field(default_factory=datetime.now)

    # Results from each module
    financial_impact: Dict[str, Any]
    scenarios: Optional[Dict[str, Any]] = None
    tdabc: Optional[Dict[str, Any]] = None
    digital_roi: Optional[Dict[str, Any]] = None
    iot_metrics: Optional[Dict[str, Any]] = None
    rpa_metrics: Optional[Dict[str, Any]] = None
    benchmarking: Optional[Dict[str, Any]] = None
    maturity_assessment: Optional[Dict[str, Any]] = None

    # Summary and recommendations
    executive_summary: Dict[str, Any]
    recommendations: List[str]
