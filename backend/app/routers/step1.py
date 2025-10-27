from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging
import os
from pathlib import Path
from ..database import get_db
from ..models.project import Project
from ..models.step1 import Step1Data
from ..schemas.step1 import InitialAssessmentData, Step1AnalysisResult
from ..services.claude_service import ClaudeService
from ..middleware.rate_limit import ai_analysis_rate_limit
from ..middleware.security import sanitize_dict
from ..utils.output_validator import OutputQualityValidator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects/{project_id}/step1", tags=["step1"])


@router.post("/analyze", response_model=Step1AnalysisResult)
def analyze_step1(
    project_id: int,
    data: InitialAssessmentData,
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(ai_analysis_rate_limit)
):
    """Analyze Step 1 data using Claude API with extended thinking."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if Step1Data already exists from document processing
    step1_data = db.query(Step1Data).filter(
        Step1Data.project_id == project_id
    ).first()
    
    if step1_data and step1_data.analysis_results:
        # Already analyzed from documents - return existing results
        logger.info(f"Using existing Step1Data from document analysis for project {project_id}")
        return Step1AnalysisResult(**step1_data.analysis_results)
    
    # Sanitize data
    clean_data = sanitize_dict(data.model_dump())
    
    # Call Claude API with extended thinking
    claude_service = ClaudeService()
    try:
        logger.info(f"Analyzing Step 1 for project {project_id} with extended thinking")
        analysis_results = claude_service.analyze_step1_comprehensive(clean_data)
        
        # Validate output quality
        validator = OutputQualityValidator()
        is_valid, warnings, word_counts = validator.validate_step1_output(analysis_results)
        
        # Log validation results
        validation_report = validator.format_validation_report("Step 1", is_valid, warnings, word_counts)
        logger.info(validation_report)
        
        # Add quality metrics to results
        analysis_results["_quality_metrics"] = {
            "is_valid": is_valid,
            "word_counts": word_counts,
            "warnings": warnings
        }
        
        if not is_valid:
            logger.warning(f"Step 1 output quality below threshold. Warnings: {warnings}")
            # Don't fail the request, but log the warning
            
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    
    # Save to database
    step1_data = db.query(Step1Data).filter(Step1Data.project_id == project_id).first()
    
    if step1_data:
        step1_data.organization_data = clean_data
        step1_data.analysis_results = analysis_results
    else:
        step1_data = Step1Data(
            project_id=project_id,
            organization_data=clean_data,
            analysis_results=analysis_results
        )
        db.add(step1_data)
    
    # Update project status
    project.status = "step2"
    
    db.commit()
    db.refresh(step1_data)
    
    # Generate markdown report
    try:
        _generate_step1_markdown_report(project, clean_data, analysis_results)
    except Exception as e:
        logger.error(f"Failed to generate markdown report: {e}")
        # Don't fail the request if report generation fails
    
    return Step1AnalysisResult(**analysis_results)


def _generate_step1_markdown_report(project: Project, data: Dict[str, Any], results: Dict[str, Any]):
    """Generate markdown report for Step 1."""
    # Create project directory
    project_dir = Path(f"./project_reports/{project.name.replace(' ', '_')}")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = project_dir / "STEP1_ANALIZA_WSTEPNA.md"
    
    # Generate markdown content
    markdown_content = f"""# KROK 1: ANALIZA WSTĘPNA - AUDYT AUTOMATYZACYJNY BFA

## Informacje o Projekcie

- **Projekt:** {project.name}
- **Klient:** {project.client_name}
- **Data:** {project.created_at.strftime('%Y-%m-%d %H:%M')}

---

## SEKCJA A: INFORMACJE ORGANIZACYJNE

### Podstawowe dane organizacji

- **Nazwa organizacji:** {data.get('organization_name', 'N/A')}
- **Branża:** {data.get('industry', 'N/A')}
- **Wielkość:** {data.get('company_size', 'N/A')}
- **Roczny obrót:** {data.get('annual_revenue', 0):,.0f} PLN
- **Lokalizacja:** {data.get('headquarters_location', 'N/A')}
- **Liczba lokalizacji:** {data.get('number_of_locations', 0)}

### Obszary funkcjonalne

**Aktywne obszary:**
{chr(10).join(f"- {area}" for area in data.get('functional_areas', []))}

**Krytyczne obszary (TOP 3):**
{chr(10).join(f"- {area}" for area in data.get('critical_areas', []))}

### Dojrzałość cyfrowa

