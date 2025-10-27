"""
Module 3: Digital ROI Framework (6 Dimensions)
==============================================

Based on PwC Strategy& - Digital ROI Framework

6 Strategic Focus Areas:
1. Customers
2. Employees
3. Operations
4. Safety & Soundness
5. Infrastructure
6. Disruption & Innovation
"""

from typing import Dict, List


class DigitalROIFramework:
    """
    Holistic Digital ROI assessment across 6 strategic dimensions
    """

    DIMENSIONS = {
        "customers": {
            "weight": 0.20,
            "metrics": [
                "nps_score",
                "social_sentiment",
                "csat_score",
                "response_time",
                "first_contact_resolution",
            ],
            "description": "Customer experience and satisfaction improvements",
        },
        "employees": {
            "weight": 0.15,
            "metrics": [
                "engagement_score",
                "employee_nps",
                "collaboration_index",
                "turnover_rate",
                "digital_adoption_rate",
            ],
            "description": "Employee satisfaction and productivity",
        },
        "operations": {
            "weight": 0.25,
            "metrics": [
                "throughput",
                "inventory_efficiency",
                "supply_chain_efficiency",
                "cycle_time",
                "operational_efficiency_ratio",
            ],
            "description": "Operational efficiency and effectiveness",
        },
        "safety_soundness": {
            "weight": 0.15,
            "metrics": [
                "threats_detected",
                "privacy_breaches",
                "fraud_losses",
                "incident_response_time",
                "compliance_rate",
            ],
            "description": "Security, risk management, and compliance",
        },
        "infrastructure": {
            "weight": 0.15,
            "metrics": [
                "implementation_speed",
                "system_uptime",
                "issue_resolution_time",
                "infrastructure_cost_efficiency",
                "tech_debt_reduction",
            ],
            "description": "Technology infrastructure and delivery",
        },
        "disruption_innovation": {
            "weight": 0.10,
            "metrics": [
                "budget_pct_disruptive_tech",
                "ideas_to_concept_rate",
                "new_customers_from_innovation",
                "innovation_velocity",
                "time_to_market",
            ],
            "description": "Innovation capability and market disruption",
        },
    }

    def score_dimension(
        self,
        dimension_name: str,
        current_metrics: Dict[str, float],
        target_metrics: Dict[str, float],
    ) -> Dict[str, any]:
        """
        Score a dimension (0-100) based on improvement from current to target

        Args:
            dimension_name: Name of dimension (must be in DIMENSIONS)
            current_metrics: Dictionary of current metric values
            target_metrics: Dictionary of target metric values

        Returns:
            Dictionary with dimension score and breakdown
        """
        if dimension_name not in self.DIMENSIONS:
            raise ValueError(f"Unknown dimension: {dimension_name}")

        dimension = self.DIMENSIONS[dimension_name]
        metrics_list = dimension["metrics"]
        improvements = []
        metrics_breakdown = []

        for metric in metrics_list:
            current = current_metrics.get(metric, 0)
            target = target_metrics.get(metric, 0)

            # Calculate improvement percentage
            if current == 0:
                improvement = 0 if target == 0 else 100
            else:
                improvement = ((target - current) / abs(current)) * 100

            # Normalize to 0-100 scale (50 = no change, >50 = improvement)
            # Cap at reasonable limits
            normalized = min(100, max(0, 50 + improvement))

            improvements.append(normalized)
            metrics_breakdown.append(
                {
                    "metric": metric,
                    "current": current,
                    "target": target,
                    "improvement_pct": round(improvement, 2),
                    "normalized_score": round(normalized, 2),
                }
            )

        # Average score for dimension
        dimension_score = sum(improvements) / len(improvements)

        return {
            "dimension": dimension_name,
            "score": round(dimension_score, 2),
            "weight": dimension["weight"],
            "metrics_breakdown": metrics_breakdown,
            "description": dimension["description"],
        }

    def calculate_overall_score(
        self, dimension_scores: Dict[str, float]
    ) -> Dict[str, any]:
        """
        Calculate weighted overall Digital ROI Score

        Args:
            dimension_scores: Dictionary of dimension scores (0-100)
                            Example: {'customers': 75, 'employees': 68, ...}

        Returns:
            Overall score and breakdown
        """
        weighted_score = 0
        breakdown = []

        for dimension, score in dimension_scores.items():
            if dimension not in self.DIMENSIONS:
                continue

            weight = self.DIMENSIONS[dimension]["weight"]
            weighted_contribution = score * weight
            weighted_score += weighted_contribution

            breakdown.append(
                {
                    "dimension": dimension,
                    "score": score,
                    "weight": weight,
                    "weighted_contribution": round(weighted_contribution, 2),
                }
            )

        # Interpretation
        if weighted_score >= 80:
            rating = "Excellent"
            color = "green"
        elif weighted_score >= 65:
            rating = "Good"
            color = "lightgreen"
        elif weighted_score >= 50:
            rating = "Fair"
            color = "yellow"
        else:
            rating = "Needs Improvement"
            color = "orange"

        return {
            "overall_score": round(weighted_score, 2),
            "rating": rating,
            "color": color,
            "breakdown": breakdown,
        }

    def calculate_comprehensive_digital_roi(
        self,
        current_metrics: Dict[str, Dict[str, float]],
        target_metrics: Dict[str, Dict[str, float]],
    ) -> Dict[str, any]:
        """
        Calculate comprehensive Digital ROI across all dimensions

        Args:
            current_metrics: Dictionary of current metrics by dimension
                           Example: {'customers': {'nps_score': 30, ...}, ...}
            target_metrics: Dictionary of target metrics by dimension

        Returns:
            Complete Digital ROI analysis
        """
        dimension_results = []
        dimension_scores = {}

        for dimension_name in self.DIMENSIONS.keys():
            current = current_metrics.get(dimension_name, {})
            target = target_metrics.get(dimension_name, {})

            dimension_result = self.score_dimension(dimension_name, current, target)
            dimension_results.append(dimension_result)
            dimension_scores[dimension_name] = dimension_result["score"]

        overall = self.calculate_overall_score(dimension_scores)

        # Identify top performers and areas for improvement
        sorted_dimensions = sorted(
            dimension_results, key=lambda x: x["score"], reverse=True
        )

        top_performers = sorted_dimensions[:2]
        areas_for_improvement = sorted_dimensions[-2:]

        return {
            "overall": overall,
            "dimensions": dimension_results,
            "top_performers": [d["dimension"] for d in top_performers],
            "areas_for_improvement": [d["dimension"] for d in areas_for_improvement],
            "recommendations": self._generate_recommendations(
                overall["overall_score"], areas_for_improvement
            ),
        }

    def _generate_recommendations(
        self, overall_score: float, weak_dimensions: List[Dict]
    ) -> List[str]:
        """Generate recommendations based on scores"""
        recommendations = []

        if overall_score < 50:
            recommendations.append(
                "Overall digital maturity is low. Focus on quick wins in operational efficiency."
            )

        for dim in weak_dimensions:
            if dim["dimension"] == "customers":
                recommendations.append(
                    "Improve customer experience through better response times and service quality."
                )
            elif dim["dimension"] == "employees":
                recommendations.append(
                    "Invest in employee training and digital adoption programs."
                )
            elif dim["dimension"] == "operations":
                recommendations.append(
                    "Streamline operations through process automation and optimization."
                )
            elif dim["dimension"] == "safety_soundness":
                recommendations.append(
                    "Strengthen cybersecurity and compliance measures."
                )
            elif dim["dimension"] == "infrastructure":
                recommendations.append(
                    "Modernize technology infrastructure and reduce technical debt."
                )
            elif dim["dimension"] == "disruption_innovation":
                recommendations.append(
                    "Increase investment in innovation and emerging technologies."
                )

        return recommendations

    def compare_with_baseline(
        self,
        baseline_scores: Dict[str, float],
        current_scores: Dict[str, float],
    ) -> Dict[str, any]:
        """
        Compare current scores with baseline

        Args:
            baseline_scores: Baseline dimension scores
            current_scores: Current dimension scores

        Returns:
            Comparison analysis
        """
        improvements = {}
        total_improvement = 0

        for dimension in self.DIMENSIONS.keys():
            baseline = baseline_scores.get(dimension, 0)
            current = current_scores.get(dimension, 0)
            improvement = current - baseline

            improvements[dimension] = {
                "baseline": baseline,
                "current": current,
                "improvement": round(improvement, 2),
                "improvement_pct": round((improvement / baseline) * 100, 2)
                if baseline > 0
                else 0,
            }

            total_improvement += improvement

        return {
            "improvements": improvements,
            "total_improvement": round(total_improvement, 2),
            "average_improvement": round(
                total_improvement / len(self.DIMENSIONS), 2
            ),
        }
