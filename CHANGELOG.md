# 📝 Changelog - BFA Audit App

## [1.1.0] - 2025-10-26

### ✨ Dodane Funkcje

#### 🖥️ Wersja Desktopowa (Electron)
- **Natywna aplikacja** na Windows, macOS i Linux
- Własne okno aplikacji zamiast przeglądarki
- Konfiguracja electron-builder dla tworzenia instalatorów
- Skrypty npm: `dev:electron`, `build:electron`, `make`
- Dokumentacja: [DESKTOP_APP.md](DESKTOP_APP.md)

#### 🧠 Dynamiczne Formularze z Extended Thinking
- **Generowanie kwestionariuszy przez Claude Sonnet 4.5**
  - Spersonalizowane pytania dla każdej branży
  - 15-25 pytań dostosowanych do organizacji
  - Mix typów: text, number, scale, select, multiselect
  
- **Extended Thinking w wszystkich analizach**
  - Krok 1: 10,000 token budget dla generowania formularzy
  - Krok 1: 10,000 token budget dla analizy odpowiedzi
  - Krok 2: 10,000 token budget dla analizy procesów
  - Krok 3: 15,000 token budget dla research technologii
  
- **Nowy endpoint**: `POST /api/projects/{id}/step1/generate-form`
- **Przepisany Step1Form.tsx** z obsługą dynamicznych pól
- Dokumentacja: [DYNAMIC_FORMS.md](DYNAMIC_FORMS.md)

### 🔧 Zmiany Techniczne

#### Backend
- Dodano metodę `generate_step1_form()` w ClaudeService
- Wszystkie wywołania Claude API używają extended thinking
- Zwiększone limity tokenów (16,000-20,000 max_tokens)
- Parsowanie thinking blocks w odpowiedziach Claude

#### Frontend
- Dodano Electron setup (electron.js, preload.js)
- Zaktualizowano package.json z Electron dependencies
- Nowy flow w Step1Form:
  1. Dane organizacji
  2. Generowanie formularza (loading)
  3. Dynamiczny kwestionariusz
  4. Analiza z extended thinking
  5. Wyniki
- Nowy API endpoint w services/api.ts

#### Konfiguracja
- Uzupełnione klucze API w .env
- Dodane skrypty Electron w package.json
- Konfiguracja electron-builder dla budowania aplikacji

### 📚 Dokumentacja
- Nowy: [DESKTOP_APP.md](DESKTOP_APP.md) - instrukcje aplikacji desktopowej
- Nowy: [DYNAMIC_FORMS.md](DYNAMIC_FORMS.md) - dokumentacja dynamicznych formularzy
- Zaktualizowany: [README.md](README.md) - dodane nowe funkcje
- Nowy: [CHANGELOG.md](CHANGELOG.md) - ten plik

### 🐛 Poprawki
- Poprawiono extracting JSON z thinking blocks w Claude responses
- Zwiększono timeouty dla długich analiz
- Lepsze error handling w generowaniu formularzy

---

## [1.0.0] - 2025-10-26

### 🎉 Pierwsze Wydanie

#### Funkcje Core

**Framework 4-Krokowy:**
- ✅ Krok 1: Analiza Wstępna (kwestionariusz, scoring, TOP procesy)
- ✅ Krok 2: Mapowanie Procesów (AS-IS, MUDA, wąskie gardła)
- ✅ Krok 3: Rekomendacje (research, scenariusze budżetowe, ROI)
- ✅ Krok 4: Generowanie (prezentacje Gamma API)

**Integracje AI:**
- ✅ Claude Sonnet 4 API (Anthropic)
- ✅ Gamma API (prezentacje)

**Backend (FastAPI):**
- 32 pliki Python
- 6 modeli bazy danych
- 26 endpointów API
- Autentykacja JWT
- SQLAlchemy ORM

**Frontend (React + TypeScript):**
- 16 komponentów
- 4 główne strony
- Tailwind CSS
- Zustand state management
- Responsywny design

**Infrastructure:**
- Docker + docker-compose
- SQLite (dev) / PostgreSQL (prod ready)
- CORS configuration
- Environment variables

**Dokumentacja:**
- README.md (12KB)
- QUICK_START.md
- PROJECT_SUMMARY.md
- GETTING_STARTED.md

---

## Planowane Funkcje

### v1.2.0 (Q1 2025)
- [ ] Multi-language support
- [ ] Advanced charts and visualizations
- [ ] Export to PDF/DOCX
- [ ] Template library (processes, questionnaires)
- [ ] Save & resume functionality

### v1.3.0 (Q2 2025)
- [ ] Collaborative mode (team audits)
- [ ] Comments and annotations
- [ ] Version history
- [ ] Benchmark comparisons
- [ ] Mobile app (React Native)

### v2.0.0 (Q3 2025)
- [ ] Multi-tenant architecture
- [ ] Advanced analytics dashboard
- [ ] Integration marketplace (Zapier, Make)
- [ ] White-label options
- [ ] Enterprise SSO

---

## Jak Zgłaszać Problemy

1. Sprawdź [Issues](https://github.com/your-repo/issues)
2. Jeśli problem nie istnieje, stwórz nowy Issue
3. Użyj template'ów (Bug Report, Feature Request)
4. Dodaj logi i screenshoty

## Contributing

Zobacz [CONTRIBUTING.md](CONTRIBUTING.md) dla guidelines.

---

**Wersja**: 1.1.0  
**Data**: 2025-10-26  
**Autor**: BFA Audit Team
