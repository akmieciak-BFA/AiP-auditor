"""
Module 2: Time-Driven Activity-Based Costing (TDABC)
=====================================================

Based on Harvard Business Review - TDABC Framework

Components:
- Capacity Cost Rate Calculator
- Cost-Driver Rate Calculator
- Capacity Utilization Analysis
- Time Equations Builder (for complex processes)
"""

from typing import Dict, List, Callable, Optional


class TDABCCalculator:
    """Time-Driven Activity-Based Costing Calculator"""

    def calculate_practical_capacity(
        self, theoretical_capacity_minutes: float, resource_type: str = "people"
    ) -> float:
        """
        Calculate practical capacity from theoretical capacity

        Args:
            theoretical_capacity_minutes: Theoretical maximum capacity
            resource_type: 'people' or 'machines'

        Returns:
            Practical capacity in minutes

        Notes:
            - People: 80% of theoretical (20% for breaks, communication, training)
            - Machines: 85% of theoretical (15% for maintenance, downtime)
        """
        if resource_type.lower() == "people":
            return theoretical_capacity_minutes * 0.80
        elif resource_type.lower() == "machines":
            return theoretical_capacity_minutes * 0.85
        else:
            return theoretical_capacity_minutes * 0.80  # Default to people

    def calculate_capacity_cost_rate(
        self, total_cost: float, practical_capacity_minutes: float
    ) -> float:
        """
        Calculate Capacity Cost Rate

        Capacity Cost Rate = Total Cost / Practical Capacity

        Args:
            total_cost: Total cost of resources (annual salary, benefits, overhead, etc.)
            practical_capacity_minutes: Practical capacity in minutes

        Returns:
            Cost per minute
        """
        if practical_capacity_minutes == 0:
            return 0.0
        return total_cost / practical_capacity_minutes

    def calculate_cost_driver_rate(
        self, unit_time_minutes: float, capacity_cost_rate: float
    ) -> float:
        """
        Calculate Cost-Driver Rate

        Cost-Driver Rate = Unit Time × Capacity Cost Rate

        Args:
            unit_time_minutes: Time required for one unit of activity
            capacity_cost_rate: Cost per minute from calculate_capacity_cost_rate()

        Returns:
            Cost per unit of activity
        """
        return unit_time_minutes * capacity_cost_rate

    def analyze_capacity_utilization(
        self, practical_capacity: float, activities: List[Dict[str, any]]
    ) -> Dict[str, any]:
        """
        Analyze capacity utilization and identify unused capacity

        Args:
            practical_capacity: Practical capacity in minutes
            activities: List of activities with 'unit_time' and 'volume'
                       Example: [{'name': 'Process Orders', 'unit_time': 8, 'volume': 1000}]

        Returns:
            Dictionary with utilization analysis and recommendations
        """
        # Calculate used capacity
        used_capacity = sum(
            activity["unit_time"] * activity["volume"] for activity in activities
        )

        unused_capacity = practical_capacity - used_capacity
        utilization_rate = (used_capacity / practical_capacity) * 100 if practical_capacity > 0 else 0

        # Interpretation and recommendation
        if utilization_rate < 70:
            status = "OVERCAPACITY"
            recommendation = "Consider cost reduction or workload increase"
            color = "red"
        elif utilization_rate > 90:
            status = "BOTTLENECK"
            recommendation = "Investment needed to increase capacity"
            color = "orange"
        else:
            status = "HEALTHY"
            recommendation = "Optimal capacity utilization"
            color = "green"

        # Calculate activity breakdown
        activities_breakdown = []
        for activity in activities:
            activity_capacity = activity["unit_time"] * activity["volume"]
            activity_pct = (activity_capacity / practical_capacity) * 100 if practical_capacity > 0 else 0
            activities_breakdown.append(
                {
                    "name": activity.get("name", "Unknown"),
                    "unit_time": activity["unit_time"],
                    "volume": activity["volume"],
                    "total_time": activity_capacity,
                    "percentage_of_capacity": round(activity_pct, 2),
                }
            )

        return {
            "practical_capacity": practical_capacity,
            "used_capacity": used_capacity,
            "unused_capacity": unused_capacity,
            "utilization_rate": round(utilization_rate, 2),
            "status": status,
            "recommendation": recommendation,
            "status_color": color,
            "activities_breakdown": activities_breakdown,
        }

    def calculate_activity_cost(
        self,
        activity_name: str,
        unit_time: float,
        volume: int,
        capacity_cost_rate: float,
    ) -> Dict[str, float]:
        """
        Calculate total cost for an activity

        Args:
            activity_name: Name of the activity
            unit_time: Time per unit (minutes)
            volume: Number of units
            capacity_cost_rate: Cost per minute

        Returns:
            Dictionary with cost breakdown
        """
        cost_per_unit = self.calculate_cost_driver_rate(unit_time, capacity_cost_rate)
        total_cost = cost_per_unit * volume
        total_time = unit_time * volume

        return {
            "activity_name": activity_name,
            "unit_time_minutes": unit_time,
            "volume": volume,
            "total_time_minutes": total_time,
            "cost_per_minute": capacity_cost_rate,
            "cost_per_unit": round(cost_per_unit, 2),
            "total_cost": round(total_cost, 2),
        }

    def calculate_tdabc_full_analysis(
        self,
        total_cost: float,
        theoretical_capacity_minutes: float,
        resource_type: str,
        activities: List[Dict[str, any]],
    ) -> Dict[str, any]:
        """
        Perform complete TDABC analysis

        Args:
            total_cost: Total cost of resources
            theoretical_capacity_minutes: Theoretical capacity
            resource_type: 'people' or 'machines'
            activities: List of activities with 'name', 'unit_time', and 'volume'

        Returns:
            Complete TDABC analysis
        """
        # Step 1: Calculate practical capacity
        practical_capacity = self.calculate_practical_capacity(
            theoretical_capacity_minutes, resource_type
        )

        # Step 2: Calculate capacity cost rate
        capacity_cost_rate = self.calculate_capacity_cost_rate(
            total_cost, practical_capacity
        )

        # Step 3: Analyze capacity utilization
        utilization_analysis = self.analyze_capacity_utilization(
            practical_capacity, activities
        )

        # Step 4: Calculate costs for each activity
        activities_costs = []
        total_activity_cost = 0

        for activity in activities:
            activity_cost = self.calculate_activity_cost(
                activity.get("name", "Unknown"),
                activity["unit_time"],
                activity["volume"],
                capacity_cost_rate,
            )
            activities_costs.append(activity_cost)
            total_activity_cost += activity_cost["total_cost"]

        # Step 5: Calculate cost of unused capacity
        unused_capacity_cost = (
            utilization_analysis["unused_capacity"] * capacity_cost_rate
        )

        return {
            "summary": {
                "total_cost": total_cost,
                "theoretical_capacity_minutes": theoretical_capacity_minutes,
                "practical_capacity_minutes": practical_capacity,
                "resource_type": resource_type,
                "capacity_cost_rate": round(capacity_cost_rate, 4),
            },
            "utilization": utilization_analysis,
            "activities": activities_costs,
            "cost_allocation": {
                "total_activity_cost": round(total_activity_cost, 2),
                "unused_capacity_cost": round(unused_capacity_cost, 2),
                "total_cost": total_cost,
            },
        }


