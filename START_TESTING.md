# 🧪 Jak uruchomić test systemu

## Przygotowanie środowiska

### 1. Upewnij się, że masz klucz API Claude
```bash
# Sprawdź czy .env istnieje
cat /workspace/.env

# Jeśli nie ma, stwórz z template
cp /workspace/.env.example /workspace/.env

# Edytuj i dodaj swój klucz
nano /workspace/.env
# Zmień linię:
# CLAUDE_API_KEY=sk-ant-your-actual-key-here
```

### 2. Uruchom backend

**Opcja A: Lokalnie**
```bash
cd /workspace/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Opcja B: Docker**
```bash
cd /workspace
docker-compose up -d
```

Sprawdź czy działa:
```bash
curl http://localhost:8000/docs
# Powinno zwrócić HTML dokumentacji API
```

### 3. (Opcjonalnie) Uruchom frontend
```bash
cd /workspace/frontend
npm install
npm run dev
# Frontend będzie na http://localhost:5173
```

---

## Uruchomienie testu automatycznego

### Prosty sposób - jeden skrypt:
```bash
cd /workspace
./run_document_test.sh
```

Ten skrypt:
1. ✅ Sprawdzi czy backend działa
2. ✅ Sprawdzi czy .env jest skonfigurowany
3. ✅ Utworzy testowy projekt
4. ✅ Prześle 3 dokumenty testowe
5. ✅ Poczeka na analizę Claude (~90-120s)
6. ✅ Wyświetli wyniki:
   - Digital maturity score
   - TOP procesy do automatyzacji
   - Szczegółowy scoring procesów
   - Key findings
   - Confidence scores

### Ręczny test przez API:

```bash
# 1. Utwórz projekt
PROJECT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/projects" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Test Project",
        "client_name": "Test Client"
    }')

PROJECT_ID=$(echo "$PROJECT_RESPONSE" | jq -r '.id')
echo "Project ID: $PROJECT_ID"

# 2. Prześlij dokumenty
curl -X POST "http://localhost:8000/api/projects/${PROJECT_ID}/documents/upload" \
    -F "files=@test_documents/company_overview.md" \
    -F "files=@test_documents/process_pain_points.md" \
    -F "files=@test_documents/systems_and_infrastructure.txt" \
    | jq '.'

# To zajmie 90-120 sekund!

