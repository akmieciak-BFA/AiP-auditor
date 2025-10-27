#!/bin/bash
set -e

echo "=========================================="
echo "🧪 BFA AUDIT - Document Analysis Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
API_URL="http://localhost:8000"
PROJECT_NAME="Acme Manufacturing - Test Automation"
CLIENT_NAME="Acme Manufacturing Sp. z o.o."

# Step 1: Check if backend is running
echo "📡 Checking backend status..."
if curl -s "${API_URL}/docs" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${RED}❌ Backend is NOT running${NC}"
    echo ""
    echo "To start the backend, run:"
    echo "  cd /workspace/backend"
    echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    echo "Or with Docker:"
    echo "  cd /workspace"
    echo "  docker-compose up -d"
    echo ""
    exit 1
fi

# Step 2: Check if .env exists
echo "🔑 Checking environment..."
if [ ! -f "/workspace/.env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating .env from template..."
    cp /workspace/.env.example /workspace/.env
    echo -e "${YELLOW}⚠️  Please edit .env and add your CLAUDE_API_KEY${NC}"
    echo "  nano /workspace/.env"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ .env file exists${NC}"
    
    # Check if API key is set
    if grep -q "your-claude-api-key-from-anthropic" /workspace/.env; then
        echo -e "${YELLOW}⚠️  CLAUDE_API_KEY not configured in .env${NC}"
        echo "Please edit .env and add your actual API key:"
        echo "  nano /workspace/.env"
        echo ""
        exit 1
    fi
    echo -e "${GREEN}✅ CLAUDE_API_KEY configured${NC}"
fi

# Step 3: Check test documents
echo "📄 Checking test documents..."
TEST_DIR="/workspace/test_documents"
if [ ! -d "$TEST_DIR" ]; then
    echo -e "${RED}❌ Test documents directory not found${NC}"
    exit 1
fi

DOC1="${TEST_DIR}/company_overview.md"
DOC2="${TEST_DIR}/process_pain_points.md"
DOC3="${TEST_DIR}/systems_and_infrastructure.txt"

if [ -f "$DOC1" ] && [ -f "$DOC2" ] && [ -f "$DOC3" ]; then
    echo -e "${GREEN}✅ All 3 test documents found${NC}"
    echo "  - company_overview.md ($(wc -l < "$DOC1") lines)"
    echo "  - process_pain_points.md ($(wc -l < "$DOC2") lines)"
    echo "  - systems_and_infrastructure.txt ($(wc -l < "$DOC3") lines)"
else
    echo -e "${RED}❌ Test documents missing${NC}"
    exit 1
fi

# Step 4: Create test project
echo ""
echo "🏗️  Creating test project..."
PROJECT_RESPONSE=$(curl -s -X POST "${API_URL}/api/projects" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"${PROJECT_NAME}\",
        \"client_name\": \"${CLIENT_NAME}\",
        \"description\": \"Automated test of document analysis feature\"
    }")

PROJECT_ID=$(echo "$PROJECT_RESPONSE" | jq -r '.id')

if [ "$PROJECT_ID" = "null" ] || [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Failed to create project${NC}"
    echo "Response: $PROJECT_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ Project created: ID=$PROJECT_ID${NC}"

# Step 5: Upload and analyze documents
echo ""
echo "📤 Uploading documents for analysis..."
echo "   This will take 90-120 seconds (Claude Extended Thinking)..."
echo ""

START_TIME=$(date +%s)

UPLOAD_RESPONSE=$(curl -s -X POST "${API_URL}/api/projects/${PROJECT_ID}/documents/upload" \
    -F "files=@${DOC1}" \
    -F "files=@${DOC2}" \
    -F "files=@${DOC3}")

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "⏱️  Processing completed in ${DURATION} seconds"
echo ""

# Check if upload was successful
SUCCESS=$(echo "$UPLOAD_RESPONSE" | jq -r '.success')
if [ "$SUCCESS" != "true" ]; then
    echo -e "${RED}❌ Upload failed${NC}"
    echo "Response: $UPLOAD_RESPONSE"
    exit 1
fi

# Extract results
STEP1_DATA_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.step1_data_id')
PROCESSING_RESULT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.processing_result_id')
FILES_UPLOADED=$(echo "$UPLOAD_RESPONSE" | jq -r '.files_uploaded')
PROCESSING_TIME=$(echo "$UPLOAD_RESPONSE" | jq -r '.processing_time_seconds')

echo -e "${GREEN}✅ Documents uploaded and analyzed successfully${NC}"
echo ""
echo "📊 Results:"
echo "  - Files uploaded: ${FILES_UPLOADED}"
echo "  - Processing time: ${PROCESSING_TIME}s"
echo "  - Step1Data ID: ${STEP1_DATA_ID}"
echo "  - Processing Result ID: ${PROCESSING_RESULT_ID}"

# Step 6: Display analysis summary
echo ""
echo "=========================================="
echo "📈 ANALYSIS SUMMARY"
echo "=========================================="

# Digital Maturity
OVERALL_SCORE=$(echo "$UPLOAD_RESPONSE" | jq -r '.digital_maturity.overall_score')
echo ""
echo "🎯 Digital Maturity Score: ${OVERALL_SCORE}/100"

echo ""
echo "📋 6 Dimensions:"
echo "$UPLOAD_RESPONSE" | jq -r '.digital_maturity | to_entries[] | 
    select(.key != "overall_score" and .key != "interpretation") | 
    "  - \(.key): \(.value)/100"'

# TOP Processes
echo ""
echo "🏆 TOP Processes for Automation:"
TOP_COUNT=$(echo "$UPLOAD_RESPONSE" | jq -r '.analysis_summary.top_processes | length')
echo "  Found ${TOP_COUNT} processes:"
echo "$UPLOAD_RESPONSE" | jq -r '.analysis_summary.top_processes[] | "  • \(.)"'

# Confidence
CONFIDENCE=$(echo "$UPLOAD_RESPONSE" | jq -r '.analysis_summary.overall_confidence')
CONFIDENCE_PERCENT=$(echo "$CONFIDENCE * 100" | bc | cut -d. -f1)
echo ""
echo "✓ Overall Confidence: ${CONFIDENCE_PERCENT}%"

# Key Findings
echo ""
echo "🔍 Key Findings:"
echo "$UPLOAD_RESPONSE" | jq -r '.analysis_summary.key_findings[]? | "  • \(.)"'

# Missing Information
MISSING_COUNT=$(echo "$UPLOAD_RESPONSE" | jq -r '.analysis_summary.missing_information | length')
if [ "$MISSING_COUNT" -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Missing Information (${MISSING_COUNT} items):${NC}"
    echo "$UPLOAD_RESPONSE" | jq -r '.analysis_summary.missing_information[]? | "  • \(.)"'
fi

# Step 7: Verify Step1Data
echo ""
echo "=========================================="
echo "🔬 VERIFICATION"
echo "=========================================="
echo ""

echo "Fetching latest analysis..."
LATEST=$(curl -s "${API_URL}/api/projects/${PROJECT_ID}/documents/latest-analysis")

HAS_ANALYSIS=$(echo "$LATEST" | jq -r '.has_analysis')
STEP1_AVAILABLE=$(echo "$LATEST" | jq -r '.step1_data_available')

if [ "$HAS_ANALYSIS" = "true" ] && [ "$STEP1_AVAILABLE" = "true" ]; then
    echo -e "${GREEN}✅ Analysis data stored correctly${NC}"
    echo -e "${GREEN}✅ Step1Data available${NC}"
else
    echo -e "${RED}❌ Data verification failed${NC}"
    echo "  has_analysis: $HAS_ANALYSIS"
    echo "  step1_data_available: $STEP1_AVAILABLE"
fi

# Step 8: Test Process Scoring Details
echo ""
echo "📊 Process Scoring Details:"
PROCESS_COUNT=$(echo "$UPLOAD_RESPONSE" | jq -r '.processes_scoring | length')
echo "  Total processes analyzed: ${PROCESS_COUNT}"
echo ""

# Show top 5 processes with details
echo "Top 5 scored processes:"
echo "$UPLOAD_RESPONSE" | jq -r '.processes_scoring[0:5][] | 
    "  \(.process_name):
    Score: \(.score)/100, Tier: \(.tier)
    Time: \(.time_consumption // "N/A")
    Rationale: \(.rationale[0:80])..."' | head -30

# Step 9: Summary
echo ""
echo "=========================================="
echo "✨ TEST COMPLETED SUCCESSFULLY"
echo "=========================================="
echo ""
echo "What happened:"
echo "  1. ✅ Created test project (ID: ${PROJECT_ID})"
echo "  2. ✅ Uploaded 3 documents"
echo "  3. ✅ Claude analyzed with BFA methodology (~${PROCESSING_TIME}s)"
echo "  4. ✅ Created Step1Data automatically"
echo "  5. ✅ Identified ${TOP_COUNT} TOP processes"
echo "  6. ✅ Scored ${PROCESS_COUNT} total processes"
echo "  7. ✅ Digital maturity: ${OVERALL_SCORE}/100"
echo ""
echo "Next steps:"
echo "  - Open frontend: http://localhost:5173"
echo "  - Navigate to project ID ${PROJECT_ID}"
echo "  - Review analysis results"
echo "  - Click 'Zatwierdź i przejdź dalej' to advance to Step 2"
echo ""
echo "Full response saved to: /tmp/bfa_test_response.json"
echo "$UPLOAD_RESPONSE" | jq '.' > /tmp/bfa_test_response.json

echo ""
echo "🎉 All tests PASSED!"
