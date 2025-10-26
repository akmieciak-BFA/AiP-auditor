#!/bin/bash

# Szybki skrypt naprawy bazy danych
# Użyj tego jeśli masz problemy z tworzeniem projektów

echo "=========================================="
echo "🔧 BFA Audit App - Naprawa bazy danych"
echo "=========================================="
echo ""
echo "Ten skrypt:"
echo "  1. Zatrzyma Docker containers"
echo "  2. Usunie starą bazę danych"
echo "  3. Uruchomi aplikację z czystą bazą"
echo ""
echo "⚠️  UWAGA: Wszystkie dane zostaną usunięte!"
echo ""
echo "Naciśnij ENTER aby kontynuować lub Ctrl+C aby anulować..."
read

echo ""
echo "⏸️  Zatrzymywanie kontenerów..."
docker-compose down

echo ""
echo "🗑️  Usuwanie starej bazy danych..."
docker volume rm aip-auditor-main_backend_data 2>/dev/null || echo "Volume już usunięty"

echo ""
echo "🧹 Czyszczenie nieużywanych volumes..."
docker volume prune -f

echo ""
echo "🏗️  Budowanie i uruchamianie aplikacji..."
docker-compose up --build -d

echo ""
echo "⏳ Czekam na start backendu (15 sekund)..."
sleep 15

echo ""
echo "=========================================="
echo "✅ GOTOWE!"
echo "=========================================="
echo ""
echo "Aplikacja powinna być dostępna na:"
echo "  🌐 Frontend: http://localhost:3000"
echo "  🔧 Backend:  http://localhost:8000"
echo "  📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Sprawdź logi jeśli coś nie działa:"
echo "  docker-compose logs -f backend"
echo ""
echo "Aby zatrzymać aplikację:"
echo "  docker-compose down"
echo ""
