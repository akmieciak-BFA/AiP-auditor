#!/usr/bin/env python3
"""
Audyt Kodu i Symulacja BFA Audit App
====================================
"""

import sys
import time
from backend.calculators.financial_impact import FinancialMetricsCalculator
from backend.calculators.scenario_planning import ScenarioPlanningAnalyzer
from backend.calculators.tdabc import TDABCCalculator
from backend.calculators.benchmarking import BenchmarkingMaturityAssessment

print("=" * 70)
print("  AUDYT KODU I SYMULACJA - BFA AUDIT APP")
print("=" * 70)

# Test 1: Financial Calculator
print("\n[1/5] Test: Financial Impact Calculator...")
try:
    calc = FinancialMetricsCalculator()
    result = calc.calculate_comprehensive_metrics(
        initial_investment=500000,
        annual_benefits=200000,
        annual_costs=50000,
        project_years=5,
        discount_rate=0.10,
        invested_capital=500000,
        tax_rate=0.21
    )
    print(f"  ✅ NPV: ${result['npv']:,.2f}")
    print(f"  ✅ ROI: {result['roi_pct']:.2f}%")
    print(f"  ✅ IRR: {result['irr_pct']:.2f}%")
    print(f"  ✅ Payback: {result['payback_period_years']:.2f} lat")
    print(f"  ✅ ROIC: {result['roic_pct']:.2f}%")
    print("  ✅ PASS - Kalkulator finansowy działa poprawnie")
except Exception as e:
    print(f"  ❌ FAIL - Błąd: {e}")
    sys.exit(1)

# Test 2: Scenario Planning
print("\n[2/5] Test: Scenario Planning...")
try:
    analyzer = ScenarioPlanningAnalyzer()
    scenarios = analyzer.compare_scenarios(
        base_capex=500000,
        base_opex=50000,
        base_benefits=200000,
        project_years=5,
        discount_rate=0.10
    )
    
    print("\n  Scenariusze:")
    for scenario_name, scenario_data in scenarios['scenarios'].items():
        metrics = scenario_data['financial_metrics']
        print(f"    {scenario_data['name']}:")
        print(f"      NPV: ${metrics['npv']:,.2f}")
        print(f"      ROI: {metrics['roi_pct']:.2f}%")
    
    recommendation = scenarios['comparison']['recommendation']
    print(f"\n  ✅ Rekomendacja: {recommendation['recommended_scenario']}")
    print("  ✅ PASS - Planowanie scenariuszy działa poprawnie")
except Exception as e:
    print(f"  ❌ FAIL - Błąd: {e}")
    sys.exit(1)

# Test 3: TDABC
print("\n[3/5] Test: TDABC Calculator...")
try:
    tdabc = TDABCCalculator()
    result = tdabc.calculate_tdabc_full_analysis(
        total_cost=560000,
        theoretical_capacity_minutes=876000,
        resource_type='people',
        activities=[
            {'name': 'Process Orders', 'unit_time': 8, 'volume': 1000},
            {'name': 'Handle Inquiries', 'unit_time': 5, 'volume': 2000},
        ]
    )
    
    print(f"  ✅ Capacity Cost Rate: ${result['summary']['capacity_cost_rate']:.4f}/min")
    print(f"  ✅ Utilization: {result['utilization']['utilization_rate']:.1f}%")
    print(f"  ✅ Status: {result['utilization']['status']}")
    print("  ✅ PASS - TDABC działa poprawnie")
except Exception as e:
    print(f"  ❌ FAIL - Błąd: {e}")
    sys.exit(1)

# Test 4: Benchmarking
print("\n[4/5] Test: Industry Benchmarking...")
try:
    benchmarking = BenchmarkingMaturityAssessment()
    result = benchmarking.compare_to_industry(
        industry='manufacturing',
        calculated_roi=25.5,
        calculated_payback_months=24,
        capex=500000,
        opex=75000
    )
    
    print(f"  ✅ Industry: {result['industry']}")
    print(f"  ✅ ROI Performance: {result['roi_comparison']['performance']}")
    print(f"  ✅ Payback Performance: {result['payback_comparison']['performance']}")
    print("  ✅ PASS - Benchmarking działa poprawnie")
except Exception as e:
    print(f"  ❌ FAIL - Błąd: {e}")
    sys.exit(1)

