"""
Module 5: RPA/AI Automation Metrics
===================================

Based on Blue Prism - RPA ROI Methodology

Components:
- FTE Savings Calculation
- Accuracy Improvement Value
- Velocity Improvement
- Bot Utilization Tracking
"""

from typing import Dict, List, Optional


class RPAAutomationMetrics:
    """RPA and AI Automation specific metrics"""

    def calculate_fte_savings(
        self,
        hours_saved_annually: float,
        average_hourly_cost: float,
        working_hours_per_year: int = 2080,
        include_overhead: bool = True,
        overhead_multiplier: float = 1.3,
    ) -> Dict[str, any]:
        """
        Calculate Full-Time Equivalent (FTE) savings

        Args:
            hours_saved_annually: Total hours saved per year through automation
            average_hourly_cost: Average hourly cost (salary + benefits)
            working_hours_per_year: Working hours per FTE per year (default 2080)
            include_overhead: Include overhead costs (default True)
            overhead_multiplier: Overhead multiplier (default 1.3 = 30% overhead)

        Returns:
            FTE savings analysis
        """
        fte_saved = hours_saved_annually / working_hours_per_year

        # Calculate cost savings
        direct_cost_savings = hours_saved_annually * average_hourly_cost

        if include_overhead:
            total_cost_savings = direct_cost_savings * overhead_multiplier
        else:
            total_cost_savings = direct_cost_savings

        return {
            "hours_saved_annually": hours_saved_annually,
            "fte_saved": round(fte_saved, 2),
            "average_hourly_cost": average_hourly_cost,
            "direct_cost_savings": round(direct_cost_savings, 2),
            "overhead_savings": round(
                direct_cost_savings * (overhead_multiplier - 1), 2
            )
            if include_overhead
            else 0,
            "total_annual_cost_savings": round(total_cost_savings, 2),
        }

    def calculate_accuracy_improvement_value(
        self,
        transaction_volume: int,
        error_rate_before_pct: float,
        error_rate_after_pct: float,
        cost_per_error: float,
        revenue_impact_per_error: float = 0,
    ) -> Dict[str, any]:
        """
        Calculate value from accuracy improvements

        Args:
            transaction_volume: Annual transaction volume
            error_rate_before_pct: Error rate before automation (%)
            error_rate_after_pct: Error rate after automation (%)
            cost_per_error: Direct cost to fix each error
            revenue_impact_per_error: Revenue loss per error (optional)

        Returns:
            Accuracy improvement value analysis
        """
        errors_before = transaction_volume * (error_rate_before_pct / 100)
        errors_after = transaction_volume * (error_rate_after_pct / 100)
        errors_prevented = errors_before - errors_after

        # Calculate savings
        direct_cost_savings = errors_prevented * cost_per_error
        revenue_protection = errors_prevented * revenue_impact_per_error
        total_value = direct_cost_savings + revenue_protection

        # Calculate accuracy improvement
        accuracy_improvement_pct = (
            ((error_rate_before_pct - error_rate_after_pct) / error_rate_before_pct)
            * 100
            if error_rate_before_pct > 0
            else 0
        )

        return {
            "transaction_volume": transaction_volume,
            "errors_before": round(errors_before, 2),
            "errors_after": round(errors_after, 2),
            "errors_prevented": round(errors_prevented, 2),
            "error_rate_improvement": {
                "before_pct": error_rate_before_pct,
                "after_pct": error_rate_after_pct,
                "improvement_pct": round(accuracy_improvement_pct, 2),
            },
            "financial_impact": {
                "direct_cost_savings": round(direct_cost_savings, 2),
                "revenue_protection": round(revenue_protection, 2),
                "total_annual_value": round(total_value, 2),
            },
        }

    def calculate_velocity_improvement(
        self,
        transactions_per_day_before: float,
        transactions_per_day_after: float,
        revenue_per_transaction: float = 0,
        working_days_per_year: int = 250,
    ) -> Dict[str, any]:
        """
        Calculate value from velocity improvements

        Args:
            transactions_per_day_before: Daily transaction capacity before automation
            transactions_per_day_after: Daily transaction capacity after automation
            revenue_per_transaction: Revenue generated per transaction
            working_days_per_year: Working days per year (default 250)

        Returns:
            Velocity improvement analysis
        """
        additional_daily_capacity = (
            transactions_per_day_after - transactions_per_day_before
        )
        additional_annual_transactions = (
            additional_daily_capacity * working_days_per_year
        )

        # Calculate potential revenue impact
        potential_additional_revenue = (
            additional_annual_transactions * revenue_per_transaction
        )

        # Calculate velocity improvement percentage
        velocity_improvement_pct = (
            (additional_daily_capacity / transactions_per_day_before) * 100
            if transactions_per_day_before > 0
            else 0
        )

        return {
            "daily_capacity": {
                "before": transactions_per_day_before,
                "after": transactions_per_day_after,
                "additional": round(additional_daily_capacity, 2),
                "improvement_pct": round(velocity_improvement_pct, 2),
            },
            "annual_impact": {
                "additional_transactions": round(additional_annual_transactions, 2),
                "potential_additional_revenue": round(potential_additional_revenue, 2),
            },
        }

    def calculate_bot_utilization(
        self,
        number_of_bots: int,
        available_hours_per_bot_per_day: float,
        actual_processing_hours_per_day: float,
        working_days_per_year: int = 250,
    ) -> Dict[str, any]:
        """
        Calculate bot utilization metrics

        Args:
            number_of_bots: Number of deployed bots
            available_hours_per_bot_per_day: Available hours per bot per day (typically 24)
            actual_processing_hours_per_day: Actual total processing hours across all bots
            working_days_per_year: Working days per year

        Returns:
            Bot utilization analysis
        """
        total_available_hours_daily = number_of_bots * available_hours_per_bot_per_day
        utilization_rate = (
            (actual_processing_hours_per_day / total_available_hours_daily) * 100
            if total_available_hours_daily > 0
            else 0
        )

        # Annual metrics
        annual_available_hours = total_available_hours_daily * working_days_per_year
        annual_processing_hours = actual_processing_hours_per_day * working_days_per_year
        unused_capacity_hours = annual_available_hours - annual_processing_hours

        # Utilization interpretation
        if utilization_rate < 50:
            status = "Underutilized"
            recommendation = "Consider additional automation opportunities or reduce bot count"
            color = "red"
        elif utilization_rate < 75:
            status = "Good"
            recommendation = "Healthy utilization with room for growth"
            color = "green"
        elif utilization_rate < 90:
            status = "High"
            recommendation = "Near optimal utilization"
            color = "lightgreen"
        else:
            status = "At Capacity"
            recommendation = "Consider scaling bot infrastructure"
            color = "orange"

        return {
            "number_of_bots": number_of_bots,
            "daily_metrics": {
                "available_hours": total_available_hours_daily,
                "processing_hours": actual_processing_hours_per_day,
                "utilization_rate_pct": round(utilization_rate, 2),
            },
            "annual_metrics": {
                "available_hours": round(annual_available_hours, 2),
                "processing_hours": round(annual_processing_hours, 2),
                "unused_capacity_hours": round(unused_capacity_hours, 2),
            },
            "status": status,
            "recommendation": recommendation,
            "status_color": color,
        }

    def calculate_process_cycle_time_reduction(
        self,
        process_name: str,
        manual_cycle_time_minutes: float,
        automated_cycle_time_minutes: float,
        annual_volume: int,
        cost_per_minute: float,
    ) -> Dict[str, any]:
        """
        Calculate value from process cycle time reduction

        Args:
            process_name: Name of the process
            manual_cycle_time_minutes: Manual cycle time
            automated_cycle_time_minutes: Automated cycle time
            annual_volume: Annual process volume
            cost_per_minute: Cost per minute of processing time

        Returns:
            Cycle time reduction analysis
        """
        time_saved_per_transaction = (
            manual_cycle_time_minutes - automated_cycle_time_minutes
        )
        total_time_saved_minutes = time_saved_per_transaction * annual_volume
        total_time_saved_hours = total_time_saved_minutes / 60

        annual_cost_savings = total_time_saved_minutes * cost_per_minute

        cycle_time_reduction_pct = (
            (time_saved_per_transaction / manual_cycle_time_minutes) * 100
            if manual_cycle_time_minutes > 0
            else 0
        )

        return {
            "process_name": process_name,
            "cycle_time": {
                "manual_minutes": manual_cycle_time_minutes,
                "automated_minutes": automated_cycle_time_minutes,
                "time_saved_per_transaction": round(time_saved_per_transaction, 2),
                "reduction_pct": round(cycle_time_reduction_pct, 2),
            },
            "annual_impact": {
                "volume": annual_volume,
                "total_time_saved_hours": round(total_time_saved_hours, 2),
                "annual_cost_savings": round(annual_cost_savings, 2),
            },
        }

    def calculate_comprehensive_rpa_roi(
        self,
        fte_savings_params: Dict,
        accuracy_params: Dict,
        velocity_params: Dict,
        bot_utilization_params: Optional[Dict] = None,
        cycle_time_params: Optional[Dict] = None,
    ) -> Dict[str, any]:
        """
        Calculate comprehensive RPA ROI across all dimensions

        Args:
            fte_savings_params: Parameters for FTE savings
            accuracy_params: Parameters for accuracy improvement
            velocity_params: Parameters for velocity improvement
            bot_utilization_params: Optional bot utilization parameters
            cycle_time_params: Optional cycle time reduction parameters

        Returns:
            Comprehensive RPA ROI analysis
        """
        # Calculate each component
        fte_savings = self.calculate_fte_savings(**fte_savings_params)
        accuracy = self.calculate_accuracy_improvement_value(**accuracy_params)
        velocity = self.calculate_velocity_improvement(**velocity_params)

        # Calculate total benefits
        total_benefits = (
            fte_savings["total_annual_cost_savings"]
            + accuracy["financial_impact"]["total_annual_value"]
            + velocity["annual_impact"]["potential_additional_revenue"]
        )

        results = {
            "fte_savings": fte_savings,
            "accuracy_improvement": accuracy,
            "velocity_improvement": velocity,
            "summary": {
                "total_annual_benefits": round(total_benefits, 2),
                "breakdown": {
                    "fte_savings": fte_savings["total_annual_cost_savings"],
                    "accuracy_value": accuracy["financial_impact"][
                        "total_annual_value"
                    ],
                    "velocity_value": velocity["annual_impact"][
                        "potential_additional_revenue"
                    ],
                },
            },
        }

        # Add optional components
        if bot_utilization_params:
            bot_util = self.calculate_bot_utilization(**bot_utilization_params)
            results["bot_utilization"] = bot_util

        if cycle_time_params:
            cycle_time = self.calculate_process_cycle_time_reduction(**cycle_time_params)
            results["cycle_time_reduction"] = cycle_time
            results["summary"]["total_annual_benefits"] += cycle_time["annual_impact"][
                "annual_cost_savings"
            ]
            results["summary"]["breakdown"]["cycle_time"] = cycle_time["annual_impact"][
                "annual_cost_savings"
            ]

        return results

    def calculate_automation_potential(
        self,
        total_processes: int,
        automatable_processes: int,
        automated_processes: int,
        avg_savings_per_process: float,
    ) -> Dict[str, any]:
        """
        Calculate automation potential and pipeline value

        Args:
            total_processes: Total number of processes
            automatable_processes: Number of processes suitable for automation
            automated_processes: Number of processes already automated
            avg_savings_per_process: Average savings per automated process

        Returns:
            Automation potential analysis
        """
        automation_rate = (automated_processes / total_processes) * 100
        remaining_opportunities = automatable_processes - automated_processes
        potential_additional_savings = remaining_opportunities * avg_savings_per_process

        current_savings = automated_processes * avg_savings_per_process
        total_potential_savings = automatable_processes * avg_savings_per_process

        return {
            "current_state": {
                "total_processes": total_processes,
                "automatable_processes": automatable_processes,
                "automated_processes": automated_processes,
                "automation_rate_pct": round(automation_rate, 2),
            },
            "opportunity": {
                "remaining_processes": remaining_opportunities,
                "potential_additional_savings": round(potential_additional_savings, 2),
            },
            "savings": {
                "current_annual_savings": round(current_savings, 2),
                "total_potential_savings": round(total_potential_savings, 2),
                "unrealized_value": round(potential_additional_savings, 2),
            },
        }
