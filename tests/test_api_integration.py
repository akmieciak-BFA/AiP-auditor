"""
Integration Tests for API Endpoints
===================================

These tests verify that the API endpoints work correctly end-to-end.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health and info endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "BFA Audit" in data["message"]

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/calculator/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "modules" in data
        assert len(data["modules"]) == 8

    def test_api_info(self):
        """Test API info endpoint"""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = response.json()
        assert "modules" in data
        assert "methodologies" in data


class TestFinancialImpactEndpoint:
    """Test Financial Impact endpoint"""

    def test_financial_impact_basic(self):
        """Test basic financial impact calculation"""
        data = {
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
            "production_increase_pct": 0,
            "capex_breakdown": {
                "hardware": 200000,
                "installation": 100000,
                "software_licenses": 50000,
                "services": 30000,
                "infrastructure": 50000,
                "training": 20000,
            },
            "opex_yearly": {
                "maintenance_contracts": 30000,
                "spare_parts": 10000,
                "administration": 15000,
                "training": 5000,
                "upgrades": 10000,
                "cybersecurity": 5000,
            },
        }

        response = client.post("/api/calculator/financial-impact", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "results" in result
        assert "financial_metrics" in result["results"]

    def test_financial_impact_invalid_input(self):
        """Test financial impact with invalid input"""
        data = {
            "project_capital": -500000,  # Negative value should fail
        }

        response = client.post("/api/calculator/financial-impact", json=data)
        assert response.status_code == 422  # Validation error


class TestScenarioComparisonEndpoint:
    """Test Scenario Comparison endpoint"""

    def test_scenario_comparison_basic(self):
        """Test basic scenario comparison"""
        data = {
            "base_capex": 500000,
            "base_opex": 50000,
            "base_annual_benefits": 200000,
            "project_years": 5,
            "discount_rate": 0.10,
        }

        response = client.post("/api/calculator/scenarios/compare", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "results" in result
        assert "scenarios" in result["results"]
        assert "comparison" in result["results"]

        # Check that all 3 scenarios are present
        scenarios = result["results"]["scenarios"]
        assert "budget_conscious" in scenarios
        assert "strategic_implementation" in scenarios
        assert "enterprise_transformation" in scenarios

        # Check that comparison has recommendation
        assert "recommendation" in result["results"]["comparison"]

    def test_scenario_comparison_custom_years(self):
        """Test scenario comparison with different project years"""
        data = {
            "base_capex": 500000,
            "base_opex": 50000,
            "base_annual_benefits": 200000,
            "project_years": 10,  # 10 years instead of default 5
            "discount_rate": 0.08,
        }

        response = client.post("/api/calculator/scenarios/compare", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"


class TestTDABCEndpoint:
    """Test TDABC endpoint"""

    def test_tdabc_basic(self):
        """Test basic TDABC calculation"""
        data = {
            "total_cost": 560000,
            "theoretical_capacity_minutes": 876000,
            "resource_type": "people",
            "activities": [
                {"name": "Process Orders", "unit_time": 8, "volume": 1000},
                {"name": "Handle Inquiries", "unit_time": 5, "volume": 2000},
            ],
        }

        response = client.post("/api/calculator/tdabc", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "utilization" in result["results"]
        assert "activities" in result["results"]

    def test_tdabc_machines(self):
        """Test TDABC with machines resource type"""
        data = {
            "total_cost": 1000000,
            "theoretical_capacity_minutes": 1000000,
            "resource_type": "machines",
            "activities": [
                {"name": "Production Run", "unit_time": 60, "volume": 5000},
            ],
        }

        response = client.post("/api/calculator/tdabc", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"


class TestBenchmarkingEndpoints:
    """Test Benchmarking endpoints"""

    def test_get_industry_benchmarks(self):
        """Test getting industry benchmarks"""
        response = client.get("/api/calculator/benchmarks/manufacturing")
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert result["industry"] == "manufacturing"
        assert "benchmarks" in result

    def test_get_invalid_industry_benchmarks(self):
        """Test getting benchmarks for invalid industry"""
        response = client.get("/api/calculator/benchmarks/invalid_industry")
        assert response.status_code == 404

    def test_benchmarking_comparison(self):
        """Test benchmarking comparison"""
        data = {
            "industry": "manufacturing",
            "calculated_roi": 25.5,
            "calculated_payback_months": 24,
            "capex": 500000,
            "opex": 75000,
        }

        response = client.post("/api/calculator/benchmarking", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "roi_comparison" in result["results"]
        assert "payback_comparison" in result["results"]


class TestMaturityAssessmentEndpoint:
    """Test Maturity Assessment endpoint"""

    def test_maturity_assessment_basic(self):
        """Test basic maturity assessment"""
        data = {
            "assessment_scores": {
                "strategy_governance": 75,
                "technology_infrastructure": 60,
                "process_operations": 70,
                "people_culture": 55,
                "measurement_optimization": 65,
            }
        }

        response = client.post("/api/calculator/maturity-assessment", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "overall_score" in result["results"]
        assert "maturity_level" in result["results"]

    def test_maturity_assessment_high_maturity(self):
        """Test maturity assessment with high scores"""
        data = {
            "assessment_scores": {
                "strategy_governance": 90,
                "technology_infrastructure": 85,
                "process_operations": 88,
                "people_culture": 82,
                "measurement_optimization": 87,
            }
        }

        response = client.post("/api/calculator/maturity-assessment", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        # Should be level 4 or 5
        assert result["results"]["maturity_level"]["level"] >= 4


class TestDigitalROIEndpoint:
    """Test Digital ROI endpoint"""

    def test_digital_roi_basic(self):
        """Test basic Digital ROI calculation"""
        data = {
            "current_metrics": {
                "customers": {"nps_score": 30, "csat_score": 75},
                "employees": {"engagement_score": 65, "turnover_rate": 15},
            },
            "target_metrics": {
                "customers": {"nps_score": 50, "csat_score": 85},
                "employees": {"engagement_score": 80, "turnover_rate": 10},
            },
        }

        response = client.post("/api/calculator/digital-roi", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "overall" in result["results"]
        assert "dimensions" in result["results"]


class TestComprehensiveAnalysis:
    """Test Comprehensive Analysis endpoint"""

    def test_comprehensive_analysis_minimal(self):
        """Test comprehensive analysis with minimal input"""
        data = {
            "project_name": "Test Project",
            "industry": "manufacturing",
            "financial_impact": {
                "project_capital": 500000,
                "commissioning_cost": 50000,
                "fixed_assets": 100000,
                "inventory": 20000,
                "operating_cash": 10000,
                "financial_wc": 5000,
                "cost_reductions": {
                    "feedstocks_energy": {"baseline": 100000, "reduction_pct": 15}
                },
                "current_revenue": 1000000,
                "quality_premium_pct": 5,
                "production_increase_pct": 0,
                "capex_breakdown": {
                    "hardware": 200000,
                    "installation": 100000,
                    "software_licenses": 50000,
                    "services": 30000,
                    "infrastructure": 50000,
                    "training": 20000,
                },
                "opex_yearly": {
                    "maintenance_contracts": 30000,
                    "spare_parts": 10000,
                    "administration": 15000,
                    "training": 5000,
                    "upgrades": 10000,
                    "cybersecurity": 5000,
                },
            },
            "include_scenario_planning": True,
        }

        response = client.post("/api/calculator/comprehensive-analysis", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["project_name"] == "Test Project"
        assert "financial_impact" in result
        assert "scenarios" in result
        assert "executive_summary" in result
        assert "recommendations" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
