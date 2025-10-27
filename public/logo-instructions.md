# Instrukcje Dodania Logo BFA

## Twoje logo

Umieść logo BFA w następujących formatach w katalogu `public/`:

1. **logo.png** - Oryginalne logo (wysokość: 200-300px)
2. **logo.webp** - Wersja WebP (zoptymalizowana, -30% rozmiaru)
3. **logo-small.webp** - Mała wersja dla mobile (100px)

## Jak przekonwertować:

```bash
# Jeśli masz ImageMagick lub podobne narzędzie:
convert logo.png -quality 90 -define webp:lossless=false logo.webp
convert logo.png -resize 100x100 logo-small.webp

# Online: https://squoosh.app/ (zalecane)
# Lub: https://cloudconvert.com/png-to-webp
```

## Obecna konfiguracja

Aplikacja automatycznie używa:
- `logo.webp` jeśli dostępny (najlepiej)
- `logo.png` jako fallback
- `logo.svg` jako ostatnia opcja (obecny)

Zalecany rozmiar: **200px wysokości, szerokość proporcjonalna**
Format: **WebP** dla najlepszej wydajności (30% mniejszy niż PNG!)
