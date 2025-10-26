"""
Module 1: Financial Impact Calculator
======================================

Based on Emerson Process Management - ROIC Framework

Components:
- Capital Analysis (Fixed & Working Capital)
- Cost Reduction Analysis (8 categories)
- Revenue Enhancement Analysis
- Life Cycle Cost Analysis (CapEx & OpEx)
- Financial Metrics (ROIC, NPV, IRR, Payback, ROI%)
"""

from typing import Dict, List, Optional
import numpy as np
from numpy_financial import npv, irr


class CapitalAnalyzer:
    """Analyze capital requirements (Fixed and Working Capital)"""

    def calculate_fixed_capital(
        self, project_capital: float, commissioning_cost: float, fixed_assets: float
    ) -> float:
        """
        Calculate Fixed Capital

        Args:
            project_capital: Initial project capital investment
            commissioning_cost: Costs to commission the system
            fixed_assets: Additional fixed assets required

        Returns:
            Total fixed capital
        """
        return project_capital + commissioning_cost + fixed_assets

    def calculate_working_capital(
        self, inventory: float, operating_cash: float, financial_wc: float
    ) -> float:
        """
        Calculate Working Capital

        Args:
            inventory: Total inventory (raw materials + intermediates + products + spares)
            operating_cash: Operating cash requirements
            financial_wc: Financial working capital

        Returns:
            Total working capital
        """
        return inventory + operating_cash + financial_wc

    def calculate_invested_capital(
        self, fixed_capital: float, working_capital: float
    ) -> float:
        """
        Calculate Total Invested Capital

        Args:
            fixed_capital: Fixed capital
            working_capital: Working capital

        Returns:
            Total invested capital (basis for ROIC calculation)
        """
        return fixed_capital + working_capital


class CostReductionAnalyzer:
    """Analyze cost reductions across 8 key categories"""

    CATEGORIES = [
        "feedstocks_energy",  # Yield optimization, energy efficiency
        "maintenance_scheduled",  # Routine maintenance reduction
        "maintenance_unscheduled",  # Emergency repairs reduction
        "maintenance_shutdown",  # Major shutdown optimization
        "off_spec_material",  # Quality improvement
        "demurrage",  # Logistics optimization
        "staffing",  # Labor optimization
        "abnormal_events",  # HS&E improvements
    ]

    def calculate_category_savings(
        self, baseline_cost: float, reduction_percentage: float
    ) -> float:
        """
        Calculate savings for a single category

        Args:
            baseline_cost: Current annual cost in category
            reduction_percentage: Expected reduction (%)

        Returns:
            Annual savings in currency
        """
        return baseline_cost * (reduction_percentage / 100)

    def calculate_total_savings(
        self,
        baseline_costs: Dict[str, float],
        reduction_percentages: Dict[str, float],
    ) -> Dict[str, any]:
        """
        Calculate total savings across all categories

        Args:
            baseline_costs: Dictionary of current costs by category
            reduction_percentages: Dictionary of reduction % by category

        Returns:
            Dictionary with total savings and breakdown by category
        """
        savings_breakdown = {}
        total_savings = 0

        for category in self.CATEGORIES:
            baseline = baseline_costs.get(category, 0)
            reduction_pct = reduction_percentages.get(category, 0)
            savings = self.calculate_category_savings(baseline, reduction_pct)

            savings_breakdown[category] = {
                "baseline_cost": baseline,
                "reduction_pct": reduction_pct,
                "annual_savings": savings,
            }
            total_savings += savings

        return {
            "total_annual_savings": total_savings,
            "breakdown": savings_breakdown,
        }


