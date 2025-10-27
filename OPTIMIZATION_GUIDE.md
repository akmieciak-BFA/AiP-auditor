# 🚀 Przewodnik Optymalizacji - BFA AiP Auditor

Praktyczny przewodnik po zaimplementowanych optymalizacjach i best practices.

---

## 📦 Jak Używać Nowych Struktur

### 1. Constants

**Zamiast hardcoded values:**
```typescript
// ❌ Złe
<button>Nowy Audyt</button>
<img src="/logo.svg" alt="Logo" />
```

**Użyj constants:**
```typescript
// ✅ Dobre
import { APP_CONFIG, NAVIGATION_LINKS } from '../constants';

<img src="/logo.svg" alt={`${APP_CONFIG.name} Logo`} />
```

### 2. Types

**Zamiast inline types:**
```typescript
// ❌ Złe
const audit: { id: string; title: string; status: string } = {...};
```

**Użyj zdefiniowanych typów:**
```typescript
// ✅ Dobre
import type { Audit } from '../types';

const audit: Audit = {...};
```

### 3. Helper Functions

**Zamiast powtarzającego się kodu:**
```typescript
// ❌ Złe
const formatted = `${change > 0 ? '↑' : '↓'} ${Math.abs(change)}% vs. ostatni miesiąc`;
```

**Użyj helpers:**
```typescript
// ✅ Dobre
import { formatPercentageChange } from '../utils/helpers';

const formatted = formatPercentageChange(change);
```

### 4. Media Queries

**Zamiast powtarzanych breakpoints:**
```typescript
// ❌ Złe
const Component = styled.div`
  @media (max-width: ${theme.breakpoints.md}) {
    padding: ${theme.spacing.md};
  }
`;
```

**Użyj media helpers:**
```typescript
// ✅ Dobre
import { media } from '../utils/mediaQueries';

const Component = styled.div`
  ${media.md} {
    padding: ${theme.spacing.md};
  }
`;
```

### 5. Icons

**Zamiast inline SVG:**
```typescript
// ❌ Złe
<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
</svg>
```

**Użyj Icon component:**
```typescript
// ✅ Dobre
import { Icon } from './common/Icon';

<Icon name="menu" size={24} />
```

---

## ⚡ Performance Best Practices

### 1. Memoization

**Kiedy używać `memo`:**
```typescript
// ✅ Użyj dla komponentów które:
// - Renderują się często
// - Mają expensive rendering
// - Otrzymują te same props często

export const ExpensiveComponent = memo(({ data }) => {
  // Heavy calculations
  return <div>{/* ... */}</div>;
});
```

### 2. useCallback

**Kiedy używać:**
```typescript
// ✅ Dla funkcji przekazywanych jako props
const handleClick = useCallback(() => {
  doSomething();
}, [dependency]);

<ChildComponent onClick={handleClick} />
```

### 3. useMemo

**Kiedy używać:**
```typescript
// ✅ Dla expensive calculations
const expensiveValue = useMemo(() => {
  return complexCalculation(data);
}, [data]);
```

### 4. Lazy Loading

**Dla dużych komponentów:**
```typescript
// ✅ Dobre dla:
// - Route components
// - Modals
// - Heavy features

const HeavyComponent = lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>
```

---

## ♿ Accessibility Checklist

### Semantic HTML
```typescript
// ✅ Użyj właściwych tagów
<header role="banner">     // Dla nagłówka
<nav role="navigation">    // Dla nawigacji
<main role="main">         // Dla głównej treści
<footer role="contentinfo"> // Dla stopki
<article>                  // Dla niezależnych elementów
<section>                  // Dla sekcji
```

### ARIA Labels
```typescript
// ✅ Dodaj dla przycisków bez tekstu
<button aria-label="Zamknij menu">
  <Icon name="close" />
</button>

// ✅ Dla dynamic content
<div role="status" aria-live="polite">
  Loading...
</div>

// ✅ Dla navigation
<nav aria-label="Main navigation">
```

### Keyboard Navigation
```typescript
// ✅ Dla custom clickable elements
<div 
  role="button" 
  tabIndex={0}
  onClick={handleClick}
  onKeyPress={(e) => e.key === 'Enter' && handleClick()}
>
```

---

## 🎨 Styling Best Practices

### 1. Użyj Theme

**Zamiast hardcoded values:**
```typescript
// ❌ Złe
const Box = styled.div`
  color: #374151;
  padding: 16px;
  border-radius: 8px;
`;
```

**Użyj theme:**
```typescript
// ✅ Dobre
const Box = styled.div`
  color: ${theme.colors.neutral.gray700};
  padding: ${theme.spacing.md};
  border-radius: ${theme.borderRadius.md};
`;
```

### 2. Container Styles

**Dla consistent max-width:**
```typescript
import { containerStyles } from '../utils/mediaQueries';

const Container = styled.div`
  ${containerStyles}
`;
```

### 3. Transitions

**Użyj z theme:**
```typescript
const Button = styled.button`
  transition: all ${theme.transitions.base};
  
  &:hover {
    transform: translateY(-2px);
  }
`;
```

---

## 🧪 Testing Guidelines

### Component Tests

```typescript
import { render, screen } from '@testing-library/react';
import { Header } from './Header';

describe('Header', () => {
  it('renders logo', () => {
    render(<Header />);
    expect(screen.getByAlt(/BFA.*Logo/i)).toBeInTheDocument();
  });

  it('opens menu on button click', async () => {
    const { user } = render(<Header />);
    const menuButton = screen.getByLabelText(/otwórz menu/i);
    
    await user.click(menuButton);
    expect(screen.getByRole('navigation')).toBeVisible();
  });
});
```

