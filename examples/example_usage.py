"""
Example Usage of BFA Audit App Calculator API
==============================================

This file demonstrates how to use the calculator API endpoints.
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def example_1_financial_impact():
    """Example 1: Financial Impact Calculation"""
    print_section("Example 1: Financial Impact Calculation")

    url = f"{BASE_URL}/api/calculator/financial-impact"

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
            "staffing": {"baseline": 80000, "reduction_pct": 10},
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
        "discount_rate": 0.10,
        "tax_rate": 0.21,
        "project_years": 5,
    }

    response = requests.post(url, json=data)
    results = response.json()

    metrics = results["results"]["financial_metrics"]

    print("Financial Metrics:")
    print(f"  NPV: ${metrics['npv']:,.2f}")
    print(f"  ROI: {metrics['roi_pct']:.2f}%")
    print(f"  IRR: {metrics['irr_pct']:.2f}%")
    print(f"  Payback Period: {metrics['payback_period_years']:.2f} years")
    print(f"  ROIC: {metrics['roic_pct']:.2f}%")
    print(f"  Benefit-Cost Ratio: {metrics['benefit_cost_ratio']:.2f}")

    print("\nInterpretation:")
    if metrics["npv"] > 0:
        print("  ✅ Positive NPV - Project is financially viable")
    else:
        print("  ❌ Negative NPV - Project may not be financially viable")

    if metrics["payback_period_years"] < 3:
        print("  ✅ Quick payback period")
    else:
        print("  ⚠️  Extended payback period")


def example_2_scenario_comparison():
    """Example 2: Scenario Comparison"""
    print_section("Example 2: Scenario Comparison")

    url = f"{BASE_URL}/api/calculator/scenarios/compare"

    data = {
        "base_capex": 500000,
        "base_opex": 50000,
        "base_annual_benefits": 200000,
        "project_years": 5,
        "discount_rate": 0.10,
    }

    response = requests.post(url, json=data)
    results = response.json()

    print("Scenario Comparison:\n")

    for scenario_name, scenario_data in results["results"]["scenarios"].items():
        metrics = scenario_data["financial_metrics"]
        print(f"{scenario_data['name']}:")
        print(f"  CapEx: ${scenario_data['capex']:,.0f}")
        print(f"  Annual OpEx: ${scenario_data['opex_yearly']:,.0f}")
        print(f"  Annual Benefits: ${scenario_data['annual_benefits']:,.0f}")
        print(f"  NPV: ${metrics['npv']:,.2f}")
        print(f"  ROI: {metrics['roi_pct']:.2f}%")
        print(f"  Payback: {metrics['payback_period_years']:.2f} years")
        print(f"  Risk Level: {scenario_data['risk_level']}")
        print()

    recommendation = results["results"]["comparison"]["recommendation"]
    print("Recommendation:")
    print(f"  Scenario: {recommendation['recommended_scenario']}")
    print(f"  Reason: {recommendation['reason']}")


def example_3_industry_benchmarking():
    """Example 3: Industry Benchmarking"""
    print_section("Example 3: Industry Benchmarking")

    url = f"{BASE_URL}/api/calculator/benchmarking"

    data = {
        "industry": "manufacturing",
        "calculated_roi": 25.5,
        "calculated_payback_months": 24,
        "capex": 500000,
        "opex": 75000,
    }

    response = requests.post(url, json=data)
    results = response.json()

    print("Industry Benchmarking (Manufacturing):\n")

    roi_comp = results["results"]["roi_comparison"]
    print(f"ROI Comparison:")
    print(f"  Your Project: {roi_comp['project_roi']:.1f}%")
    print(f"  Industry Avg: {roi_comp['industry_avg']:.1f}%")
    print(f"  Difference: {roi_comp['vs_industry']:+.1f}%")
    print(f"  Performance: {roi_comp['performance']}")

    payback_comp = results["results"]["payback_comparison"]
    print(f"\nPayback Comparison:")
    print(f"  Your Project: {payback_comp['project_payback_months']:.1f} months")
    print(f"  Industry Avg: {payback_comp['industry_avg_months']:.1f} months")
    print(f"  Difference: {payback_comp['vs_industry']:+.1f} months")
    print(f"  Performance: {payback_comp['performance']}")


def example_4_maturity_assessment():
    """Example 4: Maturity Assessment"""
    print_section("Example 4: Maturity Assessment")

    url = f"{BASE_URL}/api/calculator/maturity-assessment"

    data = {
        "assessment_scores": {
            "strategy_governance": 75,
            "technology_infrastructure": 60,
            "process_operations": 70,
            "people_culture": 55,
            "measurement_optimization": 65,
        }
    }

    response = requests.post(url, json=data)
    results = response.json()

    print("Maturity Assessment:\n")

    print(f"Overall Score: {results['results']['overall_score']:.1f}/100")
    print(
        f"Maturity Level: {results['results']['maturity_level']['level']} - {results['results']['maturity_level']['name']}"
    )
    print(f"Description: {results['results']['maturity_level']['description']}")

    print(f"\nDimension Scores:")
    for dim, score in results["results"]["dimension_scores"].items():
        print(f"  {dim}: {score}")

    if results["results"]["strengths"]:
        print(f"\nStrengths: {', '.join(results['results']['strengths'])}")

    if results["results"]["weaknesses"]:
        print(f"Weaknesses: {', '.join(results['results']['weaknesses'])}")


def example_5_tdabc():
    """Example 5: TDABC Analysis"""
    print_section("Example 5: TDABC Analysis")

    url = f"{BASE_URL}/api/calculator/tdabc"

    data = {
        "total_cost": 560000,
        "theoretical_capacity_minutes": 876000,
        "resource_type": "people",
        "activities": [
            {"name": "Process Orders", "unit_time": 8, "volume": 1000},
            {"name": "Handle Inquiries", "unit_time": 5, "volume": 2000},
            {"name": "Quality Control", "unit_time": 10, "volume": 500},
        ],
    }

    response = requests.post(url, json=data)
    results = response.json()

    print("TDABC Analysis:\n")

    summary = results["results"]["summary"]
    print(f"Capacity Cost Rate: ${summary['capacity_cost_rate']:.4f}/minute")
    print(
        f"Practical Capacity: {summary['practical_capacity_minutes']:,.0f} minutes/year"
    )

    utilization = results["results"]["utilization"]
    print(f"\nCapacity Utilization: {utilization['utilization_rate']:.1f}%")
    print(f"Status: {utilization['status']}")
    print(f"Recommendation: {utilization['recommendation']}")

    print(f"\nActivity Costs:")
    for activity in results["results"]["activities"]:
        print(f"  {activity['activity_name']}:")
        print(f"    Volume: {activity['volume']}")
        print(f"    Cost per Unit: ${activity['cost_per_unit']:.2f}")
        print(f"    Total Cost: ${activity['total_cost']:,.2f}")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("  BFA Audit App - Calculator API Examples")
    print("=" * 60)

    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/api/calculator/health")
        if response.status_code != 200:
            print("\n❌ Error: Server is not running!")
            print("Please start the server with: python run.py")
            return

        print("\n✅ Server is running\n")

        # Run examples
        example_1_financial_impact()
        example_2_scenario_comparison()
        example_3_industry_benchmarking()
        example_4_maturity_assessment()
        example_5_tdabc()

        print("\n" + "=" * 60)
        print("  All examples completed successfully!")
        print("=" * 60 + "\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server!")
        print("Please start the server with: python run.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
