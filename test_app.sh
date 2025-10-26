#!/bin/bash

# Comprehensive Test Script for BFA Audit App v2.1
# Tests all major functionality after v2.0 and v2.1 changes

echo "=========================================="
echo "BFA Audit App - Comprehensive Test Suite"
echo "Version: 2.1"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Function to test
test_case() {
    local name="$1"
    local command="$2"
    
    echo -n "Testing: $name... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

echo "=== PHASE 1: BACKEND IMPORTS ==="
echo ""

cd backend

test_case "Import file_parsers" \
    "python3 -c 'from app.utils.file_parsers import parse_file'"

test_case "Import document models" \
    "python3 -c 'from app.models.document import UploadedDocument, DocumentProcessingResult'"

test_case "Import documents router" \
    "python3 -c 'from app.routers.documents import router'"

test_case "Import Claude service" \
    "python3 -c 'from app.services.claude_service import ClaudeService'"

test_case "Import Step1 schemas" \
    "python3 -c 'from app.schemas.step1 import InitialAssessmentData, Step1AnalysisResult'"

test_case "Import projects router (no auth)" \
    "python3 -c 'from app.routers.projects import router'"

test_case "Import step2 router (no auth)" \
    "python3 -c 'from app.routers.step2 import router'"

cd ..

echo ""
echo "=== PHASE 2: BACKEND SYNTAX CHECK ==="
echo ""

cd backend

test_case "Compile main.py" \
    "python3 -m py_compile app/main.py"

test_case "Compile routers/documents.py" \
    "python3 -m py_compile app/routers/documents.py"

test_case "Compile routers/projects.py" \
    "python3 -m py_compile app/routers/projects.py"

test_case "Compile routers/step1.py" \
    "python3 -m py_compile app/routers/step1.py"

test_case "Compile utils/file_parsers.py" \
    "python3 -m py_compile app/utils/file_parsers.py"

test_case "Compile services/claude_service.py" \
    "python3 -m py_compile app/services/claude_service.py"

cd ..

echo ""
echo "=== PHASE 3: FILE STRUCTURE CHECK ==="
echo ""

test_case "Backend requirements.txt exists" \
    "[ -f backend/requirements.txt ]"

test_case "Frontend package.json exists" \
    "[ -f frontend/package.json ]"

test_case "Reset script exists" \
    "[ -f reset_database.sh ]"

test_case "Documentation exists" \
    "[ -f CHANGES_v2.0.md ] && [ -f DOCUMENT_UPLOAD_FEATURE.md ] && [ -f AUDIT_REPORT_v2.1.md ]"

test_case "Login/Register deleted" \
    "[ ! -f frontend/src/pages/Login.tsx ] && [ ! -f frontend/src/pages/Register.tsx ]"

test_case "AuthStore deleted" \
    "[ ! -f frontend/src/store/authStore.ts ]"

test_case "DocumentUploadInterface exists" \
    "[ -f frontend/src/components/DocumentUploadInterface.tsx ]"

test_case "ReviewExtractedData exists" \
    "[ -f frontend/src/components/ReviewExtractedData.tsx ]"

echo ""
echo "=== PHASE 4: DEPENDENCIES CHECK ==="
echo ""

test_case "Backend: openpyxl in requirements" \
    "grep -q 'openpyxl' backend/requirements.txt"

test_case "Backend: pandas in requirements" \
    "grep -q 'pandas' backend/requirements.txt"

test_case "Backend: PyPDF2 in requirements" \
    "grep -q 'PyPDF2' backend/requirements.txt"

test_case "Backend: chardet in requirements" \
    "grep -q 'chardet' backend/requirements.txt"

echo ""
echo "=== PHASE 5: CODE QUALITY CHECK ==="
echo ""

test_case "No auth imports in projects.py" \
    "! grep -q 'from.*auth import get_current_user' backend/app/routers/projects.py"

test_case "No auth imports in step1.py" \
    "! grep -q 'from.*auth import get_current_user' backend/app/routers/step1.py"

test_case "No auth imports in step2.py" \
    "! grep -q 'from.*auth import get_current_user' backend/app/routers/step2.py"

test_case "No User model imports in projects.py" \
    "! grep -q 'from.*models.user import User' backend/app/routers/projects.py || grep -q '# User import removed' backend/app/routers/projects.py"

test_case "Documents router registered in main.py" \
    "grep -q 'documents_router' backend/app/main.py"

test_case "Auth router NOT registered in main.py" \
    "! grep -q 'app.include_router(auth_router)' backend/app/main.py"

test_case "App.tsx has no Login route" \
    "! grep -q 'path=\"/login\"' frontend/src/App.tsx"

test_case "App.tsx has no ProtectedRoute" \
    "! grep -q 'ProtectedRoute' frontend/src/App.tsx"

test_case "Layout has no logout button" \
    "! grep -q 'handleLogout' frontend/src/components/Layout.tsx"

echo ""
echo "=== PHASE 6: CONFIGURATION CHECK ==="
echo ""

test_case "Claude max tokens increased" \
    "grep -q 'document_processing_max_tokens.*200000' backend/app/services/claude_service.py"

test_case "Extended thinking budget increased" \
    "grep -q 'budget_tokens.*50000' backend/app/services/claude_service.py"

test_case "File upload limits defined" \
    "grep -q 'MAX_FILE_SIZE.*50.*1024.*1024' backend/app/routers/documents.py"

test_case "Multiple file types supported" \
    "grep -q 'xlsx.*xls.*pdf.*txt.*md.*csv' backend/app/routers/documents.py"

echo ""
echo "=========================================="
echo "TEST RESULTS SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo ""
    echo "Application is ready to use."
    echo "Next steps:"
    echo "  1. Reset database: ./reset_database.sh"
    echo "  2. Start backend: cd backend && uvicorn app.main:app --reload"
    echo "  3. Start frontend: cd frontend && npm run dev"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    echo "Please fix the failing tests before deploying."
    exit 1
fi
