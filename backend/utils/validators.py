"""
Enhanced Input Validators
=========================

Business logic validation for calculator inputs
"""

from typing import Dict, List, Tuple
from pydantic import validator


class FinancialValidators:
    """Validators for financial inputs"""

    @staticmethod
    def validate_positive(value: float, field_name: str) -> float:
        """Ensure value is positive"""
        if value < 0:
            raise ValueError(f"{field_name} must be positive, got {value}")
        return value

    @staticmethod
    def validate_percentage(value: float, field_name: str) -> float:
        """Ensure percentage is between 0 and 100"""
        if not 0 <= value <= 100:
            raise ValueError(f"{field_name} must be between 0 and 100, got {value}")
        return value

    @staticmethod
    def validate_rate(value: float, field_name: str) -> float:
        """Ensure rate is between 0 and 1"""
        if not 0 <= value <= 1:
            raise ValueError(f"{field_name} must be between 0 and 1, got {value}")
        return value

    @staticmethod
    def validate_discount_rate(value: float) -> float:
        """Validate discount rate (typically 5-20%)"""
        if not 0.01 <= value <= 0.30:
            raise ValueError(
                f"Discount rate seems unusual: {value*100:.1f}%. "
                f"Typical range is 5-20% (0.05-0.20)"
            )
        return value

    @staticmethod
    def validate_tax_rate(value: float) -> float:
        """Validate tax rate (typically 15-35%)"""
        if not 0.10 <= value <= 0.50:
            raise ValueError(
                f"Tax rate seems unusual: {value*100:.1f}%. "
                f"Typical range is 15-35% (0.15-0.35)"
            )
        return value

    @staticmethod
    def validate_project_years(value: int) -> int:
        """Validate project evaluation period"""
        if not 1 <= value <= 20:
            raise ValueError(
                f"Project years should be between 1 and 20, got {value}"
            )
        if value > 10:
            import warnings
            warnings.warn(
                f"Long evaluation period ({value} years) may reduce accuracy "
                f"due to uncertainty in long-term projections"
            )
        return value

    @staticmethod
    def validate_roi_consistency(
        initial_investment: float, 
        annual_benefits: float, 
        annual_costs: float,
        project_years: int
    ) -> Tuple[bool, str]:
        """
        Validate that ROI inputs are consistent and reasonable
        
        Returns:
            (is_valid, message)
        """
        net_annual = annual_benefits - annual_costs
        
        if net_annual <= 0:
            return False, "Annual benefits must exceed annual costs for positive ROI"
        
        simple_payback = initial_investment / net_annual
        
        if simple_payback > project_years * 2:
            return False, (
                f"Project may never pay back within evaluation period. "
                f"Simple payback: {simple_payback:.1f} years, "
                f"Evaluation period: {project_years} years"
            )
        
        total_benefit = net_annual * project_years
        if total_benefit < initial_investment:
            return False, (
                f"Total net benefits (${total_benefit:,.0f}) are less than "
                f"initial investment (${initial_investment:,.0f})"
            )
        
        return True, "OK"

    @staticmethod
    def validate_capacity_utilization(utilization_rate: float) -> Tuple[str, str]:
        """
        Validate and interpret capacity utilization rate
        
        Returns:
            (status, recommendation)
        """
        if utilization_rate < 0 or utilization_rate > 100:
            raise ValueError(f"Utilization rate must be 0-100%, got {utilization_rate}")
        
        if utilization_rate < 50:
            return "CRITICAL_OVERCAPACITY", "Severe overcapacity - immediate action needed"
        elif utilization_rate < 70:
            return "OVERCAPACITY", "Consider cost reduction or workload increase"
        elif utilization_rate <= 90:
            return "HEALTHY", "Optimal capacity utilization"
        elif utilization_rate <= 95:
            return "HIGH", "Near capacity - monitor closely"
        else:
            return "BOTTLENECK", "At capacity limit - investment needed urgently"


class BusinessLogicValidators:
    """Business logic validators"""

    @staticmethod
    def validate_cost_reduction_realistic(
        category: str, reduction_pct: float
    ) -> Tuple[bool, str]:
        """
        Validate that cost reduction percentages are realistic
        
        Returns:
            (is_valid, message)
        """
        # Typical maximum reductions by category
        max_reductions = {
            'feedstocks_energy': 25,
            'maintenance_scheduled': 30,
            'maintenance_unscheduled': 50,
            'maintenance_shutdown': 40,
            'off_spec_material': 60,
            'demurrage': 70,
            'staffing': 40,
            'abnormal_events': 80,
        }
        
        max_reduction = max_reductions.get(category, 30)
        
        if reduction_pct > max_reduction:
            return False, (
                f"Cost reduction of {reduction_pct}% in '{category}' seems unrealistic. "
                f"Typical maximum is {max_reduction}%"
            )
        
        if reduction_pct > max_reduction * 0.8:
            return True, (
                f"Cost reduction of {reduction_pct}% is aggressive but possible with "
                f"significant process changes"
            )
        
        return True, "Cost reduction target is realistic"

    @staticmethod
    def validate_benchmark_comparison(
        calculated_roi: float, industry_avg_roi: float, variance_threshold: float = 50
    ) -> Tuple[str, str]:
        """
        Validate ROI against industry benchmarks
        
        Returns:
            (status, message)
        """
        if calculated_roi < 0:
            return "NEGATIVE", "Project has negative ROI - not viable"
        
        variance = ((calculated_roi - industry_avg_roi) / industry_avg_roi) * 100
        
        if variance < -variance_threshold:
            return "WELL_BELOW", (
                f"ROI is {abs(variance):.1f}% below industry average - "
                f"review assumptions"
            )
        elif variance < -20:
            return "BELOW", "ROI is below industry average"
        elif variance <= 20:
            return "ON_PAR", "ROI is on par with industry"
        elif variance <= variance_threshold:
            return "ABOVE", "ROI is above industry average"
        else:
            return "EXCEPTIONAL", (
                f"ROI is {variance:.1f}% above industry average - "
                f"verify assumptions are realistic"
            )
