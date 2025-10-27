# Acme Manufacturing - Problemy i Procesy Biznesowe

## Główne wyzwania operacyjne

### 1. Wysokie koszty operacyjne
- Koszty pracy wzrosły o 18% w ostatnich 2 latach
- Nadgodziny: średnio 250h/miesiąc w księgowości
- Koszty błędów: ~80 000 PLN/rok

### 2. Długie czasy realizacji procesów
- Czas od zamówienia do wysyłki: 8-12 dni (standard branżowy: 5-7 dni)
- Czas procesowania faktury: 3-5 dni
- Czas zatwierdzenia zamówienia: 2-3 dni

### 3. Błędy i niska jakość
- Reklamacje klientów: 4.5% (cel: <2%)
- Błędy w fakturach: 8% wymaga korekt
- Błędy inwentaryzacyjne: różnice ~5% wartości magazynu

### 4. Brak widoczności procesów
- Brak real-time tracking zamówień
- Ręczne raportowanie (Excel)
- Brak KPI dashboardów

## Szczegółowa analiza procesów

### FINANSE - Procesy czasochłonne

#### 1. Fakturowanie (Invoice Processing)
- **Czas:** 35 godzin/tydzień (2 osoby FTE)
- **Wolumen:** ~800 faktur/miesiąc
- **Błędy:** 8% wymaga korekt
- **Cykl:** Przyjęcie faktury → Weryfikacja → Księgowanie → Zatwierdzenie → Płatność
- **Problemy:**
  - Ręczne wprowadzanie danych z PDF/papier
  - Brak OCR
  - Ręczne uzgadnianie z zamówieniami
  - 3-stopniowy proces zatwierdzania (email)
  - Częste zapytania o status faktury

#### 2. Reconciliation / Uzgodnienia księgowe
- **Czas:** 20 godzin/tydzień
- **Częstotliwość:** Dziennie, tygodniowo, miesięcznie
- **Błędy:** Rozbieżności w 15% uzgodnień wymagają manualnych korekt
- **Systemy:** SAP + Symfonia + Excel (3 systemy, brak automatycznej synchronizacji)

#### 3. Raportowanie finansowe
- **Czas:** 40 godzin/miesiąc
- **Raporty:** 25+ różnych raportów dla zarządu, audytorów, banków
- **Problemy:** Ręczne zbieranie danych z różnych systemów, Excel consolidation

#### 4. Payment approvals / Zatwierdzanie płatności
- **Czas:** 15 godzin/tydzień
- **Proces:** Email workflow, brak automatyzacji
- **Delays:** Średnio 2-3 dni na zatwierdzenie (czasem do 7 dni przy urlopach)

### LOGISTYKA - Wąskie gardła

#### 5. Order Fulfillment / Realizacja zamówień
- **Czas:** 60 godzin/tydzień (4 osoby)
- **Wolumen:** ~450 zamówień/miesiąc
- **Błędy:** 3% zamówień ma błędy (zły produkt, zła ilość)
- **Problemy:**
  - Ręczne przepisywanie z CRM do WMS
  - Brak automatycznego rezerwowania stanów magazynowych
  - Ręczne drukowanie dokumentów wysyłkowych
  - Brak integracji z kurierami

#### 6. Inventory Management / Zarządzanie magazynem
- **Czas:** 40 godzin/tydzień
- **Problemy:**
  - Ręczne inwentaryzacje
  - Różnice stanów: ~5% wartości
  - Brak real-time visibility
  - Overstocking: 180 000 PLN zamrożone w nadmiarowych zapasach
  - Stockouts: 12 przypadków/miesiąc

#### 7. Shipping & Logistics / Wysyłka
- **Czas:** 25 godzin/tydzień
- **Problemy:**
  - Ręczne tworzenie dokumentów przewozowych
  - Brak integracji z systemami kurierskimi
  - Tracking ręczny (email + Excel)

### PRODUKCJA

