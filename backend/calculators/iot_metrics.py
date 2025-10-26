"""
Module 4: IoT/Automation Specific Metrics
=========================================

Based on Siemens Advanta - IoT ROI Framework

Components:
- Connectivity Value Calculation
- OEE (Overall Equipment Effectiveness) Improvement
- Predictive Maintenance Value
- Energy Optimization Value
"""

from typing import Dict, Optional


class IoTAutomationMetrics:
    """IoT and Industrial Automation specific metrics"""

    def calculate_connectivity_value(
        self,
        num_devices: int,
        data_points_per_device: int,
        monitoring_value_per_point: float,
        data_quality_improvement_pct: float = 0,
    ) -> Dict[str, any]:
        """
        Calculate value from connected devices and data collection

        Args:
            num_devices: Number of connected devices
            data_points_per_device: Data points collected per device
            monitoring_value_per_point: Annual value per monitored data point
            data_quality_improvement_pct: Data quality improvement (%)

        Returns:
            Connectivity value breakdown
        """
        total_data_points = num_devices * data_points_per_device
        base_value = total_data_points * monitoring_value_per_point

        # Add value from data quality improvement
        quality_bonus = base_value * (data_quality_improvement_pct / 100)
        total_value = base_value + quality_bonus

        return {
            "num_devices": num_devices,
            "data_points_per_device": data_points_per_device,
            "total_data_points": total_data_points,
            "monitoring_value_per_point": monitoring_value_per_point,
            "base_connectivity_value": round(base_value, 2),
            "data_quality_bonus": round(quality_bonus, 2),
            "total_annual_value": round(total_value, 2),
        }

    def calculate_oee_improvement(
        self,
        baseline_availability: float = 0.85,
        baseline_performance: float = 0.90,
        baseline_quality: float = 0.95,
        availability_improvement_pct: float = 0,
        performance_improvement_pct: float = 0,
        quality_improvement_pct: float = 0,
    ) -> Dict[str, any]:
        """
        Calculate Overall Equipment Effectiveness (OEE) improvement

        OEE = Availability × Performance × Quality

        Args:
            baseline_availability: Current availability (default 85%)
            baseline_performance: Current performance (default 90%)
            baseline_quality: Current quality (default 95%)
            availability_improvement_pct: Expected improvement in availability (%)
            performance_improvement_pct: Expected improvement in performance (%)
            quality_improvement_pct: Expected improvement in quality (%)

        Returns:
            OEE improvement analysis
        """
        # Current OEE
        current_oee = baseline_availability * baseline_performance * baseline_quality

        # New metrics after improvement
        new_availability = baseline_availability * (
            1 + availability_improvement_pct / 100
        )
        new_performance = baseline_performance * (
            1 + performance_improvement_pct / 100
        )
        new_quality = baseline_quality * (1 + quality_improvement_pct / 100)

        # Cap at 1.0 (100%)
        new_availability = min(1.0, new_availability)
        new_performance = min(1.0, new_performance)
        new_quality = min(1.0, new_quality)

        # New OEE
        new_oee = new_availability * new_performance * new_quality

        # Calculate improvement
        oee_improvement = ((new_oee - current_oee) / current_oee) * 100

        return {
            "current": {
                "availability": round(baseline_availability * 100, 2),
                "performance": round(baseline_performance * 100, 2),
                "quality": round(baseline_quality * 100, 2),
                "oee": round(current_oee * 100, 2),
            },
            "improved": {
                "availability": round(new_availability * 100, 2),
                "performance": round(new_performance * 100, 2),
                "quality": round(new_quality * 100, 2),
                "oee": round(new_oee * 100, 2),
            },
            "improvement": {
                "oee_points": round((new_oee - current_oee) * 100, 2),
                "oee_improvement_pct": round(oee_improvement, 2),
            },
        }

    def calculate_oee_financial_impact(
        self,
        oee_improvement_pct: float,
        annual_production_capacity: float,
        revenue_per_unit: float,
        cost_per_unit: float,
    ) -> Dict[str, float]:
        """
        Calculate financial impact of OEE improvement

        Args:
            oee_improvement_pct: OEE improvement percentage
            annual_production_capacity: Annual production capacity
            revenue_per_unit: Revenue per unit
            cost_per_unit: Cost per unit

        Returns:
            Financial impact of OEE improvement
        """
        additional_production = annual_production_capacity * (
            oee_improvement_pct / 100
        )
        additional_revenue = additional_production * revenue_per_unit
        additional_costs = additional_production * cost_per_unit
        additional_profit = additional_revenue - additional_costs

        return {
            "additional_production_units": round(additional_production, 2),
            "additional_revenue": round(additional_revenue, 2),
            "additional_costs": round(additional_costs, 2),
            "additional_profit": round(additional_profit, 2),
        }

    def calculate_predictive_maintenance_value(
        self,
        unplanned_downtime_hours_baseline: float,
        downtime_cost_per_hour: float,
        prevention_rate_pct: float,
        maintenance_cost_increase_pct: float = 10,
    ) -> Dict[str, any]:
        """
        Calculate value from predictive maintenance

        Args:
            unplanned_downtime_hours_baseline: Current annual unplanned downtime (hours)
            downtime_cost_per_hour: Cost per hour of downtime
            prevention_rate_pct: Percentage of downtime prevented (typically 30-50%)
            maintenance_cost_increase_pct: Increase in maintenance costs (default 10%)

        Returns:
            Predictive maintenance value analysis
        """
        # Calculate prevented downtime
        prevented_downtime_hours = unplanned_downtime_hours_baseline * (
            prevention_rate_pct / 100
        )
        downtime_savings = prevented_downtime_hours * downtime_cost_per_hour

        # Calculate increased maintenance costs
        baseline_maintenance_cost = (
            unplanned_downtime_hours_baseline * downtime_cost_per_hour * 0.3
        )  # Assume maintenance is 30% of downtime cost
        increased_maintenance = baseline_maintenance_cost * (
            maintenance_cost_increase_pct / 100
        )

        # Net savings
        net_savings = downtime_savings - increased_maintenance

        return {
            "baseline_downtime_hours": unplanned_downtime_hours_baseline,
            "prevented_downtime_hours": round(prevented_downtime_hours, 2),
            "downtime_cost_per_hour": downtime_cost_per_hour,
            "downtime_savings": round(downtime_savings, 2),
            "increased_maintenance_costs": round(increased_maintenance, 2),
            "net_annual_savings": round(net_savings, 2),
            "roi_multiplier": round(net_savings / increased_maintenance, 2)
            if increased_maintenance > 0
            else 0,
        }

    def calculate_energy_optimization_value(
        self,
        current_annual_energy_cost: float,
        reduction_pct: float,
        implementation_cost: float = 0,
    ) -> Dict[str, float]:
        """
        Calculate value from energy optimization

        Args:
            current_annual_energy_cost: Current annual energy costs
            reduction_pct: Expected energy reduction (%)
            implementation_cost: One-time implementation cost

        Returns:
            Energy optimization value
        """
        annual_savings = current_annual_energy_cost * (reduction_pct / 100)

        payback_period = (
            implementation_cost / annual_savings if annual_savings > 0 else 0
        )

        return {
            "current_annual_cost": current_annual_energy_cost,
            "reduction_pct": reduction_pct,
            "annual_savings": round(annual_savings, 2),
            "implementation_cost": implementation_cost,
            "payback_period_years": round(payback_period, 2),
            "five_year_savings": round(annual_savings * 5, 2),
        }

    def calculate_quality_improvement_value(
        self,
        annual_production: float,
        current_defect_rate_pct: float,
        improved_defect_rate_pct: float,
        cost_per_defect: float,
    ) -> Dict[str, any]:
        """
        Calculate value from quality improvements

        Args:
            annual_production: Annual production volume
            current_defect_rate_pct: Current defect rate (%)
            improved_defect_rate_pct: Target defect rate (%)
            cost_per_defect: Cost per defective unit (scrap, rework, warranty)

        Returns:
            Quality improvement value
        """
        current_defects = annual_production * (current_defect_rate_pct / 100)
        improved_defects = annual_production * (improved_defect_rate_pct / 100)
        defects_prevented = current_defects - improved_defects

        annual_savings = defects_prevented * cost_per_defect

        return {
            "annual_production": annual_production,
            "current_defects": round(current_defects, 2),
            "improved_defects": round(improved_defects, 2),
            "defects_prevented": round(defects_prevented, 2),
            "cost_per_defect": cost_per_defect,
            "annual_savings": round(annual_savings, 2),
        }

    def calculate_comprehensive_iot_roi(
        self,
        connectivity_params: Dict,
        oee_params: Dict,
        predictive_maintenance_params: Dict,
        energy_params: Dict,
        quality_params: Optional[Dict] = None,
    ) -> Dict[str, any]:
        """
        Calculate comprehensive IoT ROI across all dimensions

        Args:
            connectivity_params: Parameters for connectivity value
            oee_params: Parameters for OEE improvement
            predictive_maintenance_params: Parameters for predictive maintenance
            energy_params: Parameters for energy optimization
            quality_params: Optional parameters for quality improvement

        Returns:
            Comprehensive IoT ROI analysis
        """
        # Calculate each component
        connectivity = self.calculate_connectivity_value(**connectivity_params)
        oee = self.calculate_oee_improvement(**oee_params)
        predictive_maint = self.calculate_predictive_maintenance_value(
            **predictive_maintenance_params
        )
        energy = self.calculate_energy_optimization_value(**energy_params)

        # Total annual benefits
        total_benefits = (
            connectivity["total_annual_value"]
            + predictive_maint["net_annual_savings"]
            + energy["annual_savings"]
        )

        if quality_params:
            quality = self.calculate_quality_improvement_value(**quality_params)
            total_benefits += quality["annual_savings"]
        else:
            quality = None

        return {
            "connectivity_value": connectivity,
            "oee_improvement": oee,
            "predictive_maintenance": predictive_maint,
            "energy_optimization": energy,
            "quality_improvement": quality,
            "summary": {
                "total_annual_benefits": round(total_benefits, 2),
                "breakdown": {
                    "connectivity": connectivity["total_annual_value"],
                    "predictive_maintenance": predictive_maint["net_annual_savings"],
                    "energy": energy["annual_savings"],
                    "quality": quality["annual_savings"] if quality else 0,
                },
            },
        }
