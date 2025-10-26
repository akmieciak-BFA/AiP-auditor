# BFA AiP Auditor 🧠

<div align="center">
  <img src="./public/logo.svg" alt="BFA Logo" width="200"/>
  
  <h3>Nowoczesne narzędzie do zarządzania audytami i analizy ryzyka</h3>
  
  <p>
    Połączenie technologii i ludzkiej ekspertyzy dla lepszego biznesu
  </p>
</div>

---

## 🎨 Branding

Aplikacja wykorzystuje spójny system brandingu BFA:

- **Kolory Główne:**
  - Orange Gradient: `#FF7A00` → `#C41E3A` (Technologia/AI)
  - Teal Gradient: `#2B7A78` → `#17545A` (Natura/Człowiek)
  - Brand Dark: `#1A4645` (Tekst i akcenty)

- **Logo:** Symbolizuje połączenie technologii AI (obwody elektroniczne) z ludzką ekspertyzą (struktura organiczna)

## ✨ Funkcje

- 📊 **Dashboard z kluczowymi metrykami** - Przegląd wszystkich audytów w jednym miejscu
- 🎯 **Zarządzanie audytami** - Tworzenie, edycja i śledzenie postępów
- 📈 **Raporty i analizy** - Generowanie szczegółowych raportów
- 👥 **Historia aktywności** - Śledzenie działań zespołu
- 📱 **Responsive Design** - Działa na wszystkich urządzeniach
- 🎨 **Nowoczesny UI/UX** - Intuicyjny i przyjemny w użyciu

## 🚀 Instalacja

### Wymagania

- Node.js 18+ 
- npm lub yarn

### Szybki start

1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/akmieciak-BFA/AiP-auditor.git
   cd AiP-auditor
   ```

2. **Zainstaluj zależności:**
   ```bash
   npm install
   ```

3. **Uruchom serwer deweloperski:**
   ```bash
   npm run dev
   ```

4. **Otwórz w przeglądarce:**
   ```
   http://localhost:3000
   ```

## 📦 Dostępne Skrypty

- `npm run dev` - Uruchamia serwer deweloperski
- `npm run build` - Buduje aplikację do produkcji
- `npm run preview` - Podgląd produkcyjnej wersji
- `npm run lint` - Sprawdza kod pod kątem błędów TypeScript

## 🛠️ Stack Technologiczny

- **Frontend Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** Styled Components
- **Design System:** Własny system oparty na brandingu BFA
- **Icons:** SVG inline

## 📱 Responsive Breakpoints

```typescript
{
  sm: '640px',   // Telefony
  md: '768px',   // Tablety
  lg: '1024px',  // Laptopy
  xl: '1280px',  // Desktopy
  '2xl': '1536px' // Duże ekrany
}
```

## 🎨 Design System

Aplikacja wykorzystuje kompleksowy system designu zdefiniowany w `src/styles/theme.ts`:

- **Kolory:** Paleta brandowa + kolory semantyczne
- **Typografia:** Hierarchia fontów i wag
- **Spacing:** Konsystentny system odstępów
- **Shadows:** Zestaw cieni dla głębi
- **Transitions:** Płynne animacje

## 📂 Struktura Projektu

```
AiP-auditor/
├── public/
│   └── logo.svg           # Logo BFA
├── src/
│   ├── components/        # Komponenty React
│   │   ├── Header.tsx    # Nagłówek z nawigacją
│   │   ├── Dashboard.tsx # Główny dashboard
│   │   └── Footer.tsx    # Stopka
│   ├── styles/
│   │   ├── theme.ts      # System designu
│   │   └── global.css    # Globalne style
│   ├── App.tsx           # Główny komponent
│   └── main.tsx          # Entry point
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## 🎯 UX/UI Highlights

### Animacje i Mikrointerakcje
- Płynne fade-in dla elementów strony
- Hover effects na kartach i przyciskach
- Smooth transitions na wszystkich interakcjach
- Loading states i feedback wizualny

### Dostępność
- Semantic HTML
- Keyboard navigation
- Focus states
- ARIA labels
- Responsive typography

### Performance
- Lazy loading komponentów
- Optimized bundle size
- Fast refresh w rozwoju
- Production-ready builds

## 🌐 Przeglądarkowe Wsparcie

- Chrome (ostatnie 2 wersje)
- Firefox (ostatnie 2 wersje)
- Safari (ostatnie 2 wersje)
- Edge (ostatnie 2 wersje)

## 🤝 Rozwój

### Dodawanie nowych funkcji

1. Utwórz nowy komponent w `src/components/`
2. Dodaj typy w TypeScript
3. Użyj theme z `src/styles/theme.ts`
4. Dodaj do głównego App.tsx

### Stylowanie

Używamy Styled Components z dostępem do theme:

```typescript
import styled from 'styled-components';
import { theme } from '../styles/theme';

const StyledComponent = styled.div`
  color: ${theme.colors.primary.teal};
  padding: ${theme.spacing.md};
`;
```

## 📄 Licencja

ISC © BFA

## 👥 Kontakt

Dla pytań i wsparcia, skontaktuj się z zespołem BFA.

---

<div align="center">
  <p>Zbudowano z ❤️ przez zespół BFA</p>
  <p>Powered by React + TypeScript + Vite</p>
</div>