#### 8. Production Planning / Planowanie produkcji
- **Czas:** 30 godzin/tydzień
- **Narzędzia:** Excel + ręczne harmonogramy
- **Problemy:**
  - Brak real-time visibility capacity
  - Częste zmiany harmonogramu (5-8 razy/tydzień)
  - Konflikty resource allocation

#### 9. Quality Control Reporting / Raportowanie QC
- **Czas:** 20 godzin/tydzień
- **Problemy:**
  - Papierowe formularze
  - Ręczne wprowadzanie do systemu
  - Opóźnione dane (2-3 dni delay)

### SPRZEDAŻ I OBSŁUGA KLIENTA

#### 10. Customer Onboarding / Wdrożenie klienta
- **Czas:** 15 godzin na klienta (średnio 8 nowych klientów/miesiąc = 120h/miesiąc)
- **Problemy:**
  - 18-stopniowy proces manualny
  - Wiele działów zaangażowanych
  - Email workflow

#### 11. Quote Generation / Generowanie ofert
- **Czas:** 25 godzin/tydzień
- **Wolumen:** ~120 ofert/miesiąc
- **Problemy:**
  - Ręczne wyceny w Excel
  - Brak templates
  - Długi czas odpowiedzi (3-5 dni)

#### 12. Customer Inquiries / Zapytania klientów
- **Czas:** 45 godzin/tydzień
- **Kanały:** Email (70%), telefon (25%), portal (5%)
- **Problemy:**
  - Brak ticketing system
  - Średni czas odpowiedzi: 24-48h
  - Powtarzające się pytania (30% to FAQ)

### HR

#### 13. Employee Onboarding / Wdrożenie pracownika
- **Czas:** 12 godzin na osobę (średnio 4 nowe osoby/miesiąc = 48h/miesiąc)
- **Problemy:**
  - 25+ dokumentów do wypełnienia
  - Ręczne obiegi (papier + skan)
  - Długi czas setup IT/dostępów (3-5 dni)

#### 14. Payroll Processing / Naliczanie wynagrodzeń
- **Czas:** 40 godzin/miesiąc
- **Problemy:**
  - Ręczne zbieranie danych z systemu czasu pracy
  - Weryfikacja urlopów/nieobecności
  - Częste błędy wymagające korekt

## Priorytetyzacja - TOP procesy do automatyzacji (wstępna ocena)

Bazując na:
- Time consumption (TDABC)
- Error rates
- Business impact
- Repeatability

**TOP 10 procesów:**
1. Fakturowanie (35h/tydz, 8% błędów, wysoki ROI potential)
2. Order Fulfillment (60h/tydz, 3% błędów, bezpośredni wpływ na klienta)
3. Raportowanie finansowe (40h/miesiąc, strategiczne)
4. Inventory Management (40h/tydz, 5% błędów, 180k PLN frozen)
5. Customer Inquiries (45h/tydz, customer satisfaction)
6. Payment Approvals (15h/tydz, delays impact cash flow)
7. Quote Generation (25h/tydz, konkurencyjność)
8. Production Planning (30h/tydz, core business)
9. Uzgodnienia księgowe (20h/tydz, compliance)
10. Quality Control Reporting (20h/tydz, product quality)

## Cele automatyzacji

**Finansowe:**
- Redukcja kosztów operacyjnych: 25% (cel: 300 000 PLN/rok oszczędności)
- ROI: minimum 150% w 24 miesiące
- Payback: 12-18 miesięcy

**Operacyjne:**
- Skrócenie czasu procesowania faktur o 70% (z 35h do 10h/tydzień)
- Redukcja błędów w fakturowaniu z 8% do <2%
- Skrócenie czasu realizacji zamówień z 8-12 dni do 5-7 dni
- Redukcja różnic magazynowych z 5% do <1%
- Poprawa customer response time z 24-48h do <8h

**Strategiczne:**
- Zwiększenie przepustowości bez zatrudniania nowych osób
- Lepsza widoczność procesów (real-time dashboards)
- Skalowalność na wzrost produkcji o 40%