# 3. Sprawdź wyniki
curl "http://localhost:8000/api/projects/${PROJECT_ID}/documents/latest-analysis" | jq '.'
```

---

## Test przez Frontend UI

1. **Otwórz przeglądarkę:** http://localhost:5173

2. **Utwórz nowy projekt:**
   - Kliknij "Nowy Projekt"
   - Nazwa: "Acme Manufacturing Test"
   - Klient: "Acme Manufacturing Sp. z o.o."

3. **Wejdź w projekt → Step 1**

4. **Wybierz "Prześlij dokumenty"**

5. **Upload plików:**
   - Przeciągnij 3 pliki z `/workspace/test_documents/`
   - LUB kliknij "Wybierz pliki"
   - Kliknij "Przetwórz dokumenty"

6. **Poczekaj 90-120 sekund** (progress bar pokaże postęp)

7. **Przejrzyj wyniki:**
   Powinieneś zobaczyć:
   - ✅ Ocena Dojrzałości Cyfrowej (6 wymiarów + overall score)
   - ✅ TOP Procesy do Automatyzacji (lista 10 procesów)
   - ✅ Szczegółowy Scoring Procesów (z tier badges)
   - ✅ Kluczowe Ustalenia
   - ✅ Rekomendacje

8. **Kliknij "Zatwierdź i przejdź do Analizy"**
   - Powinno przejść do Step 2 bez błędów
   - Żadnego Error 422!

---

## Dokumenty testowe

Utworzone 3 realistyczne dokumenty w `/workspace/test_documents/`:

1. **company_overview.md** (1.9 KB)
   - Informacje o firmie Acme Manufacturing
   - 185 pracowników, 48 mln PLN obrotu
   - Systemy: SAP, Salesforce, legacy
   - Poziom cyfryzacji dla 10 obszarów

2. **process_pain_points.md** (6 KB)
   - 14 szczegółowych procesów biznesowych
   - Time consumption, error rates, volumes
   - Problemy w: Finansach, Logistyce, Produkcji, HR
   - TOP 10 procesów do automatyzacji

3. **systems_and_infrastructure.txt** (6.7 KB)
   - Infrastruktura IT
   - Obecne systemy i integracje
   - Problemy techniczne
   - Budżet i zasoby

**Zawartość:** Realistyczne dane dla firmy produkcyjnej z konkretymi metrykami, które Claude może przeanalizować zgodnie z metodologią BFA.

---

## Czego się spodziewać

### ✅ Sukces wygląda tak:

**Claude powinien zidentyfikować:**
- ~10-14 procesów biznesowych
- Scoring każdego procesu (0-100)
- Kategoryzację na Tier 1-4
- TOP 10 procesów według potencjału automatyzacji

**TOP procesy (oczekiwane):**
1. Fakturowanie (35h/tydz, 8% błędów) → Tier 1
2. Order Fulfillment (60h/tydz, bezpośredni wpływ na klienta) → Tier 1
3. Raportowanie finansowe (40h/miesiąc) → Tier 2
4. Inventory Management (5% błędów, 180k PLN frozen) → Tier 1
5. Customer Inquiries (45h/tydz) → Tier 2
6-10. Inne procesy...

**Digital Maturity (oczekiwane):**
- Overall Score: ~50-60/100 (średnia dojrzałość)
- Process Maturity: 40-50
- Digital Infrastructure: 60-70
- RPA/Automation: 10-20 (bardzo niska)

**Confidence:**
- Overall: 75-85% (dobre dokumenty)
- Process identification: 85-90%
- Cost data: 60-70% (częściowe)

### ⏱️ Wydajność:

- Upload + analiza: 90-120 sekund
- Zależy od: rozmiaru dokumentów, złożoności
- Claude Extended Thinking: 50000 tokenów budget

### ❌ Możliwe problemy:

1. **"Claude API key not configured"**
   - Sprawdź `.env` file
   - Upewnij się że klucz zaczyna się od `sk-ant-`

2. **"Backend NOT running"**
   - Uruchom backend (patrz wyżej)
   - Sprawdź port 8000

3. **Timeout po 120s**
   - Dokumenty są bardzo duże
   - Spróbuj z mniejszą liczbą plików

4. **"No processes identified"**
   - Dokumenty nie zawierają opisów procesów
   - Użyj przygotowanych dokumentów testowych

---

## Weryfikacja wyników

### Sprawdź w bazie danych:

```python
# W Python console
from backend.app.database import SessionLocal
from backend.app.models.step1 import Step1Data

db = SessionLocal()
step1 = db.query(Step1Data).filter(Step1Data.project_id == PROJECT_ID).first()

print("✅ Step1Data exists:", step1 is not None)
print("✅ Has analysis_results:", step1.analysis_results is not None)
print("✅ TOP processes:", step1.analysis_results.get('top_processes', []))
print("✅ Digital maturity:", step1.analysis_results.get('digital_maturity', {}).get('overall_score'))
print("✅ Total processes:", len(step1.analysis_results.get('processes_scoring', [])))
```

### Sprawdź przez API:

```bash
curl http://localhost:8000/api/projects/${PROJECT_ID}/documents/latest-analysis | jq '{
  has_analysis,
  step1_data_available,
  top_processes: .extracted_data.top_processes,
  digital_maturity_score: .extracted_data.digital_maturity.overall_score,
  total_processes: (.extracted_data.processes_scoring | length),
  confidence: .confidence_scores.overall
}'
```

---

## Czyszczenie po testach

```bash
# Usuń testowy projekt z bazy
python /workspace/cleanup_test_documents.py ${PROJECT_ID}

# Lub wszystkie projekty testowe
for id in 1 2 3 4 5; do
    python /workspace/cleanup_test_documents.py $id
done
```

---

## 🎉 Gotowe!

Po pomyślnym teście system jest gotowy do:
- Prawdziwych dokumentów klientów
- Produkcyjnego użycia
- Pełnego flow: Upload → Review → Step 2

**Pytania? Problemy?**
- Sprawdź logi backend: `docker-compose logs bfa-audit-backend`
- Sprawdź `IMPLEMENTATION_SUMMARY.md` - pełna dokumentacja
- Sprawdź `TESTING_GUIDE.md` - troubleshooting
