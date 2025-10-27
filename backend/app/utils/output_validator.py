"""Output quality validation module for BFA Audit App.

This module validates that generated content meets minimum quality thresholds
based on the Turris presentation analysis (126 slides, 13,307 words).
"""

import re
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)


class OutputQualityValidator:
    """Validates that audit outputs meet minimum word count requirements."""
    
    # Minimum word counts based on Turris presentation analysis
    STEP1_REQUIREMENTS = {
        "executive_summary": {"min": 150, "max": 200},
        "methodology": {"min": 100, "max": 150},
        "top_processes": {"min": 400, "max": 600},  # For TOP 5
        "matrix": {"min": 150, "max": 250},
        "lean_sigma": {"min": 100, "max": 150},
        "total": {"min": 900, "optimal": 1200, "max": 1500}
    }
    
    STEP2_REQUIREMENTS = {
        "process_description": {"min": 150, "max": 200},
        "as_is_mapping": {"min": 200, "max": 300},
        "bottlenecks": {"min": 150, "max": 200},
        "muda_analysis": {"min": 250, "max": 350},
        "cost_analysis": {"min": 200, "max": 300},
        "bpmn_description": {"min": 100, "max": 150},
        "per_process": {"min": 1050, "optimal": 1200, "max": 1500}
    }
    
    STEP3_REQUIREMENTS = {
        "introduction": {"min": 100, "max": 150},
        "scenario_lb": {"min": 300, "max": 400},
        "scenario_mb": {"min": 300, "max": 400},
        "scenario_hb": {"min": 300, "max": 400},
        "comparison": {"min": 100, "max": 150},
        "per_process": {"min": 1100, "optimal": 1300, "max": 1600}
    }
    
    STEP4_REQUIREMENTS = {
        "executive_summary": {"min": 200, "max": 300},
        "timeline": {"min": 200, "max": 300},
        "risk_management": {"min": 150, "max": 200},
        "next_steps": {"min": 100, "max": 150},
        "total": {"min": 1000, "optimal": 1200, "max": 1500}
    }
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text, handling Polish characters correctly."""
        if not text:
            return 0
        # Remove extra whitespace and count words
        words = re.findall(r'\b\w+\b', text, re.UNICODE)
        return len(words)
    
    @staticmethod
    def validate_step1_output(result: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, int]]:
        """Validate Step 1 output meets minimum requirements.
        
        Returns:
            Tuple of (is_valid, warnings, word_counts)
        """
        warnings = []
        word_counts = {}
        
        # Executive Summary
        exec_summary = result.get("digital_maturity", {}).get("interpretation", "")
        exec_count = OutputQualityValidator.count_words(exec_summary)
        word_counts["executive_summary"] = exec_count
        
        if exec_count < OutputQualityValidator.STEP1_REQUIREMENTS["executive_summary"]["min"]:
            warnings.append(
                f"Executive Summary zbyt krótkie: {exec_count} słów "
                f"(minimum: {OutputQualityValidator.STEP1_REQUIREMENTS['executive_summary']['min']})"
            )
        
        # Legal Analysis (methodology + lean/sigma)
        legal = result.get("legal_analysis", "")
        legal_count = OutputQualityValidator.count_words(legal)
        word_counts["legal_analysis"] = legal_count
        
        if legal_count < 200:  # Combined min for methodology + lean/sigma
            warnings.append(
                f"Analiza prawna i metodologia zbyt krótka: {legal_count} słów (minimum: 200)"
            )
        
        # TOP Processes
        processes = result.get("processes_scoring", [])
        process_text = "\n".join([
            f"{p.get('process_name', '')} {p.get('rationale', '')}"
            for p in processes[:5]  # TOP 5
        ])
        process_count = OutputQualityValidator.count_words(process_text)
        word_counts["top_processes"] = process_count
        
        if process_count < OutputQualityValidator.STEP1_REQUIREMENTS["top_processes"]["min"]:
            warnings.append(
                f"Opis TOP procesów zbyt krótki: {process_count} słów "
                f"(minimum: {OutputQualityValidator.STEP1_REQUIREMENTS['top_processes']['min']})"
            )
        
        # Recommendations (matrix + recommendations)
        recommendations = result.get("recommendations", "")
        rec_count = OutputQualityValidator.count_words(recommendations)
        word_counts["recommendations"] = rec_count
        
        if rec_count < 150:
            warnings.append(
                f"Rekomendacje zbyt krótkie: {rec_count} słów (minimum: 150)"
            )
        
        # Total word count
        total_count = exec_count + legal_count + process_count + rec_count
        word_counts["total"] = total_count
        
        if total_count < OutputQualityValidator.STEP1_REQUIREMENTS["total"]["min"]:
            warnings.append(
                f"Całkowita liczba słów niewystarczająca: {total_count} słów "
                f"(minimum: {OutputQualityValidator.STEP1_REQUIREMENTS['total']['min']}, "
                f"optymalnie: {OutputQualityValidator.STEP1_REQUIREMENTS['total']['optimal']})"
            )
        
        is_valid = len(warnings) == 0
        return is_valid, warnings, word_counts
    
    @staticmethod
    def validate_step2_output(result: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, int]]:
        """Validate Step 2 output meets minimum requirements per process.
        
        Returns:
            Tuple of (is_valid, warnings, word_counts)
        """
        warnings = []
        word_counts = {}
        
        # BPMN Description (should contain process description + AS-IS mapping)
        bpmn = result.get("bpmn_description", "")
        bpmn_count = OutputQualityValidator.count_words(bpmn)
        word_counts["bpmn_description"] = bpmn_count
        
        if bpmn_count < 300:  # Combined min for description + AS-IS
            warnings.append(
                f"Opis procesu i mapowanie AS-IS zbyt krótkie: {bpmn_count} słów (minimum: 300)"
            )
        
        # Bottlenecks Analysis
        bottlenecks = result.get("bottlenecks", [])
        bottleneck_text = "\n".join([
            f"{b.get('name', '')} {b.get('description', '')}"
            for b in bottlenecks
        ])
        bottleneck_count = OutputQualityValidator.count_words(bottleneck_text)
        word_counts["bottlenecks"] = bottleneck_count
        
        if bottleneck_count < OutputQualityValidator.STEP2_REQUIREMENTS["bottlenecks"]["min"]:
            warnings.append(
                f"Analiza wąskich gardeł zbyt krótka: {bottleneck_count} słów "
                f"(minimum: {OutputQualityValidator.STEP2_REQUIREMENTS['bottlenecks']['min']})"
            )
        
        # MUDA Analysis
        muda = result.get("muda_analysis", {})
        muda_text = "\n".join([
            f"{v.get('description', '')}"
            for k, v in muda.items()
            if isinstance(v, dict) and k != "total_waste_cost"
        ])
        muda_count = OutputQualityValidator.count_words(muda_text)
        word_counts["muda_analysis"] = muda_count
        
        if muda_count < OutputQualityValidator.STEP2_REQUIREMENTS["muda_analysis"]["min"]:
            warnings.append(
                f"Analiza MUDA zbyt krótka: {muda_count} słów "
                f"(minimum: {OutputQualityValidator.STEP2_REQUIREMENTS['muda_analysis']['min']})"
            )
        
        # Automation Potential (includes cost analysis context)
        automation = result.get("automation_potential", {})
        auto_text = automation.get("rationale", "")
        auto_count = OutputQualityValidator.count_words(auto_text)
        word_counts["automation_rationale"] = auto_count
        
        # Process Costs should have descriptive context
        costs = result.get("process_costs", {})
        # Estimate that cost analysis should be described in bpmn or automation rationale
        
        # Total word count per process
        total_count = bpmn_count + bottleneck_count + muda_count + auto_count
        word_counts["total"] = total_count
        
        if total_count < OutputQualityValidator.STEP2_REQUIREMENTS["per_process"]["min"]:
            warnings.append(
                f"Całkowita liczba słów dla procesu niewystarczająca: {total_count} słów "
                f"(minimum: {OutputQualityValidator.STEP2_REQUIREMENTS['per_process']['min']}, "
                f"optymalnie: {OutputQualityValidator.STEP2_REQUIREMENTS['per_process']['optimal']})"
            )
        
        is_valid = len(warnings) == 0
        return is_valid, warnings, word_counts
    
    @staticmethod
    def validate_step3_output(result: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, int]]:
        """Validate Step 3 output meets minimum requirements per process.
        
        Returns:
            Tuple of (is_valid, warnings, word_counts)
        """
        warnings = []
        word_counts = {}
        
        # Scenarios analysis
        scenarios = result.get("scenarios", [])
        
        for i, scenario in enumerate(scenarios):
            scenario_name = scenario.get("name", f"scenario_{i}")
            scenario_text = (
                f"{scenario.get('description', '')} "
                f"{scenario.get('scope', '')} "
                f"{scenario.get('process_to_be', {}).get('description', '')}"
            )
            scenario_count = OutputQualityValidator.count_words(scenario_text)
            word_counts[f"scenario_{i}_{scenario_name}"] = scenario_count
            
            min_required = 300
            if scenario_count < min_required:
                warnings.append(
                    f"Scenariusz {scenario_name} zbyt krótki: {scenario_count} słów (minimum: {min_required})"
                )
        
        # Comparison and Recommendation
        comparison = result.get("comparison", {})
        comp_text = f"{comparison.get('recommendation', '')} {comparison.get('rationale', '')}"
        comp_count = OutputQualityValidator.count_words(comp_text)
        word_counts["comparison"] = comp_count
        
        if comp_count < OutputQualityValidator.STEP3_REQUIREMENTS["comparison"]["min"]:
            warnings.append(
                f"Porównanie i rekomendacja zbyt krótkie: {comp_count} słów "
                f"(minimum: {OutputQualityValidator.STEP3_REQUIREMENTS['comparison']['min']})"
            )
        
        # Total word count
        total_count = sum([v for k, v in word_counts.items() if k.startswith("scenario_")]) + comp_count
        word_counts["total"] = total_count
        
        if total_count < OutputQualityValidator.STEP3_REQUIREMENTS["per_process"]["min"]:
            warnings.append(
                f"Całkowita liczba słów dla procesu niewystarczająca: {total_count} słów "
                f"(minimum: {OutputQualityValidator.STEP3_REQUIREMENTS['per_process']['min']}, "
                f"optymalnie: {OutputQualityValidator.STEP3_REQUIREMENTS['per_process']['optimal']})"
            )
        
        is_valid = len(warnings) == 0
        return is_valid, warnings, word_counts
    
    @staticmethod
    def format_validation_report(step: str, is_valid: bool, warnings: List[str], word_counts: Dict[str, int]) -> str:
        """Format a validation report for logging/display."""
        report = [f"\n=== Walidacja jakości outputu: {step} ==="]
        report.append(f"Status: {'✓ PASSED' if is_valid else '✗ FAILED'}")
        report.append(f"\nLiczba słów:")
        for key, count in word_counts.items():
            report.append(f"  - {key}: {count} słów")
        
        if warnings:
            report.append(f"\nOstrzeżenia ({len(warnings)}):")
            for warning in warnings:
                report.append(f"  - {warning}")
        
        return "\n".join(report)