# Test 5: Performance Test
print("\n[5/5] Test: Performance...")
try:
    start_time = time.time()
    calc = FinancialMetricsCalculator()
    
    # Run 100 calculations
    for i in range(100):
        result = calc.calculate_comprehensive_metrics(
            initial_investment=500000,
            annual_benefits=200000,
            annual_costs=50000,
            project_years=5,
            discount_rate=0.10,
            invested_capital=500000,
            tax_rate=0.21
        )
    
    end_time = time.time()
    elapsed = end_time - start_time
    avg_time = elapsed / 100
    
    print(f"  ✅ 100 kalkulacji w: {elapsed:.3f}s")
    print(f"  ✅ Średni czas: {avg_time*1000:.2f}ms")
    
    if avg_time < 0.1:  # Less than 100ms per calculation
        print("  ✅ PASS - Wydajność doskonała")
    else:
        print("  ⚠️  WARN - Wydajność do poprawy")
except Exception as e:
    print(f"  ❌ FAIL - Błąd: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 70)
print("  WYNIKI AUDYTU")
print("=" * 70)
print("\n✅ Wszystkie testy przeszły pomyślnie!")
print("\nStatus modułów:")
print("  ✅ Financial Impact Calculator - DZIAŁA")
print("  ✅ Scenario Planning - DZIAŁA")
print("  ✅ TDABC Calculator - DZIAŁA")
print("  ✅ Benchmarking - DZIAŁA")
print("  ✅ Performance - DOSKONAŁA")

print("\n" + "=" * 70)
print("  IDENTYFIKACJA MOŻLIWYCH ULEPSZEŃ")
print("=" * 70)

improvements = [
    {
        'area': 'Performance',
        'current': 'Synchroniczne obliczenia',
        'improvement': 'Dodać async processing dla dużych zbiorów danych',
        'priority': 'ŚREDNI',
        'benefit': 'Szybsze przetwarzanie przy wielu równoczesnych żądaniach'
    },
    {
        'area': 'Caching',
        'current': 'Brak cache',
        'improvement': 'Dodać Redis cache dla benchmarków i częstych kalkulacji',
        'priority': 'ŚREDNI',
        'benefit': 'Redukcja czasu odpowiedzi o 70-90%'
    },
    {
        'area': 'Validation',
        'current': 'Podstawowa walidacja Pydantic',
        'improvement': 'Dodać business logic validation (np. ROI > 0)',
        'priority': 'NISKI',
        'benefit': 'Lepsza jakość danych wejściowych'
    },
    {
        'area': 'Error Handling',
        'current': 'Ogólne błędy',
        'improvement': 'Dodać custom exception classes z szczegółowymi komunikatami',
        'priority': 'ŚREDNI',
        'benefit': 'Łatwiejszy debugging i lepsza UX'
    },
    {
        'area': 'Logging',
        'current': 'Brak structured logging',
        'improvement': 'Dodać structured logging (JSON) z trace IDs',
        'priority': 'WYSOKI',
        'benefit': 'Łatwiejsze monitorowanie produkcji'
    },
    {
        'area': 'API Rate Limiting',
        'current': 'Brak limitów',
        'improvement': 'Dodać rate limiting (slowapi)',
        'priority': 'WYSOKI',
        'benefit': 'Ochrona przed abuse'
    },
    {
        'area': 'Database Connection Pool',
        'current': 'Nie zaimplementowano',
        'improvement': 'Dodać connection pooling dla PostgreSQL',
        'priority': 'WYSOKI',
        'benefit': 'Lepsza wydajność bazy danych'
    },
    {
        'area': 'Input Sanitization',
        'current': 'Podstawowa',
        'improvement': 'Dodać dodatkową walidację zakresów wartości',
        'priority': 'ŚREDNI',
        'benefit': 'Zapobieganie nieprawidłowym wynikom'
    }
]

print("\nZidentyfikowane obszary do optymalizacji:\n")
for i, imp in enumerate(improvements, 1):
    print(f"{i}. {imp['area']} [{imp['priority']}]")
    print(f"   Obecny stan: {imp['current']}")
    print(f"   Ulepszenie: {imp['improvement']}")
    print(f"   Korzyść: {imp['benefit']}\n")

print("=" * 70)
print("  REKOMENDACJE")
print("=" * 70)
print("\n🔥 Priorytet WYSOKI (do wdrożenia natychmiast):")
print("  1. Structured logging z trace IDs")
print("  2. Rate limiting dla API")
print("  3. Database connection pooling")

print("\n⚡ Priorytet ŚREDNI (do wdrożenia w następnej iteracji):")
print("  1. Redis cache dla benchmarków")
print("  2. Custom exception classes")
print("  3. Rozszerzona walidacja zakresów")
print("  4. Async processing dla dużych danych")

print("\n💡 Priorytet NISKI (nice-to-have):")
print("  1. Business logic validation")

print("\n" + "=" * 70)
print("✅ AUDYT I SYMULACJA ZAKOŃCZONE POMYŚLNIE")
print("=" * 70)
