"""Gamma.app API service for generating presentations.

This module handles interaction with Gamma.app API to generate
professional presentations from audit content.
"""

import logging
import requests
from typing import Dict, Any, Optional
from ..config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class GammaService:
    """Service for interacting with Gamma.app API."""
    
    def __init__(self):
        self.api_key = settings.gamma_api_key
        self.base_url = "https://api.gamma.app/v1"
    
    def generate_presentation(
        self,
        content: str,
        title: str,
        theme: str = "professional",
        slide_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate a presentation using Gamma.app API.
        
        Args:
            content: Markdown content for the presentation
            title: Presentation title
            theme: Theme name (default: professional)
            slide_count: Target number of slides (optional)
        
        Returns:
            Dict with presentation URL and metadata
        """
        if not self.api_key:
            raise ValueError("Gamma API key not configured")
        
        logger.info(f"Generating Gamma presentation: {title}")
        
        # Note: This is a placeholder for actual Gamma API integration
        # Actual API endpoints and authentication may differ
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "title": title,
            "content": content,
            "theme": theme,
            "format": "markdown"
        }
        
        if slide_count:
            payload["slide_count"] = slide_count
        
        try:
            response = requests.post(
                f"{self.base_url}/presentations",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Gamma presentation created: {result.get('url', 'N/A')}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Gamma API error: {e}")
            raise ValueError(f"Failed to generate presentation: {str(e)}")
    
    def estimate_slide_count(self, word_count: int) -> int:
        """Estimate slide count based on word count.
        
        Based on Turris analysis:
        - TOP 5 processes: 14,700 words → 50-80 slides
        - TOP 10 processes: 28,000 words → 90-140 slides
        
        Average: ~200-250 words per slide
        """
        words_per_slide = 220  # Average from Turris analysis
        return max(10, int(word_count / words_per_slide))
    
    def format_audit_for_gamma(
        self,
        step1_data: Dict[str, Any],
        step2_data: Dict[str, Any],
        step3_data: Dict[str, Any],
        step4_data: Optional[Dict[str, Any]] = None,
        client_name: str = "Client"
    ) -> str:
        """Format audit data into Gamma-compatible markdown.
        
        Args:
            step1_data: Step 1 analysis results
            step2_data: Step 2 process mapping results (dict of processes)
            step3_data: Step 3 recommendations (dict of processes)
            step4_data: Step 4 summary (optional)
            client_name: Client organization name
        
        Returns:
            Markdown formatted string for Gamma
        """
        markdown = []
        
        # Title slide
        markdown.append(f"# Audyt Automatyzacyjny BFA")
        markdown.append(f"## {client_name}")
        markdown.append(f"\n---\n")
        
        # Step 1: Initial Analysis
        markdown.append("# Krok 1: Analiza Wstępna\n")
        
        if "digital_maturity" in step1_data:
            dm = step1_data["digital_maturity"]
            markdown.append("## Executive Summary\n")
            markdown.append(dm.get("interpretation", ""))
            markdown.append("\n---\n")
            
            markdown.append("## Dojrzałość Cyfrowa\n")
            markdown.append(f"- Process Maturity: {dm.get('process_maturity', 0)}/100")
            markdown.append(f"- Digital Infrastructure: {dm.get('digital_infrastructure', 0)}/100")
            markdown.append(f"- Data Quality: {dm.get('data_quality', 0)}/100")
            markdown.append(f"- Organizational Readiness: {dm.get('organizational_readiness', 0)}/100")
            markdown.append(f"- Financial Capacity: {dm.get('financial_capacity', 0)}/100")
            markdown.append(f"- Strategic Alignment: {dm.get('strategic_alignment', 0)}/100")
            markdown.append(f"\n**Ogólny wynik**: {dm.get('overall_score', 0)}/100")
            markdown.append("\n---\n")
        
        if "processes_scoring" in step1_data:
            markdown.append("## TOP Procesy do Automatyzacji\n")
            for i, proc in enumerate(step1_data["processes_scoring"][:5], 1):
                markdown.append(f"\n### {i}. {proc.get('process_name', 'Proces')}")
                markdown.append(f"**Scoring**: {proc.get('score', 0)}/100 (Tier {proc.get('tier', 'N/A')})")
                markdown.append(f"\n{proc.get('rationale', '')}")
                markdown.append("\n---\n")
        
        if "legal_analysis" in step1_data:
            markdown.append("## Metodologia i Analiza Prawna\n")
            markdown.append(step1_data.get("legal_analysis", ""))
            markdown.append("\n---\n")
        
        if "recommendations" in step1_data:
            markdown.append("## Współzależności i Rekomendacje\n")
            markdown.append(step1_data.get("recommendations", ""))
            markdown.append("\n---\n")
        
        # Step 2: Process Mapping (for each process)
        if step2_data:
            markdown.append("# Krok 2: Mapowanie Procesów\n")
            markdown.append("\n---\n")
            
            for proc_name, proc_data in step2_data.items():
                markdown.append(f"## Proces: {proc_name}\n")
                
                # BPMN Description
                if "bpmn_description" in proc_data:
                    markdown.append("### Opis Procesu AS-IS\n")
                    markdown.append(proc_data.get("bpmn_description", ""))
                    markdown.append("\n---\n")
                
                # Bottlenecks
                if "bottlenecks" in proc_data:
                    markdown.append("### Wąskie Gardła\n")
                    for bn in proc_data.get("bottlenecks", []):
                        markdown.append(f"\n**{bn.get('name', 'N/A')}** ({bn.get('impact', 'N/A')})")
                        markdown.append(f"\n{bn.get('description', '')}")
                        markdown.append(f"\n*Koszt roczny*: {bn.get('cost_per_year', 0):,.0f} PLN")
                    markdown.append("\n---\n")
                
                # MUDA Analysis
                if "muda_analysis" in proc_data:
                    markdown.append("### Analiza MUDA (8 Typów Marnotrawstwa)\n")
                    muda = proc_data.get("muda_analysis", {})
                    for muda_type, muda_data in muda.items():
                        if isinstance(muda_data, dict) and muda_type != "total_waste_cost":
                            markdown.append(f"\n**{muda_type.replace('_', ' ').title()}**")
                            markdown.append(f"\n{muda_data.get('description', '')}")
                            markdown.append(f"\n*Koszt*: {muda_data.get('cost_per_year', 0):,.0f} PLN/rok")
                    markdown.append(f"\n\n**Łączny koszt marnotrawstwa**: {muda.get('total_waste_cost', 0):,.0f} PLN/rok")
                    markdown.append("\n---\n")
                
                # Costs
                if "process_costs" in proc_data:
                    markdown.append("### Koszty Procesu\n")
                    costs = proc_data.get("process_costs", {})
                    markdown.append(f"- Koszty pracy: {costs.get('labor_costs', 0):,.0f} PLN")
                    markdown.append(f"- Koszty operacyjne: {costs.get('operational_costs', 0):,.0f} PLN")
                    markdown.append(f"- Koszty błędów: {costs.get('error_costs', 0):,.0f} PLN")
                    markdown.append(f"- Koszty opóźnień: {costs.get('delay_costs', 0):,.0f} PLN")
                    markdown.append(f"\n**Całkowity koszt**: {costs.get('total_cost', 0):,.0f} PLN/rok")
                    markdown.append("\n---\n")
                
                # Automation Potential
                if "automation_potential" in proc_data:
                    markdown.append("### Potencjał Automatyzacji\n")
                    auto = proc_data.get("automation_potential", {})
                    markdown.append(f"**{auto.get('percentage', 0)}%** procesu możliwe do automatyzacji")
                    markdown.append(f"\n{auto.get('rationale', '')}")
                    markdown.append("\n---\n")
        
        # Step 3: Recommendations (for each process)
        if step3_data:
            markdown.append("# Krok 3: Rekomendacje Technologiczne\n")
            markdown.append("\n---\n")
            
            for proc_name, proc_recs in step3_data.items():
                markdown.append(f"## Rekomendacje: {proc_name}\n")
                
                # Scenarios
                if "scenarios" in proc_recs:
                    for scenario in proc_recs.get("scenarios", []):
                        markdown.append(f"\n### {scenario.get('name', 'Scenariusz')}\n")
                        markdown.append(f"\n{scenario.get('description', '')}")
                        markdown.append(f"\n**Zakres**: {scenario.get('scope', '')}")
                        
                        # Costs
                        if "costs" in scenario:
                            costs = scenario["costs"]
                            if "capex" in costs:
                                capex = costs["capex"]
                                markdown.append(f"\n**CAPEX**: {capex.get('total', 0):,.0f} PLN")
                            if "opex_year1" in costs:
                                opex = costs["opex_year1"]
                                markdown.append(f"\n**OPEX** (rok 1): {opex.get('total', 0):,.0f} PLN")
                        
                        # Financial Analysis
                        if "financial_analysis" in scenario:
                            fa = scenario["financial_analysis"]
                            markdown.append(f"\n**ROI** (3 lata): {fa.get('roi_3years', 0):.1f}%")
                            markdown.append(f"\n**Payback**: {fa.get('payback_months', 0)} miesięcy")
                            markdown.append(f"\n**NPV** (3 lata): {fa.get('npv', 0):,.0f} PLN")
                        
                        # Process TO-BE
                        if "process_to_be" in scenario:
                            tobe = scenario["process_to_be"]
                            markdown.append(f"\n\n**Proces TO-BE**:")
                            markdown.append(f"\n{tobe.get('description', '')}")
                        
                        markdown.append("\n---\n")
                
                # Comparison
                if "comparison" in proc_recs:
                    markdown.append("### Porównanie Scenariuszy\n")
                    comp = proc_recs.get("comparison", {})
                    markdown.append(f"\n{comp.get('recommendation', '')}")
                    markdown.append(f"\n{comp.get('rationale', '')}")
                    markdown.append("\n---\n")
        
        # Step 4: Summary (optional)
        if step4_data:
            markdown.append("# Krok 4: Podsumowanie i Harmonogram\n")
            markdown.append("\n---\n")
            # Add Step 4 content here when implemented
        
        return "\n".join(markdown)
