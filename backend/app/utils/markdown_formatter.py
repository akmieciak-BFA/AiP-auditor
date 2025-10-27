"""Markdown formatter for BFA Audit reports.

This module formats complete audit data into downloadable Markdown files.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MarkdownFormatter:
    """Formats audit data into professional Markdown reports."""
    
    @staticmethod
    def format_complete_audit(
        project_name: str,
        client_name: str,
        step1_data: Optional[Dict[str, Any]] = None,
        step2_data: Optional[Dict[str, Any]] = None,
        step3_data: Optional[Dict[str, Any]] = None,
        step4_data: Optional[Dict[str, Any]] = None,
        organization_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate complete audit report in Markdown format.
        
        Args:
            project_name: Project name
            client_name: Client organization name
            step1_data: Step 1 analysis results
            step2_data: Step 2 process mapping results (dict of processes)
            step3_data: Step 3 recommendations (dict of processes)
            step4_data: Step 4 summary (optional)
            organization_data: Original organization data from questionnaire
        
        Returns:
            Markdown formatted string ready for download
        """
        md = []
        
        # Header
        md.append(MarkdownFormatter._format_header(project_name, client_name))
        
        # Table of Contents
        md.append(MarkdownFormatter._format_toc(step1_data, step2_data, step3_data, step4_data))
        
        # Step 1: Initial Analysis
        if step1_data:
            md.append(MarkdownFormatter._format_step1(step1_data, organization_data))
        
        # Step 2: Process Mapping
        if step2_data:
            md.append(MarkdownFormatter._format_step2(step2_data))
        
        # Step 3: Recommendations
        if step3_data:
            md.append(MarkdownFormatter._format_step3(step3_data))
        
        # Step 4: Summary
        if step4_data:
            md.append(MarkdownFormatter._format_step4(step4_data))
        
        # Footer with quality metrics
        md.append(MarkdownFormatter._format_footer(step1_data, step2_data, step3_data))
        
        return "\n\n".join(md)
    
    @staticmethod
    def _format_header(project_name: str, client_name: str) -> str:
        """Format report header."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        return f"""# Audyt Automatyzacyjny BFA
## {client_name}

**Projekt:** {project_name}  
**Data wygenerowania:** {now}  
**Wygenerowane przez:** BFA Audit App

