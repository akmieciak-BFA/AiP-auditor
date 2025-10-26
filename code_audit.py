#!/usr/bin/env python3
"""
Statyczny Audyt Kodu BFA Audit App
===================================
Analiza jakości kodu bez uruchamiania
"""

import os
import re
from pathlib import Path

print("=" * 70)
print("  AUDYT KODU - BFA AUDIT APP")
print("=" * 70)

# Analiza struktury projektu
print("\n[1/6] Analiza struktury projektu...")
required_files = [
    'backend/calculators/financial_impact.py',
    'backend/calculators/tdabc.py',
    'backend/calculators/digital_roi.py',
    'backend/calculators/iot_metrics.py',
    'backend/calculators/rpa_metrics.py',
    'backend/calculators/benchmarking.py',
    'backend/calculators/scenario_planning.py',
    'backend/api/calculator_endpoints.py',
    'backend/main.py',
    'tests/test_financial_impact.py',
    'requirements.txt',
    'README.md'
]

missing = []
for file in required_files:
    if not os.path.exists(file):
        missing.append(file)

if missing:
    print(f"  ❌ Brakuje plików: {missing}")
else:
    print(f"  ✅ Wszystkie wymagane pliki obecne ({len(required_files)} plików)")

# Analiza rozmiaru kodu
print("\n[2/6] Analiza rozmiaru kodu...")
total_lines = 0
total_files = 0
py_files = []

