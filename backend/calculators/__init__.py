"""
BFA Audit App - Advanced ROI/TCO Calculator
============================================

7 Module Calculator System based on industry-leading methodologies:
- Emerson Process Management - ROIC Framework
- Siemens Advanta - IoT ROI Framework
- Blue Prism - RPA ROI Methodology
- PwC Strategy& - Digital ROI Framework
- Harvard Business Review - Time-Driven Activity-Based Costing (TDABC)
"""

from .financial_impact import (
    CapitalAnalyzer,
    CostReductionAnalyzer,
    RevenueEnhancementAnalyzer,
    LifeCycleCostAnalyzer,
    FinancialMetricsCalculator,
)
from .tdabc import TDABCCalculator, TimeEquationsBuilder
from .digital_roi import DigitalROIFramework
from .iot_metrics import IoTAutomationMetrics
from .rpa_metrics import RPAAutomationMetrics
from .benchmarking import BenchmarkingMaturityAssessment
from .scenario_planning import ScenarioPlanningAnalyzer

__all__ = [
    "CapitalAnalyzer",
    "CostReductionAnalyzer",
    "RevenueEnhancementAnalyzer",
    "LifeCycleCostAnalyzer",
    "FinancialMetricsCalculator",
    "TDABCCalculator",
    "TimeEquationsBuilder",
    "DigitalROIFramework",
    "IoTAutomationMetrics",
    "RPAAutomationMetrics",
    "BenchmarkingMaturityAssessment",
    "ScenarioPlanningAnalyzer",
]
