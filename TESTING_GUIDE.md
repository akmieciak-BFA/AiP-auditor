# Testing Guide - Document Analysis Feature

## Quick Test Checklist

### 1. Backend Setup
```bash
# Verify environment
cd /workspace
cat .env | grep CLAUDE_API_KEY
# Should show: CLAUDE_API_KEY=sk-ant-...

# Clean database (optional)
python cleanup_test_documents.py 1

# Check backend is running
curl http://localhost:8000/health || echo "Backend not running!"
```

### 2. Test Document Upload

#### Prepare Test Files:
Create 3 test documents with business process information:

**test_processes.md:**
```markdown
# Business Processes

## Finance
- Invoice processing: 20 hours/week, 5% error rate
- Payment approvals: 15 hours/week, 2% error rate
- Budget reconciliation: 10 hours/week, 8% error rate

## Operations
- Order fulfillment: 40 hours/week, 3% error rate
- Inventory management: 25 hours/week, 10% error rate

## HR
- Employee onboarding: 12 hours/week, 6% error rate
```

**company_info.txt:**
```
Company: Test Manufacturing Inc.
Industry: Manufacturing
Size: 150 employees
Annual Revenue: 50M PLN
Location: Warsaw, Poland

Systems: SAP ERP, Salesforce CRM, custom production system
Integration: Partial
Digital Maturity: Medium (ERP: 7/10, RPA: 2/10)
```

**budget.xlsx:**
- Create Excel with columns: Process, Current Cost, Expected Savings
- Add 5-10 rows with sample data

#### Upload via API:
```bash
PROJECT_ID=1

curl -X POST "http://localhost:8000/api/projects/${PROJECT_ID}/documents/upload" \
  -F "files=@test_processes.md" \
  -F "files=@company_info.txt" \
  -F "files=@budget.xlsx"
```

**Expected Response:**
```json
{
  "success": true,
  "project_id": 1,
  "processing_result_id": 1,
  "step1_data_id": 1,
  "files_uploaded": 3,
  "analysis_summary": {
    "top_processes": ["Invoice processing", "Order fulfillment", ...],
    "overall_confidence": 0.75,
    "key_findings": [...]
  },
  "digital_maturity": {
    "overall_score": 65,
    ...
  },
  "processes_scoring": [
    {
      "process_name": "Invoice processing",
      "score": 85,
      "tier": 1,
      ...
    }
  ],
  "processing_time_seconds": 95
}
```

### 3. Verify Database

```python
# In Python console or script
from backend.app.database import SessionLocal
from backend.app.models.step1 import Step1Data
from backend.app.models.document import DocumentProcessingResult

db = SessionLocal()

# Check Step1Data
step1 = db.query(Step1Data).filter(Step1Data.project_id == 1).first()
print(f"Step1Data exists: {step1 is not None}")
print(f"Has analysis_results: {step1.analysis_results is not None}")
print(f"TOP processes: {step1.analysis_results.get('top_processes', [])}")

# Check DocumentProcessingResult
result = db.query(DocumentProcessingResult).filter(
    DocumentProcessingResult.project_id == 1
).first()
print(f"Processing result exists: {result is not None}")
print(f"Digital maturity score: {result.extracted_data.get('digital_maturity', {}).get('overall_score')}")
```

### 4. Test Latest Analysis Endpoint

```bash
curl http://localhost:8000/api/projects/1/documents/latest-analysis | jq '.'
```

**Expected:**
```json
{
  "has_analysis": true,
  "step1_data_available": true,
  "processing_result_id": 1,
  "step1_data_id": 1,
  "extracted_data": {
    "digital_maturity": {...},
    "top_processes": [...],
    "processes_scoring": [...],
    ...
  }
}
```

### 5. Test Step1 Analyze with Existing Data

```bash
curl -X POST "http://localhost:8000/api/projects/1/step1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_data": {},
    "questionnaire_answers": {},
    "processes_list": []
  }'
```

**Expected:**
- Status: 200 OK
- Returns existing Step1Data analysis (not 422 error)
- No re-analysis, instant response

### 6. Frontend Testing

#### Start Frontend:
```bash
cd frontend
npm run dev
# Open http://localhost:5173
```

