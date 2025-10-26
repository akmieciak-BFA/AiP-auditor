"""Comprehensive validators for business logic."""
from typing import List, Dict, Any
from fastapi import HTTPException, status


def validate_processes_list(processes: List[str]) -> List[str]:
    """Validate and clean processes list."""
    if not processes or len(processes) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Musisz podać przynajmniej 1 proces biznesowy"
        )
    
    if len(processes) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maksymalnie 50 procesów"
        )
    
    # Remove empty strings and duplicates
    clean_processes = []
    seen = set()
    for p in processes:
        p_clean = p.strip()
        if p_clean and p_clean not in seen:
            clean_processes.append(p_clean)
            seen.add(p_clean)
    
    if not clean_processes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wszystkie procesy są puste"
        )
    
    return clean_processes


def validate_questionnaire_answers(answers: Dict[str, Any]) -> Dict[str, Any]:
    """Validate questionnaire answers."""
    if not answers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kwestionariusz nie może być pusty"
        )
    
    if len(answers) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wypełnij przynajmniej 3 pytania kwestionariusza"
        )
    
    return answers


def validate_process_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate process steps."""
    if not steps or len(steps) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Proces musi mieć przynajmniej 1 krok"
        )
    
    if len(steps) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maksymalnie 100 kroków procesu"
        )
    
    # Validate each step has required fields
    for i, step in enumerate(steps):
        if not step.get('name'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Krok {i+1} musi mieć nazwę"
            )
        if not step.get('executor'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Krok {i+1} musi mieć wykonawcę"
            )
    
    return steps


def validate_budget_level(budget_level: str) -> str:
    """Validate budget level."""
    valid_levels = ['low', 'medium', 'high']
    if budget_level not in valid_levels:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nieprawidłowy poziom budżetu. Dostępne: {', '.join(valid_levels)}"
        )
    return budget_level


def validate_selected_processes(
    selected: List[str],
    available: List[str]
) -> List[str]:
    """Validate selected processes against available ones."""
    if not selected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wybierz przynajmniej 1 proces"
        )
    
    # Check if all selected processes are in available list
    invalid = [p for p in selected if p not in available]
    if invalid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nieprawidłowe procesy: {', '.join(invalid)}"
        )
    
    return selected


def validate_costs(costs: Dict[str, Any]) -> Dict[str, Any]:
    """Validate cost values."""
    required_fields = ['labor_costs', 'operational_costs', 'error_costs', 'delay_costs']
    
    for field in required_fields:
        if field not in costs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Brak wymaganego pola kosztu: {field}"
            )
        
        value = costs[field]
        if not isinstance(value, (int, float)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field} musi być liczbą"
            )
        
        if value < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field} nie może być ujemny"
            )
        
        if value > 1_000_000_000:  # 1 billion PLN sanity check
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field} przekracza rozsądną wartość (max 1 mld PLN)"
            )
    
    return costs