---
"""
    
    @staticmethod
    def _format_toc(step1: Any, step2: Any, step3: Any, step4: Any) -> str:
        """Format table of contents."""
        toc = ["## Spis Treści\n"]
        
        if step1:
            toc.append("1. [Krok 1: Analiza Wstępna](#krok-1-analiza-wstępna)")
        if step2:
            toc.append("2. [Krok 2: Mapowanie Procesów](#krok-2-mapowanie-procesów)")
        if step3:
            toc.append("3. [Krok 3: Rekomendacje Technologiczne](#krok-3-rekomendacje-technologiczne)")
        if step4:
            toc.append("4. [Krok 4: Podsumowanie i Harmonogram](#krok-4-podsumowanie-i-harmonogram)")
        
        toc.append("\n---")
        return "\n".join(toc)
    
    @staticmethod
    def _format_step1(step1_data: Dict[str, Any], org_data: Optional[Dict[str, Any]] = None) -> str:
        """Format Step 1: Initial Analysis."""
        md = ["# Krok 1: Analiza Wstępna\n"]
        
        # Quality Metrics
        if "_quality_metrics" in step1_data:
            metrics = step1_data["_quality_metrics"]
            total_words = sum(metrics.get("word_counts", {}).values())
            status = "✅ Spełnia standardy" if metrics.get("is_valid") else "⚠️ Poniżej standardów"
            md.append(f"**Jakość outputu:** {status} ({total_words} słów)\n")
        
        # Executive Summary
        if "digital_maturity" in step1_data:
            dm = step1_data["digital_maturity"]
            md.append("## 1.1 Executive Summary\n")
            md.append(dm.get("interpretation", ""))
            md.append("\n### Ocena Dojrzałości Cyfrowej\n")
            md.append(f"- **Process Maturity:** {dm.get('process_maturity', 0)}/100")
            md.append(f"- **Digital Infrastructure:** {dm.get('digital_infrastructure', 0)}/100")
            md.append(f"- **Data Quality:** {dm.get('data_quality', 0)}/100")
            md.append(f"- **Organizational Readiness:** {dm.get('organizational_readiness', 0)}/100")
            md.append(f"- **Financial Capacity:** {dm.get('financial_capacity', 0)}/100")
            md.append(f"- **Strategic Alignment:** {dm.get('strategic_alignment', 0)}/100")
            md.append(f"\n**Ogólny wynik:** {dm.get('overall_score', 0)}/100\n")
        
        # Methodology and Legal Analysis
        if "legal_analysis" in step1_data:
            md.append("## 1.2 Metodologia i Analiza Prawna (Lex/Sigma)\n")
            md.append(step1_data.get("legal_analysis", ""))
            md.append("")
        
        # TOP Processes
        if "processes_scoring" in step1_data:
            md.append("## 1.3 TOP Procesy do Automatyzacji\n")
            for i, proc in enumerate(step1_data["processes_scoring"], 1):
                md.append(f"### {i}. {proc.get('process_name', 'Proces')}")
                md.append(f"**Scoring:** {proc.get('score', 0)}/100 | **Tier:** {proc.get('tier', 'N/A')}\n")
                md.append(proc.get("rationale", ""))
                md.append("")
        
        # System Dependencies and Recommendations
        if "recommendations" in step1_data:
            md.append("## 1.4 Współzależności i Rekomendacje\n")
            md.append(step1_data.get("recommendations", ""))
            md.append("")
        
        # System Dependencies Matrix
        if "system_dependencies" in step1_data:
            sys_dep = step1_data["system_dependencies"]
            if "systems" in sys_dep and sys_dep["systems"]:
                md.append("### Systemy IT\n")
                for system in sys_dep["systems"]:
                    md.append(f"- {system}")
                md.append("")
        
        md.append("---")
        return "\n".join(md)
    
    @staticmethod
    def _format_step2(step2_data: Dict[str, Any]) -> str:
        """Format Step 2: Process Mapping."""
        md = ["# Krok 2: Mapowanie Procesów\n"]
        
        for process_name, process_results in step2_data.items():
            md.append(f"## 2. Proces: {process_name}\n")
            
            # Quality Metrics
            if "_quality_metrics" in process_results:
                metrics = process_results["_quality_metrics"]
                total_words = sum(metrics.get("word_counts", {}).values())
                status = "✅ Spełnia standardy" if metrics.get("is_valid") else "⚠️ Poniżej standardów"
                md.append(f"**Jakość outputu:** {status} ({total_words} słów)\n")
            
            # BPMN Description (Process Description + AS-IS Mapping)
            if "bpmn_description" in process_results:
                md.append("### 2.1 Opis Procesu i Mapowanie AS-IS\n")
                md.append(process_results.get("bpmn_description", ""))
                md.append("")
            
            # Bottlenecks
            if "bottlenecks" in process_results:
                md.append("### 2.2 Wąskie Gardła\n")
                for i, bn in enumerate(process_results.get("bottlenecks", []), 1):
                    md.append(f"#### {i}. {bn.get('name', 'Wąskie gardło')}")
                    md.append(f"**Wpływ:** {bn.get('impact', 'N/A')}")
                    md.append(f"\n{bn.get('description', '')}")
                    md.append(f"\n**Koszt roczny:** {bn.get('cost_per_year', 0):,.0f} PLN\n")
            
            # MUDA Analysis
            if "muda_analysis" in process_results:
                md.append("### 2.3 Analiza MUDA (8 Typów Marnotrawstwa)\n")
                muda = process_results["muda_analysis"]
                
                muda_types = {
                    "defects": "Defekty",
                    "overproduction": "Nadprodukcja",
                    "waiting": "Oczekiwanie",
                    "non_utilized_talent": "Niewykorzystany potencjał ludzki",
                    "transportation": "Transport",
                    "inventory": "Zapasy",
                    "motion": "Zbędny ruch",
                    "extra_processing": "Nadmierne przetwarzanie"
                }
                
                for key, label in muda_types.items():
                    if key in muda and isinstance(muda[key], dict):
                        md.append(f"#### {label}")
                        md.append(muda[key].get("description", ""))
                        md.append(f"**Koszt roczny:** {muda[key].get('cost_per_year', 0):,.0f} PLN\n")
                
                if "total_waste_cost" in muda:
                    md.append(f"**Łączny koszt marnotrawstwa:** {muda['total_waste_cost']:,.0f} PLN/rok\n")
            
            # Process Costs
            if "process_costs" in process_results:
                md.append("### 2.4 Koszty Procesu (Time-Driven ABC)\n")
                costs = process_results["process_costs"]
                md.append(f"- **Koszty pracy:** {costs.get('labor_costs', 0):,.0f} PLN/rok")
                md.append(f"- **Koszty operacyjne:** {costs.get('operational_costs', 0):,.0f} PLN/rok")
                md.append(f"- **Koszty błędów:** {costs.get('error_costs', 0):,.0f} PLN/rok")
                md.append(f"- **Koszty opóźnień:** {costs.get('delay_costs', 0):,.0f} PLN/rok")
                md.append(f"\n**Całkowity koszt roczny:** {costs.get('total_cost', 0):,.0f} PLN\n")
            
            # Automation Potential
            if "automation_potential" in process_results:
                md.append("### 2.5 Potencjał Automatyzacji\n")
                auto = process_results["automation_potential"]
                md.append(f"**{auto.get('percentage', 0)}%** procesu możliwe do automatyzacji\n")
                md.append(auto.get("rationale", ""))
                
                if "automatable_steps" in auto and auto["automatable_steps"]:
                    md.append("\n**Kroki do automatyzacji:**")
                    for step in auto["automatable_steps"]:
                        md.append(f"- {step}")
                md.append("")
            
            md.append("---\n")
        
        return "\n".join(md)
    
    @staticmethod
    def _format_step3(step3_data: Dict[str, Any]) -> str:
        """Format Step 3: Technology Recommendations."""
        md = ["# Krok 3: Rekomendacje Technologiczne i Analiza ROI\n"]
        
        for process_name, recommendations in step3_data.items():
            md.append(f"## 3. Rekomendacje dla procesu: {process_name}\n")
            
            # Quality Metrics
            if "_quality_metrics" in recommendations:
                metrics = recommendations["_quality_metrics"]
                total_words = sum(metrics.get("word_counts", {}).values())
                status = "✅ Spełnia standardy" if metrics.get("is_valid") else "⚠️ Poniżej standardów"
                md.append(f"**Jakość outputu:** {status} ({total_words} słów)\n")
            
            # Technology Research
            if "technology_research" in recommendations:
                tech = recommendations["technology_research"]
                if "categories" in tech and tech["categories"]:
                    md.append("### 3.1 Kategorie Technologii\n")
                    md.append(", ".join(tech["categories"]))
                    md.append("\n")
            
            # Scenarios
            if "scenarios" in recommendations:
                for i, scenario in enumerate(recommendations["scenarios"], 1):
                    md.append(f"### 3.{i+1} {scenario.get('name', f'Scenariusz {i}')}\n")
                    md.append(scenario.get("description", ""))
                    md.append(f"\n**Zakres:** {scenario.get('scope', '')}\n")
                    
                    # Technologies
                    if "technologies" in scenario and scenario["technologies"]:
                        md.append("**Technologie:**")
                        for tech in scenario["technologies"]:
                            md.append(f"- {tech}")
                        md.append("")
                    
                    # Solutions
                    if "solutions" in scenario and scenario["solutions"]:
                        md.append("**Rozwiązania:**")
                        for sol in scenario["solutions"]:
                            md.append(f"- **{sol.get('vendor', 'N/A')}** - {sol.get('product', 'N/A')}")
                            if "rationale" in sol:
                                md.append(f"  {sol['rationale']}")
                        md.append("")
                    
                    # Costs
                    if "costs" in scenario:
                        costs = scenario["costs"]
                        md.append("#### Koszty\n")
                        
                        if "capex" in costs and isinstance(costs["capex"], dict):
                            capex = costs["capex"]
                            md.append(f"**CAPEX (inwestycja jednorazowa):** {capex.get('total', 0):,.0f} PLN")
                            if "licenses" in capex:
                                md.append(f"- Licencje: {capex['licenses']:,.0f} PLN")
                            if "infrastructure" in capex:
                                md.append(f"- Infrastruktura: {capex['infrastructure']:,.0f} PLN")
                            if "consulting" in capex:
                                md.append(f"- Consulting: {capex['consulting']:,.0f} PLN")
                            if "training" in capex:
                                md.append(f"- Szkolenia: {capex['training']:,.0f} PLN")
                            md.append("")
                        
                        if "opex_year1" in costs and isinstance(costs["opex_year1"], dict):
                            opex = costs["opex_year1"]
                            md.append(f"**OPEX (koszty roczne):** {opex.get('total', 0):,.0f} PLN/rok")
                            if "licenses" in opex:
                                md.append(f"- Licencje: {opex['licenses']:,.0f} PLN/rok")
                            if "support" in opex:
                                md.append(f"- Wsparcie: {opex['support']:,.0f} PLN/rok")
                            md.append("")
                    
                    # Benefits
                    if "benefits_year1" in scenario:
                        benefits = scenario["benefits_year1"]
                        md.append("#### Korzyści (rok 1)\n")
                        md.append(f"**Całkowite oszczędności:** {benefits.get('total', 0):,.0f} PLN/rok")
                        if "fte_savings" in benefits:
                            md.append(f"- Oszczędności FTE: {benefits['fte_savings']:,.0f} PLN/rok")
                        if "operational_savings" in benefits:
                            md.append(f"- Oszczędności operacyjne: {benefits['operational_savings']:,.0f} PLN/rok")
                        if "error_reduction" in benefits:
                            md.append(f"- Redukcja błędów: {benefits['error_reduction']:,.0f} PLN/rok")
                        md.append("")
                    
                    # Financial Analysis
                    if "financial_analysis" in scenario:
                        fa = scenario["financial_analysis"]
                        md.append("#### Analiza Finansowa (3 lata)\n")
                        md.append(f"- **ROI:** {fa.get('roi_3years', 0):.1f}%")
                        md.append(f"- **Payback Period:** {fa.get('payback_months', 0)} miesięcy")
                        md.append(f"- **NPV:** {fa.get('npv', 0):,.0f} PLN")
                        md.append("")
                    
                    # Process TO-BE
                    if "process_to_be" in scenario:
                        tobe = scenario["process_to_be"]
                        md.append("#### Proces TO-BE (po automatyzacji)\n")
                        md.append(tobe.get("description", ""))
                        md.append(f"\n- **Czas cyklu:** {tobe.get('cycle_time_hours', 0):.1f}h")
                        md.append(f"- **FTE wymagane:** {tobe.get('fte_required', 0):.1f}")
                        md.append("")
                    
                    md.append("---\n")
            
            # Comparison and Recommendation
            if "comparison" in recommendations:
                md.append("### 3.X Porównanie Scenariuszy i Rekomendacja\n")
                comp = recommendations["comparison"]
                
                # Table
                if "table" in comp and comp["table"]:
                    md.append("#### Tabela Porównawcza\n")
                    table = comp["table"]
                    if len(table) > 0:
                        # Header
                        md.append("| " + " | ".join(str(cell) for cell in table[0]) + " |")
                        md.append("|" + "|".join(["---" for _ in table[0]]) + "|")
                        # Rows
                        for row in table[1:]:
                            md.append("| " + " | ".join(str(cell) for cell in row) + " |")
                        md.append("")
                
                md.append("#### Rekomendacja\n")
                md.append(comp.get("recommendation", ""))
                md.append(f"\n**Uzasadnienie:**\n{comp.get('rationale', '')}")
                md.append("")
            
            md.append("---\n")
        
        return "\n".join(md)
    
    @staticmethod
    def _format_step4(step4_data: Dict[str, Any]) -> str:
        """Format Step 4: Summary and Timeline."""
        md = ["# Krok 4: Podsumowanie i Harmonogram\n"]
        
        # Add Step 4 content when implemented
        md.append("*Krok 4 w trakcie implementacji*\n")
        
        md.append("---")
        return "\n".join(md)
    
    @staticmethod
    def _format_footer(step1: Any, step2: Any, step3: Any) -> str:
        """Format report footer with overall quality metrics."""
        md = ["---\n", "## Podsumowanie Jakości Raportu\n"]
        
        total_words = 0
        all_valid = True
        
        if step1 and "_quality_metrics" in step1:
            metrics = step1["_quality_metrics"]
            words = sum(metrics.get("word_counts", {}).values())
            total_words += words
            status = "✅" if metrics.get("is_valid") else "⚠️"
            all_valid = all_valid and metrics.get("is_valid", False)
            md.append(f"- **Krok 1:** {status} {words} słów")
        
        if step2:
            step2_words = 0
            for proc_name, proc_data in step2.items():
                if "_quality_metrics" in proc_data:
                    metrics = proc_data["_quality_metrics"]
                    words = sum(metrics.get("word_counts", {}).values())
                    step2_words += words
                    all_valid = all_valid and metrics.get("is_valid", False)
            total_words += step2_words
            status = "✅" if all_valid else "⚠️"
            md.append(f"- **Krok 2:** {status} {step2_words} słów ({len(step2)} procesów)")
        
        if step3:
            step3_words = 0
            for proc_name, proc_data in step3.items():
                if "_quality_metrics" in proc_data:
                    metrics = proc_data["_quality_metrics"]
                    words = sum(metrics.get("word_counts", {}).values())
                    step3_words += words
                    all_valid = all_valid and metrics.get("is_valid", False)
            total_words += step3_words
            status = "✅" if all_valid else "⚠️"
            md.append(f"- **Krok 3:** {status} {step3_words} słów ({len(step3)} procesów)")
        
        md.append(f"\n**Całkowita liczba słów:** {total_words}")
        
        # Estimate slides
        estimated_slides = max(10, int(total_words / 220))
        md.append(f"**Szacowana liczba slajdów Gamma:** {estimated_slides}")
        
        overall_status = "✅ Spełnia standard Turris" if all_valid else "⚠️ Wymaga poprawy"
        md.append(f"\n**Status ogólny:** {overall_status}")
        
        md.append(f"\n---\n*Raport wygenerowany przez BFA Audit App v1.0*")
        
        return "\n".join(md)
