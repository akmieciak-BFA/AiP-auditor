# 🎨 Dynamiczne Formularze - Dokumentacja

## Przegląd

Aplikacja BFA Audit App wykorzystuje **Claude Sonnet 4.5 z Extended Thinking** do generowania spersonalizowanych kwestionariuszy diagnostycznych w Kroku 1.

## 🧠 Jak to Działa

### 1. Zbieranie Danych Organizacji

Użytkownik podaje podstawowe informacje:
- Nazwę firmy
- Branżę
- Wielkość organizacji
- Strukturę organizacyjną
- Opis (opcjonalnie)

### 2. Generowanie Kwestionariusza przez Claude

**Extended Thinking Process:**

Claude Sonnet 4.5 analizuje dane organizacji używając extended thinking (10,000 token budget) i:

1. **Analiza Kontekstu** - rozumie specyfikę branży i wielkości organizacji
2. **Dobór Kategorii** - wybiera odpowiednie 6 kategorii pytań:
   - Process Maturity (Dojrzałość Procesowa)
   - Digital Infrastructure (Infrastruktura Cyfrowa)
   - Data Quality (Jakość Danych)
   - Organizational Readiness (Gotowość Organizacyjna)
   - Financial Capacity (Zdolność Finansowa)
   - Strategic Alignment (Zgodność Strategiczna)

3. **Tworzenie Pytań** - generuje 15-25 spersonalizowanych pytań z mix typów:
   - **text** - pytania otwarte tekstowe
   - **number** - wartości numeryczne
   - **scale** - skale 1-10 (suwaki)
   - **select** - wybór jednej opcji
   - **multiselect** - wybór wielu opcji

4. **Sugestie Procesów** - proponuje procesy typowe dla branży

### 3. Prezentacja Formularza

Frontend renderuje dynamicznie wygenerowany formularz z:
- Pytaniami pogrupowanymi po kategoriach
- Odpowiednimi kontrolkami (text area, suwaki, checkboxy)
- Tekstami pomocniczymi (help_text)
- Walidacją (required fields)

### 4. Analiza Odpowiedzi

Po wypełnieniu, Claude analizuje odpowiedzi z extended thinking i zwraca:
- Scoring dojrzałości cyfrowej (6 wymiarów)
- Scoring procesów (0-100)
- TOP procesy do automatyzacji
- Rekomendacje

## 📋 Struktura Wygenerowanego Formularza

### Format JSON

```json
{
  "questionnaire": [
    {
      "id": "pm_process_documentation",
      "category": "Process Maturity",
      "question": "Czy procesy biznesowe w Twojej organizacji są udokumentowane?",
      "type": "text",
      "required": true,
      "placeholder": "Opisz stopień dokumentacji procesów...",
      "help_text": "Zwróć uwagę na formaty dokumentacji (diagramy, opisy tekstowe, wideo)"
    },
    {
      "id": "di_systems_count",
      "category": "Digital Infrastructure",
      "question": "Ile systemów IT wykorzystuje Twoja organizacja?",
      "type": "number",
      "required": true,
      "min": 0,
      "max": 100,
      "help_text": "Uwzględnij wszystkie systemy: ERP, CRM, HR, etc."
    },
    {
      "id": "dq_data_quality",
      "category": "Data Quality",
      "question": "Oceń jakość danych w systemach organizacji",
      "type": "scale",
      "required": true,
      "min": 1,
      "max": 10,
      "help_text": "1 = bardzo niska jakość, 10 = doskonała jakość"
    },
    {
      "id": "or_change_culture",
      "category": "Organizational Readiness",
      "question": "Jak opisałbyś kulturę organizacji wobec zmian?",
      "type": "select",
      "required": true,
      "options": [
        "Opór wobec zmian",
        "Neutralna",
        "Otwarta na zmiany",
        "Proaktywna w zmianach"
      ]
    },
    {
      "id": "fc_budget_areas",
      "category": "Financial Capacity",
      "question": "Które obszary automatyzacji są priorytetowe budżetowo?",
      "type": "multiselect",
      "required": false,
      "options": [
        "Procesy finansowe",
        "HR i rekrutacja",
        "Sprzedaż i marketing",
        "Produkcja",
        "Logistyka",
        "Obsługa klienta"
      ]
    }
  ],
  "process_suggestions": [
    "Proces Zakupowy",
    "Fakturowanie i Rozliczenia",
    "Onboarding Pracowników",
    "Zarządzanie Zamówieniami",
    "Kontrola Jakości"
  ]
}
```

## 🔧 Implementacja Techniczna

### Backend - Claude Service

**Endpoint:** `POST /api/projects/{project_id}/step1/generate-form`

```python
def generate_step1_form(self, organization_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate dynamic form for Step 1 based on organization data."""
    
    response = self.client.messages.create(
        model="claude-sonnet-4",
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000  # Extended thinking!
        },
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    # Extract JSON from response
    result_text = ""
    for block in response.content:
        if block.type == "text":
            result_text += block.text
    
    return json.loads(result_text)
```

### Frontend - Step1Form Component

**Flow:**

```typescript
1. org-data → Użytkownik podaje dane organizacji
   ↓
2. form-generation → Claude generuje formularz (30-60s)
   ↓
3. questionnaire → Użytkownik wypełnia dynamiczny formularz
   ↓
4. analyze → Claude analizuje odpowiedzi z extended thinking
   ↓
5. results → Wyniki analizy + TOP procesy
```