#### Test Flow:
1. **Navigate to project:**
   - Click on project from dashboard
   - Should show Step 1

2. **Choose Upload Method:**
   - Click "Prześlij dokumenty" option
   - Should show upload interface

3. **Upload Files:**
   - Drag & drop or select test files
   - Click "Przetwórz dokumenty"
   - **Wait 90-120 seconds** (important!)
   - Progress bar should show
   - Messages: "Parsowanie dokumentów...", "Ekstrakcja danych...", etc.

4. **Review Results:**
   - Should automatically navigate to review page
   - Check displays:
     - [ ] "Ocena Dojrzałości Cyfrowej" section with overall score
     - [ ] 6 dimension bars (process maturity, digital infrastructure, etc.)
     - [ ] "TOP Procesy do Automatyzacji" list (numbered 1-10)
     - [ ] "Szczegółowy Scoring Procesów" with tier badges
     - [ ] Each process shows: name, score, tier, rationale, metrics
     - [ ] "Kluczowe Ustalenia" bullet points
     - [ ] "Rekomendacje" text section
   
5. **Confirm and Continue:**
   - Click "Zatwierdź i przejdź do Analizy"
   - Should show "Analizowanie..." briefly (1 second)
   - Should advance to Step 2
   - **No Error 422!**

### 7. Re-Analysis Test

```bash
curl -X POST "http://localhost:8000/api/projects/1/documents/reanalyze"
```

**Expected:**
- Re-processes all documents
- Updates Step1Data
- Returns new analysis
- Takes 90-120 seconds

### 8. Validation Tests

#### A. Empty File:
```bash
touch empty.txt
curl -X POST "http://localhost:8000/api/projects/1/documents/upload" \
  -F "files=@empty.txt"
# Expected: 400 Error "File empty.txt is empty"
```

#### B. Invalid File Type:
```bash
echo "test" > test.exe
curl -X POST "http://localhost:8000/api/projects/1/documents/upload" \
  -F "files=@test.exe"
# Expected: 400 Error "Unsupported file type: .exe"
```

#### C. Too Many Files:
```bash
# Create 11 files
for i in {1..11}; do echo "test" > "file$i.txt"; done
curl -X POST "http://localhost:8000/api/projects/1/documents/upload" \
  $(for i in {1..11}; do echo "-F files=@file$i.txt"; done)
# Expected: 400 Error "Too many files"
```

#### D. Document Limit:
```bash
# After uploading 100 files
curl -X POST "http://localhost:8000/api/projects/1/documents/upload" \
  -F "files=@one_more.txt"
# Expected: 400 Error "Project document limit exceeded. Maximum 100"
```

---

## Common Issues & Solutions

### Issue: "Claude API key not configured"
**Solution:**
```bash
# Check .env file
cat .env | grep CLAUDE_API_KEY
# If missing or wrong, update:
echo "CLAUDE_API_KEY=sk-ant-your-key-here" >> .env
# Restart backend
```

### Issue: "Analysis takes too long (>120s)"
**Causes:**
- Large documents (>50 pages PDF)
- Many documents (>10)
- Complex Excel files with many sheets

**Solutions:**
- Split large PDFs
- Upload fewer documents at once
- Simplify Excel files

### Issue: "Error 422 on confirm button"
**Diagnosis:**
```bash
# Check if Step1Data was created
curl http://localhost:8000/api/projects/1/documents/latest-analysis | jq '.step1_data_available'
# Should return: true
```

**If false:**
- Step1Data wasn't created during upload
- Check backend logs for errors
- Verify Claude API worked correctly

### Issue: Frontend shows blank review page
**Diagnosis:**
```bash
# Check API response
curl http://localhost:8000/api/projects/1/documents/latest-analysis
```

**If extracted_data is null:**
- Analysis failed
- Check backend logs
- Re-run /reanalyze endpoint

### Issue: TOP processes list is empty
**Cause:** Claude didn't identify enough processes in documents

**Solution:**
- Provide documents with clearer process descriptions
- Include process names, time consumption, pain points
- Use structured format (tables, bullet lists)

---

## Performance Benchmarks