class RevenueEnhancementAnalyzer:
    """Analyze revenue enhancement opportunities"""

    def calculate_price_improvement(
        self,
        current_revenue: float,
        quality_premium_pct: float,
        off_spec_reduction_pct: float,
    ) -> Dict[str, float]:
        """
        Calculate revenue gains from price improvements

        Args:
            current_revenue: Current annual revenue
            quality_premium_pct: Premium from quality improvement (%)
            off_spec_reduction_pct: Revenue gain from off-spec reduction (%)

        Returns:
            Dictionary with quality gain, off-spec gain, and total
        """
        quality_gain = current_revenue * (quality_premium_pct / 100)
        off_spec_gain = current_revenue * (off_spec_reduction_pct / 100)

        return {
            "quality_premium_gain": quality_gain,
            "off_spec_reduction_gain": off_spec_gain,
            "total_price_improvement": quality_gain + off_spec_gain,
        }

    def calculate_production_increase(
        self,
        current_production: float,
        current_price: float,
        capacity_improvement_pct: float,
        downtime_reduction_pct: float,
        cycle_time_reduction_pct: float,
    ) -> Dict[str, float]:
        """
        Calculate revenue gains from production increases
        NOTE: Only applicable for production-limited plants!

        Args:
            current_production: Current annual production volume
            current_price: Price per unit
            capacity_improvement_pct: Capacity increase (%)
            downtime_reduction_pct: Downtime reduction impact on production (%)
            cycle_time_reduction_pct: Cycle time reduction impact (%)

        Returns:
            Dictionary with additional production and revenue
        """
        total_improvement = (
            capacity_improvement_pct
            + downtime_reduction_pct
            + cycle_time_reduction_pct
        ) / 100

        additional_production = current_production * total_improvement
        additional_revenue = additional_production * current_price

        return {
            "additional_production": additional_production,
            "additional_revenue": additional_revenue,
            "total_improvement_pct": total_improvement * 100,
        }

    def calculate_total_revenue_enhancement(
        self,
        price_improvement: Dict[str, float],
        production_increase: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Calculate total revenue enhancement

        Args:
            price_improvement: Result from calculate_price_improvement()
            production_increase: Optional result from calculate_production_increase()

        Returns:
            Total annual revenue enhancement
        """
        total = price_improvement["total_price_improvement"]

        if production_increase:
            total += production_increase["additional_revenue"]

        return total


class LifeCycleCostAnalyzer:
    """
    Analyze Life Cycle Costs (CapEx and OpEx)

    Industry rule of thumb: >66% of total cost occurs after installation
    """

    def calculate_capex(
        self,
        hardware: float,
        installation: float,
        infrastructure: float,
        software_licenses: float,
        services: float,
        training: float,
    ) -> Dict[str, float]:
        """
        Calculate Capital Expenditure breakdown

        Args:
            hardware: Hardware costs
            installation: Installation costs
            infrastructure: Infrastructure costs (network, power, etc.)
            software_licenses: Software license costs
            services: Professional services
            training: Initial training costs

        Returns:
            Dictionary with CapEx breakdown and total
        """
        return {
            "hardware": hardware,
            "installation": installation,
            "infrastructure": infrastructure,
            "software_licenses": software_licenses,
            "services": services,
            "training": training,
            "total": sum(
                [
                    hardware,
                    installation,
                    infrastructure,
                    software_licenses,
                    services,
                    training,
                ]
            ),
        }

    def calculate_opex_yearly(
        self,
        maintenance_contracts: float,
        spare_parts: float,
        administration: float,
        training: float,
        upgrades: float,
        cybersecurity: float,
    ) -> Dict[str, float]:
        """
        Calculate annual Operating Expenditure

        Args:
            maintenance_contracts: Annual maintenance contracts
            spare_parts: Spare parts costs
            administration: Administration costs
            training: Ongoing training costs
            upgrades: Software/hardware upgrades
            cybersecurity: Cybersecurity costs

        Returns:
            Dictionary with OpEx breakdown and total
        """
        return {
            "maintenance_contracts": maintenance_contracts,
            "spare_parts": spare_parts,
            "administration": administration,
            "training": training,
            "upgrades": upgrades,
            "cybersecurity": cybersecurity,
            "total": sum(
                [
                    maintenance_contracts,
                    spare_parts,
                    administration,
                    training,
                    upgrades,
                    cybersecurity,
                ]
            ),
        }

    def project_opex_5_years(
        self, year1_opex: float, inflation_rate: float = 0.03
    ) -> List[float]:
        """
        Project OpEx over 5 years with inflation

        Args:
            year1_opex: First year OpEx
            inflation_rate: Annual inflation rate (default 3%)

        Returns:
            List of OpEx for 5 years
        """
        projection = []
        for year in range(1, 6):
            yearly_opex = year1_opex * ((1 + inflation_rate) ** (year - 1))
            projection.append(yearly_opex)
        return projection

    def calculate_total_life_cycle_cost(
        self, capex: float, opex_projection: List[float]
    ) -> Dict[str, float]:
        """
        Calculate total life cycle cost

        Args:
            capex: Total CapEx
            opex_projection: List of yearly OpEx

        Returns:
            Dictionary with CapEx, total OpEx, and total life cycle cost
        """
        total_opex = sum(opex_projection)
        total_lcc = capex + total_opex

        return {
            "capex": capex,
            "total_opex": total_opex,
            "total_life_cycle_cost": total_lcc,
            "opex_percentage": (total_opex / total_lcc) * 100,
            "capex_percentage": (capex / total_lcc) * 100,
        }


class FinancialMetricsCalculator:
    """Calculate key financial metrics (ROIC, NPV, IRR, Payback, ROI%)"""

    def calculate_roic(
        self, after_tax_cash_adjusted_income: float, invested_capital: float
    ) -> float:
        """
        Calculate Return on Invested Capital (ROIC)

        ROIC = After-Tax Cash-Adjusted Income / Invested Capital × 100

        Args:
            after_tax_cash_adjusted_income: After-tax operating income
            invested_capital: Total invested capital

        Returns:
            ROIC as percentage
        """
        if invested_capital == 0:
            return 0.0
        return (after_tax_cash_adjusted_income / invested_capital) * 100

    def calculate_npv(
        self, initial_investment: float, cash_flows: List[float], discount_rate: float
    ) -> float:
        """
        Calculate Net Present Value (NPV)

        Args:
            initial_investment: Initial investment (positive number)
            cash_flows: List of annual cash flows
            discount_rate: Discount rate (e.g., 0.10 for 10%)

        Returns:
            NPV in currency
        """
        return npv(discount_rate, [-initial_investment] + cash_flows)

    def calculate_irr(
        self, initial_investment: float, cash_flows: List[float]
    ) -> Optional[float]:
        """
        Calculate Internal Rate of Return (IRR)

        Args:
            initial_investment: Initial investment (positive number)
            cash_flows: List of annual cash flows

        Returns:
            IRR as percentage, or None if cannot be calculated
        """
        try:
            irr_value = irr([-initial_investment] + cash_flows)
            return irr_value * 100
        except:
            return None

    def calculate_payback_period(
        self, initial_investment: float, annual_cash_flow: float
    ) -> float:
        """
        Calculate Simple Payback Period

        Args:
            initial_investment: Initial investment
            annual_cash_flow: Average annual cash flow

        Returns:
            Payback period in years
        """
        if annual_cash_flow <= 0:
            return float("inf")
        return initial_investment / annual_cash_flow

    def calculate_discounted_payback(
        self, initial_investment: float, cash_flows: List[float], discount_rate: float
    ) -> Optional[float]:
        """
        Calculate Discounted Payback Period

        Args:
            initial_investment: Initial investment
            cash_flows: List of annual cash flows
            discount_rate: Discount rate (e.g., 0.10 for 10%)

        Returns:
            Discounted payback period in years, or None if never pays back
        """
        cumulative = 0
        for year, cf in enumerate(cash_flows, 1):
            discounted_cf = cf / ((1 + discount_rate) ** year)
            cumulative += discounted_cf

            if cumulative >= initial_investment:
                # Interpolate to find exact payback point
                previous_cumulative = cumulative - discounted_cf
                fraction = (initial_investment - previous_cumulative) / discounted_cf
                return year - 1 + fraction

        return None  # Never pays back within the time horizon

    def calculate_roi_percentage(
        self, net_benefit: float, total_investment: float
    ) -> float:
        """
        Calculate ROI percentage

        ROI% = (Net Benefit / Total Investment) × 100

        Args:
            net_benefit: Total benefits minus total costs
            total_investment: Total investment

        Returns:
            ROI as percentage
        """
        if total_investment == 0:
            return 0.0
        return (net_benefit / total_investment) * 100

    def calculate_benefit_cost_ratio(
        self, total_benefits: float, total_costs: float
    ) -> float:
        """
        Calculate Benefit-Cost Ratio (BCR)

        BCR = Total Benefits / Total Costs

        Args:
            total_benefits: Sum of all benefits
            total_costs: Sum of all costs

        Returns:
            Benefit-cost ratio (>1 means profitable)
        """
        if total_costs == 0:
            return 0.0
        return total_benefits / total_costs

    def calculate_comprehensive_metrics(
        self,
        initial_investment: float,
        annual_benefits: float,
        annual_costs: float,
        project_years: int,
        discount_rate: float,
        invested_capital: float,
        tax_rate: float = 0.21,
    ) -> Dict[str, any]:
        """
        Calculate comprehensive financial metrics

        Args:
            initial_investment: Initial investment (CapEx)
            annual_benefits: Annual benefits
            annual_costs: Annual OpEx
            project_years: Number of years to evaluate
            discount_rate: Discount rate
            invested_capital: Total invested capital
            tax_rate: Corporate tax rate (default 21%)

        Returns:
            Dictionary with all financial metrics
        """
        # Calculate cash flows
        annual_net_cash_flow = annual_benefits - annual_costs
        cash_flows = [annual_net_cash_flow] * project_years

        # Calculate after-tax income for ROIC
        after_tax_income = annual_net_cash_flow * (1 - tax_rate)

        # Calculate all metrics
        roic = self.calculate_roic(after_tax_income, invested_capital)
        npv_value = self.calculate_npv(initial_investment, cash_flows, discount_rate)
        irr_value = self.calculate_irr(initial_investment, cash_flows)
        payback = self.calculate_payback_period(
            initial_investment, annual_net_cash_flow
        )
        discounted_payback = self.calculate_discounted_payback(
            initial_investment, cash_flows, discount_rate
        )

        total_benefits = annual_benefits * project_years
        total_costs = initial_investment + (annual_costs * project_years)
        net_benefit = total_benefits - total_costs

        roi_pct = self.calculate_roi_percentage(net_benefit, initial_investment)
        bcr = self.calculate_benefit_cost_ratio(total_benefits, total_costs)

        return {
            "roic_pct": round(roic, 2),
            "npv": round(npv_value, 2),
            "irr_pct": round(irr_value, 2) if irr_value else None,
            "payback_period_years": round(payback, 2),
            "discounted_payback_years": (
                round(discounted_payback, 2) if discounted_payback else None
            ),
            "roi_pct": round(roi_pct, 2),
            "benefit_cost_ratio": round(bcr, 2),
            "total_benefits": round(total_benefits, 2),
            "total_costs": round(total_costs, 2),
            "net_benefit": round(net_benefit, 2),
            "annual_net_cash_flow": round(annual_net_cash_flow, 2),
        }
