#!/bin/bash

# BFA Audit App - Smart Startup Script
# Automatycznie wykrywa tryb i uruchamia aplikację

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════╗"
echo "║                                                    ║"
echo "║          BFA AUDIT APP v1.2.0                     ║"
echo "║          Perfected Edition                         ║"
echo "║                                                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Plik .env nie istnieje${NC}"
    echo "Tworzę z .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Utworzono .env"
    echo ""
    echo -e "${YELLOW}📝 WAŻNE: Uzupełnij klucze API w pliku .env przed kontynuowaniem${NC}"
    echo ""
    read -p "Naciśnij Enter gdy uzupełnisz klucze API..."
fi

# Check Claude API key
if ! grep -q "CLAUDE_API_KEY=sk-ant-" .env; then
    echo -e "${RED}❌ Brak klucza Claude API w .env${NC}"
    echo "Dodaj: CLAUDE_API_KEY=sk-ant-your-key"
    exit 1
fi

echo -e "${GREEN}✓${NC} Konfiguracja OK"
echo ""

# Ask user which mode
echo "Wybierz tryb uruchomienia:"
echo ""
echo -e "  ${BLUE}1${NC} - Aplikacja Desktopowa (Electron) ${GREEN}[Zalecane]${NC}"
echo -e "  ${BLUE}2${NC} - Aplikacja Webowa (Docker Compose)"
echo -e "  ${BLUE}3${NC} - Tylko Backend (do testowania API)"
echo -e "  ${BLUE}4${NC} - Uruchom testy"
echo ""
read -p "Wybór (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${CYAN}🖥️  Uruchamianie Aplikacji Desktopowej...${NC}"
        echo ""
        
        # Start backend
        echo "Krok 1/3: Uruchamianie backendu..."
        docker-compose up -d backend
        
        # Wait for backend
        echo "Krok 2/3: Oczekiwanie na backend..."
        sleep 5
        
        # Check backend health
        if curl -s http://localhost:8000/health | grep -q "healthy"; then
            echo -e "${GREEN}✓${NC} Backend ready"
        else
            echo -e "${RED}✗${NC} Backend nie odpowiada"
            exit 1
        fi
        
        # Start Electron
        echo "Krok 3/3: Uruchamianie aplikacji desktopowej..."
        cd frontend
        
        if [ ! -d "node_modules" ]; then
            echo "Instalowanie zależności..."
            npm install --silent
        fi
        
        npm run dev:electron
        ;;
        
    2)
        echo ""
        echo -e "${CYAN}🌐 Uruchamianie Aplikacji Webowej...${NC}"
        echo ""
        
        echo "Budowanie i uruchamianie kontenerów..."
        docker-compose up --build
        ;;
        
    3)
        echo ""
        echo -e "${CYAN}🔧 Uruchamianie tylko Backend...${NC}"
        echo ""
        
        docker-compose up backend
        
        echo ""
        echo -e "${GREEN}Backend dostępny:${NC}"
        echo "  API: http://localhost:8000"
        echo "  Docs: http://localhost:8000/docs"
        ;;
        
    4)
        echo ""
        echo -e "${CYAN}🧪 Uruchamianie testów...${NC}"
        echo ""
        
        ./run_tests.sh
        ;;
        
    *)
        echo -e "${RED}Nieprawidłowy wybór${NC}"
        exit 1
        ;;
esac
