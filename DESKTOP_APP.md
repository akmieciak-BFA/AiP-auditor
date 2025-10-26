# 🖥️ BFA Audit App - Wersja Desktopowa (Electron)

## Przegląd

Aplikacja BFA Audit App jest dostępna w dwóch wersjach:
- **Webowa** - dostępna przez przeglądarkę (http://localhost:3000)
- **Desktopowa** - natywna aplikacja na Windows, macOS i Linux

## 🚀 Uruchomienie Aplikacji Desktopowej

### Metoda 1: Development Mode (z live reload)

```bash
cd frontend

# Zainstaluj zależności (pierwszy raz)
npm install

# Uruchom aplikację desktopową w trybie development
npm run dev:electron
```

Ta komenda:
1. Uruchamia Vite dev server (http://localhost:3000)
2. Czeka aż serwer będzie gotowy
3. Otwiera aplikację Electron z live reload

### Metoda 2: Production Build

```bash
cd frontend

# Build aplikacji
npm run build:electron

# Znajdziesz spakowaną aplikację w katalogu:
# frontend/release/
```

## 📦 Tworzenie Instalatorów

### Windows

```bash
cd frontend
npm run make

# Wygeneruje:
# - frontend/release/BFA Audit App Setup X.X.X.exe (instalator)
# - frontend/release/BFA Audit App X.X.X.exe (portable)
```

### macOS

```bash
cd frontend
npm run make

# Wygeneruje:
# - frontend/release/BFA Audit App-X.X.X.dmg
# - frontend/release/BFA Audit App-X.X.X-mac.zip
```

### Linux

```bash
cd frontend
npm run make

# Wygeneruje:
# - frontend/release/BFA Audit App-X.X.X.AppImage
# - frontend/release/bfa-audit-app_X.X.X_amd64.deb
```

## ⚙️ Konfiguracja

### Backend

Aplikacja desktopowa wymaga uruchomionego backendu:

```bash
# Uruchom backend (w osobnym terminalu)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**LUB** użyj Docker:

```bash
docker-compose up backend
```

### Ustawienia Electron

Plik konfiguracyjny: `frontend/electron.js`

Można zmienić:
- Rozmiar okna (width, height)
- Minimalne wymiary (minWidth, minHeight)
- Kolor tła (backgroundColor)
- Czy pokazywać DevTools w dev mode

## 🎨 Różnice między Wersją Webową a Desktopową

| Funkcja | Web | Desktop |
|---------|-----|---------|
| Dostęp | Przeglądarka | Natywna aplikacja |
| Ikona | Favicon | Ikona aplikacji |
| Okno | Tab przeglądarki | Własne okno |
| Skróty klawiaturowe | Standardowe | Dostosowane |
| Powiadomienia | Web notifications | System notifications |
| Auto-update | Reload strony | Wbudowane (opcjonalne) |

## 🔧 Zaawansowana Konfiguracja

### Zmiana Portu Backendu

Edytuj `frontend/src/services/api.ts`:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### Dodanie Custom Ikony

1. Umieść ikonę w `frontend/public/icon.png`
2. Electron automatycznie użyje jej jako ikony aplikacji

### Konfiguracja electron-builder

Edytuj `frontend/package.json` sekcja `"build"`:

```json
"build": {
  "appId": "com.bfa.audit",
  "productName": "BFA Audit App",
  "directories": {
    "output": "release"
  },
  "files": [
    "dist/**/*",
    "electron.js",
    "preload.js"
  ],
  "mac": {
    "category": "public.app-category.business",
    "target": ["dmg", "zip"],
    "icon": "build/icon.icns"
  },
  "win": {
    "target": ["nsis", "portable"],
    "icon": "build/icon.ico"
  },
  "linux": {
    "target": ["AppImage", "deb"],
    "category": "Office",
    "icon": "build/icon.png"
  }
}
```

## 📋 Wymagania Systemowe

### Development

- Node.js 18+
- npm 9+
- Python 3.11+ (dla backendu)

### Production (użytkownik końcowy)

**Windows:**
- Windows 10/11 (64-bit)
- .NET Framework 4.6.2+

**macOS:**
- macOS 10.13 (High Sierra) lub nowszy

**Linux:**
- Ubuntu 18.04+, Debian 10+, Fedora 30+
- GLIBC 2.28+

## 🐛 Troubleshooting

### Problem: "Cannot find module 'electron'"

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Problem: Backend nie odpowiada

Sprawdź czy backend działa:
```bash
curl http://localhost:8000/health
```

Jeśli nie, uruchom backend:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Problem: "App failed to load"

1. Sprawdź czy Vite dev server działa (http://localhost:3000)
2. Sprawdź logi Electron w konsoli
3. Spróbuj:
```bash
cd frontend
npm run dev
# W nowym terminalu:
npm run electron
```

### Problem: Aplikacja się nie buduje

```bash
cd frontend
# Wyczyść cache
rm -rf dist release node_modules
npm install
npm run build
```

## 💡 Wskazówki

1. **Development**: Używaj `npm run dev:electron` dla szybszego developmentu z hot reload
2. **Testing**: Testuj zawsze na docelowym systemie operacyjnym przed release
3. **Icons**: Przygotuj ikony w różnych rozmiarach (16x16 do 512x512)
4. **Code Signing**: Dla dystrybucji rozważ podpisanie kodu (Windows, macOS)
5. **Auto-Update**: Możesz dodać electron-updater dla automatycznych aktualizacji

## 🔐 Bezpieczeństwo

- ✅ `contextIsolation: true` - izolacja kontekstu
- ✅ `nodeIntegration: false` - wyłączona integracja Node.js w rendererze
- ✅ `preload.js` - bezpieczne API dla renderera
- ✅ External links - otwierane w przeglądarce systemowej

## 📚 Dodatkowe Zasoby

- [Electron Docs](https://www.electronjs.org/docs)
- [electron-builder Docs](https://www.electron.build/)
- [Electron Security Best Practices](https://www.electronjs.org/docs/tutorial/security)

---

**Gotowe!** Masz teraz pełnofunkcjonalną aplikację desktopową BFA Audit App! 🎉
