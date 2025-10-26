# Szybki skrypt naprawy bazy danych dla Windows
# Użyj tego jeśli masz problemy z tworzeniem projektów

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🔧 BFA Audit App - Naprawa bazy danych" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ten skrypt:" -ForegroundColor Yellow
Write-Host "  1. Zatrzyma Docker containers"
Write-Host "  2. Usunie starą bazę danych"
Write-Host "  3. Uruchomi aplikację z czystą bazą"
Write-Host ""
Write-Host "⚠️  UWAGA: Wszystkie dane zostaną usunięte!" -ForegroundColor Red
Write-Host ""
Write-Host "Naciśnij ENTER aby kontynuować lub Ctrl+C aby anulować..."
$null = Read-Host

Write-Host ""
Write-Host "⏸️  Zatrzymywanie kontenerów..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "🗑️  Usuwanie starej bazy danych..." -ForegroundColor Yellow
docker volume rm aip-auditor-main_backend_data 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Volume już usunięty lub nie istnieje" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🧹 Czyszczenie nieużywanych volumes..." -ForegroundColor Yellow
docker volume prune -f

Write-Host ""
Write-Host "🏗️  Budowanie i uruchamianie aplikacji..." -ForegroundColor Yellow
docker-compose up --build -d

Write-Host ""
Write-Host "⏳ Czekam na start backendu (15 sekund)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✅ GOTOWE!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Aplikacja powinna być dostępna na:" -ForegroundColor Cyan
Write-Host "  🌐 Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  🔧 Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  📖 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Sprawdź logi jeśli coś nie działa:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f backend" -ForegroundColor Gray
Write-Host ""
Write-Host "Aby zatrzymać aplikację:" -ForegroundColor Yellow
Write-Host "  docker-compose down" -ForegroundColor Gray
Write-Host ""
Write-Host "Naciśnij ENTER aby zamknąć to okno..."
$null = Read-Host
