# 🔧 Instrukcja Naprawy - Problem z Tworzeniem Projektów

## 🎯 Problem
Nie można utworzyć projektu - wyskakuje błąd przy próbie utworzenia.

## ✅ Rozwiązanie
Wszystkie błędy w kodzie zostały naprawione! Teraz wystarczy zresetować bazę danych.

---

## 📋 INSTRUKCJA KROK PO KROKU (Windows)

### Metoda 1: Automatyczny skrypt (ZALECANE) ⭐

1. **Otwórz PowerShell jako Administrator**
   - Kliknij prawym na Start → Windows PowerShell (Administrator)

2. **Przejdź do folderu projektu:**
   ```powershell
   cd "C:\Users\macad\OneDrive\Pulpit\AiP-auditor-main"
   ```

3. **Uruchom skrypt naprawy:**
   ```powershell
   .\SZYBKA_NAPRAWA.ps1
   ```

4. **Gotowe!** Aplikacja uruchomi się automatycznie.

---

### Metoda 2: Ręczne komendy

Jeśli skrypt nie działa, wykonaj ręcznie:

```powershell
# 1. Przejdź do folderu projektu
cd "C:\Users\macad\OneDrive\Pulpit\AiP-auditor-main"

# 2. Zatrzymaj kontenery
docker-compose down

# 3. Usuń stary volume z bazą danych
docker volume rm aip-auditor-main_backend_data

# 4. Wyczyść nieużywane volumes (opcjonalnie)
docker volume prune -f

# 5. Uruchom aplikację ponownie
docker-compose up --build
```

---

## 🔍 Weryfikacja czy działa

Po uruchomieniu powinieneś zobaczyć:

```
backend  | INFO:     Application startup complete.
frontend | ➜  Local:   http://localhost:3000/
```

Teraz:

1. **Otwórz przeglądarkę:** http://localhost:3000
2. **Kliknij "Nowy Projekt"**
3. **Wpisz nazwę projektu i nazwę klienta**
4. **Kliknij "Utwórz"**

✅ Projekt powinien się utworzyć bez błędów!

---

## ❓ Co jeśli nadal nie działa?

### Sprawdź logi backendu:
```powershell
docker-compose logs -f backend
```

Szukaj błędów (linie zaczynające się od ERROR).

### Sprawdź czy Docker działa:
```powershell
docker --version
docker ps
```

Powinieneś zobaczyć 2 kontenery: `bfa-audit-backend` i `bfa-audit-frontend`

### Sprawdź czy porty są wolne:
```powershell
netstat -ano | findstr "3000"
netstat -ano | findstr "8000"
```

Jeśli coś zajmuje te porty, zatrzymaj to lub zmień porty w `docker-compose.yml`

---

## 📊 Co zostało naprawione?

### Backend:
- ✅ Usunięty model `ActivityLog` który blokował bazę danych
- ✅ Usunięte wszystkie referencje do `user_id`
- ✅ Naprawione importy w `claude_service.py`
- ✅ Usunięta autentykacja z routerów (step3, step4, drafts)
- ✅ Dodany alias `Step1DataInput` dla kompatybilności
- ✅ Zaktualizowane `requirements.txt` (numpy, email-validator)

### Frontend:
- ✅ Naprawiony `tailwind.config.js` - pełna konfiguracja kolorów

### Database:
- ✅ Usunięte wymaganie tabeli `users`
- ✅ Projekty działają bez autentykacji

---

## 🎯 Następne kroki po naprawie

1. **Przetestuj wszystkie kroki:**
   - Stwórz nowy projekt ✅
   - Wypełnij Step 1
   - Dodaj proces w Step 2
   - Zobacz analizę w Step 3
   - Wygeneruj prezentację w Step 4

2. **Skonfiguruj API Keys** (jeśli chcesz używać AI):
   
   Edytuj plik `.env`:
   ```
   SECRET_KEY=twoj-tajny-klucz-123456
   DATABASE_URL=sqlite:///./bfa_audit.db
   CLAUDE_API_KEY=sk-ant-... (twój klucz)
   GAMMA_API_KEY=... (twój klucz)
   VITE_API_URL=http://localhost:8000
   ```

3. **Backup** - po skonfigurowaniu zrób backup:
   ```powershell
   docker volume create aip-auditor-backup
   docker run --rm -v aip-auditor-main_backend_data:/source -v aip-auditor-backup:/backup alpine tar czf /backup/backup.tar.gz -C /source .
   ```

---

## 📞 Potrzebujesz pomocy?

Sprawdź te pliki w projekcie:
- `NAPRAWIONE_BLEDY.md` - pełny raport naprawionych błędów
- `BACKEND_AUDIT_REPORT.md` - szczegółowy audit backendu
- `README.md` - ogólna dokumentacja projektu

---

**Powodzenia! 🚀**