### Hook Tests

```typescript
import { renderHook } from '@testing-library/react';
import { useClickOutside } from './useClickOutside';

describe('useClickOutside', () => {
  it('calls handler on outside click', () => {
    const handler = jest.fn();
    const ref = { current: document.createElement('div') };
    
    renderHook(() => useClickOutside(ref, handler));
    
    document.dispatchEvent(new MouseEvent('mousedown'));
    expect(handler).toHaveBeenCalled();
  });
});
```

---

## 📊 Performance Monitoring

### Web Vitals

```typescript
// src/utils/vitals.ts
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

export function reportWebVitals(onPerfEntry?: (metric: any) => void) {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    getCLS(onPerfEntry);
    getFID(onPerfEntry);
    getFCP(onPerfEntry);
    getLCP(onPerfEntry);
    getTTFB(onPerfEntry);
  }
}

// src/main.tsx
import { reportWebVitals } from './utils/vitals';

reportWebVitals(console.log);
```

### Bundle Analysis

```bash
# Install
npm install --save-dev rollup-plugin-visualizer

# vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true })
  ]
});

# Run
npm run build
```

---

## 🔧 Developer Tools

### 1. React DevTools

```typescript
// Profiler component
import { Profiler } from 'react';

<Profiler id="Dashboard" onRender={onRenderCallback}>
  <Dashboard />
</Profiler>
```

### 2. Debug Renders

```typescript
// Log component renders
export const Component = memo(() => {
  console.log('Component rendered');
  return <div>...</div>;
});
```

### 3. TypeScript Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

---

## 📝 Code Review Checklist

### Przed Commit

- [ ] Brak console.log()
- [ ] Brak unused imports
- [ ] Brak TypeScript errors
- [ ] Wszystkie props mają typy
- [ ] Accessibility attributes dodane
- [ ] Performance considerations (memo, callback)
- [ ] Error handling dodany
- [ ] Constants użyte zamiast hardcoded values
- [ ] Tests dodane (jeśli applicable)

### Przed PR

- [ ] Build passes (`npm run build`)
- [ ] Lint passes (`npm run lint`)
- [ ] Tests pass (`npm test`)
- [ ] Bundle size check
- [ ] README updated (jeśli potrzebne)
- [ ] Documentation updated
- [ ] Performance measured
- [ ] Accessibility tested

---

## 🎯 Quick Wins

### 1. Image Optimization

```typescript
// Dodaj lazy loading
<img 
  src="/logo.svg" 
  alt="Logo" 
  loading="lazy"
/>

// Użyj srcset dla różnych sizes
<img 
  src="/image.jpg"
  srcSet="/image-small.jpg 480w, /image-large.jpg 1080w"
  sizes="(max-width: 768px) 480px, 1080px"
/>
```

### 2. Preconnect

```html
<!-- index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://api.example.com">
```

### 3. Meta Tags

```html
<!-- index.html -->
<meta name="description" content="BFA AiP Auditor - Nowoczesne narzędzie do zarządzania audytami">
<meta name="theme-color" content="#1A4645">
```

---

## 🚨 Common Pitfalls

### 1. ❌ Avoid

```typescript
// Tworzenie objects/arrays w render
<Component data={{ foo: 'bar' }} />  // ❌ Tworzy nowy object każdy render

// Inline functions bez memo
<Component onClick={() => doSomething()} />  // ❌ Nowa funkcja każdy render

// Używanie index jako key
{items.map((item, index) => <Item key={index} />)}  // ❌ Problemy z updates
```

### 2. ✅ Instead

```typescript
// Memo dla stable objects
const data = useMemo(() => ({ foo: 'bar' }), []);
<Component data={data} />

// useCallback dla funkcji
const handleClick = useCallback(() => doSomething(), []);
<Component onClick={handleClick} />

// Unique keys
{items.map(item => <Item key={item.id} />)}
```

---

## 📚 Recommended Reading

1. **React Performance**
   - [React.memo](https://react.dev/reference/react/memo)
   - [useCallback](https://react.dev/reference/react/useCallback)
   - [Code Splitting](https://react.dev/learn/code-splitting)

2. **TypeScript**
   - [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
   - [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

3. **Accessibility**
   - [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
   - [WebAIM Checklist](https://webaim.org/standards/wcag/checklist)

4. **Performance**
   - [Web Vitals](https://web.dev/vitals/)
   - [Lighthouse](https://developers.google.com/web/tools/lighthouse)

---

## 🎓 Next Steps

1. **Add Testing** (High Priority)
   ```bash
   npm install --save-dev vitest @testing-library/react
   ```

2. **Add Linting** (High Priority)
   ```bash
   npm install --save-dev eslint @typescript-eslint/eslint-plugin
   ```

3. **Add Storybook** (Medium Priority)
   ```bash
   npx storybook@latest init
   ```

4. **Add E2E Tests** (Medium Priority)
   ```bash
   npm install --save-dev @playwright/test
   ```

5. **Add Analytics** (Medium Priority)
   ```bash
   npm install @vercel/analytics
   ```

---

**Remember**: Optimization is an ongoing process. Monitor, measure, and improve continuously! 🚀

**Questions?** Check the [CODE_AUDIT_REPORT.md](./CODE_AUDIT_REPORT.md) for detailed analysis.
