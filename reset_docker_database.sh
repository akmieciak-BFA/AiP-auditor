#!/bin/bash

# Script to reset database in Docker environment
# This will remove all existing data and recreate the database schema

echo "=========================================="
echo "BFA Audit App - Docker Database Reset"
echo "=========================================="
echo ""
echo "⚠️  WARNING: This will DELETE all existing data!"
echo "Press CTRL+C to cancel, or ENTER to continue..."
read

echo ""
echo "🛑 Stopping containers..."
docker-compose down

echo ""
echo "🗑️  Removing database volume..."
docker volume rm aip-auditor-main_backend_data 2>/dev/null || echo "Volume already removed or doesn't exist"

echo ""
echo "🚀 Starting containers with fresh database..."
docker-compose up --build -d

echo ""
echo "⏳ Waiting for backend to initialize database..."
sleep 5

echo ""
echo "=========================================="
echo "✅ Database reset complete!"
echo "=========================================="
echo ""
echo "Application is now running:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
