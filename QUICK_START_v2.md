# Quick Start Guide - BFA Audit App v2.0

## 🚀 Szybki Start (5 minut)

### Wymagania wstępne
- Python 3.8+
- Node.js 16+
- Claude API Key (Anthropic)

---

## 📦 Instalacja

### 1. Reset bazy danych (WAŻNE!)

Ze względu na zmianę struktury (usunięcie user_id), musisz zresetować bazę:

```bash
./reset_database.sh
```

### 2. Backend Setup

```bash
cd backend

# Zainstaluj zależności
pip install -r requirements.txt

# Skonfiguruj Claude API Key
export CLAUDE_API_KEY="your-api-key-here"

# Uruchom serwer
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend będzie dostępny na: http://localhost:8000

### 3. Frontend Setup (nowe okno terminala)

```bash
cd frontend

# Zainstaluj zależności
npm install

# Uruchom dev server
npm run dev
```

Frontend będzie dostępny na: http://localhost:5173

---

## ✅ Weryfikacja

### Test 1: Backend działa
Otwórz: http://localhost:8000/health

Powinieneś zobaczyć:
```json
{
  "status": "healthy",
  "version": "1.1.0",
  "database": "healthy"
}
```

### Test 2: API Docs dostępne
Otwórz: http://localhost:8000/docs

### Test 3: Frontend działa
Otwórz: http://localhost:5173

Powinieneś zobaczyć stronę główną bez wymogu logowania.

---

## 🎯 Pierwszy Audyt

### Krok 1: Utwórz projekt
1. Kliknij "Nowy Projekt"
2. Wprowadź:
   - Nazwa: "Test Audyt Q1 2024"
   - Klient: "ACME Corporation"
3. Kliknij "Utwórz"

### Krok 2: Wypełnij formularz (5 sekcji)

#### Sekcja A: Organizacja
- Nazwa: ACME Corporation
- Branża: Manufacturing
- Wielkość: Średnia (50-249)
- Lokalizacja: Warszawa
- Wypełnij oceny cyfryzacji (slidery 0-10)

#### Sekcja B: Problemy
- Opisz główne wyzwania operacyjne

#### Sekcja C: Cele
- Oczekiwana redukcja kosztów: 20%
- Oczekiwany ROI: 150%
- Opisz źródła oszczędności

#### Sekcja D: Zasoby
- Zespół IT: Tak
- Doświadczenie: Ograniczone

#### Sekcja E: Strategia
- Opisz strategię biznesową na 3-5 lat

### Krok 3: Analizuj
1. Kliknij "Zakończ i Analizuj"
2. Poczekaj ~60 sekund (Claude Extended Thinking)
3. Zobacz wyniki analizy

### Krok 4: Sprawdź raport
```bash
cat project_reports/Test_Audyt_Q1_2024/STEP1_ANALIZA_WSTEPNA.md
```

---

## 📁 Struktura folderów

```
/workspace/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   └── step1.py (NEW - z markdown generation)
│   │   ├── schemas/
│   │   │   └── step1.py (NEW - InitialAssessmentData)
│   │   └── services/
│   │       └── claude_service.py (NEW - analyze_step1_comprehensive)
│   └── bfa_audit.db (NEW schema bez user_id)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Step1Form.tsx (CAŁKOWICIE PRZEPISANY)
│   │   ├── App.tsx (bez auth)
│   │   └── types/index.ts (bez User types)
│   └── (Login.tsx, Register.tsx, authStore.ts USUNIĘTE)
│
├── project_reports/ (NOWY - generowany automatycznie)
│   └── {Nazwa_Projektu}/
│       └── STEP1_ANALIZA_WSTEPNA.md
│
├── CHANGES_v2.0.md (dokumentacja zmian)
└── QUICK_START_v2.md (ten plik)
```

---

## 🔧 Konfiguracja

### Zmienne środowiskowe (backend)

Utwórz plik `backend/.env`:

```env
# Claude API
CLAUDE_API_KEY=sk-ant-...

# Database
DATABASE_URL=sqlite:///./bfa_audit.db

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Optional
GAMMA_API_KEY=your-gamma-key  # Dla generowania prezentacji
```

### Zmienne środowiskowe (frontend)

Utwórz plik `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

## 🐛 Rozwiązywanie problemów

### Problem: "Module not found" (backend)
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Problem: "Failed to fetch" (frontend)
1. Sprawdź czy backend działa (http://localhost:8000/health)
2. Sprawdź CORS w backend/app/main.py
3. Sprawdź VITE_API_URL w frontend/.env

### Problem: "Column user_id not found"
Musisz zresetować bazę danych:
```bash
./reset_database.sh
```

### Problem: "Claude API error"
1. Sprawdź czy CLAUDE_API_KEY jest ustawiony
2. Sprawdź czy masz wystarczający limit API
3. Sprawdź logi: backend terminal

### Problem: Raport markdown nie został wygenerowany
1. Sprawdź uprawnienia do zapisu w folderze workspace
2. Sprawdź logi backend - funkcja `_generate_step1_markdown_report`
3. Upewnij się, że nazwa projektu nie zawiera niedozwolonych znaków

---

## 📝 Szybkie testy

### Test backend lokalnie
```bash
cd backend
python -c "from app.database import SessionLocal; db = SessionLocal(); print('✅ Database OK')"
```

### Test Claude API
```bash
cd backend
python << EOF
from app.services.claude_service import ClaudeService
from app.config import get_settings

settings = get_settings()
if settings.claude_api_key:
    print("✅ Claude API Key configured")
else:
    print("❌ Claude API Key NOT configured")
EOF
```

---

## 🎉 Gotowe!

Aplikacja jest teraz:
- ✅ Bez wymogu logowania
- ✅ Z nowym formularzem 20 pytań
- ✅ Z automatycznym generowaniem raportów markdown
- ✅ Z Claude Extended Thinking analysis

---

## 📞 Wsparcie

W razie problemów:
1. Sprawdź CHANGES_v2.0.md dla szczegółów technicznych
2. Sprawdź logi backendu (uvicorn)
3. Sprawdź konsolę przeglądarki (F12)
4. Sprawdź http://localhost:8000/docs dla API documentation

---

**Wersja:** 2.0  
**Data:** 2025-10-26  
**Powered by:** Claude Sonnet 4.5 with Extended Thinking
