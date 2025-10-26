# BFA Audit App - Aplikacja do Automatyzacji Audytów BFA

Kompleksowa aplikacja webowa do tworzenia profesjonalnych audytów automatyzacyjnych według 4-krokowego frameworku BFA.

## 📋 Spis treści

- [Przegląd](#przegląd)
- [Technologie](#technologie)
- [Architektura](#architektura)
- [Framework Audytowy](#framework-audytowy)
- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Uruchomienie](#uruchomienie)
- [Użytkowanie](#użytkowanie)
- [API Documentation](#api-documentation)
- [Struktura Projektu](#struktura-projektu)

## 🎯 Przegląd

BFA Audit App to narzędzie wspierające proces audytowy, które:
- ✅ Zbiera dane przez intuicyjne formularze
- ✅ Analizuje procesy biznesowe za pomocą AI (Claude Sonnet 4.5)
- ✅ Generuje profesjonalne prezentacje (Gamma API)
- ✅ Oblicza ROI i payback period
- ✅ Dostarcza konkretne rekomendacje technologiczne

## 🛠 Technologie

### Backend
- **FastAPI** (Python 3.11+) - nowoczesny framework API
- **SQLAlchemy** - ORM do zarządzania bazą danych
- **SQLite/PostgreSQL** - baza danych
- **Claude API** (Anthropic) - analiza AI
- **Pydantic** - walidacja danych

### Frontend
- **React 18+** - biblioteka UI
- **TypeScript** - typowany JavaScript
- **Tailwind CSS** - stylowanie
- **React Router** - routing
- **Zustand** - zarządzanie stanem
- **Axios** - klient HTTP

### Deployment
- **Docker** + **docker-compose** - konteneryzacja
- **Uvicorn** - serwer ASGI

## 🏗 Architektura

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   React     │  HTTP   │   FastAPI   │  API    │   Claude    │
│  Frontend   │────────▶│   Backend   │────────▶│   Sonnet    │
│   (Port     │         │   (Port     │         │     4.5     │
│    3000)    │         │    8000)    │         └─────────────┘
└─────────────┘         └─────────────┘                │
                              │                        │
                              │                        │
                        ┌─────▼──────┐          ┌─────▼──────┐
                        │   SQLite   │          │   Gamma    │
                        │  Database  │          │    API     │
                        └────────────┘          └────────────┘
```

## 📊 Framework Audytowy (4 Kroki)

### **Krok 1: Analiza Wstępna**
- Identyfikacja TOP 3-5-10 procesów do dalszej analizy
- Kwestionariusz diagnostyczny (20-30 pytań)
- Scoring procesów (0-100)
- Kategoryzacja na Tier 1-4
- Analiza dojrzałości cyfrowej (6 wymiarów)

### **Krok 2: Mapowanie Procesów**
- Szczegółowa analiza procesu AS-IS
- Identyfikacja 8 typów marnotrawstwa (Lean Six Sigma MUDA)
- Time-Driven ABC
- Analiza wąskich gardeł
- Potencjał automatyzacji (%)

### **Krok 3: Rekomendacje Technologiczne**
- Research technologii (RPA, BPM, AI/ML, IDP, iPaaS)
- 3 scenariusze budżetowe (niski/średni/wysoki)
- Ocena vendorów (TOP 5-10)
- Proces TO-BE
- Kalkulacja ROI, payback, NPV

### **Krok 4: Generowanie Dokumentacji**
- Profesjonalna prezentacja (Gamma API)
- Styl: ciemny granatowy + zielone akcenty
- Kompletna struktura (wprowadzenie, metodologia, analizy, rekomendacje)

## 🚀 Instalacja

### Wymagania
- Docker Desktop (zalecane) LUB
- Python 3.11+
- Node.js 18+
- Git

### Klonowanie repozytorium
```bash
git clone <repo_url>
cd bfa-audit-app
```

## ⚙️ Konfiguracja

### 1. Utwórz plik `.env`
```bash
cp .env.example .env
```

### 2. Uzupełnij klucze API w `.env`
```bash
# Backend
DATABASE_URL=sqlite:///./bfa_audit.db
SECRET_KEY=wygeneruj-bezpieczny-klucz-openssl-rand-hex-32

# API Keys (wymagane!)
CLAUDE_API_KEY=sk-ant-xxx...  # Pobierz z https://console.anthropic.com
GAMMA_API_KEY=gamma-xxx...     # Pobierz z https://gamma.app

# Frontend
VITE_API_URL=http://localhost:8000
```

### 3. Uzyskanie kluczy API

**Claude API Key:**
1. Zarejestruj się na https://console.anthropic.com
2. Przejdź do Settings → API Keys
3. Utwórz nowy klucz API
4. Skopiuj klucz do `.env`

**Gamma API Key:**
1. Zarejestruj się na https://gamma.app
2. Przejdź do ustawień konta
3. Wygeneruj API key (jeśli dostępne)
4. Skopiuj klucz do `.env`

> ⚠️ **Uwaga**: Bez kluczy API aplikacja nie będzie mogła wykonywać analiz i generować prezentacji.

## 🏃 Uruchomienie

### Metoda 1: Docker (zalecane)

```bash
# Uruchom aplikację
docker-compose up --build

# Aplikacja będzie dostępna pod:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

Zatrzymanie:
```bash
docker-compose down
```

### Metoda 2: Manualne uruchomienie

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📱 Użytkowanie

### 1. Rejestracja i logowanie
- Otwórz http://localhost:3000
- Kliknij "Zarejestruj się"
- Wypełnij formularz (email, hasło, imię)
- Zaloguj się

### 2. Tworzenie projektu audytowego
- Kliknij "Nowy Projekt" na Dashboard
- Podaj nazwę projektu i nazwę klienta
- Kliknij "Utwórz"

### 3. Krok 1: Analiza Wstępna
- Wypełnij dane organizacji (nazwa, branża, wielkość)
- Odpowiedz na kwestionariusz diagnostyczny (suwaki 1-10)
- Dodaj listę procesów biznesowych (min. 5-10)
- Kliknij "Analizuj i Przejdź do Kroku 2"
- Poczekaj na wyniki AI (30-60 sekund)

### 4. Krok 2: Mapowanie Procesów
- Wybierz proces z listy TOP procesów
- Wypełnij formularz dla procesu:
  - **Sekcja A**: Podstawowe informacje
  - **Sekcja B**: Kroki procesu AS-IS (dodaj min. 5 kroków)
  - **Sekcja C**: Koszty i zasoby
- Kliknij "Analizuj Proces"
- Poczekaj na wyniki AI (30-60 sekund)
- Powtórz dla wszystkich wybranych procesów
- Kliknij "Przejdź do Kroku 3"

### 5. Krok 3: Rekomendacje Technologiczne
- Wybierz poziom budżetu (niski/średni/wysoki)
- Kliknij "Wykonaj Research i Analizę"
- Poczekaj na wyniki (2-5 minut - AI wykonuje research)
- Przejdź do Kroku 4

### 6. Krok 4: Generowanie Prezentacji
- Podaj nazwę klienta i autora audytu
- Wybierz scenariusz budżetowy
- Zaznacz procesy do uwzględnienia
- Kliknij "Generuj Prezentację"
- Poczekaj na generowanie (30-60 sekund)
- Kliknij "Otwórz Prezentację" aby zobaczyć wynik

## 📚 API Documentation

Po uruchomieniu backendu, dokumentacja API jest dostępna pod:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Główne endpointy:

**Autentykacja:**
- `POST /api/auth/register` - rejestracja użytkownika
- `POST /api/auth/login` - logowanie (zwraca JWT token)
- `GET /api/auth/me` - informacje o zalogowanym użytkowniku

**Projekty:**
- `GET /api/projects` - lista projektów
- `POST /api/projects` - tworzenie projektu
- `GET /api/projects/{id}` - szczegóły projektu
- `PUT /api/projects/{id}` - aktualizacja projektu
- `DELETE /api/projects/{id}` - usunięcie projektu

**Krok 1:**
- `POST /api/projects/{id}/step1/analyze` - analiza Kroku 1
- `GET /api/projects/{id}/step1/results` - wyniki Kroku 1

**Krok 2:**
- `POST /api/projects/{id}/step2/processes` - dodanie procesu
- `PUT /api/projects/{id}/step2/processes/{process_id}` - aktualizacja procesu
- `POST /api/projects/{id}/step2/processes/{process_id}/analyze` - analiza procesu
- `GET /api/projects/{id}/step2/results` - wyniki wszystkich procesów

**Krok 3:**
- `POST /api/projects/{id}/step3/analyze` - analiza technologii i scenariuszy
- `GET /api/projects/{id}/step3/results` - wyniki Kroku 3

**Krok 4:**
- `POST /api/projects/{id}/step4/generate-presentation` - generowanie prezentacji
- `GET /api/projects/{id}/step4/downloads` - lista wygenerowanych dokumentów

## 📁 Struktura Projektu

```
bfa-audit-app/
├── backend/
│   ├── app/
│   │   ├── models/          # Modele bazy danych (SQLAlchemy)
│   │   ├── schemas/         # Schematy Pydantic (walidacja)
│   │   ├── routers/         # Endpointy API (FastAPI)
│   │   ├── services/        # Logika biznesowa (Claude, Gamma)
│   │   ├── utils/           # Narzędzia pomocnicze (auth)
│   │   ├── config.py        # Konfiguracja aplikacji
│   │   ├── database.py      # Konfiguracja bazy danych
│   │   └── main.py          # Główna aplikacja FastAPI
│   ├── requirements.txt     # Zależności Python
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # Komponenty React
│   │   ├── pages/           # Strony (Dashboard, ProjectView)
│   │   ├── services/        # Klient API (Axios)
│   │   ├── store/           # Store (Zustand)
│   │   ├── types/           # Typy TypeScript
│   │   ├── utils/           # Narzędzia pomocnicze
│   │   ├── App.tsx          # Główny komponent
│   │   ├── main.tsx         # Entry point
│   │   └── index.css        # Style globalne (Tailwind)
│   ├── package.json         # Zależności Node.js
│   ├── tsconfig.json        # Konfiguracja TypeScript
│   ├── tailwind.config.js   # Konfiguracja Tailwind
│   ├── vite.config.ts       # Konfiguracja Vite
│   └── Dockerfile
├── docker-compose.yml       # Orkiestracja Docker
├── .env.example             # Przykładowa konfiguracja
├── .gitignore
└── README.md                # Ten plik
```

## 🎨 Styl Prezentacji

Prezentacje generowane przez aplikację mają profesjonalny wygląd zgodny ze stylem BFA:

**Kolory:**
- Tło: Ciemny granatowy (#1a1d3a, #2d3561)
- Akcenty: Zielony (#00ff00, #00cc00)
- Tekst: Biały (#ffffff)
- Ilustracje: Różowy/fioletowy (#ff6b9d, #c084fc)

**Elementy:**
- Ikony: Płaskie, białe w zielonych okręgach
- Ilustracje: Izometryczne, kolorowe
- Diagramy: Timeline z ikonami
- Boxy: Zielone z zaokrąglonymi rogami

## 🔒 Bezpieczeństwo

- ✅ Hasła hashowane (bcrypt)
- ✅ Autentykacja JWT z expiracją
- ✅ API keys w zmiennych środowiskowych
- ✅ CORS skonfigurowany
- ✅ Input validation (Pydantic)

## 🐛 Troubleshooting

### Problem: "Claude API error"
**Rozwiązanie**: Sprawdź czy klucz API Claude jest poprawny w `.env` i czy masz aktywne konto na console.anthropic.com

### Problem: "Port already in use"
**Rozwiązanie**: 
```bash
# Zatrzymaj inne aplikacje na portach 3000/8000
docker-compose down
# lub zmień porty w docker-compose.yml
```

### Problem: "Database locked"
**Rozwiązanie**: Zatrzymaj wszystkie instancje aplikacji i usuń plik `bfa_audit.db`, uruchom ponownie

### Problem: Frontend nie łączy się z backendem
**Rozwiązanie**: Sprawdź czy `VITE_API_URL` w `.env` wskazuje na `http://localhost:8000`

## 📈 Performance

- **Krok 1 analiza**: 30-60 sekund
- **Krok 2 analiza procesu**: 30-60 sekund
- **Krok 3 research**: 2-5 minut (zależy od liczby procesów)
- **Krok 4 generowanie prezentacji**: 30-60 sekund

## 🤝 Contributing

1. Fork projektu
2. Utwórz branch (`git checkout -b feature/AmazingFeature`)
3. Commit zmian (`git commit -m 'Add some AmazingFeature'`)
4. Push do brancha (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📝 License

Ten projekt jest stworzony dla celów demonstracyjnych.

## 👨‍💻 Autor

Aplikacja stworzona jako kompleksowe narzędzie do audytów automatyzacyjnych BFA.

## 🙏 Acknowledgments

- Anthropic za Claude API
- Gamma za API do generowania prezentacji
- Społeczność open-source za wspaniałe narzędzia

---

**Potrzebujesz pomocy?** Sprawdź:
- API Docs: http://localhost:8000/docs
- Issues: [GitHub Issues]
- Claude API Docs: https://docs.anthropic.com
