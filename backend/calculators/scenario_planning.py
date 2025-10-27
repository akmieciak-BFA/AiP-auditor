"""
Module 7: Scenario Planning & Sensitivity Analysis
===================================================

Components:
- Scenario Templates (Budget Conscious, Strategic, Enterprise)
- Sensitivity Analysis (Tornado Diagram)
- Monte Carlo Simulation
- Risk Assessment
"""

from typing import Dict, List, Callable, Optional
import numpy as np
from scipy import stats


class ScenarioPlanningAnalyzer:
    """Analyze scenarios and perform sensitivity analysis"""

    SCENARIO_TEMPLATES = {
        "budget_conscious": {
            "name": "Budget Conscious",
            "description": "Minimal investment with proven ROI",
            "capex_multiplier": 0.6,
            "opex_multiplier": 0.7,
            "benefit_multiplier": 0.75,
            "implementation_months": 12,
            "risk_level": "medium",
            "risk_score": 5,  # 1-10 scale
        },
        "strategic_implementation": {
            "name": "Strategic Implementation",
            "description": "Balanced approach with optimal risk-reward",
            "capex_multiplier": 1.0,
            "opex_multiplier": 1.0,
            "benefit_multiplier": 1.0,
            "implementation_months": 8,
            "risk_level": "low",
            "risk_score": 3,
        },
        "enterprise_transformation": {
            "name": "Enterprise Transformation",
            "description": "Comprehensive solution with maximum benefits",
            "capex_multiplier": 1.5,
            "opex_multiplier": 1.2,
            "benefit_multiplier": 1.3,
            "implementation_months": 6,
            "risk_level": "very_low",
            "risk_score": 2,
        },
    }

    def generate_scenario(
        self,
        scenario_type: str,
        base_capex: float,
        base_opex: float,
        base_benefits: float,
        custom_multipliers: Optional[Dict[str, float]] = None,
    ) -> Dict[str, any]:
        """
        Generate scenario based on template

        Args:
            scenario_type: One of 'budget_conscious', 'strategic_implementation', 'enterprise_transformation'
            base_capex: Base CapEx amount
            base_opex: Base annual OpEx
            base_benefits: Base annual benefits
            custom_multipliers: Optional custom multipliers to override template

        Returns:
            Dictionary with scenario details
        """
        if scenario_type not in self.SCENARIO_TEMPLATES:
            raise ValueError(
                f"Invalid scenario type. Must be one of: {list(self.SCENARIO_TEMPLATES.keys())}"
            )

        template = self.SCENARIO_TEMPLATES[scenario_type].copy()

        # Apply custom multipliers if provided
        if custom_multipliers:
            template.update(custom_multipliers)

        return {
            "scenario_type": scenario_type,
            "name": template["name"],
            "description": template["description"],
            "capex": base_capex * template["capex_multiplier"],
            "opex_yearly": base_opex * template["opex_multiplier"],
            "annual_benefits": base_benefits * template["benefit_multiplier"],
            "implementation_months": template["implementation_months"],
            "risk_level": template["risk_level"],
            "risk_score": template["risk_score"],
            "multipliers": {
                "capex": template["capex_multiplier"],
                "opex": template["opex_multiplier"],
                "benefits": template["benefit_multiplier"],
            },
        }

    def compare_scenarios(
        self,
        base_capex: float,
        base_opex: float,
        base_benefits: float,
        project_years: int = 5,
        discount_rate: float = 0.10,
    ) -> Dict[str, any]:
        """
        Generate and compare all three standard scenarios

        Args:
            base_capex: Base CapEx amount
            base_opex: Base annual OpEx
            base_benefits: Base annual benefits
            project_years: Number of years to evaluate
            discount_rate: Discount rate for NPV

        Returns:
            Dictionary with all scenarios and comparison
        """
        from .financial_impact import FinancialMetricsCalculator

        calc = FinancialMetricsCalculator()
        scenarios = {}

        for scenario_type in self.SCENARIO_TEMPLATES.keys():
            scenario = self.generate_scenario(
                scenario_type, base_capex, base_opex, base_benefits
            )

            # Calculate financial metrics for this scenario
            metrics = calc.calculate_comprehensive_metrics(
                initial_investment=scenario["capex"],
                annual_benefits=scenario["annual_benefits"],
                annual_costs=scenario["opex_yearly"],
                project_years=project_years,
                discount_rate=discount_rate,
                invested_capital=scenario["capex"],  # Simplified
            )

            scenarios[scenario_type] = {
                **scenario,
                "financial_metrics": metrics,
            }

        # Generate comparison
        comparison = self._generate_comparison(scenarios)

        return {"scenarios": scenarios, "comparison": comparison}

    def _generate_comparison(self, scenarios: Dict[str, any]) -> Dict[str, any]:
        """
        Generate comparison summary and recommendation

        Args:
            scenarios: Dictionary of scenario results

        Returns:
            Comparison summary with recommendation
        """
        # Extract key metrics for comparison
        comparison_data = []

        for scenario_type, scenario in scenarios.items():
            metrics = scenario["financial_metrics"]
            comparison_data.append(
                {
                    "scenario": scenario_type,
                    "name": scenario["name"],
                    "npv": metrics["npv"],
                    "roi_pct": metrics["roi_pct"],
                    "payback_years": metrics["payback_period_years"],
                    "risk_score": scenario["risk_score"],
                    "capex": scenario["capex"],
                }
            )

        # Sort by NPV (descending)
        comparison_data.sort(key=lambda x: x["npv"], reverse=True)

        # Generate recommendation
        best_npv = comparison_data[0]
        best_payback = min(comparison_data, key=lambda x: x["payback_years"])
        best_risk_adjusted = min(
            comparison_data, key=lambda x: x["risk_score"] / (x["npv"] + 1)
        )

        recommendation = self._generate_recommendation(
            best_npv, best_payback, best_risk_adjusted
        )

        return {
            "ranking_by_npv": comparison_data,
            "best_npv": best_npv["scenario"],
            "best_payback": best_payback["scenario"],
            "best_risk_adjusted": best_risk_adjusted["scenario"],
            "recommendation": recommendation,
        }

    def _generate_recommendation(
        self, best_npv: Dict, best_payback: Dict, best_risk_adjusted: Dict
    ) -> Dict[str, str]:
        """Generate recommendation text"""

        if best_npv["scenario"] == best_payback["scenario"]:
            recommended = best_npv["scenario"]
            reason = "This scenario offers both the highest NPV and fastest payback period."
        elif best_npv["npv"] > 0 and best_npv["payback_years"] < 3:
            recommended = best_npv["scenario"]
            reason = "This scenario maximizes value with acceptable payback period."
        else:
            recommended = best_risk_adjusted["scenario"]
            reason = "This scenario offers the best risk-adjusted return."

        return {"recommended_scenario": recommended, "reason": reason}

    def sensitivity_analysis(
        self,
        base_npv: float,
        parameters: Dict[str, Dict[str, any]],
        variation_pct: float = 20,
    ) -> List[Dict[str, any]]:
        """
        Perform sensitivity analysis (Tornado diagram data)

        Args:
            base_npv: Base case NPV
            parameters: Dictionary of parameters with 'base' value and 'calculate_npv' function
                       Example: {'discount_rate': {'base': 0.10, 'calculate_npv': func}}
            variation_pct: Percentage variation to test (default ±20%)

        Returns:
            List of sensitivity results sorted by impact (for Tornado diagram)
        """
        results = []

        for param_name, param_info in parameters.items():
            base_value = param_info["base"]
            calc_func = param_info["calculate_npv"]

            # Calculate NPV at ±variation_pct
            low_value = base_value * (1 - variation_pct / 100)
            high_value = base_value * (1 + variation_pct / 100)

            try:
                npv_low = calc_func(low_value)
                npv_high = calc_func(high_value)

                # Impact = range of NPV change
                impact = abs(npv_high - npv_low)

                results.append(
                    {
                        "parameter": param_name,
                        "base_value": base_value,
                        "low_value": low_value,
                        "high_value": high_value,
                        "npv_base": base_npv,
                        "npv_low": npv_low,
                        "npv_high": npv_high,
                        "impact": impact,
                        "impact_pct": (impact / abs(base_npv)) * 100
                        if base_npv != 0
                        else 0,
                    }
                )
            except Exception as e:
                # Skip parameters that cause calculation errors
                continue

        # Sort by impact (descending) for Tornado diagram
        results.sort(key=lambda x: x["impact"], reverse=True)

        return results

    def monte_carlo_simulation(
        self,
        calculate_npv_func: Callable,
        parameters_distributions: Dict[str, Dict[str, any]],
        iterations: int = 1000,
        random_seed: Optional[int] = None,
    ) -> Dict[str, any]:
        """
        Perform Monte Carlo simulation for NPV distribution

        Args:
            calculate_npv_func: Function that takes parameters dict and returns NPV
            parameters_distributions: Dictionary of parameter distributions
                Example: {
                    'discount_rate': {'distribution': 'normal', 'mean': 0.10, 'std': 0.02},
                    'cost_overrun': {'distribution': 'triangular', 'low': 0, 'mode': 0.1, 'high': 0.3}
                }
            iterations: Number of Monte Carlo iterations
            random_seed: Optional random seed for reproducibility

        Returns:
            Dictionary with statistical summary and full distribution
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        npv_results = []

        for _ in range(iterations):
            # Sample parameters from distributions
            sampled_params = {}

            for param, dist_info in parameters_distributions.items():
                dist_type = dist_info["distribution"]

                if dist_type == "normal":
                    sampled_params[param] = np.random.normal(
                        dist_info["mean"], dist_info["std"]
                    )
                elif dist_type == "uniform":
                    sampled_params[param] = np.random.uniform(
                        dist_info["low"], dist_info["high"]
                    )
                elif dist_type == "triangular":
                    sampled_params[param] = np.random.triangular(
                        dist_info["low"], dist_info["mode"], dist_info["high"]
                    )
                elif dist_type == "lognormal":
                    sampled_params[param] = np.random.lognormal(
                        dist_info["mean"], dist_info["sigma"]
                    )
                else:
                    raise ValueError(f"Unsupported distribution type: {dist_type}")

            # Calculate NPV with sampled parameters
            try:
                npv = calculate_npv_func(sampled_params)
                npv_results.append(npv)
            except:
                # Skip failed calculations
                continue

        npv_array = np.array(npv_results)

        # Calculate statistics
        mean_npv = np.mean(npv_array)
        median_npv = np.median(npv_array)
        std_npv = np.std(npv_array)
        min_npv = np.min(npv_array)
        max_npv = np.max(npv_array)

        # Percentiles
        percentiles = {
            "p5": np.percentile(npv_array, 5),
            "p10": np.percentile(npv_array, 10),
            "p25": np.percentile(npv_array, 25),
            "p50": np.percentile(npv_array, 50),
            "p75": np.percentile(npv_array, 75),
            "p90": np.percentile(npv_array, 90),
            "p95": np.percentile(npv_array, 95),
        }

        # Probability of positive NPV
        probability_positive = (npv_array > 0).sum() / len(npv_array) * 100

        # Value at Risk (VaR) - 5th percentile loss
        var_5 = percentiles["p5"]

        return {
            "iterations": len(npv_results),
            "mean": round(mean_npv, 2),
            "median": round(median_npv, 2),
            "std": round(std_npv, 2),
            "min": round(min_npv, 2),
            "max": round(max_npv, 2),
            "percentiles": {k: round(v, 2) for k, v in percentiles.items()},
            "probability_positive_npv": round(probability_positive, 2),
            "value_at_risk_5pct": round(var_5, 2),
            "confidence_interval_95": (
                round(percentiles["p5"], 2),
                round(percentiles["p95"], 2),
            ),
            "distribution_data": npv_array.tolist(),
        }

    def risk_assessment(
        self, scenario: Dict[str, any], monte_carlo_results: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Perform risk assessment based on scenario and Monte Carlo results

        Args:
            scenario: Scenario dictionary
            monte_carlo_results: Results from monte_carlo_simulation()

        Returns:
            Risk assessment with rating and recommendations
        """
        risk_score = scenario.get("risk_score", 5)
        prob_positive = monte_carlo_results["probability_positive_npv"]
        std = monte_carlo_results["std"]
        mean = monte_carlo_results["mean"]

        # Calculate Coefficient of Variation (CV)
        cv = abs(std / mean) if mean != 0 else float("inf")

        # Risk rating based on multiple factors
        if prob_positive > 90 and cv < 0.3 and risk_score < 4:
            risk_rating = "Low Risk"
            risk_color = "green"
        elif prob_positive > 75 and cv < 0.5 and risk_score < 6:
            risk_rating = "Medium Risk"
            risk_color = "yellow"
        elif prob_positive > 60 and cv < 0.8:
            risk_rating = "Medium-High Risk"
            risk_color = "orange"
        else:
            risk_rating = "High Risk"
            risk_color = "red"

        # Generate risk mitigation recommendations
        recommendations = []

        if prob_positive < 80:
            recommendations.append(
                "Consider implementing project in phases to reduce risk"
            )

        if cv > 0.5:
            recommendations.append(
                "High variability in outcomes - focus on locking in key assumptions"
            )

        if risk_score > 5:
            recommendations.append(
                "Scenario has inherent implementation risks - ensure strong project management"
            )

        if monte_carlo_results["value_at_risk_5pct"] < 0:
            recommendations.append(
                f"Worst case scenario (5% probability) shows loss - consider contingency planning"
            )

        return {
            "risk_rating": risk_rating,
            "risk_color": risk_color,
            "risk_score": risk_score,
            "probability_positive": prob_positive,
            "coefficient_of_variation": round(cv, 3),
            "recommendations": recommendations,
        }
