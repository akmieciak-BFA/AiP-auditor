"""
Unit Tests for TDABC Calculator
================================
"""

import pytest
from backend.calculators.tdabc import TDABCCalculator, TimeEquationsBuilder


class TestTDABCCalculator:
    """Test TDABC Calculator"""

    def test_calculate_practical_capacity_people(self):
        calc = TDABCCalculator()
        practical = calc.calculate_practical_capacity(
            theoretical_capacity_minutes=1000, resource_type="people"
        )
        assert practical == 800  # 80% of 1000

    def test_calculate_practical_capacity_machines(self):
        calc = TDABCCalculator()
        practical = calc.calculate_practical_capacity(
            theoretical_capacity_minutes=1000, resource_type="machines"
        )
        assert practical == 850  # 85% of 1000

    def test_calculate_capacity_cost_rate(self):
        calc = TDABCCalculator()
        rate = calc.calculate_capacity_cost_rate(
            total_cost=560000, practical_capacity_minutes=700000
        )
        assert rate == pytest.approx(0.8, abs=0.01)  # $0.80 per minute

    def test_calculate_cost_driver_rate(self):
        calc = TDABCCalculator()
        cost = calc.calculate_cost_driver_rate(unit_time_minutes=10, capacity_cost_rate=0.8)
        assert cost == 8.0  # $8 per unit

    def test_analyze_capacity_utilization_healthy(self):
        calc = TDABCCalculator()
        activities = [
            {"name": "Activity 1", "unit_time": 10, "volume": 1000},  # 10,000 minutes
            {"name": "Activity 2", "unit_time": 5, "volume": 2000},  # 10,000 minutes
        ]
        result = calc.analyze_capacity_utilization(
            practical_capacity=25000, activities=activities
        )

        assert result["utilization_rate"] == 80.0  # (20,000 / 25,000) * 100
        assert result["status"] == "HEALTHY"
        assert result["used_capacity"] == 20000
        assert result["unused_capacity"] == 5000

    def test_analyze_capacity_utilization_overcapacity(self):
        calc = TDABCCalculator()
        activities = [
            {"name": "Activity 1", "unit_time": 10, "volume": 500},  # 5,000 minutes
        ]
        result = calc.analyze_capacity_utilization(
            practical_capacity=10000, activities=activities
        )

        assert result["utilization_rate"] == 50.0
        assert result["status"] == "OVERCAPACITY"

    def test_analyze_capacity_utilization_bottleneck(self):
        calc = TDABCCalculator()
        activities = [
            {"name": "Activity 1", "unit_time": 10, "volume": 950},  # 9,500 minutes
        ]
        result = calc.analyze_capacity_utilization(
            practical_capacity=10000, activities=activities
        )

        assert result["utilization_rate"] == 95.0
        assert result["status"] == "BOTTLENECK"

    def test_calculate_activity_cost(self):
        calc = TDABCCalculator()
        result = calc.calculate_activity_cost(
            activity_name="Process Orders",
            unit_time=8,
            volume=1000,
            capacity_cost_rate=0.8,
        )

        assert result["cost_per_unit"] == 6.4  # 8 * 0.8
        assert result["total_cost"] == 6400  # 6.4 * 1000
        assert result["total_time_minutes"] == 8000

    def test_calculate_tdabc_full_analysis(self):
        calc = TDABCCalculator()
        activities = [
            {"name": "Process Orders", "unit_time": 8, "volume": 1000},
            {"name": "Handle Inquiries", "unit_time": 5, "volume": 2000},
        ]

        result = calc.calculate_tdabc_full_analysis(
            total_cost=560000,
            theoretical_capacity_minutes=876000,
            resource_type="people",
            activities=activities,
        )

        assert "summary" in result
        assert "utilization" in result
        assert "activities" in result
        assert "cost_allocation" in result
        assert len(result["activities"]) == 2


class TestTimeEquationsBuilder:
    """Test Time Equations Builder"""

    def test_build_time_equation_no_conditions(self):
        builder = TimeEquationsBuilder()
        time_eq = builder.build_time_equation(base_time=10, conditional_times=[])

        assert time_eq([]) == 10

    def test_build_time_equation_with_conditions(self):
        builder = TimeEquationsBuilder()
        time_eq = builder.build_time_equation(
            base_time=8,
            conditional_times=[
                {"condition": "international", "additional_time": 5},
                {"condition": "custom", "additional_time": 3},
            ],
        )

        assert time_eq([]) == 8
        assert time_eq(["international"]) == 13
        assert time_eq(["custom"]) == 11
        assert time_eq(["international", "custom"]) == 16

    def test_analyze_process_complexity(self):
        builder = TimeEquationsBuilder()
        time_eq = builder.build_time_equation(
            base_time=8,
            conditional_times=[
                {"condition": "international", "additional_time": 5},
                {"condition": "custom", "additional_time": 3},
            ],
        )

        scenarios = [
            {"name": "Simple", "conditions": [], "volume": 100},
            {"name": "International", "conditions": ["international"], "volume": 50},
            {"name": "Complex", "conditions": ["international", "custom"], "volume": 25},
        ]

        result = builder.analyze_process_complexity(
            time_equation=time_eq, condition_scenarios=scenarios, capacity_cost_rate=0.8
        )

        assert "scenarios" in result
        assert "summary" in result
        assert len(result["scenarios"]) == 3
        assert result["summary"]["total_time_minutes"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
