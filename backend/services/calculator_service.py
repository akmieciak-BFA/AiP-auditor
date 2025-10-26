"""
Calculator Orchestrator Service
================================

Orchestrates multiple calculator modules and provides comprehensive analysis
"""

from typing import Dict, Any, Optional
from ..calculators import (
    FinancialMetricsCalculator,
    CapitalAnalyzer,
    CostReductionAnalyzer,
    RevenueEnhancementAnalyzer,
    LifeCycleCostAnalyzer,
    TDABCCalculator,
    DigitalROIFramework,
    IoTAutomationMetrics,
    RPAAutomationMetrics,
    BenchmarkingMaturityAssessment,
    ScenarioPlanningAnalyzer,
)


class CalculatorService:
    """
    Orchestrator service that coordinates all calculator modules
    """

    def __init__(self):
        # Initialize all calculator modules
        self.capital_analyzer = CapitalAnalyzer()
        self.cost_reduction = CostReductionAnalyzer()
        self.revenue_enhancement = RevenueEnhancementAnalyzer()
        self.lifecycle_cost = LifeCycleCostAnalyzer()
        self.financial_metrics = FinancialMetricsCalculator()
        self.tdabc = TDABCCalculator()
        self.digital_roi = DigitalROIFramework()
        self.iot_metrics = IoTAutomationMetrics()
        self.rpa_metrics = RPAAutomationMetrics()
        self.benchmarking = BenchmarkingMaturityAssessment()
        self.scenario_planner = ScenarioPlanningAnalyzer()

    def calculate_financial_impact(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive financial impact

        Args:
            input_data: Dictionary with all financial impact inputs

        Returns:
            Complete financial impact analysis
        """
        # 1. Capital Analysis
        fixed_capital = self.capital_analyzer.calculate_fixed_capital(
            input_data["project_capital"],
            input_data["commissioning_cost"],
            input_data["fixed_assets"],
        )

        working_capital = self.capital_analyzer.calculate_working_capital(
            input_data["inventory"],
            input_data["operating_cash"],
            input_data["financial_wc"],
        )

        invested_capital = self.capital_analyzer.calculate_invested_capital(
            fixed_capital, working_capital
        )

        # 2. Cost Reduction Analysis
        cost_savings = self.cost_reduction.calculate_total_savings(
            input_data["cost_reductions"], input_data["cost_reductions"]
        )

        # 3. Revenue Enhancement (if applicable)
        revenue_improvement = {}
        if input_data.get("quality_premium_pct", 0) > 0:
            price_improvement = self.revenue_enhancement.calculate_price_improvement(
                input_data["current_revenue"],
                input_data.get("quality_premium_pct", 0),
                0,  # off_spec_reduction_pct
            )
            revenue_improvement["price_improvement"] = price_improvement

        # 4. Life Cycle Costs
        capex = self.lifecycle_cost.calculate_capex(**input_data["capex_breakdown"])
        opex_yearly = self.lifecycle_cost.calculate_opex_yearly(
            **input_data["opex_yearly"]
        )
        opex_projection = self.lifecycle_cost.project_opex_5_years(
            opex_yearly["total"]
        )

        # 5. Calculate Financial Metrics
        annual_benefits = cost_savings["total_annual_savings"]
        if revenue_improvement:
            annual_benefits += revenue_improvement["price_improvement"].get(
                "total_price_improvement", 0
            )

        metrics = self.financial_metrics.calculate_comprehensive_metrics(
            initial_investment=capex["total"],
            annual_benefits=annual_benefits,
            annual_costs=opex_yearly["total"],
            project_years=input_data.get("project_years", 5),
            discount_rate=input_data.get("discount_rate", 0.10),
            invested_capital=invested_capital,
            tax_rate=input_data.get("tax_rate", 0.21),
        )

        return {
            "capital_analysis": {
                "fixed_capital": fixed_capital,
                "working_capital": working_capital,
                "invested_capital": invested_capital,
            },
            "cost_savings": cost_savings,
            "revenue_enhancement": revenue_improvement,
            "lifecycle_costs": {
                "capex": capex,
                "opex_yearly": opex_yearly,
                "opex_projection_5yr": opex_projection,
            },
            "financial_metrics": metrics,
        }

    def calculate_scenario_comparison(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate and compare scenarios

        Args:
            input_data: Base scenario parameters

        Returns:
            Scenario comparison with recommendations
        """
        return self.scenario_planner.compare_scenarios(
            base_capex=input_data["base_capex"],
            base_opex=input_data["base_opex"],
            base_benefits=input_data["base_annual_benefits"],
            project_years=input_data.get("project_years", 5),
            discount_rate=input_data.get("discount_rate", 0.10),
        )

    def calculate_comprehensive_analysis(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive multi-module analysis

        Args:
            input_data: Complete analysis inputs

        Returns:
            Comprehensive analysis results
        """
        results = {
            "project_name": input_data.get("project_name", "Unnamed Project"),
            "industry": input_data.get("industry", "Unknown"),
            "analysis_modules": [],
        }

        # 1. Financial Impact (always calculated)
        if "financial_impact" in input_data:
            financial_results = self.calculate_financial_impact(
                input_data["financial_impact"]
            )
            results["financial_impact"] = financial_results
            results["analysis_modules"].append("financial_impact")

        # 2. Scenario Planning
        if input_data.get("include_scenario_planning", True):
            scenario_input = {
                "base_capex": financial_results["lifecycle_costs"]["capex"]["total"],
                "base_opex": financial_results["lifecycle_costs"]["opex_yearly"][
                    "total"
                ],
                "base_annual_benefits": financial_results["financial_metrics"][
                    "annual_net_cash_flow"
                ],
                "project_years": input_data["financial_impact"].get("project_years", 5),
                "discount_rate": input_data["financial_impact"].get(
                    "discount_rate", 0.10
                ),
            }
            scenario_results = self.calculate_scenario_comparison(scenario_input)
            results["scenarios"] = scenario_results
            results["analysis_modules"].append("scenario_planning")

        # 3. TDABC (if provided)
        if "tdabc" in input_data:
            tdabc_results = self.tdabc.calculate_tdabc_full_analysis(
                **input_data["tdabc"]
            )
            results["tdabc"] = tdabc_results
            results["analysis_modules"].append("tdabc")

        # 4. Digital ROI (if provided)
        if "digital_roi" in input_data:
            digital_roi_results = self.digital_roi.calculate_comprehensive_digital_roi(
                input_data["digital_roi"]["current_metrics"],
                input_data["digital_roi"]["target_metrics"],
            )
            results["digital_roi"] = digital_roi_results
            results["analysis_modules"].append("digital_roi")

        # 5. IoT Metrics (if provided)
        if "iot_metrics" in input_data:
            iot_results = self.iot_metrics.calculate_comprehensive_iot_roi(
                **input_data["iot_metrics"]
            )
            results["iot_metrics"] = iot_results
            results["analysis_modules"].append("iot_metrics")

        # 6. RPA Metrics (if provided)
        if "rpa_metrics" in input_data:
            rpa_results = self.rpa_metrics.calculate_comprehensive_rpa_roi(
                **input_data["rpa_metrics"]
            )
            results["rpa_metrics"] = rpa_results
            results["analysis_modules"].append("rpa_metrics")

        # 7. Benchmarking (always included if industry is provided)
        if results.get("industry"):
            roi_pct = financial_results["financial_metrics"]["roi_pct"]
            payback_years = financial_results["financial_metrics"][
                "payback_period_years"
            ]
            benchmarking_results = self.benchmarking.compare_to_industry(
                industry=results["industry"],
                calculated_roi=roi_pct,
                calculated_payback_months=payback_years * 12,
                capex=financial_results["lifecycle_costs"]["capex"]["total"],
                opex=financial_results["lifecycle_costs"]["opex_yearly"]["total"],
            )
            results["benchmarking"] = benchmarking_results
            results["analysis_modules"].append("benchmarking")

        # 8. Maturity Assessment (if provided)
        if "maturity_assessment" in input_data:
            maturity_results = self.benchmarking.assess_maturity(
                input_data["maturity_assessment"]["assessment_scores"]
            )
            results["maturity_assessment"] = maturity_results
            results["analysis_modules"].append("maturity_assessment")

        # Generate Executive Summary
        results["executive_summary"] = self._generate_executive_summary(results)

        # Generate Recommendations
        results["recommendations"] = self._generate_recommendations(results)

        return results

    def _generate_executive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary from all results"""
        financial = results.get("financial_impact", {})
        metrics = financial.get("financial_metrics", {})

        summary = {
            "total_investment": financial.get("lifecycle_costs", {})
            .get("capex", {})
            .get("total", 0),
            "npv": metrics.get("npv", 0),
            "roi_pct": metrics.get("roi_pct", 0),
            "payback_years": metrics.get("payback_period_years", 0),
            "irr_pct": metrics.get("irr_pct", 0),
        }

        # Add scenario recommendation if available
        if "scenarios" in results:
            summary["recommended_scenario"] = results["scenarios"]["comparison"][
                "recommendation"
            ]["recommended_scenario"]

        # Add maturity level if available
        if "maturity_assessment" in results:
            summary["maturity_level"] = results["maturity_assessment"][
                "maturity_level"
            ]["level"]

        return summary

    def _generate_recommendations(self, results: Dict[str, Any]) -> list:
        """Generate recommendations from all results"""
        recommendations = []

        # Financial recommendations
        financial = results.get("financial_impact", {})
        metrics = financial.get("financial_metrics", {})

        if metrics.get("npv", 0) > 0:
            recommendations.append(
                f"Positive NPV of ${metrics['npv']:,.0f} indicates strong financial viability"
            )
        else:
            recommendations.append(
                "Negative NPV suggests project may not be financially viable without adjustments"
            )

        if metrics.get("payback_period_years", 999) < 2:
            recommendations.append(
                "Excellent payback period - quick return on investment"
            )
        elif metrics.get("payback_period_years", 999) < 3:
            recommendations.append("Good payback period - acceptable investment timeline")
        else:
            recommendations.append(
                "Extended payback period - consider phased implementation"
            )

        # Benchmarking recommendations
        if "benchmarking" in results:
            bench = results["benchmarking"]
            if bench.get("roi_comparison", {}).get("performance") == "Above Average":
                recommendations.append(
                    "ROI exceeds industry average - strong competitive position"
                )

        # Digital ROI recommendations
        if "digital_roi" in results:
            recommendations.extend(results["digital_roi"].get("recommendations", []))

        # Maturity recommendations
        if "maturity_assessment" in results:
            maturity = results["maturity_assessment"]
            if maturity["maturity_level"]["level"] < 3:
                recommendations.append(
                    "Focus on building automation maturity through structured approach"
                )

        return recommendations
