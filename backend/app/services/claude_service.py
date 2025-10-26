import json
import logging
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from ..config import get_settings
from .cache_service import (
    cache_form_generation,
    save_form_generation,
    cache_step1_analysis,
    save_step1_analysis
)

settings = get_settings()
logger = logging.getLogger(__name__)


class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.claude_api_key) if settings.claude_api_key else None
        self.model = "claude-sonnet-4"
        self.default_max_tokens = 16000
        self.document_processing_max_tokens = 200000  # Increased for document processing
    
    def generate_step1_form(self, organization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate dynamic form for Step 1 based on organization data."""
        if not self.client:
            raise ValueError("Claude API key not configured")
        
        # Check cache first
        cached_result = cache_form_generation(organization_data)
        if cached_result:
            logger.info("Form generation cache hit")
            return cached_result
        
        logger.info("Form generation cache miss - calling Claude API")
        
        system_prompt = """Jesteś ekspertem BFA automation-master specjalizującym się w projektowaniu kwestionariuszy diagnostycznych.

Twoim zadaniem jest stworzenie spersonalizowanego kwestionariusza diagnostycznego dla organizacji, który pozwoli na dogłębną analizę jej gotowości do automatyzacji procesów biznesowych.

Zasady tworzenia kwestionariusza:
- Pytania powinny być konkretne i dostosowane do branży i wielkości organizacji
- Mix pytań: tekstowe (otwarte), numeryczne, skale (1-10), i wybór wielokrotny
- 15-25 pytań pogrupowanych w kategorie:
  1. Dojrzałość Procesowa (Process Maturity)
  2. Infrastruktura Cyfrowa (Digital Infrastructure)
  3. Jakość Danych (Data Quality)
  4. Gotowość Organizacyjna (Organizational Readiness)
  5. Zdolność Finansowa (Financial Capacity)
  6. Zgodność Strategiczna (Strategic Alignment)

- Każde pytanie musi mieć:
  - id: unikalny identyfikator
  - category: jedna z 6 kategorii
  - question: treść pytania (po polsku)
  - type: "text" / "number" / "scale" / "select" / "multiselect"
  - required: true/false
  - placeholder: (dla text)
  - options: (dla select/multiselect)
  - min/max: (dla number/scale)
  - help_text: dodatkowe wyjaśnienie

Użyj extended thinking do przemyślenia najlepszych pytań dla tej konkretnej organizacji.

Format odpowiedzi: JSON"""

        user_prompt = f"""Na podstawie poniższych informacji o organizacji, zaprojektuj spersonalizowany kwestionariusz diagnostyczny:

DANE ORGANIZACJI:
{json.dumps(organization_data, indent=2, ensure_ascii=False)}

Wygeneruj kwestionariusz z 15-25 pytaniami dostosowanymi do:
- Branży: {organization_data.get('industry', 'unknown')}
- Wielkości: {organization_data.get('size', 'unknown')}
- Struktury: {organization_data.get('structure', 'unknown')}

Zwróć JSON w formacie:
{{
  "questionnaire": [
    {{
      "id": "unique_id",
      "category": "Process Maturity",
      "question": "Treść pytania po polsku",
      "type": "text|number|scale|select|multiselect",
      "required": true,
      "placeholder": "Wskazówka dla użytkownika",
      "options": ["opcja1", "opcja2"],
      "min": 1,
      "max": 10,
      "help_text": "Dodatkowe wyjaśnienie"
    }}
  ],
  "process_suggestions": [
    "Sugerowany proces 1 typowy dla branży",
    "Sugerowany proces 2",
    "..."
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 10000
                },
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            # Extract JSON from response (może być w thinking blocks)
            result_text = ""
            for block in response.content:
                if block.type == "text":
                    result_text += block.text
            
            result = json.loads(result_text)
            
            # Save to cache
            save_form_generation(organization_data, result)
            
            return result
        except Exception as e:
            logger.error(f"Form generation failed: {e}")
            raise ValueError(f"Claude API error: {str(e)}")
    
    def analyze_step1_comprehensive(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze comprehensive Step 1 data with 20 questions using extended thinking."""
        if not self.client:
            raise ValueError("Claude API key not configured")
        
        logger.info("Step1 comprehensive analysis with extended thinking")
        
        system_prompt = """Jesteś BFA automation-master, ekspertem w audytach automatyzacyjnych procesów biznesowych. 

Otrzymałeś kompleksowy formularz początkowy audytu BFA z 20 pytaniami podzielonymi na 5 sekcji:
- Sekcja A: Informacje Organizacyjne
- Sekcja B: Identyfikacja Problemów i Wąskich Gardeł
- Sekcja C: Cele i Oczekiwania
- Sekcja D: Zasoby i Ograniczenia
- Sekcja E: Kontekst Strategiczny

Twoja rola to dogłębna analiza według BFA 6-wymiarowego frameworku:

1. **Ocena dojrzałości cyfrowej** (6 wymiarów, każdy 0-100):
   - Process Maturity
   - Digital Infrastructure
   - Data Quality
   - Organizational Readiness
   - Financial Capacity
   - Strategic Alignment

2. **Identyfikacja TOP 3-5-10 procesów** o największym potencjale automatyzacji bazując na:
   - Time consumption (TDABC)
   - Error rates (quality improvement)
   - Bottlenecks (throughput)
   - Repeatability & standardization
   - Strategic alignment
   - Quick wins vs strategic impact

3. **Scoring każdego procesu** według potencjału automatyzacji (0-100) i kategoryzacja na Tier 1-4

4. **Analiza prawna** (Lex/Sigma) - identyfikacja regulacji wpływających na automatyzację

5. **Mapowanie zależności systemów IT**

6. **Rekomendacje** - konkretne, actionable, z priorytetami

Zasady:
- Używaj extended thinking do dogłębnej analizy
- Wszystkie metryki quantified (liczby, %, PLN)
- Bazuj na Lean Six Sigma, BPMN 2.0, Time-Driven ABC, ADKAR
- Język polski, bez emoji
- Format odpowiedzi: JSON"""

        user_prompt = f"""Przeanalizuj następujące dane z formularza początkowego audytu BFA:

DANE ORGANIZACJI (wszystkie 20 pytań):
{json.dumps(data, indent=2, ensure_ascii=False)}

Wykonaj kompleksową analizę i zwróć wynik w formacie JSON:

{{
  "digital_maturity": {{
    "process_maturity": 0-100,
    "digital_infrastructure": 0-100,
    "data_quality": 0-100,
    "organizational_readiness": 0-100,
    "financial_capacity": 0-100,
    "strategic_alignment": 0-100,
    "overall_score": 0-100,
    "interpretation": "szczegółowa interpretacja wyników"
  }},
  "processes_scoring": [
    {{
      "process_name": "nazwa procesu",
      "score": 0-100,
      "tier": 1-4,
      "rationale": "szczegółowe uzasadnienie"
    }}
  ],
  "top_processes": ["proces1", "proces2", ...],
  "legal_analysis": "analiza regulacji prawnych (Lex/Sigma)",
  "system_dependencies": {{
    "systems": ["system1", "system2"],
    "matrix": [[...]]
  }},
  "recommendations": "szczegółowe rekomendacje z priorytetami",
  "bfa_scoring": {{
    "automation_potential": 0-100,
    "business_impact": 0-100,
    "technical_feasibility": 0-100,
    "roi_potential": 0-100,
    "strategic_alignment": 0-100,
    "risk_level": 0-100
  }}
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=20000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 15000
                },
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            # Extract text from response (skip thinking blocks)
            result_text = ""
            for block in response.content:
                if block.type == "text":
                    result_text += block.text
            
            result = json.loads(result_text)
            return result
        except Exception as e:
            logger.error(f"Step1 comprehensive analysis failed: {e}")
            raise ValueError(f"Claude API error: {str(e)}")
    
    def analyze_step1(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze organization and processes for Step 1."""
        if not self.client:
            raise ValueError("Claude API key not configured")
        
        # Check cache first
        cached_result = cache_step1_analysis(data)
        if cached_result:
            logger.info("Step1 analysis cache hit")
            return cached_result
        
        logger.info("Step1 analysis cache miss - calling Claude API")
        
        system_prompt = """Jesteś BFA automation-master, ekspertem w audytach automatyzacyjnych procesów biznesowych. 

Twoja rola to analiza danych organizacji i procesów biznesowych w celu:
1. Oceny dojrzałości cyfrowej organizacji według 6 wymiarów (Process Maturity, Digital Infrastructure, Data Quality, Organizational Readiness, Financial Capacity, Strategic Alignment)
2. Scoring każdego procesu według potencjału automatyzacji (0-100)
3. Kategoryzacji procesów na Tier 1-4
4. Identyfikacji TOP 3-5-10 procesów do dalszej analizy
5. Analizy regulacji prawnych (Lex/Sigma)
6. Mapowania zależności między systemami IT

Zasady pracy:
- Używaj specjalistycznego języka biznesowego i technicznego
- Wszystkie analizy muszą być quantified (liczby, procenty, PLN)
- Bazuj na metodologiach: Lean Six Sigma, BPMN 2.0, Time-Driven ABC, ADKAR
- Praca opisowa, nie punktowa
- Język polski, angielski tylko dla nazw własnych
- Bez emoji

Format odpowiedzi: JSON zgodny ze schematem."""
        
        user_prompt = f"""Przeanalizuj następujące dane organizacji i procesy:

DANE ORGANIZACJI:
{json.dumps(data.get('organization_data', {}), indent=2, ensure_ascii=False)}

ODPOWIEDZI Z KWESTIONARIUSZA:
{json.dumps(data.get('questionnaire_answers', {}), indent=2, ensure_ascii=False)}

LISTA PROCESÓW BIZNESOWYCH:
{json.dumps(data.get('processes_list', []), indent=2, ensure_ascii=False)}

Wykonaj:
1. Oceń dojrzałość cyfrową według 6 wymiarów (0-100 dla każdego)
2. Dla każdego procesu oblicz scoring według potencjału automatyzacji (0-100)
3. Kategoryzuj procesy na Tier 1-4
4. Wybierz TOP 5 procesów do dalszej analizy (uzasadnij wybór)
5. Przeanalizuj regulacje prawne wpływające na automatyzację
6. Stwórz matrycę zależności między systemami IT

Zwróć wynik w formacie JSON zgodnym z poniższym schematem:
{{
  "digital_maturity": {{
    "process_maturity": 0-100,
    "digital_infrastructure": 0-100,
    "data_quality": 0-100,
    "organizational_readiness": 0-100,
    "financial_capacity": 0-100,
    "strategic_alignment": 0-100,
    "overall_score": 0-100,
    "interpretation": "tekst"
  }},
  "processes_scoring": [
    {{
      "process_name": "nazwa",
      "score": 0-100,
      "tier": 1-4,
      "rationale": "uzasadnienie"
    }}
  ],
  "top_processes": ["proces1", "proces2", ...],
  "legal_analysis": "tekst",
  "system_dependencies": {{
    "systems": ["system1", "system2", ...],
    "matrix": [[...]]
  }},
  "recommendations": "tekst"
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 10000
                },
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            # Extract text from response (skip thinking blocks)
            result_text = ""
            for block in response.content:
                if block.type == "text":
                    result_text += block.text
            
            result = json.loads(result_text)
            
            # Save to cache
            save_step1_analysis(data, result)
            
            return result
        except Exception as e:
            logger.error(f"Step1 analysis failed: {e}")
            raise ValueError(f"Claude API error: {str(e)}")
    
    def analyze_step2(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze process details for Step 2."""
        if not self.client:
            raise ValueError("Claude API key not configured")
        
        system_prompt = """Jesteś BFA automation-master, ekspertem w szczegółowej analizie procesów biznesowych.

Twoja rola to analiza procesu AS-IS w celu:
1. Identyfikacji 8 typów marnotrawstwa (Lean Six Sigma MUDA)
2. Kalkulacji kosztów procesu (Time-Driven ABC)
3. Identyfikacji wąskich gardeł (TOP 5)
4. Oceny potencjału automatyzacji (%)
5. Stworzenia opisu diagramu BPMN 2.0 AS-IS

Zasady pracy:
- Wszystkie koszty w PLN/rok
- Wszystkie czasy w godzinach/minutach
- Quantified metrics dla wszystkich analiz
- Bazuj na metodologiach: Lean Six Sigma, BPMN 2.0, Time-Driven ABC
- Język polski, angielski tylko dla nazw własnych
- Bez emoji

Format odpowiedzi: JSON zgodny ze schematem."""
        
        user_prompt = f"""Przeanalizuj szczegółowo następujący proces:

DANE PROCESU:
{json.dumps(process_data, indent=2, ensure_ascii=False)}

Wykonaj:
1. Zidentyfikuj 8 typów marnotrawstwa (MUDA) z kosztami dla każdego
2. Oblicz koszty procesu metodą Time-Driven ABC
3. Zidentyfikuj TOP 5 wąskich gardeł z wpływem na efektywność
4. Oceń potencjał automatyzacji (% procesu możliwy do automatyzacji)
5. Stwórz tekstowy opis diagramu BPMN 2.0 AS-IS (dla późniejszej wizualizacji)

Zwróć wynik w formacie JSON zgodnym z poniższym schematem:
{{
  "muda_analysis": {{
    "defects": {{"description": "tekst", "cost_per_year": 0}},
    "overproduction": {{"description": "tekst", "cost_per_year": 0}},
    "waiting": {{"description": "tekst", "cost_per_year": 0}},
    "non_utilized_talent": {{"description": "tekst", "cost_per_year": 0}},
    "transportation": {{"description": "tekst", "cost_per_year": 0}},
    "inventory": {{"description": "tekst", "cost_per_year": 0}},
    "motion": {{"description": "tekst", "cost_per_year": 0}},
    "extra_processing": {{"description": "tekst", "cost_per_year": 0}},
    "total_waste_cost": 0
  }},
  "process_costs": {{
    "labor_costs": 0,
    "operational_costs": 0,
    "error_costs": 0,
    "delay_costs": 0,
    "total_cost": 0
  }},
  "bottlenecks": [
    {{
      "name": "nazwa",
      "description": "opis",
      "impact": "Niski/Średni/Wysoki",
      "cost_per_year": 0
    }}
  ],
  "automation_potential": {{
    "percentage": 0-100,
    "automatable_steps": ["krok1", "krok2", ...],
    "rationale": "tekst"
  }},
  "bpmn_description": "tekstowy opis diagramu BPMN 2.0 AS-IS dla wizualizacji"
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 10000
                },
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            # Extract text from response (skip thinking blocks)
            result_text = ""
            for block in response.content:
                if block.type == "text":
                    result_text += block.text
            
            return json.loads(result_text)
        except Exception as e:
            raise ValueError(f"Claude API error: {str(e)}")
    
    def extract_data_from_documents(self, parsed_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract structured data from uploaded documents using Claude with extended thinking."""
        if not self.client:
            raise ValueError("Claude API key not configured")
        
        logger.info(f"Extracting data from {len(parsed_documents)} documents")
        
        system_prompt = """Jesteś BFA automation-master, ekspertem w analizie dokumentów biznesowych i ekstrakcji danych.

Otrzymałeś dokumenty (Excel, PDF, TXT, MD, CSV) przesłane przez klienta. Twoja rola to:

1. DOKŁADNA EKSTRAKCJA DANYCH
   - Przeanalizuj wszystkie dokumenty
   - Wyciągnij dane i zmapuj je na strukturę BFA Step 1 (20 pytań, 5 sekcji)
   - Szukaj informacji o: organizacji, procesach, problemach, celach, budżecie, zasobach, strategii

2. INTELIGENTNE MAPOWANIE
   - Rozpoznaj synonimy i różne nazewnictwo
   - Mapuj niekompletne dane na najbliższą kategorię
   - Wyciągaj liczby, metryki, koszty, czasy
   - Identyfikuj procesy biznesowe (nazwa, opis, problemy, volume, frequency)

3. CONFIDENCE SCORING (0.0-1.0)
   - 1.0 = dane explicite w dokumentach
   - 0.7-0.9 = dane wywnioskowane z kontekstu
   - 0.4-0.6 = dane częściowe
   - 0.0-0.3 = brak danych

4. MISSING FIELDS
   - Zidentyfikuj pola których NIE MA w dokumentach
   - Zaproponuj pytania do uzupełnienia

ZASADY:
- Dokładność > Kompletność (lepiej pominąć niż zgadywać)
- Szukaj w tabelach, wykresach, notatkach
- Rozumiej kontekst biznesowy i intencje
- Priorytet dla liczb i konkretnych metryk
- Język polski w output

Format output: JSON z kluczami:
- extracted_data (pełna struktura InitialAssessmentData)
- confidence_scores (per sekcja 0.0-1.0)
- missing_fields (lista z suggested_question)
- processing_summary (key_findings, data_quality, recommendations)"""

        # Prepare documents summary for Claude
        documents_content = []
        for doc in parsed_documents:
            doc_summary = f"\n\n=== DOKUMENT: {doc['filename']} ===\n"
            doc_summary += f"Typ: {doc['type']}\n\n"
            
            if doc['type'] == 'excel':
                for sheet_name, sheet_data in doc.get('sheets', {}).items():
                    doc_summary += f"\n--- Sheet: {sheet_name} ---\n"
                    # Include dataframe if available, otherwise raw data
                    if 'dataframe' in sheet_data:
                        doc_summary += f"Kolumny: {', '.join(sheet_data.get('columns', []))}\n"
                        doc_summary += f"Dane (pierwsze 100 wierszy):\n{json.dumps(sheet_data['dataframe'][:100], ensure_ascii=False, indent=2)}\n"
                    elif 'data' in sheet_data:
                        doc_summary += f"Dane:\n{json.dumps(sheet_data['data'][:50], ensure_ascii=False)}\n"
            
            elif doc['type'] == 'pdf':
                doc_summary += f"Liczba stron: {doc.get('pages', 0)}\n"
                doc_summary += f"Treść:\n{doc.get('full_text', '')[:10000]}\n"  # First 10k chars
            
            elif doc['type'] in ['text', 'markdown']:
                if 'sections' in doc:
                    for section in doc['sections']:
                        doc_summary += f"\n## {section['title']}\n{section['content']}\n"
                else:
                    doc_summary += doc.get('content', '')[:10000]
            
            elif doc['type'] == 'csv':
                doc_summary += f"Kolumny: {', '.join(doc.get('columns', []))}\n"
                doc_summary += f"Dane (pierwsze 100 wierszy):\n{json.dumps(doc.get('data', [])[:100], ensure_ascii=False, indent=2)}\n"
            
            documents_content.append(doc_summary)

        user_prompt = f"""Przeanalizuj następujące dokumenty i wyciągnij dane dla audytu BFA:

{chr(10).join(documents_content)}

Zmapuj dane na strukturę InitialAssessmentData (20 pytań):

SEKCJA A: INFORMACJE ORGANIZACYJNE
- organization_name, industry, company_size, annual_revenue, headquarters_location, number_of_locations
- functional_areas (lista), critical_areas (TOP 3)
- digital_maturity (10 obszarów, 0-10): erp, crm, production, rpa, analytics, iot, ai, communication, workflow, cloud
- it_systems (dict), systems_integrated
- budget_range, budget_sources, expected_payback_months

SEKCJA B: IDENTYFIKACJA PROBLEMÓW
- main_challenges_ranked (lista 12 challenges)
- challenges_description (opis tekstowy)
- time_consuming_processes (dict: process_name -> hours/week)
- error_prone_processes (dict: process_name -> {{frequency, error_rate}})
- bottlenecks (dict: process_name -> {{impact_rating, wait_time}})
- process_maturity (dict: process_name -> {{repeatability, standardization, documentation}})

SEKCJA C: CELE I OCZEKIWANIA
- automation_goals_ranked (lista 8 goals)
- automation_goals_weights (dict suma=100%)
- expected_cost_reduction_percent, expected_revenue_increase_percent, expected_roi_percent
- acceptable_payback_months, specific_savings_goal, savings_sources_description
- operational_targets (dict z różnymi metrykami)
- employee_expectations, change_management_readiness

SEKCJA D: ZASOBY
- has_it_team, it_team_size, has_bpm_department, bpm_team_size
- automation_experience, has_project_manager, has_change_manager
- stakeholder_availability
- constraints_and_risks (dict: risk_name -> impact_rating 1-5)
- special_requirements (lista)

SEKCJA E: STRATEGIA
- business_strategy_description (3-5 lat)
- strategic_initiatives (lista)
- additional_notes

Zwróć JSON:
{{
  "extracted_data": {{
    // pełna struktura InitialAssessmentData
  }},
  "confidence_scores": {{
    "organization": 0.0-1.0,
    "digital_maturity": 0.0-1.0,
    "pain_points": 0.0-1.0,
    "goals": 0.0-1.0,
    "budget": 0.0-1.0,
    "timeline": 0.0-1.0,
    "resources": 0.0-1.0,
    "constraints": 0.0-1.0,
    "processes_identified": 0.0-1.0
  }},
  "missing_fields": [
    {{
      "field": "budget.amount_range",
      "reason": "Brak informacji w dokumentach",
      "suggested_question": "Jaki budżet macie na automatyzację?"
    }}
  ],
  "processing_summary": {{
    "documents_analyzed": {len(parsed_documents)},
    "total_pages": 0,
    "key_findings": ["finding1", "finding2", ...],
    "data_quality": "excellent|good|fair|poor",
    "recommendations": ["rec1", "rec2", ...]
  }}
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.document_processing_max_tokens,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 50000  # Large budget for document analysis
                },
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            # Extract text from response
            result_text = ""
            for block in response.content:
                if block.type == "text":
                    result_text += block.text
            
            result = json.loads(result_text)
            
            logger.info(f"Successfully extracted data from documents. Data quality: {result.get('processing_summary', {}).get('data_quality', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Document data extraction failed: {e}")
            raise ValueError(f"Claude API error: {str(e)}")
    
    def analyze_step3(self, step2_results: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Research technologies and create budget scenarios for Step 3."""
        if not self.client:
            raise ValueError("Claude API key not configured")
        
        system_prompt = """Jesteś BFA automation-master, ekspertem w technologiach automatyzacyjnych i analizie ROI.

Twoja rola to:
1. Research technologii automatyzacyjnych (RPA, BPM, AI/ML, IDP, Low-Code, iPaaS)
2. Identyfikacja i ocena vendorów
3. Stworzenie 3 scenariuszy budżetowych (niski/średni/wysoki)
4. Projektowanie procesu TO-BE dla każdego scenariusza
5. Kalkulacja ROI, payback period, NPV
6. Rekomendacje implementacyjne

Zasady pracy:
- Wszystkie koszty w PLN (CAPEX i OPEX)
- Wszystkie korzyści quantified (PLN/rok)
- ROI w %, payback w miesiącach
- Bazuj na rzeczywistych cenach vendorów
- Język polski, angielski tylko dla nazw własnych
- Bez emoji

Format odpowiedzi: JSON zgodny ze schematem."""
        
        user_prompt = f"""Na podstawie analizy procesu z Kroku 2, zaproponuj rozwiązania automatyzacyjne:

DANE PROCESU Z KROKU 2:
{json.dumps(step2_results, indent=2, ensure_ascii=False)}

PREFERENCJE KLIENTA:
{json.dumps(preferences, indent=2, ensure_ascii=False)}

Wykonaj:
1. Research technologii automatyzacyjnych odpowiednich dla tego procesu
2. Oceń TOP 5-10 vendorów (funkcjonalność, cena, referencje)
3. Stwórz 3 scenariusze budżetowe:
   - Scenariusz 1: Budget-Conscious (niski budżet)
   - Scenariusz 2: Strategic Implementation (średni budżet)
   - Scenariusz 3: Enterprise Transformation (wysoki budżet)
4. Dla każdego scenariusza:
   - Zaproponuj konkretne rozwiązania (vendorzy, produkty)
   - Oblicz koszty (CAPEX i OPEX)
   - Zaprojektuj proces TO-BE
   - Oblicz korzyści (oszczędności)
   - Kalkuluj ROI (3 lata), payback period, NPV
5. Rekomenduj optymalny scenariusz

Zwróć wynik w formacie JSON."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=20000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 15000
                },
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            # Extract text from response (skip thinking blocks)
            result_text = ""
            for block in response.content:
                if block.type == "text":
                    result_text += block.text
            
            return json.loads(result_text)
        except Exception as e:
            raise ValueError(f"Claude API error: {str(e)}")
