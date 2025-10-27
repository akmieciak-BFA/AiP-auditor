# Quick Start - Pobieranie Raportów Markdown

## 🚀 Jak Pobrać Raport Audytu jako Plik Markdown

### Krok 1: Przejdź do Projektu
1. Otwórz Dashboard BFA Audit App
2. Wybierz projekt z listą (lub utwórz nowy)
3. Przejdź do widoku projektu

### Krok 2: Wykonaj Przynajmniej Step 1
- Aplikacja musi mieć dane do wygenerowania
- Minimum: zakończony Step 1 (Analiza Wstępna)
- Najlepiej: zakończone Step 1 + Step 2 + Step 3

### Krok 3: Kliknij Przycisk "Pobierz Markdown"
- Przycisk pojawia się w prawym górnym rogu (obok nazwy projektu)
- Wygląd: `📄 Pobierz Markdown`

### Krok 4: Poczekaj na Pobranie
- Stan loading: `🔄 Pobieranie...`
- Toast notification: "Raport Markdown został pobrany" ✅

### Krok 5: Otwórz Pobrany Plik
Plik zostanie zapisany w katalogu Downloads jako:
```
Audyt_BFA_{Klient}_{Projekt}.md
```

## 📖 Czytanie Pliku Markdown

### Rekomendowane edytory:

**Windows:**
- [Typora](https://typora.io/) - piękny WYSIWYG editor
- [Visual Studio Code](https://code.visualstudio.com/) + Markdown Preview
- [MarkText](https://marktext.app/) - darmowy open-source

**macOS:**
- [Typora](https://typora.io/)
- [MacDown](https://macdown.uranusjr.com/) - darmowy
- [iA Writer](https://ia.net/writer) - minimalistyczny

**Linux:**
- [ReText](https://github.com/retext-project/retext)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Ghostwriter](https://ghostwriter.kde.org/)

**Online:**
- [StackEdit](https://stackedit.io/)
- [Dillinger](https://dillinger.io/)
- GitHub (upload i preview)

## 🔄 Konwersja do Innych Formatów

### Do PDF:
```bash
# Używając Pandoc
pandoc Audyt_BFA_Client_Project.md -o raport.pdf

# Używając Markdown-PDF (VS Code extension)
# 1. Otwórz .md w VS Code
# 2. Ctrl+Shift+P
# 3. Wpisz "Markdown PDF: Export (pdf)"
```

### Do Word (.docx):
```bash
# Używając Pandoc
pandoc Audyt_BFA_Client_Project.md -o raport.docx
```

### Do HTML:
```bash
# Używając Pandoc
pandoc Audyt_BFA_Client_Project.md -o raport.html

# Z custom CSS
pandoc Audyt_BFA_Client_Project.md -c style.css -o raport.html
```

## 🎯 Co Jest w Raporcie?

### Zawsze dostępne:
- ✅ Nagłówek z metadanymi
- ✅ Spis treści z linkami
- ✅ Footer z metrykami jakości

### Zależy od postępu:
- 📊 **Krok 1**: Executive Summary, Dojrzałość Cyfrowa, TOP Procesy
- 🔍 **Krok 2**: Szczegółowe mapowanie procesów, MUDA, wąskie gardła
- 💡 **Krok 3**: Scenariusze budżetowe, ROI, rekomendacje
- 📅 **Krok 4**: Harmonogram, podsumowanie

## 💡 Przykładowy Workflow

```
1. Utwórz projekt "Audyt ABC Corp"
   ↓
2. Wypełnij formularz Step 1
   ↓
3. Kliknij "Analizuj" (Claude generuje analizę)
   ↓
4. Kliknij "Pobierz Markdown" 
   ↓
5. Otwórz plik w Typora/VS Code
   ↓
6. Edytuj/doprecyzuj raport
   ↓
7. Wyeksportuj do PDF dla klienta
```

## 🔧 Troubleshooting

### Przycisk "Pobierz Markdown" nie jest widoczny
**Problem:** Projekt nie ma jeszcze danych
**Rozwiązanie:** Zakończ przynajmniej Step 1 analizy

### Błąd: "No audit data available"
**Problem:** Baza danych nie zawiera wyników analizy
**Rozwiązanie:** Wróć do Step 1 i uruchom analizę Claude

### Plik jest pusty lub niepełny
**Problem:** Niektóre kroki nie zostały zakończone
**Rozwiązanie:** Raport zawiera tylko zakończone kroki. Dokończ pozostałe kroki dla pełnego raportu.

### Błąd pobierania w przeglądarce
**Problem:** Blokada pobierania przez przeglądarkę
**Rozwiązanie:** Sprawdź ustawienia pobierania w przeglądarce, odblokuj popup dla BFA App

## 📊 Metryki Jakości w Raporcie

Na końcu każdego raportu znajdziesz podsumowanie:

```markdown
## Podsumowanie Jakości Raportu

- **Krok 1:** ✅ 1,240 słów
- **Krok 2:** ✅ 6,420 słów (5 procesów)  
- **Krok 3:** ✅ 7,100 słów (5 procesów)

**Całkowita liczba słów:** 14,760
**Szacowana liczba slajdów Gamma:** 67

**Status ogólny:** ✅ Spełnia standard Turris
```

**Legenda:**
- ✅ = Spełnia standard Turris (minimum słów osiągnięte)
- ⚠️ = Poniżej standardów (wymaga regeneracji)

## 🎓 Wskazówki Pro

### 1. Edytuj przed wysłaniem do klienta
Markdown pozwala łatwo dodać:
- Logo firmy
- Komentarze dodatkowe
- Custom sekcje

### 2. Użyj version control
```bash
git init
git add Audyt_BFA_*.md
git commit -m "Initial audit report"
```

### 3. Stwórz template CSS dla PDF
Dostosuj wygląd eksportowanego PDF:
```css
/* style.css */
h1 { color: #2563eb; }
table { border-collapse: collapse; }
```

### 4. Automatyzuj eksport
Stwórz skrypt bash/PowerShell:
```bash
#!/bin/bash
# auto-export.sh
pandoc "$1" -o "${1%.md}.pdf"
pandoc "$1" -o "${1%.md}.docx"
echo "Exported to PDF and DOCX"
```

## 🔗 Przydatne Linki

- [Markdown Guide](https://www.markdownguide.org/) - pełna dokumentacja Markdown
- [Pandoc](https://pandoc.org/) - uniwersalny konwerter dokumentów
- [Mermaid](https://mermaid-js.github.io/) - dodawanie diagramów do Markdown

## ❓ FAQ

**Q: Czy mogę pobrać tylko wybrane sekcje?**
A: Obecnie nie, ale możesz edytować plik .md i usunąć niepotrzebne sekcje.

**Q: Czy mogę dostosować format raportu?**
A: Tak, edytuj plik .md w dowolnym edytorze i dostosuj do swoich potrzeb.

**Q: Czy mogę udostępnić raport klientowi?**
A: Tak! Wyeksportuj do PDF i wyślij klientowi. Markdown może być też otwarty bezpośrednio w GitHub.

**Q: Jak często mogę pobierać raport?**
A: Bez ograniczeń. Za każdym razem generowany jest fresh raport z aktualnych danych.

**Q: Czy raport zawiera dane wrażliwe?**
A: Raport zawiera wszystkie dane wprowadzone w audycie. Upewnij się przed udostępnieniem.

---

**Gotowe! Teraz możesz pobierać profesjonalne raporty audytów jako pliki Markdown. 🎉**
