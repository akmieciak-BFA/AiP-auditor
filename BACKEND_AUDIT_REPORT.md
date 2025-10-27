# Backend Audit Report - Znalezione błędy i niedociągnięcia

Data audytu: 2025-10-26

## 🔴 KRYTYCZNE BŁĘDY

### 1. ActivityLog model - referencja do nieistniejącej tabeli users
**Lokalizacja:** `backend/app/models/draft.py` (linie 22-37)

**Problem:**
```python
class ActivityLog(Base):
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", back_populates="activity_logs")
```

- Model `ActivityLog` wymaga `user_id` jako NOT NULL
- Tabela `users` nie istnieje (autentykacja została usunięta)
- ForeignKey constraint spowoduje błąd tworzenia tabel
- Relacje w `Project` i `User` modelu też odwołują się do `ActivityLog`

**Wpływ:**
- ❌ Baza danych NIE MOŻE zostać utworzona
- ❌ Wszystkie operacje na projektach mogą zakończyć się błędem
- ❌ **TO BLOKUJE TWORZENIE PROJEKTÓW**

**Rozwiązanie:**
1. Usunąć kolumnę `user_id` z modelu `ActivityLog`
2. Usunąć relację do `User` model
3. Usunąć relację `activity_logs` z modelu `Project`
4. LUB całkowicie usunąć model `ActivityLog` jeśli nie jest używany

---

### 2. Project model - relacja do ActivityLog
**Lokalizacja:** `backend/app/models/project.py` (linia 32)

**Problem:**
```python
activity_logs = relationship("ActivityLog", back_populates="project", cascade="all, delete-orphan")
```

Relacja do modelu który ma niepoprawną strukturę.

---

### 3. User model - relacja do ActivityLog  
**Lokalizacja:** `backend/app/models/user.py` (linia 19)

**Problem:**
```python
activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
```

---

## ⚠️ POTENCJALNE PROBLEMY

### 4. Brak walidacji dostępności Claude/Gamma API
**Lokalizacja:** Wszystkie serwisy

**Problem:**
- Brak graceful degradation gdy API key nie jest skonfigurowany
- Aplikacja może crashować zamiast zwrócić przyjazny błąd

**Rekomendacja:**
Dodać sprawdzanie na starcie aplikacji i logować warnings.

---

### 5. Brak limitów rozmiaru JSON w modelach
**Lokalizacja:** Wszystkie modele z kolumnami JSON

**Problem:**
- SQLite ma limit ~1GB na pole TEXT/BLOB
- Brak walidacji rozmiaru danych przed zapisem
- Potencjalny overflow przy dużych analizach

**Rekomendacja:**
Dodać walidację rozmiaru JSON przed zapisem do bazy.

---

## ✅ POZYTYWNE OBSERWACJE

1. ✅ **Wszystkie routery prawidłowo usunięte user authentication** (step1, step2, step3, step4, drafts, documents, projects)
2. ✅ **Import typing poprawiony** w `claude_service.py`
3. ✅ **Alias Step1DataInput** dodany prawidłowo
4. ✅ **Dependencies (requirements.txt)** zaktualizowane poprawnie
5. ✅ **Error handling** jest dobry w większości endpointów
6. ✅ **Middleware security** i rate limiting działają
7. ✅ **File upload validation** jest kompleksowa

---

## 📋 LISTA ZMIAN DO WPROWADZENIA

### Priorytet 1 (KRYTYCZNE - MUSI BYĆ NAPRAWIONE):
- [ ] Usunąć lub naprawić model `ActivityLog` w `backend/app/models/draft.py`
- [ ] Usunąć relację `activity_logs` z modelu `Project`
- [ ] Usunąć eksport `ActivityLog` z `backend/app/models/__init__.py`
- [ ] Zresetować bazę danych po zmianach

### Priorytet 2 (WAŻNE):
- [ ] Dodać walidację API keys na starcie aplikacji
- [ ] Dodać limity rozmiaru JSON w modelach

### Priorytet 3 (NICE TO HAVE):
- [ ] Dodać health check dla external APIs
- [ ] Dodać więcej unit testów
- [ ] Rozważyć użycie Redis zamiast in-memory cache

---

## 🎯 PODSUMOWANIE

**Główny problem:** Model `ActivityLog` blokuje tworzenie bazy danych bo wymaga nieistniejącej tabeli `users`.

**Najszybsze rozwiązanie:** Usunąć model `ActivityLog` całkowicie (nie jest używany w żadnym endpoincie).

**Dlaczego projekty nie działają:** Podczas inicjalizacji bazy danych (`init_db()`) SQLAlchemy próbuje utworzyć tabelę `activity_logs` z ForeignKey do `users.id`, co kończy się błędem.