| Obszar | Ocena (0-10) |
|--------|--------------|
| Systemy ERP | {data.get('digital_maturity_erp', 0)} |
| CRM | {data.get('digital_maturity_crm', 0)} |
| Automatyzacja produkcji | {data.get('digital_maturity_production', 0)} |
| RPA | {data.get('digital_maturity_rpa', 0)} |
| Analityka BI | {data.get('digital_maturity_analytics', 0)} |
| IoT | {data.get('digital_maturity_iot', 0)} |
| AI/ML | {data.get('digital_maturity_ai', 0)} |
| Automatyzacja komunikacji | {data.get('digital_maturity_communication', 0)} |
| Workflow BPM | {data.get('digital_maturity_workflow', 0)} |
| Cloud | {data.get('digital_maturity_cloud', 0)} |

### Budżet i inwestycje

- **Planowany budżet:** {data.get('budget_range', 'N/A')}
- **Oczekiwany payback:** {data.get('expected_payback_months', 0)} miesięcy

---

## SEKCJA B: IDENTYFIKACJA PROBLEMÓW

### Główne wyzwania operacyjne

{data.get('challenges_description', 'Brak opisu')}

---

## SEKCJA C: CELE I OCZEKIWANIA

### Cele finansowe

- **Redukcja kosztów operacyjnych:** {data.get('expected_cost_reduction_percent', 0)}% rocznie
- **Wzrost przychodów:** {data.get('expected_revenue_increase_percent', 0)}% rocznie
- **Oczekiwany ROI:** {data.get('expected_roi_percent', 0)}%
- **Cel oszczędności:** {data.get('specific_savings_goal', 0):,.0f} PLN

### Źródła oszczędności

{data.get('savings_sources_description', 'Brak opisu')}

---

## SEKCJA D: ZASOBY WEWNĘTRZNE

- **Zespół IT:** {data.get('has_it_team', 'N/A')} ({data.get('it_team_size', 0)} osób)
- **Dział BPM:** {data.get('has_bpm_department', 'N/A')}
- **Doświadczenie automatyzacji:** {data.get('automation_experience', 'N/A')}
- **Project Manager:** {data.get('has_project_manager', 'N/A')}
- **Change Manager:** {data.get('has_change_manager', 'N/A')}

---

## SEKCJA E: STRATEGIA BIZNESOWA

### Strategia 3-5 lat

{data.get('business_strategy_description', 'Brak opisu')}

### Dodatkowe uwagi

{data.get('additional_notes', 'Brak')}

---

## WYNIKI ANALIZY CLAUDE API (Extended Thinking)

### Ocena dojrzałości cyfrowej

{results.get('digital_maturity', {}).get('interpretation', 'Brak danych')}

**Scoring:**
- **Process Maturity:** {results.get('digital_maturity', {}).get('process_maturity', 0)}/100
- **Digital Infrastructure:** {results.get('digital_maturity', {}).get('digital_infrastructure', 0)}/100
- **Data Quality:** {results.get('digital_maturity', {}).get('data_quality', 0)}/100
- **Organizational Readiness:** {results.get('digital_maturity', {}).get('organizational_readiness', 0)}/100
- **Financial Capacity:** {results.get('digital_maturity', {}).get('financial_capacity', 0)}/100
- **Strategic Alignment:** {results.get('digital_maturity', {}).get('strategic_alignment', 0)}/100

**Overall Score:** {results.get('digital_maturity', {}).get('overall_score', 0)}/100

### TOP Procesy do automatyzacji

{chr(10).join(f"{i+1}. **{proc}**" for i, proc in enumerate(results.get('top_processes', [])))}

### Scoring procesów według BFA 6-wymiarowego frameworku

{chr(10).join(f"#### {proc.get('process_name', 'N/A')}{chr(10)}- **Score:** {proc.get('score', 0)}/100{chr(10)}- **Tier:** {proc.get('tier', 0)}{chr(10)}- **Uzasadnienie:** {proc.get('rationale', 'N/A')}{chr(10)}" for proc in results.get('processes_scoring', []))}

### Analiza prawna (Lex/Sigma)

{results.get('legal_analysis', 'Brak danych')}

### Rekomendacje

{results.get('recommendations', 'Brak rekomendacji')}

---

**Raport wygenerowany automatycznie przez BFA Audit App**
**Powered by Claude Sonnet 4.5 with Extended Thinking**
"""
    
    # Write to file
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    logger.info(f"Step 1 markdown report generated: {report_path}")


@router.get("/results", response_model=Step1AnalysisResult)
def get_step1_results(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get Step 1 analysis results."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    step1_data = db.query(Step1Data).filter(Step1Data.project_id == project_id).first()
    
    if not step1_data or not step1_data.analysis_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step 1 analysis not found"
        )
    
    return Step1AnalysisResult(**step1_data.analysis_results)
