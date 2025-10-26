"""
Calculator API Endpoints
=======================

FastAPI endpoints for all calculator modules
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..models.calculation_models import (
    FinancialImpactInput,
    TDABCInput,
    DigitalROIInput,
    IoTMetricsInput,
    RPAMetricsInput,
    BenchmarkingInput,
    MaturityAssessmentInput,
    ScenarioComparisonInput,
    ComprehensiveAnalysisInput,
    ComprehensiveAnalysisOutput,
)
from ..services.calculator_service import CalculatorService
from ..calculators import (
    FinancialMetricsCalculator,
    TDABCCalculator,
    DigitalROIFramework,
    IoTAutomationMetrics,
    RPAAutomationMetrics,
    BenchmarkingMaturityAssessment,
    ScenarioPlanningAnalyzer,
)

router = APIRouter(prefix="/api/calculator", tags=["Calculator"])

# Initialize calculator service
calculator_service = CalculatorService()


@router.post("/financial-impact")
async def calculate_financial_impact(data: FinancialImpactInput) -> Dict[str, Any]:
    """
    Calculate comprehensive financial impact metrics

    Returns:
    - Capital analysis (fixed, working, invested)
    - Cost savings breakdown
    - Revenue enhancements
    - Life cycle costs (CapEx, OpEx)
    - Financial metrics (ROIC, NPV, IRR, Payback, ROI%)
    """
    try:
        results = calculator_service.calculate_financial_impact(data.model_dump())
        return {
            "status": "success",
            "module": "financial_impact",
            "results": results,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tdabc")
async def calculate_tdabc(data: TDABCInput) -> Dict[str, Any]:
    """
    Calculate Time-Driven Activity-Based Costing metrics

    Returns:
    - Capacity cost rate
    - Capacity utilization analysis
    - Activity costs breakdown
    - Recommendations for capacity optimization
    """
    try:
        calc = TDABCCalculator()
        results = calc.calculate_tdabc_full_analysis(
            total_cost=data.total_cost,
            theoretical_capacity_minutes=data.theoretical_capacity_minutes,
            resource_type=data.resource_type,
            activities=[a.model_dump() for a in data.activities],
        )
        return {"status": "success", "module": "tdabc", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/digital-roi")
async def calculate_digital_roi(data: DigitalROIInput) -> Dict[str, Any]:
    """
    Calculate 6-dimensional Digital ROI score

    Returns:
    - Overall digital ROI score
    - Scores for each dimension (Customers, Employees, Operations, etc.)
    - Top performers and areas for improvement
    - Recommendations
    """
    try:
        framework = DigitalROIFramework()
        results = framework.calculate_comprehensive_digital_roi(
            data.current_metrics, data.target_metrics
        )
        return {"status": "success", "module": "digital_roi", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/iot-metrics")
async def calculate_iot_metrics(data: IoTMetricsInput) -> Dict[str, Any]:
    """
    Calculate IoT/Automation specific metrics

    Returns:
    - Connectivity value
    - OEE improvements
    - Predictive maintenance value
    - Energy optimization value
    - Quality improvement value (if provided)
    """
    try:
        metrics = IoTAutomationMetrics()
        results = metrics.calculate_comprehensive_iot_roi(
            connectivity_params=data.connectivity_params,
            oee_params=data.oee_params,
            predictive_maintenance_params=data.predictive_maintenance_params,
            energy_params=data.energy_params,
            quality_params=data.quality_params,
        )
        return {"status": "success", "module": "iot_metrics", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rpa-metrics")
async def calculate_rpa_metrics(data: RPAMetricsInput) -> Dict[str, Any]:
    """
    Calculate RPA/AI Automation metrics

    Returns:
    - FTE savings
    - Accuracy improvement value
    - Velocity improvement
    - Bot utilization (if provided)
    - Cycle time reduction (if provided)
    """
    try:
        metrics = RPAAutomationMetrics()
        results = metrics.calculate_comprehensive_rpa_roi(
            fte_savings_params=data.fte_savings_params,
            accuracy_params=data.accuracy_params,
            velocity_params=data.velocity_params,
            bot_utilization_params=data.bot_utilization_params,
            cycle_time_params=data.cycle_time_params,
        )
        return {"status": "success", "module": "rpa_metrics", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/benchmarking")
async def get_industry_benchmarking(data: BenchmarkingInput) -> Dict[str, Any]:
    """
    Compare project metrics to industry benchmarks

    Returns:
    - ROI comparison with industry average
    - Payback comparison
    - CapEx/OpEx comparison (if provided)
    - Industry benchmarks reference data
    """
    try:
        benchmarking = BenchmarkingMaturityAssessment()
        results = benchmarking.compare_to_industry(
            industry=data.industry,
            calculated_roi=data.calculated_roi,
            calculated_payback_months=data.calculated_payback_months,
            capex=data.capex,
            opex=data.opex,
        )
        return {"status": "success", "module": "benchmarking", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/benchmarks/{industry}")
async def get_industry_benchmarks(industry: str) -> Dict[str, Any]:
    """
    Get all benchmark data for a specific industry

    Available industries:
    - manufacturing
    - financial_services
    - healthcare
    - logistics
    - retail
    """
    try:
        benchmarking = BenchmarkingMaturityAssessment()

        if industry not in benchmarking.INDUSTRY_BENCHMARKS:
            raise HTTPException(
                status_code=404,
                detail=f"Industry '{industry}' not found. Available: {list(benchmarking.INDUSTRY_BENCHMARKS.keys())}",
            )

        benchmarks = benchmarking.INDUSTRY_BENCHMARKS[industry]
        return {
            "status": "success",
            "industry": industry,
            "benchmarks": benchmarks,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/maturity-assessment")
async def assess_maturity(data: MaturityAssessmentInput) -> Dict[str, Any]:
    """
    Assess automation maturity level (1-5)

    Returns:
    - Overall maturity score
    - Maturity level (1: Ad-Hoc to 5: Autonomous Operations)
    - Strengths and weaknesses
    - Roadmap to next level
    """
    try:
        benchmarking = BenchmarkingMaturityAssessment()
        results = benchmarking.assess_maturity(data.assessment_scores)
        return {
            "status": "success",
            "module": "maturity_assessment",
            "results": results,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/scenarios/compare")
async def compare_scenarios(data: ScenarioComparisonInput) -> Dict[str, Any]:
    """
    Compare 3 budget scenarios with full analysis

    Scenarios:
    1. Budget Conscious - Minimal investment
    2. Strategic Implementation - Balanced approach
    3. Enterprise Transformation - Comprehensive solution

    Returns:
    - Full financial analysis for each scenario
    - Comparison table
    - Recommended scenario with reasoning
    """
    try:
        results = calculator_service.calculate_scenario_comparison(data.model_dump())
        return {"status": "success", "module": "scenario_planning", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/comprehensive-analysis")
async def comprehensive_analysis(
    data: ComprehensiveAnalysisInput,
) -> ComprehensiveAnalysisOutput:
    """
    Perform comprehensive multi-module analysis

    This endpoint orchestrates all calculator modules and provides:
    - Financial impact analysis
    - Scenario comparison (3 scenarios)
    - Optional TDABC analysis
    - Optional Digital ROI assessment
    - Optional IoT/RPA metrics
    - Industry benchmarking
    - Optional maturity assessment
    - Executive summary
    - Recommendations

    This is the main endpoint for complete project analysis.
    """
    try:
        results = calculator_service.calculate_comprehensive_analysis(data.model_dump())
        return ComprehensiveAnalysisOutput(**results)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BFA Audit Calculator API",
        "version": "1.0.0",
        "modules": [
            "financial_impact",
            "tdabc",
            "digital_roi",
            "iot_metrics",
            "rpa_metrics",
            "benchmarking",
            "maturity_assessment",
            "scenario_planning",
        ],
    }
