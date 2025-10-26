"""
Unit Tests for Scenario Planning
================================
"""

import pytest
from backend.calculators.scenario_planning import ScenarioPlanningAnalyzer


class TestScenarioPlanningAnalyzer:
    """Test Scenario Planning Analyzer"""

    def test_generate_scenario_budget_conscious(self):
        analyzer = ScenarioPlanningAnalyzer()
        scenario = analyzer.generate_scenario(
            scenario_type="budget_conscious",
            base_capex=500000,
            base_opex=50000,
            base_benefits=200000,
        )

        assert scenario["scenario_type"] == "budget_conscious"
        assert scenario["capex"] == 500000 * 0.6  # 60% of base
        assert scenario["opex_yearly"] == 50000 * 0.7  # 70% of base
        assert scenario["annual_benefits"] == 200000 * 0.75  # 75% of base
        assert scenario["implementation_months"] == 12
        assert scenario["risk_level"] == "medium"

    def test_generate_scenario_strategic(self):
        analyzer = ScenarioPlanningAnalyzer()
        scenario = analyzer.generate_scenario(
            scenario_type="strategic_implementation",
            base_capex=500000,
            base_opex=50000,
            base_benefits=200000,
        )

        assert scenario["capex"] == 500000  # 100% of base
        assert scenario["opex_yearly"] == 50000  # 100% of base
        assert scenario["annual_benefits"] == 200000  # 100% of base

    def test_generate_scenario_enterprise(self):
        analyzer = ScenarioPlanningAnalyzer()
        scenario = analyzer.generate_scenario(
            scenario_type="enterprise_transformation",
            base_capex=500000,
            base_opex=50000,
            base_benefits=200000,
        )

        assert scenario["capex"] == 500000 * 1.5  # 150% of base
        assert scenario["opex_yearly"] == 50000 * 1.2  # 120% of base
        assert scenario["annual_benefits"] == 200000 * 1.3  # 130% of base

    def test_generate_scenario_invalid_type(self):
        analyzer = ScenarioPlanningAnalyzer()
        with pytest.raises(ValueError):
            analyzer.generate_scenario(
                scenario_type="invalid_scenario",
                base_capex=500000,
                base_opex=50000,
                base_benefits=200000,
            )

    def test_compare_scenarios(self):
        analyzer = ScenarioPlanningAnalyzer()
        result = analyzer.compare_scenarios(
            base_capex=500000,
            base_opex=50000,
            base_benefits=200000,
            project_years=5,
            discount_rate=0.10,
        )

        assert "scenarios" in result
        assert "comparison" in result
        assert len(result["scenarios"]) == 3
        assert "budget_conscious" in result["scenarios"]
        assert "strategic_implementation" in result["scenarios"]
        assert "enterprise_transformation" in result["scenarios"]

        # Check that each scenario has financial metrics
        for scenario in result["scenarios"].values():
            assert "financial_metrics" in scenario
            assert "npv" in scenario["financial_metrics"]
            assert "roi_pct" in scenario["financial_metrics"]

    def test_monte_carlo_simulation_basic(self):
        analyzer = ScenarioPlanningAnalyzer()

        def calc_npv(params):
            # Simple NPV calculation
            discount_rate = params["discount_rate"]
            cost_overrun = params.get("cost_overrun", 0)
            initial = 100000 * (1 + cost_overrun)
            cash_flows = [30000] * 5
            npv_value = sum(
                cf / ((1 + discount_rate) ** (i + 1))
                for i, cf in enumerate(cash_flows)
            )
            return npv_value - initial

        distributions = {
            "discount_rate": {"distribution": "normal", "mean": 0.10, "std": 0.02},
            "cost_overrun": {
                "distribution": "triangular",
                "low": 0,
                "mode": 0.1,
                "high": 0.3,
            },
        }

        result = analyzer.monte_carlo_simulation(
            calculate_npv_func=calc_npv,
            parameters_distributions=distributions,
            iterations=100,
            random_seed=42,
        )

        assert "mean" in result
        assert "median" in result
        assert "std" in result
        assert "probability_positive_npv" in result
        assert "percentiles" in result
        assert result["iterations"] == 100

    def test_risk_assessment(self):
        analyzer = ScenarioPlanningAnalyzer()

        scenario = {"risk_score": 3}
        monte_carlo_results = {
            "probability_positive_npv": 85.0,
            "std": 15000,
            "mean": 50000,
            "value_at_risk_5pct": 5000,
        }

        result = analyzer.risk_assessment(scenario, monte_carlo_results)

        assert "risk_rating" in result
        assert "risk_color" in result
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