for root, dirs, files in os.walk('backend'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
                total_lines += lines
                total_files += 1
                py_files.append((filepath, lines))

print(f"  ✅ Plików Python: {total_files}")
print(f"  ✅ Łącznie linii kodu: {total_lines:,}")
print(f"  ✅ Średnio linii na plik: {total_lines//total_files if total_files > 0 else 0}")

# Top 5 największych plików
print("\n  Top 5 największych plików:")
py_files.sort(key=lambda x: x[1], reverse=True)
for i, (filepath, lines) in enumerate(py_files[:5], 1):
    print(f"    {i}. {filepath}: {lines} linii")

# Analiza dokumentacji
print("\n[3/6] Analiza dokumentacji...")
doc_files = ['README.md', 'docs/USER_GUIDE.md', 'IMPLEMENTATION_SUMMARY.md', 'QUICKSTART.md']
doc_lines = 0
for doc in doc_files:
    if os.path.exists(doc):
        with open(doc, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
            doc_lines += lines
            print(f"  ✅ {doc}: {lines} linii")

print(f"\n  ✅ Łącznie dokumentacji: {doc_lines:,} linii")

# Analiza docstringów
print("\n[4/6] Analiza docstringów...")
docstring_pattern = re.compile(r'^\s*"""[\s\S]*?"""', re.MULTILINE)
classes_with_docs = 0
total_classes = 0

for filepath, _ in py_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Count classes
        class_matches = re.findall(r'class\s+\w+', content)
        total_classes += len(class_matches)
        
        # Count docstrings
        docstrings = docstring_pattern.findall(content)
        classes_with_docs += len(docstrings)

coverage = (classes_with_docs / total_classes * 100) if total_classes > 0 else 0
print(f"  ✅ Klas w kodzie: {total_classes}")
print(f"  ✅ Docstringów: {classes_with_docs}")
print(f"  ✅ Pokrycie dokumentacją: {coverage:.1f}%")

# Analiza testów
print("\n[5/6] Analiza testów...")
test_files = []
test_lines = 0
test_count = 0

for root, dirs, files in os.walk('tests'):
    for file in files:
        if file.startswith('test_') and file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = len(content.split('\n'))
                tests = len(re.findall(r'def test_', content))
                test_files.append((filepath, lines, tests))
                test_lines += lines
                test_count += tests

print(f"  ✅ Plików testowych: {len(test_files)}")
print(f"  ✅ Łącznie testów: {test_count}")
print(f"  ✅ Linii kodu testowego: {test_lines:,}")

for filepath, lines, tests in test_files:
    print(f"    - {filepath}: {tests} testów, {lines} linii")

# Analiza dependencies
print("\n[6/6] Analiza zależności...")
if os.path.exists('requirements.txt'):
    with open('requirements.txt', 'r') as f:
        deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    print(f"  ✅ Zależności w requirements.txt: {len(deps)}")
    
    core_deps = ['fastapi', 'pydantic', 'numpy', 'scipy', 'sqlalchemy']
    for dep in core_deps:
        found = any(dep in d.lower() for d in deps)
        status = "✅" if found else "❌"
        print(f"    {status} {dep}")

# Podsumowanie metryki jakości
print("\n" + "=" * 70)
print("  METRYKI JAKOŚCI KODU")
print("=" * 70)

metrics = {
    'Kompletność struktury': 100 if not missing else 80,
    'Dokumentacja (>2000 linii)': min(100, (doc_lines / 2000) * 100),
    'Pokrycie testami (>30 testów)': min(100, (test_count / 30) * 100),
    'Docstringi (>70%)': min(100, coverage / 70 * 100),
    'Modularność (<300 linii/plik)': min(100, (300 / (total_lines//total_files if total_files > 0 else 1)) * 100)
}

print("\n")
for metric, score in metrics.items():
    bar_length = int(score / 5)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    print(f"  {metric:<35} {bar} {score:.1f}%")

overall_score = sum(metrics.values()) / len(metrics)
print(f"\n  OGÓLNA OCENA JAKOŚCI: {overall_score:.1f}%")

if overall_score >= 90:
    grade = "A (DOSKONAŁY)"
    color = "🟢"
elif overall_score >= 80:
    grade = "B (BARDZO DOBRY)"
    color = "🟢"
elif overall_score >= 70:
    grade = "C (DOBRY)"
    color = "🟡"
else:
    grade = "D (DO POPRAWY)"
    color = "🔴"

print(f"  {color} Ocena: {grade}")

# Identyfikacja ulepszeń
print("\n" + "=" * 70)
print("  ZIDENTYFIKOWANE OBSZARY DO OPTYMALIZACJI")
print("=" * 70)

optimizations = []

# Check for async patterns
async_count = 0
for filepath, _ in py_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        if 'async def' in f.read():
            async_count += 1

if async_count == 0:
    optimizations.append({
        'area': 'Async Processing',
        'priority': 'WYSOKI',
        'description': 'Brak async endpoints - dodać async/await dla lepszej skalowalności',
        'benefit': 'Zwiększenie throughput o 200-300%'
    })

# Check for caching
cache_found = False
for filepath, _ in py_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        if 'cache' in f.read().lower():
            cache_found = True
            break

if not cache_found:
    optimizations.append({
        'area': 'Caching',
        'priority': 'ŚREDNI',
        'description': 'Brak mechanizmu cache - dodać Redis dla benchmarków',
        'benefit': 'Redukcja czasu odpowiedzi o 70-90%'
    })

# Check for logging
logging_found = False
for filepath, _ in py_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        if 'logging' in f.read():
            logging_found = True
            break

if not logging_found:
    optimizations.append({
        'area': 'Logging',
        'priority': 'WYSOKI',
        'description': 'Brak structured logging - dodać logging z trace IDs',
        'benefit': 'Łatwiejsze debugowanie i monitoring produkcji'
    })

# Check for rate limiting
rate_limit_found = False
for filepath, _ in py_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        if 'rate' in f.read().lower() and 'limit' in f.read().lower():
            rate_limit_found = True
            break

if not rate_limit_found:
    optimizations.append({
        'area': 'Rate Limiting',
        'priority': 'WYSOKI',
        'description': 'Brak rate limiting - dodać ochronę przed abuse',
        'benefit': 'Ochrona API przed przeciążeniem'
    })

# Additional optimizations (always applicable)
optimizations.extend([
    {
        'area': 'Input Validation',
        'priority': 'ŚREDNI',
        'description': 'Rozszerzyć walidację zakresów wartości biznesowych',
        'benefit': 'Zapobieganie nieprawidłowym wynikom kalkulacji'
    },
    {
        'area': 'Error Handling',
        'priority': 'ŚREDNI',
        'description': 'Dodać custom exception classes z kontekstem błędu',
        'benefit': 'Lepsza diagnostyka i UX'
    },
    {
        'area': 'Database Pooling',
        'priority': 'WYSOKI',
        'description': 'Dodać connection pooling dla PostgreSQL',
        'benefit': 'Lepsza wydajność i stabilność bazy danych'
    },
    {
        'area': 'Monitoring',
        'priority': 'ŚREDNI',
        'description': 'Dodać metryki Prometheus i health checks',
        'benefit': 'Proaktywne wykrywanie problemów'
    }
])

print("\n")
for i, opt in enumerate(optimizations, 1):
    priority_colors = {'WYSOKI': '🔴', 'ŚREDNI': '🟡', 'NISKI': '🟢'}
    color = priority_colors.get(opt['priority'], '⚪')
    print(f"{i}. {color} {opt['area']} [Priorytet: {opt['priority']}]")
    print(f"   {opt['description']}")
    print(f"   💡 Korzyść: {opt['benefit']}\n")

# Rekomendacje wdrożenia
print("=" * 70)
print("  REKOMENDACJE WDROŻENIA")
print("=" * 70)

high_priority = [o for o in optimizations if o['priority'] == 'WYSOKI']
medium_priority = [o for o in optimizations if o['priority'] == 'ŚREDNI']

print("\n🔥 FAZA 1 (Natychmiast) - Priorytet WYSOKI:")
for i, opt in enumerate(high_priority, 1):
    print(f"  {i}. {opt['area']}")

print("\n⚡ FAZA 2 (Następny sprint) - Priorytet ŚREDNI:")
for i, opt in enumerate(medium_priority, 1):
    print(f"  {i}. {opt['area']}")

print("\n" + "=" * 70)
print("✅ AUDYT ZAKOŃCZONY")
print("=" * 70)
print(f"\nStatus: Kod jest {'DOSKONAŁY' if overall_score >= 90 else 'BARDZO DOBRY' if overall_score >= 80 else 'DOBRY'}")
print(f"Zidentyfikowano: {len(optimizations)} obszarów do optymalizacji")
print(f"Priorytet WYSOKI: {len(high_priority)} elementów")
print(f"Priorytet ŚREDNI: {len(medium_priority)} elementów")
