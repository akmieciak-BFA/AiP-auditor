import requests
from typing import Dict, Any, List
from ..config import get_settings

settings = get_settings()


class GammaService:
    def __init__(self):
        self.api_key = settings.gamma_api_key
        self.base_url = "https://api.gamma.app/v1"
    
    def generate_presentation(
        self,
        client_name: str,
        author_name: str,
        step1_results: Dict[str, Any],
        step2_results: List[Dict[str, Any]],
        step3_results: Dict[str, Any],
        selected_processes: List[str],
        budget_scenario: str
    ) -> str:
        """Generate presentation using Gamma API."""
        if not self.api_key:
            raise ValueError("Gamma API key not configured")
        
        # Build slides based on audit data
        slides = self._build_slides(
            client_name,
            author_name,
            step1_results,
            step2_results,
            step3_results,
            selected_processes,
            budget_scenario
        )
        
        # Note: This is a placeholder implementation
        # Actual Gamma API might have different structure
        payload = {
            "title": f"Audyt automatyzacyjny - {client_name}",
            "theme": {
                "name": "custom",
                "colors": {
                    "background": "#1a1d3a",
                    "primary": "#00ff00",
                    "text": "#ffffff",
                    "accent": "#ff6b9d"
                },
                "fonts": {
                    "heading": "Montserrat",
                    "body": "Montserrat"
                }
            },
            "slides": slides
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/presentations",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result.get("url", "")
        except requests.exceptions.RequestException as e:
            # If Gamma API is not available, return a mock URL
            return f"https://gamma.app/presentations/mock-{client_name.lower().replace(' ', '-')}"
    
    def _build_slides(
        self,
        client_name: str,
        author_name: str,
        step1_results: Dict[str, Any],
        step2_results: List[Dict[str, Any]],
        step3_results: Dict[str, Any],
        selected_processes: List[str],
        budget_scenario: str
    ) -> List[Dict[str, Any]]:
        """Build slides structure for presentation."""
        slides = []
        
        # Slide 1: Title
        slides.append({
            "type": "title",
            "layout": "center",
            "content": {
                "title": f"Audyt automatyzacyjny - {client_name}",
                "subtitle": f"przez {author_name}",
                "background": "#1a1d3a"
            }
        })
        
        # Slide 2: Introduction
        slides.append({
            "type": "content",
            "layout": "two-column",
            "content": {
                "title": "Wprowadzenie",
                "left": {
                    "type": "list",
                    "items": [
                        {
                            "icon": "search",
                            "title": "Kompleksowa analiza procesów",
                            "description": "Identyfikacja obszarów wymagających optymalizacji"
                        },
                        {
                            "icon": "lightbulb",
                            "title": "Konkretne rozwiązania",
                            "description": "Rekomendacje technologiczne dopasowane do Państwa potrzeb"
                        },
                        {
                            "icon": "chart-line",
                            "title": "Efektywność biznesowa",
                            "description": "Wymierny zwrot z inwestycji i redukcja kosztów"
                        },
                        {
                            "icon": "trophy",
                            "title": "Przewaga strategiczna",
                            "description": "Pozycjonowanie jako lider cyfrowej transformacji"
                        },
                        {
                            "icon": "rocket",
                            "title": f"Transformacja {client_name}",
                            "description": "Plan działania na najbliższe lata"
                        }
                    ]
                },
                "right": {
                    "type": "image",
                    "style": "isometric"
                }
            }
        })
        
        # Slide 3: Methodology
        slides.append({
            "type": "content",
            "layout": "single",
            "content": {
                "title": "Metodologia Audytu",
                "body": {
                    "type": "diagram",
                    "phases": [
                        {
                            "number": "1",
                            "title": "Analiza Wstępna",
                            "description": "Ocena dojrzałości i identyfikacja procesów"
                        },
                        {
                            "number": "2",
                            "title": "Mapowanie Procesów",
                            "description": "Szczegółowa analiza AS-IS"
                        },
                        {
                            "number": "3",
                            "title": "Rekomendacje",
                            "description": "Scenariusze budżetowe i ROI"
                        }
                    ]
                }
            }
        })
        
        # Slide 4: Top Processes
        top_processes = step1_results.get("top_processes", [])
        slides.append({
            "type": "content",
            "layout": "single",
            "content": {
                "title": f"Top {len(top_processes)} Wybranych Procesów do Automatyzacji",
                "body": {
                    "type": "list",
                    "items": [{"text": p} for p in top_processes]
                }
            }
        })
        
        # Add slides for each process
        for process_result in step2_results:
            if process_result.get("process_name") in selected_processes:
                process_slides = self._build_process_slides(process_result, step3_results, budget_scenario)
                slides.extend(process_slides)
        
        # Final slide: Summary
        slides.append({
            "type": "content",
            "layout": "single",
            "content": {
                "title": "Podsumowanie i Rekomendacje",
                "body": {
                    "type": "text",
                    "text": "Następne kroki i plan implementacji"
                }
            }
        })
        
        return slides
    
    def _build_process_slides(
        self,
        process_result: Dict[str, Any],
        step3_results: Dict[str, Any],
        budget_scenario: str
    ) -> List[Dict[str, Any]]:
        """Build slides for a single process."""
        slides = []
        process_name = process_result.get("process_name", "Unknown Process")
        
        # Process description slide
        slides.append({
            "type": "content",
            "layout": "single",
            "content": {
                "title": f"Proces: {process_name}",
                "body": {
                    "type": "text",
                    "text": process_result.get("process_data", {}).get("basic_info", {}).get("objective", "")
                }
            }
        })
        
        # MUDA analysis slide
        muda = process_result.get("analysis_results", {}).get("muda_analysis", {})
        slides.append({
            "type": "content",
            "layout": "two-column",
            "content": {
                "title": f"Analiza Lean/Six Sigma (MUDA) - {process_name}",
                "left": {
                    "type": "list",
                    "items": [
                        {"title": "Defekty", "value": f"{muda.get('defects', {}).get('cost_per_year', 0):,.0f} PLN/rok"},
                        {"title": "Nadprodukcja", "value": f"{muda.get('overproduction', {}).get('cost_per_year', 0):,.0f} PLN/rok"},
                        {"title": "Oczekiwanie", "value": f"{muda.get('waiting', {}).get('cost_per_year', 0):,.0f} PLN/rok"},
                        {"title": "Niewykorzystany talent", "value": f"{muda.get('non_utilized_talent', {}).get('cost_per_year', 0):,.0f} PLN/rok"}
                    ]
                },
                "right": {
                    "type": "list",
                    "items": [
                        {"title": "Transport", "value": f"{muda.get('transportation', {}).get('cost_per_year', 0):,.0f} PLN/rok"},
                        {"title": "Zapasy", "value": f"{muda.get('inventory', {}).get('cost_per_year', 0):,.0f} PLN/rok"},
                        {"title": "Ruch", "value": f"{muda.get('motion', {}).get('cost_per_year', 0):,.0f} PLN/rok"},
                        {"title": "Nadmierne przetwarzanie", "value": f"{muda.get('extra_processing', {}).get('cost_per_year', 0):,.0f} PLN/rok"}
                    ]
                }
            }
        })
        
        return slides