### Document Processing Times:
- 1 small document (1-2 pages): ~60-90s
- 3 medium documents (5-10 pages): ~90-120s
- 5 large documents (20+ pages): ~150-180s

### API Endpoints:
- POST /upload: 90-180s (depending on documents)
- GET /latest-analysis: <100ms (cached)
- POST /reanalyze: 90-180s (full re-processing)
- POST /step1/analyze (with existing data): <100ms (instant)

---

## Success Criteria

✅ All tests pass
✅ Documents upload successfully
✅ Analysis completes without errors
✅ Step1Data created automatically
✅ Frontend displays all BFA analysis sections
✅ TOP processes visible
✅ Digital maturity scores displayed
✅ Confirm button works without Error 422
✅ Project advances to Step 2
✅ No security vulnerabilities (filename sanitization works)
✅ Error handling works (file cleanup on errors)

---

## Automated Test Script

```bash
#!/bin/bash
# test_document_flow.sh

PROJECT_ID=1
API_URL="http://localhost:8000"

echo "🧪 Testing Document Upload Flow..."

# Test 1: Upload documents
echo "📤 Test 1: Uploading documents..."
response=$(curl -s -X POST "$API_URL/api/projects/$PROJECT_ID/documents/upload" \
  -F "files=@test_processes.md" \
  -F "files=@company_info.txt")

echo "$response" | jq '.'

step1_data_id=$(echo "$response" | jq -r '.step1_data_id')
if [ "$step1_data_id" != "null" ]; then
  echo "✅ Step1Data created: $step1_data_id"
else
  echo "❌ Step1Data NOT created!"
  exit 1
fi

# Test 2: Check latest analysis
echo "🔍 Test 2: Checking latest analysis..."
analysis=$(curl -s "$API_URL/api/projects/$PROJECT_ID/documents/latest-analysis")
has_analysis=$(echo "$analysis" | jq -r '.has_analysis')

if [ "$has_analysis" = "true" ]; then
  echo "✅ Analysis available"
  echo "TOP processes:"
  echo "$analysis" | jq -r '.extracted_data.top_processes[]'
else
  echo "❌ Analysis NOT available!"
  exit 1
fi

# Test 3: Verify Step1 analyze works
echo "🎯 Test 3: Testing Step1 analyze endpoint..."
analyze_response=$(curl -s -X POST "$API_URL/api/projects/$PROJECT_ID/step1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"organization_data":{},"questionnaire_answers":{},"processes_list":[]}')

if echo "$analyze_response" | jq -e '.digital_maturity' > /dev/null 2>&1; then
  echo "✅ Step1 analyze works!"
else
  echo "❌ Step1 analyze failed!"
  echo "$analyze_response"
  exit 1
fi

echo ""
echo "🎉 All tests passed!"
```

---

## Manual Testing Checklist

### Backend:
- [ ] Upload 1 document successfully
- [ ] Upload 3 documents successfully
- [ ] Verify Step1Data created in database
- [ ] Check top_processes in analysis_results
- [ ] Verify digital_maturity scores present
- [ ] Test /latest-analysis endpoint
- [ ] Test /reanalyze endpoint
- [ ] Test /step1/analyze with empty data (should use existing)
- [ ] Test file validation (empty, wrong type, too many)
- [ ] Test filename sanitization
- [ ] Test error cleanup (files deleted on error)

### Frontend:
- [ ] Navigate to project Step 1
- [ ] Choose "Upload Documents" option
- [ ] Upload 3 test files
- [ ] Wait for processing (90-120s)
- [ ] See progress indicators
- [ ] Review page loads correctly
- [ ] Digital maturity section displays
- [ ] TOP processes list shows (numbered)
- [ ] Process scoring details visible
- [ ] Tier badges color-coded correctly
- [ ] Key findings displayed
- [ ] Recommendations displayed
- [ ] Click "Confirm and Continue"
- [ ] Advance to Step 2 successfully
- [ ] No Error 422

### Integration:
- [ ] Full flow works end-to-end
- [ ] Data persists across page refresh
- [ ] Multiple uploads to same project work
- [ ] Re-analysis updates data correctly
- [ ] Cleanup script works

---

## Done! 🚀

All implementations complete. System ready for testing and deployment.
