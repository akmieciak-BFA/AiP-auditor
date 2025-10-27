"""
Module 6: Benchmarking & Maturity Assessment
============================================

Components:
- Industry Benchmarking
- Automation Maturity Assessment (5 levels)
- Best Practices Comparison
"""

from typing import Dict, List, Optional


class BenchmarkingMaturityAssessment:
    """Industry benchmarking and maturity assessment"""

    # Industry benchmarks (example data - should be loaded from database)
    INDUSTRY_BENCHMARKS = {
        "manufacturing": {
            "avg_roi": 25.0,
            "avg_payback_months": 18,
            "automation_adoption_rate": 45.0,
            "cost_reduction_range": (15, 30),
            "productivity_improvement_range": (20, 40),
            "typical_capex_range": (100000, 500000),
            "typical_opex_pct_of_capex": 15,
        },
        "financial_services": {
            "avg_roi": 35.0,
            "avg_payback_months": 12,
            "automation_adoption_rate": 60.0,
            "cost_reduction_range": (25, 45),
            "productivity_improvement_range": (30, 60),
            "typical_capex_range": (50000, 300000),
            "typical_opex_pct_of_capex": 12,
        },
        "healthcare": {
            "avg_roi": 30.0,
            "avg_payback_months": 15,
            "automation_adoption_rate": 35.0,
            "cost_reduction_range": (20, 35),
            "productivity_improvement_range": (25, 45),
            "typical_capex_range": (75000, 400000),
            "typical_opex_pct_of_capex": 18,
        },
        "logistics": {
            "avg_roi": 28.0,
            "avg_payback_months": 16,
            "automation_adoption_rate": 50.0,
            "cost_reduction_range": (18, 32),
            "productivity_improvement_range": (22, 42),
            "typical_capex_range": (120000, 600000),
            "typical_opex_pct_of_capex": 14,
        },
        "retail": {
            "avg_roi": 32.0,
            "avg_payback_months": 14,
            "automation_adoption_rate": 55.0,
            "cost_reduction_range": (22, 38),
            "productivity_improvement_range": (28, 50),
            "typical_capex_range": (60000, 350000),
            "typical_opex_pct_of_capex": 13,
        },
    }

    MATURITY_LEVELS = {
        1: {
            "name": "Ad-Hoc",
            "range": (0, 20),
            "description": "Limited to no automation. Manual processes dominate.",
            "characteristics": [
                "Sporadic automation efforts",
                "No formal strategy",
                "Limited technical skills",
                "High manual intervention",
            ],
            "next_steps": [
                "Develop automation strategy",
                "Identify quick wins",
                "Build technical capabilities",
            ],
        },
        2: {
            "name": "Task Automation",
            "range": (21, 40),
            "description": "Individual task automation. Isolated solutions.",
            "characteristics": [
                "Point solutions implemented",
                "Some automation successes",
                "Limited integration",
                "Emerging governance",
            ],
            "next_steps": [
                "Standardize automation approach",
                "Integrate isolated solutions",
                "Establish CoE (Center of Excellence)",
            ],
        },
        3: {
            "name": "Process Automation",
            "range": (41, 60),
            "description": "End-to-end process automation. Coordinated efforts.",
            "characteristics": [
                "Processes automated end-to-end",
                "Formal governance in place",
                "Reusable components",
                "Measurable ROI",
            ],
            "next_steps": [
                "Implement intelligent automation",
                "Expand to more processes",
                "Advanced analytics integration",
            ],
        },
        4: {
            "name": "Intelligent Automation",
            "range": (61, 80),
            "description": "AI/ML integration. Predictive and adaptive systems.",
            "characteristics": [
                "AI/ML capabilities deployed",
                "Predictive analytics",
                "Self-learning systems",
                "Enterprise-wide adoption",
            ],
            "next_steps": [
                "Move toward autonomous operations",
                "Advanced AI capabilities",
                "Ecosystem integration",
            ],
        },
        5: {
            "name": "Autonomous Operations",
            "range": (81, 100),
            "description": "Self-optimizing systems. Autonomous decision-making.",
            "characteristics": [
                "Fully autonomous processes",
                "Self-optimizing systems",
                "Ecosystem orchestration",
                "Continuous innovation",
            ],
            "next_steps": [
                "Maintain competitive advantage",
                "Explore emerging technologies",
                "Lead industry transformation",
            ],
        },
    }

    def compare_to_industry(
        self,
        industry: str,
        calculated_roi: float,
        calculated_payback_months: float,
        capex: Optional[float] = None,
        opex: Optional[float] = None,
    ) -> Dict[str, any]:
        """
        Compare project metrics to industry benchmarks

        Args:
            industry: Industry name (must be in INDUSTRY_BENCHMARKS)
            calculated_roi: Calculated ROI %
            calculated_payback_months: Calculated payback period in months
            capex: Optional CapEx for additional comparison
            opex: Optional OpEx for additional comparison

        Returns:
            Comparison results with industry benchmarks
        """
        if industry not in self.INDUSTRY_BENCHMARKS:
            return {
                "error": f"Industry '{industry}' not found in benchmarks",
                "available_industries": list(self.INDUSTRY_BENCHMARKS.keys()),
            }

        benchmark = self.INDUSTRY_BENCHMARKS[industry]

        comparison = {
            "industry": industry,
            "roi_comparison": {
                "project_roi": calculated_roi,
                "industry_avg": benchmark["avg_roi"],
                "vs_industry": round(calculated_roi - benchmark["avg_roi"], 2),
                "performance": (
                    "Above Average"
                    if calculated_roi > benchmark["avg_roi"]
                    else "Below Average"
                ),
            },
            "payback_comparison": {
                "project_payback_months": calculated_payback_months,
                "industry_avg_months": benchmark["avg_payback_months"],
                "vs_industry": round(
                    calculated_payback_months - benchmark["avg_payback_months"], 2
                ),
                "performance": (
                    "Faster"
                    if calculated_payback_months < benchmark["avg_payback_months"]
                    else "Slower"
                ),
            },
            "industry_benchmarks": {
                "automation_adoption_rate": benchmark["automation_adoption_rate"],
                "cost_reduction_range": benchmark["cost_reduction_range"],
                "productivity_improvement_range": benchmark[
                    "productivity_improvement_range"
                ],
            },
        }

        # Add CapEx/OpEx comparison if provided
        if capex is not None:
            capex_range = benchmark["typical_capex_range"]
            comparison["capex_comparison"] = {
                "project_capex": capex,
                "industry_range": capex_range,
                "position": self._compare_to_range(capex, capex_range),
            }

        if capex is not None and opex is not None:
            expected_opex_pct = benchmark["typical_opex_pct_of_capex"]
            actual_opex_pct = (opex / capex) * 100 if capex > 0 else 0
            comparison["opex_comparison"] = {
                "project_opex": opex,
                "opex_pct_of_capex": round(actual_opex_pct, 2),
                "industry_typical_pct": expected_opex_pct,
                "vs_industry": round(actual_opex_pct - expected_opex_pct, 2),
            }

        return comparison

    def _compare_to_range(self, value: float, range_tuple: tuple) -> str:
        """Compare value to a range"""
        min_val, max_val = range_tuple
        if value < min_val:
            return "Below Typical Range"
        elif value > max_val:
            return "Above Typical Range"
        else:
            return "Within Typical Range"

    def assess_maturity(
        self, assessment_scores: Dict[str, float]
    ) -> Dict[str, any]:
        """
        Assess automation maturity level (1-5)

        Args:
            assessment_scores: Dictionary of dimension scores (0-100)
                Example: {
                    'strategy_governance': 75,
                    'technology_infrastructure': 60,
                    'process_operations': 70,
                    'people_culture': 55,
                    'measurement_optimization': 65
                }

        Returns:
            Maturity assessment with level, score, and recommendations
        """
        # Calculate overall maturity score
        overall_score = sum(assessment_scores.values()) / len(assessment_scores)

        # Determine maturity level
        maturity_level = None
        for level, info in self.MATURITY_LEVELS.items():
            min_score, max_score = info["range"]
            if min_score <= overall_score <= max_score:
                maturity_level = {
                    "level": level,
                    "name": info["name"],
                    "description": info["description"],
                    "characteristics": info["characteristics"],
                    "next_steps": info["next_steps"],
                }
                break

        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        for dimension, score in assessment_scores.items():
            if score >= 70:
                strengths.append(dimension)
            elif score < 50:
                weaknesses.append(dimension)

        return {
            "overall_score": round(overall_score, 2),
            "maturity_level": maturity_level,
            "dimension_scores": assessment_scores,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "roadmap_to_next_level": self._generate_roadmap(
                maturity_level["level"] if maturity_level else 1
            ),
        }

    def _generate_roadmap(self, current_level: int) -> Dict[str, any]:
        """Generate roadmap to next maturity level"""
        if current_level >= 5:
            return {
                "message": "Already at highest maturity level",
                "focus": "Maintain excellence and explore emerging technologies",
            }

        next_level = current_level + 1
        next_level_info = self.MATURITY_LEVELS[next_level]

        return {
            "current_level": current_level,
            "target_level": next_level,
            "target_name": next_level_info["name"],
            "actions": next_level_info["next_steps"],
            "estimated_timeline": self._estimate_timeline(current_level, next_level),
        }

    def _estimate_timeline(self, current_level: int, target_level: int) -> str:
        """Estimate timeline to reach next level"""
        level_gap = target_level - current_level
        if level_gap <= 1:
            return "6-12 months"
        elif level_gap == 2:
            return "12-18 months"
        else:
            return "18-24+ months"

    def generate_best_practices_report(
        self, industry: str, maturity_level: int
    ) -> Dict[str, any]:
        """
        Generate best practices report for industry and maturity level

        Args:
            industry: Industry name
            maturity_level: Current maturity level (1-5)

        Returns:
            Best practices and recommendations
        """
        # This would typically pull from a database of best practices
        # For now, return a template
        return {
            "industry": industry,
            "maturity_level": maturity_level,
            "best_practices": [
                "Establish clear automation governance",
                "Build CoE (Center of Excellence)",
                "Implement robust change management",
                "Focus on measurable ROI",
                "Invest in training and upskilling",
            ],
            "common_pitfalls": [
                "Lack of executive sponsorship",
                "Insufficient change management",
                "Underestimating training needs",
                "Poor vendor selection",
                "Inadequate scalability planning",
            ],
            "success_factors": [
                "Strong business case",
                "Clear success metrics",
                "Stakeholder engagement",
                "Iterative implementation",
                "Continuous improvement mindset",
            ],
        }
