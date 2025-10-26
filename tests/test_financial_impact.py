"""
Unit Tests for Financial Impact Calculator
==========================================
"""

import pytest
from backend.calculators.financial_impact import (
    CapitalAnalyzer,
    CostReductionAnalyzer,
    RevenueEnhancementAnalyzer,
    LifeCycleCostAnalyzer,
    FinancialMetricsCalculator,
)


class TestCapitalAnalyzer:
    """Test Capital Analyzer"""

    def test_calculate_fixed_capital(self):
        analyzer = CapitalAnalyzer()
        result = analyzer.calculate_fixed_capital(
            project_capital=500000, commissioning_cost=50000, fixed_assets=100000
        )
        assert result == 650000

    def test_calculate_working_capital(self):
        analyzer = CapitalAnalyzer()
        result = analyzer.calculate_working_capital(
            inventory=20000, operating_cash=10000, financial_wc=5000
        )
        assert result == 35000

    def test_calculate_invested_capital(self):
        analyzer = CapitalAnalyzer()
        result = analyzer.calculate_invested_capital(
            fixed_capital=650000, working_capital=35000
        )
        assert result == 685000


class TestFinancialMetricsCalculator:
    """Test Financial Metrics Calculator"""

    def test_calculate_roic(self):
        calc = FinancialMetricsCalculator()
        roic = calc.calculate_roic(
            after_tax_cash_adjusted_income=100000, invested_capital=500000
        )
        assert roic == 20.0

    def test_calculate_roic_zero_capital(self):
        calc = FinancialMetricsCalculator()
        roic = calc.calculate_roic(
            after_tax_cash_adjusted_income=100000, invested_capital=0
        )
        assert roic == 0.0

    def test_calculate_npv_positive(self):
        calc = FinancialMetricsCalculator()
        npv = calc.calculate_npv(
            initial_investment=100000,
            cash_flows=[30000, 30000, 30000, 30000, 30000],
            discount_rate=0.10,
        )
        assert npv > 0  # Should be positive with these inputs

    def test_calculate_npv_negative(self):
        calc = FinancialMetricsCalculator()
        npv = calc.calculate_npv(
            initial_investment=500000,
            cash_flows=[10000, 10000, 10000, 10000, 10000],
            discount_rate=0.10,
        )
        assert npv < 0  # Should be negative

    def test_calculate_irr(self):
        calc = FinancialMetricsCalculator()
        irr_value = calc.calculate_irr(
            initial_investment=100000, cash_flows=[30000, 30000, 30000, 30000, 30000]
        )
        assert irr_value is not None
        assert irr_value > 0  # Should have positive IRR

    def test_calculate_payback_period(self):
        calc = FinancialMetricsCalculator()
        payback = calc.calculate_payback_period(
            initial_investment=100000, annual_cash_flow=25000
        )
        assert payback == 4.0

    def test_calculate_payback_period_zero_cashflow(self):
        calc = FinancialMetricsCalculator()
        payback = calc.calculate_payback_period(
            initial_investment=100000, annual_cash_flow=0
        )
        assert payback == float("inf")

    def test_calculate_roi_percentage(self):
        calc = FinancialMetricsCalculator()
        roi = calc.calculate_roi_percentage(net_benefit=50000, total_investment=100000)
        assert roi == 50.0

    def test_calculate_benefit_cost_ratio(self):
        calc = FinancialMetricsCalculator()
        bcr = calc.calculate_benefit_cost_ratio(total_benefits=150000, total_costs=100000)
        assert bcr == 1.5

    def test_comprehensive_metrics(self):
        calc = FinancialMetricsCalculator()
        metrics = calc.calculate_comprehensive_metrics(
            initial_investment=500000,
            annual_benefits=200000,
            annual_costs=50000,
            project_years=5,
            discount_rate=0.10,
            invested_capital=500000,
            tax_rate=0.21,
        )

        assert "roic_pct" in metrics
        assert "npv" in metrics
        assert "irr_pct" in metrics
        assert "payback_period_years" in metrics
        assert "roi_pct" in metrics
        assert metrics["npv"] > 0  # Should be profitable


class TestCostReductionAnalyzer:
    """Test Cost Reduction Analyzer"""

    def test_calculate_category_savings(self):
        analyzer = CostReductionAnalyzer()
        savings = analyzer.calculate_category_savings(
            baseline_cost=100000, reduction_percentage=20
        )
        assert savings == 20000

    def test_calculate_total_savings(self):
        analyzer = CostReductionAnalyzer()
        baseline_costs = {
            "feedstocks_energy": 100000,
            "maintenance_scheduled": 50000,
            "staffing": 80000,
        }
        reduction_percentages = {
            "feedstocks_energy": 15,
            "maintenance_scheduled": 20,
            "staffing": 10,
        }

        result = analyzer.calculate_total_savings(baseline_costs, reduction_percentages)

        assert "total_annual_savings" in result
        assert "breakdown" in result
        expected_total = (100000 * 0.15) + (50000 * 0.20) + (80000 * 0.10)
        assert result["total_annual_savings"] == expected_total


class TestLifeCycleCostAnalyzer:
    """Test Life Cycle Cost Analyzer"""

    def test_calculate_capex(self):
        analyzer = LifeCycleCostAnalyzer()
        capex = analyzer.calculate_capex(
            hardware=200000,
            installation=100000,
            infrastructure=50000,
            software_licenses=50000,
            services=30000,
            training=20000,
        )

        assert capex["total"] == 450000
        assert capex["hardware"] == 200000

    def test_calculate_opex_yearly(self):
        analyzer = LifeCycleCostAnalyzer()
        opex = analyzer.calculate_opex_yearly(
            maintenance_contracts=30000,
            spare_parts=10000,
            administration=15000,
            training=5000,
            upgrades=10000,
            cybersecurity=5000,
        )

        assert opex["total"] == 75000

    def test_project_opex_5_years(self):
        analyzer = LifeCycleCostAnalyzer()
        projection = analyzer.project_opex_5_years(
            year1_opex=100000, inflation_rate=0.03
        )

        assert len(projection) == 5
        assert projection[0] == 100000
        assert projection[1] > projection[0]  # Should increase with inflation
        assert projection[4] > projection[3]

    def test_calculate_total_life_cycle_cost(self):
        analyzer = LifeCycleCostAnalyzer()
        opex_projection = [100000, 103000, 106090, 109273, 112551]
        lcc = analyzer.calculate_total_life_cycle_cost(
            capex=500000, opex_projection=opex_projection
        )

        assert "capex" in lcc
        assert "total_opex" in lcc
        assert "total_life_cycle_cost" in lcc
        assert lcc["total_life_cycle_cost"] == lcc["capex"] + lcc["total_opex"]
        assert lcc["opex_percentage"] + lcc["capex_percentage"] == pytest.approx(100.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