class TimeEquationsBuilder:
    """Build time equations for complex processes with conditional steps"""

    def build_time_equation(
        self, base_time: float, conditional_times: List[Dict[str, any]]
    ) -> Callable:
        """
        Build time equation for complex processes

        Args:
            base_time: Base time for the process
            conditional_times: List of conditional time additions
                              Example: [{'condition': 'international', 'additional_time': 5}]

        Returns:
            Function that calculates time based on conditions

        Example:
            >>> builder = TimeEquationsBuilder()
            >>> order_time = builder.build_time_equation(
            ...     base_time=8,
            ...     conditional_times=[
            ...         {'condition': 'international', 'additional_time': 5},
            ...         {'condition': 'custom', 'additional_time': 3}
            ...     ]
            ... )
            >>> time = order_time(['international', 'custom'])  # Returns 16
        """

        def calculate_time(conditions_met: List[str]) -> float:
            total_time = base_time
            for ct in conditional_times:
                if ct["condition"] in conditions_met:
                    total_time += ct["additional_time"]
            return total_time

        return calculate_time

    def analyze_process_complexity(
        self,
        time_equation: Callable,
        condition_scenarios: List[Dict[str, any]],
        capacity_cost_rate: float,
    ) -> Dict[str, any]:
        """
        Analyze process complexity using time equations

        Args:
            time_equation: Time equation function from build_time_equation()
            condition_scenarios: List of scenarios with conditions and volume
                                Example: [{'name': 'Simple Order', 'conditions': [], 'volume': 100}]
            capacity_cost_rate: Cost per minute

        Returns:
            Analysis of process complexity and costs
        """
        scenarios_analysis = []
        total_time = 0
        total_cost = 0

        for scenario in condition_scenarios:
            name = scenario.get("name", "Scenario")
            conditions = scenario.get("conditions", [])
            volume = scenario.get("volume", 1)

            # Calculate time for this scenario
            unit_time = time_equation(conditions)
            scenario_total_time = unit_time * volume
            scenario_total_cost = scenario_total_time * capacity_cost_rate

            total_time += scenario_total_time
            total_cost += scenario_total_cost

            scenarios_analysis.append(
                {
                    "scenario_name": name,
                    "conditions": conditions,
                    "volume": volume,
                    "unit_time_minutes": unit_time,
                    "total_time_minutes": scenario_total_time,
                    "total_cost": round(scenario_total_cost, 2),
                }
            )

        return {
            "scenarios": scenarios_analysis,
            "summary": {
                "total_time_minutes": total_time,
                "total_cost": round(total_cost, 2),
                "average_unit_time": round(
                    total_time / sum(s.get("volume", 1) for s in condition_scenarios), 2
                )
                if condition_scenarios
                else 0,
            },
        }

    def optimize_process(
        self, current_time_equation: Callable, improvement_scenarios: List[Dict[str, any]]
    ) -> Dict[str, any]:
        """
        Compare current process with improvement scenarios

        Args:
            current_time_equation: Current time equation
            improvement_scenarios: List of improvement scenarios with modified time equations
                                  Example: [{'name': 'Automation', 'time_equation': func, 'investment': 50000}]

        Returns:
            Comparison of current vs improvement scenarios
        """
        # This is a template for process optimization
        # Implementation would depend on specific use case
        return {
            "message": "Process optimization comparison",
            "current_process": "baseline",
            "improvement_scenarios": improvement_scenarios,
        }