**Rendering Pytań:**

```typescript
const renderQuestion = (question: QuestionField) => {
  switch (question.type) {
    case 'text':
      return <textarea {...props} />;
    case 'number':
      return <input type="number" {...props} />;
    case 'scale':
      return <input type="range" {...props} />;
    case 'select':
      return <select>{options}</select>;
    case 'multiselect':
      return <div>{checkboxes}</div>;
  }
};
```

## 🎯 Przykłady Kwestionariuszy dla Różnych Branż

### Produkcja

Pytania fokusują się na:
- Automatyzacja linii produkcyjnych
- Kontrola jakości
- Zarządzanie zapasami
- Maintenance predykcyjny
- Śledzenie OEE (Overall Equipment Effectiveness)

### IT/Software

Pytania fokusują się na:
- CI/CD pipelines
- Automatyzacja testów
- DevOps maturity
- Cloud readiness
- API management

### Finanse

Pytania fokusują się na:
- Compliance i regulacje
- Fraud detection
- Reconciliation procesów
- Reporting automatyzacja
- KYC/AML procesów

### E-commerce

Pytania fokusują się na:
- Order management
- Inventory synchronization
- Customer service automation
- Marketing automation
- Returns processing

## 📊 Analiza z Extended Thinking

### Co Claude Analizuje

1. **Deep Context Understanding**
   - Specyfika branży
   - Rozmiar organizacji
   - Struktura organizacyjna
   - Challenges charakterystyczne dla sektora

2. **Question Selection Strategy**
   - Które pytania będą najbardziej insightful
   - Balans między szczegółowością a user experience
   - Priorytetyzacja kategorii według kontekstu

3. **Answer Analysis**
   - Pattern recognition w odpowiedziach
   - Korelacje między różnymi wymiarami dojrzałości
   - Identyfikacja red flags i opportunities
   - Context-aware scoring

### Korzyści Extended Thinking

✅ **Lepsze pytania** - dostosowane do konkretnej organizacji
✅ **Głębsza analiza** - Claude "myśli" przed odpowiedzią
✅ **Contextual insights** - rekomendacje uwzględniają niuanse
✅ **Higher accuracy** - lepszy scoring i priorytetyzacja

## 🔄 Workflow Użytkownika

```
1. Podaj dane firmy (30 sekund)
   ↓
2. Poczekaj na wygenerowanie formularza (30-60 sekund)
   [Claude: Extended Thinking → Generates questions]
   ↓
3. Odpowiedz na 15-25 pytań (5-10 minut)
   [Mix: text, numbers, scales, selects]
   ↓
4. Dodaj/edytuj procesy biznesowe (2 minuty)
   [Sugerowane + własne]
   ↓
5. Poczekaj na analizę (30-60 sekund)
   [Claude: Extended Thinking → Analyzes answers]
   ↓
6. Odbierz wyniki
   [Scoring + TOP procesy + Rekomendacje]
```

**Total time:** ~10-15 minut

## 💡 Wskazówki dla Użytkowników

### Wypełnianie Danych Organizacji

1. **Bądź szczegółowy w opisie** - więcej kontekstu = lepsze pytania
2. **Podaj konkretną branżę** - np. "Produkcja automotive" zamiast "Produkcja"
3. **Dokładna wielkość** - pomaga w dostosowaniu skali pytań

### Odpowiadanie na Pytania

1. **Pytania tekstowe** - bądź szczegółowy, Claude analizuje niuanse
2. **Skale 1-10** - używaj pełnego zakresu, nie tylko środka
3. **Multiselect** - zaznacz wszystkie stosowne opcje
4. **Nie wiesz?** - lepiej szczerze napisać "nie wiem" niż zgadywać

## 🚀 Future Enhancements

Potencjalne rozszerzenia:

- [ ] **Iterative refinement** - Claude zadaje follow-up questions
- [ ] **Industry templates** - pre-configured dla popularnych branż
- [ ] **Benchmark comparison** - porównanie z innymi firmami
- [ ] **Multi-language** - generowanie w różnych językach
- [ ] **Voice input** - odpowiadanie głosem
- [ ] **Collaborative filling** - wielu użytkowników wypełnia razem
- [ ] **Save & resume** - kontynuacja później
- [ ] **Export answers** - zapisz odpowiedzi do pliku

## 📚 API Reference

### Generate Form

**Request:**
```http
POST /api/projects/{project_id}/step1/generate-form
Content-Type: application/json

{
  "company_name": "ACME Corp",
  "industry": "Produkcja automotive",
  "size": "medium",
  "structure": "Funkcjonalna",
  "description": "Producent części samochodowych..."
}
```

**Response:**
```json
{
  "questionnaire": [...],
  "process_suggestions": [...]
}
```

**Timing:** 30-60 sekund (Extended Thinking)

### Analyze Answers

**Request:**
```http
POST /api/projects/{project_id}/step1/analyze
Content-Type: application/json

{
  "organization_data": {...},
  "questionnaire_answers": {...},
  "processes_list": [...]
}
```

**Response:**
```json
{
  "digital_maturity": {...},
  "processes_scoring": [...],
  "top_processes": [...],
  "legal_analysis": "...",
  "system_dependencies": {...},
  "recommendations": "..."
}
```

**Timing:** 30-60 sekund (Extended Thinking)

---

**Dynamiczne formularze sprawiają, że każdy audyt jest unikalny i dostosowany do konkretnej organizacji!** 🎯
