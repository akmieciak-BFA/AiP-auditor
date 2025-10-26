import json
from typing import Dict, Any
from anthropic import Anthropic
from ..config import get_settings

settings = get_settings()


class ClaudeService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.claude_api_key) if settings.claude_api_key else None
        self.model = "claude-sonnet-4"
    
    def analyze_step1(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze organization and processes for Step 1."""
        if not self.client:
            raise ValueError("Claude API key not configured")
        
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
                max_tokens=8000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            result_text = response.content[0].text
            return json.loads(result_text)
        except Exception as e:
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
                max_tokens=8000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            result_text = response.content[0].text
            return json.loads(result_text)
        except Exception as e:
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
                max_tokens=16000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            result_text = response.content[0].text
            return json.loads(result_text)
        except Exception as e:
            raise ValueError(f"Claude API error: {str(e)}")
