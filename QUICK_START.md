# 🚀 Quick Start Guide - BFA Audit App

## Szybkie Uruchomienie (5 minut)

### 1. Przygotowanie środowiska

```bash
# Sklonuj repozytorium
cd /workspace

# Skopiuj plik konfiguracyjny
cp .env.example .env
```

### 2. Konfiguracja API Keys

Edytuj plik `.env` i dodaj swoje klucze API:

```bash
# Otwórz plik do edycji
nano .env
# lub
vim .env
```

Wypełnij:
```
SECRET_KEY=wygeneruj-losowy-string-min-32-znaki
CLAUDE_API_KEY=sk-ant-twoj-klucz-z-anthropic
GAMMA_API_KEY=twoj-klucz-z-gamma
```

**Gdzie uzyskać klucze:**
- **Claude API**: https://console.anthropic.com → Settings → API Keys
- **Gamma API**: https://gamma.app → Settings
- **Secret Key**: Wygeneruj: `openssl rand -hex 32`

### 3. Uruchomienie aplikacji

```bash
# Uruchom Docker
docker-compose up --build
```

Poczekaj aż zobaczysz:
```
✓ frontend  Started
✓ backend   Started
```

### 4. Otwórz aplikację

Otwórz przeglądarkę i przejdź do:
- **Aplikacja**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### 5. Pierwszy projekt

1. **Zarejestruj się**:
   - Email: `test@example.com`
   - Hasło: `test123456`
   - Imię: `Jan Kowalski`

2. **Utwórz projekt**:
   - Nazwa: "Audyt Testowy"
   - Klient: "ACME Corp"

3. **Wypełnij Krok 1**:
   - Dane organizacji
   - Odpowiedzi na kwestionariusz (suwaki)
   - Lista procesów (min. 5)

4. **Analizuj** → Poczekaj na AI

5. **Przejdź przez kroki 2-4**

## 🎯 Typowy Flow Audytu

```
Start → Rejestracja → Nowy Projekt
  ↓
Krok 1: Analiza Wstępna (5-10 min)
  ↓ [AI: 30-60s]
Krok 2: Mapowanie Procesów (15-30 min na proces)
  ↓ [AI: 30-60s per proces]
Krok 3: Rekomendacje (2 min)
  ↓ [AI: 2-5 min]
Krok 4: Generowanie Prezentacji (1 min)
  ↓ [AI: 30-60s]
Gotowa Prezentacja! 🎉
```

## 💡 Wskazówki

- **Oszczędzaj czas AI**: Wypełnij wszystkie dane przed kliknięciem "Analizuj"
- **Realistyczne dane**: AI lepiej analizuje konkretne liczby (koszty, czasy)
- **Minimum 5 procesów** w Kroku 1 dla lepszych wyników
- **Szczegółowe opisy** kroków procesu w Kroku 2

## 🆘 Szybka Pomoc

**Problem**: API error
→ Sprawdź klucze API w `.env`

**Problem**: Port zajęty
→ `docker-compose down` i uruchom ponownie

**Problem**: Baza danych
→ Usuń plik `backend/bfa_audit.db` i uruchom ponownie

## 📞 Więcej Informacji

Zobacz pełną dokumentację: [README.md](README.md)
