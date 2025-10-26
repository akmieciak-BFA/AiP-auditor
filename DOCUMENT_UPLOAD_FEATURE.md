# Feature: Upload Dokumentów - Alternatywne Źródło Danych

## 📋 Przegląd

Nowa funkcjonalność umożliwia przesłanie istniejących dokumentów firmowych jako alternatywę do ręcznego wypełniania formularza Step 1. Claude API automatycznie wyciąga, segreguje i mapuje dane z dokumentów na strukturę audytu BFA.

---

## 🎯 Cel

- **Problem:** Klienci często mają już przygotowane dokumenty (raporty, analizy, dane procesowe)
- **Rozwiązanie:** Upload dokumentów → Automatyczna ekstrakcja danych przez Claude → Review i edycja → Analiza
- **Korzyść:** Oszczędność czasu (2-5 minut zamiast 15-20 minut ręcznego wypełniania)

---

## 🚀 Funkcjonalność

### 1. Wspierane Formaty Plików

| Format | Rozszerzenie | Typ parsera | Uwagi |
|--------|--------------|-------------|-------|
| Excel | `.xlsx`, `.xls` | openpyxl + pandas | Wszystkie sheety, tabele, dane |
| PDF | `.pdf` | PyPDF2 | Ekstrakcja tekstu (OCR niedostępne) |
| Text | `.txt` | chardet | Auto-detection encodingu |
| Markdown | `.md` | chardet | Ekstrakcja sekcji (#) |
| CSV | `.csv` | csv.DictReader | Auto-detection delimitera |

### 2. Limity

- **Maksymalnie:** 10 plików
- **Rozmiar pliku:** 50 MB per plik
- **Całkowity rozmiar:** 200 MB
- **Tokeny Claude:** 200,000 (zwiększony z 16,000)
- **Extended Thinking budget:** 50,000 tokenów

---

## 🔧 Architektura

### Backend Components

```
backend/
├── app/
│   ├── utils/
│   │   └── file_parsers.py          # Parsery dla różnych formatów
│   │
│   ├── models/
│   │   └── document.py               # UploadedDocument, DocumentProcessingResult
│   │
│   ├── routers/
│   │   └── documents.py              # Endpoints: upload, get-result, delete
│   │
│   └── services/
│       └── claude_service.py         # extract_data_from_documents()
```

### Frontend Components

```
frontend/src/components/
├── Step1Form.tsx                     # Główny komponent z wyborem trybu
├── DocumentUploadInterface.tsx       # Upload drag & drop
└── ReviewExtractedData.tsx           # Przegląd i edycja wyciągniętych danych
```

---

## 📡 API Endpoints

### 1. Upload i przetwarzanie dokumentów

```http
POST /api/projects/{project_id}/documents/upload
Content-Type: multipart/form-data

files: File[]
```

**Response:**
```json
{
  "project_id": 1,
  "processing_result_id": 42,
  "files_uploaded": 3,
  "extracted_data": { ... },
  "confidence_scores": {
    "organization": 0.95,
    "digital_maturity": 0.75,
    "pain_points": 0.88,
    ...
  },
  "missing_fields": [
    {
      "field": "budget.amount_range",
      "reason": "Brak informacji w dokumentach",
      "suggested_question": "Jaki budżet macie na automatyzację?"
    }
  ],
  "processing_summary": {
    "documents_analyzed": 3,
    "total_pages": 47,
    "key_findings": [...],
    "data_quality": "good",
    "recommendations": [...]
  },
  "processing_time_seconds": 123
}
```

### 2. Pobranie rezultatu przetwarzania

```http
GET /api/projects/{project_id}/documents/processing-result/{result_id}
```

### 3. Lista przesłanych dokumentów

```http
GET /api/projects/{project_id}/documents/uploaded
```

### 4. Usunięcie dokumentu

```http
DELETE /api/projects/{project_id}/documents/{document_id}
```

---

## 🤖 Claude Ekstrakcja Danych

### Proces

1. **Parsing:** Każdy plik jest parsowany odpowiednim parserem
2. **Aggregacja:** Wszystkie dane są agregowane w jeden prompt
3. **Claude Analysis:** Extended Thinking z budżetem 50k tokenów
4. **Mapping:** Claude mapuje dane na strukturę `InitialAssessmentData`
5. **Confidence Scoring:** Każda sekcja dostaje score 0.0-1.0
6. **Missing Fields Detection:** Identyfikacja brakujących pól

### Confidence Scoring

| Score | Znaczenie | Opis |
|-------|-----------|------|
| 1.0 | Wysoka pewność | Dane explicite w dokumentach |
| 0.7-0.9 | Dobra pewność | Dane wywnioskowane z kontekstu |
| 0.4-0.6 | Średnia pewność | Dane częściowe |
| 0.0-0.3 | Niska pewność | Brak danych w dokumentach |

### Output Structure

```typescript
{
  extracted_data: InitialAssessmentData,
  confidence_scores: {
    organization: 0.95,
    digital_maturity: 0.75,
    pain_points: 0.88,
    goals: 0.65,
    budget: 0.50,
    timeline: 0.40,
    resources: 0.70,
    constraints: 0.60,
    processes_identified: 0.85
  },
  missing_fields: [
    {
      field: "budget.amount_range",
      reason: "Brak informacji w dokumentach",
      suggested_question: "Jaki budżet macie na automatyzację?"
    }
  ],
  processing_summary: {
    documents_analyzed: 3,
    total_pages: 47,
    key_findings: ["..."],
    data_quality: "good",
    recommendations: ["..."]
  }
}
```

---

## 💻 Frontend Flow

### 1. Mode Selection (Step1Form)

User wybiera:
- **Formularz manualny** → Wypełnia 20 pytań ręcznie
- **Prześlij dokumenty** → Upload interface

### 2. Document Upload (DocumentUploadInterface)

- Drag & drop lub select files
- Walidacja: format, rozmiar, liczba plików
- Upload do backendu
- Progress indicator (2-5 minut)
- Przekierowanie do Review

### 3. Review Extracted Data (ReviewExtractedData)

- **Confidence indicators** per sekcja
- **Data quality badge** (excellent/good/fair/poor)
- **Processing summary** z key findings
- **Missing fields alerts** z sugerowanymi pytaniami
- **Editable fields** (możliwość korekty)
- **Confirm button** → Claude analysis → Step 2

---

## 🗄️ Database Schema

### UploadedDocument

```sql
CREATE TABLE uploaded_documents (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    filename VARCHAR(255),
    file_path VARCHAR(500),
    file_type VARCHAR(10),        -- excel, pdf, txt, md, csv
    file_size BIGINT,
    uploaded_at TIMESTAMP DEFAULT NOW()
);
```

### DocumentProcessingResult

```sql
CREATE TABLE document_processing_results (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    extracted_data JSONB,
    confidence_scores JSONB,
    missing_fields JSONB,
    processing_summary JSONB,
    tokens_used INTEGER,
    processing_time_seconds INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📦 Instalacja

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Nowe zależności:
- `openpyxl==3.1.2` - Excel parsing
- `pandas==2.0.3` - Data processing
- `PyPDF2==3.0.1` - PDF parsing
- `chardet==5.2.0` - Encoding detection

### Frontend

Brak dodatkowych zależności (używamy natywnego File API).

---

## 🧪 Testowanie

### Test 1: Upload Excel

```bash
# Przygotuj plik Excel z danymi organizacji
# Kolumny: Parametr, Wartość
# Wiersze: Nazwa firmy, Branża, Wielkość, etc.

# Upload przez UI lub curl:
curl -X POST "http://localhost:8000/api/projects/1/documents/upload" \
  -F "files=@dane_firmy.xlsx"
```

### Test 2: Upload PDF

```bash
# Przygotuj PDF raport z opisem firmy i procesów
curl -X POST "http://localhost:8000/api/projects/1/documents/upload" \
  -F "files=@raport_procesow.pdf"
```

### Test 3: Multiple Files

```bash
curl -X POST "http://localhost:8000/api/projects/1/documents/upload" \
  -F "files=@dane_organizacyjne.xlsx" \
  -F "files=@opis_procesow.pdf" \
  -F "files=@problemy_i_cele.md"
```

---

## ⚡ Performance

### Benchmarks

| Scenariusz | Pliki | Rozmiar | Czas przetwarzania |
|------------|-------|---------|-------------------|
| 1 Excel (5 sheets) | 1 | 2 MB | ~60 sekund |
| 3 PDF (total 50 pages) | 3 | 15 MB | ~150 sekund |
| 5 mixed files | 5 | 25 MB | ~180 sekund |
| 10 files (max) | 10 | 100 MB | ~300 sekund |

### Optymalizacja

- **Parsing**: Lokalny (szybki)
- **Claude API**: Extended Thinking (powolny ale dokładny)
- **Caching**: Brak (każdy upload = nowa analiza)
- **Timeout**: 10 minut (600 sekund)

---

## 🔒 Security

### Walidacja

- ✅ File extension whitelist
- ✅ File size limits
- ✅ Total size limit
- ✅ Max files limit
- ✅ Path traversal protection (filename sanitization)

### Privacy

- Pliki zapisywane lokalnie w `./uploaded_documents/project_{id}/`
- Brak wysyłania surowych plików do Claude
- Tylko sparsowane dane tekstowe
- Automatyczne kasowanie plików przy usuwaniu projektu (CASCADE)

---

## 🐛 Troubleshooting

### Problem: "Unsupported file type"
**Rozwiązanie:** Sprawdź rozszerzenie pliku (tylko .xlsx, .xls, .pdf, .txt, .md, .csv)

### Problem: "File too large"
**Rozwiązanie:** Zmniejsz rozmiar pliku (<50MB per plik, <200MB total)

### Problem: "Failed to parse Excel"
**Rozwiązanie:** 
- Sprawdź czy plik nie jest chroniony hasłem
- Upewnij się, że zawiera dane (nie jest pusty)
- Zainstaluj openpyxl: `pip install openpyxl pandas`

### Problem: "Failed to parse PDF"
**Rozwiązanie:**
- PDF musi zawierać tekst (nie tylko obrazy - brak OCR)
- Zainstaluj PyPDF2: `pip install PyPDF2`

### Problem: "Low confidence scores"
**Rozwiązanie:**
- Dodaj więcej szczegółów do dokumentów
- Użyj strukturyzowanych formatów (tabele w Excel/CSV)
- Dodaj headery/sekcje w Markdown
- Uzupełnij missing fields ręcznie w Review

### Problem: "Processing takes too long"
**Rozwiązanie:**
- Normalny czas: 2-5 minut dla 3-5 plików
- Zmniejsz liczbę/rozmiar plików
- Sprawdź Claude API limit rate
- Check backend logs dla errors

---

## 📈 Future Improvements

### Planowane

- [ ] OCR dla PDF ze skanami (pdf2image + pytesseract)
- [ ] Word documents support (.docx)
- [ ] Images support (.jpg, .png) z OCR
- [ ] Batch processing (kolejka)
- [ ] Caching results (redis)
- [ ] Preview plików przed uploadem
- [ ] Progress websockets (realtime updates)
- [ ] Partial data save (draft mode)

### Opcjonalne

- [ ] AI-powered data correction suggestions
- [ ] Multi-language support
- [ ] Export extracted data to Excel template
- [ ] Comparison between manual form vs uploaded data
- [ ] Learning from user corrections (fine-tuning)

---

## 📚 Przykłady Użycia

### Przykład 1: Firma produkcyjna

**Dokumenty:**
- `organizacja.xlsx` - dane firmy, struktura, systemy IT
- `procesy_produkcyjne.pdf` - opis linii produkcyjnych
- `problemy_i_cele.md` - Markdown z opisem wyzwań

**Rezultat:**
- Confidence: 88%
- Missing fields: budget, timeline
- Key findings: "8 procesów zidentyfikowanych, główny problem: ręczne przepisywanie danych"

### Przykład 2: Firma logistyczna

**Dokumenty:**
- `dane_firmowe.xlsx` - profil organizacji
- `kpi_raport.csv` - metryki procesowe
- `mapa_procesow.pdf` - diagram AS-IS

**Rezultat:**
- Confidence: 92%
- Missing fields: strategic initiatives
- Key findings: "Magazyn i transport - TOP priority, 45h/tydzień manual work"

---

## 🎓 Best Practices

### Dla Użytkowników

1. **Strukturyzuj dane** - Używaj tabel, kolumn, sekcji
2. **Dodaj nagłówki** - W Markdown, Excel, CSV
3. **Bądź szczegółowy** - Im więcej danych, tym lepsza ekstrakcja
4. **Mix formatów** - Excel (dane), PDF (opisy), MD (notatki)
5. **Nazwij pliki jasno** - `dane_organizacyjne.xlsx` zamiast `file123.xlsx`

### Dla Developerów

1. **Validate early** - Check files przed parsowaniem
2. **Handle errors gracefully** - Jeden zły plik nie może zepsuć całości
3. **Log everything** - Debugging Claude ekstrakcji wymaga logów
4. **Monitor token usage** - 200k to dużo ale nie nieskończoność
5. **Test edge cases** - Puste pliki, corrupted files, huge files

---

## 📞 Support

W razie problemów:
1. Sprawdź logi backend (`uvicorn` terminal)
2. Sprawdź logi frontend (Console F12)
3. Zweryfikuj Claude API key i rate limits
4. Sprawdź `uploaded_documents/` folder permissions

---

**Wersja:** 2.1  
**Data:** 2025-10-26  
**Feature by:** BFA Audit App Team  
**Powered by:** Claude Sonnet 4.5 Extended Thinking (200k tokens, 50k thinking budget)
