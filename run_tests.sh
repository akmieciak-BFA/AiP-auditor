#!/bin/bash

echo "🧪 BFA Audit App - Comprehensive Test Suite"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "📦 Step 1: Building Docker containers..."
docker-compose build --quiet 2>&1 > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Docker build successful"
else
    echo -e "${RED}✗${NC} Docker build failed"
    exit 1
fi

echo ""
echo "🚀 Step 2: Starting services..."
docker-compose up -d
sleep 5

echo ""
echo "🔍 Step 3: Health checks..."

# Backend health
echo -n "Backend API... "
response=$(curl -s http://localhost:8000/health)
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
fi

# Backend config
echo -n "API Configuration... "
response=$(curl -s http://localhost:8000/api/config)
if echo "$response" | grep -q "claude_configured"; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
fi

# Frontend
echo -n "Frontend... "
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$response" -eq 200 ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
fi

echo ""
echo "📋 Step 4: API Endpoint Tests..."

# Test endpoints (will fail without auth but should return proper errors)
endpoints=(
    "/api/projects"
    "/docs"
    "/health"
    "/"
)

for endpoint in "${endpoints[@]}"; do
    echo -n "GET $endpoint... "
    status_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000$endpoint)
    if [ "$status_code" -eq 200 ] || [ "$status_code" -eq 401 ]; then
        echo -e "${GREEN}✓${NC} ($status_code)"
    else
        echo -e "${RED}✗${NC} ($status_code)"
    fi
done

echo ""
echo "🎯 Step 5: Integration Test - User Registration & Login..."

# Register user
echo -n "POST /api/auth/register... "
response=$(curl -s -X POST http://localhost:8000/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test123456","name":"Test User"}')

if echo "$response" | grep -q "email"; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠${NC} (może już istnieć)"
fi

# Login
echo -n "POST /api/auth/login... "
response=$(curl -s -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test123456"}')

if echo "$response" | grep -q "access_token"; then
    echo -e "${GREEN}✓${NC}"
    token=$(echo $response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    
    # Test authenticated endpoint
    echo -n "GET /api/auth/me (authenticated)... "
    me_response=$(curl -s -H "Authorization: Bearer $token" http://localhost:8000/api/auth/me)
    if echo "$me_response" | grep -q "test@example.com"; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
    
    # Create project
    echo -n "POST /api/projects (authenticated)... "
    project_response=$(curl -s -X POST http://localhost:8000/api/projects \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d '{"name":"Test Project","client_name":"Test Client"}')
    
    if echo "$project_response" | grep -q "id"; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
else
    echo -e "${RED}✗${NC}"
fi

echo ""
echo "📊 Step 6: Performance Metrics..."

# Check response times
echo "Measuring response times..."
for i in {1..5}; do
    time_ms=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8000/health)
    echo "  Request $i: ${time_ms}s"
done

echo ""
echo "🎉 Test Suite Complete!"
echo ""
echo "To stop services run:"
echo "  docker-compose down"
echo ""
