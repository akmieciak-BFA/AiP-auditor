# BFA Audit App - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you run the BFA Audit App Calculator in just a few minutes.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 2: Start the Server (30 seconds)

```bash
python run.py
```

You should see:
```
============================================================
BFA Audit App - Advanced ROI/TCO Calculator
============================================================

🚀 Starting server...

📖 API Documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

🔍 Health Check: http://localhost:8000/api/calculator/health

============================================================

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Verify Installation (30 seconds)

Open your browser and visit:
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/calculator/health

You should see the interactive API documentation (Swagger UI) with all 11 endpoints.

## Step 4: Try an Example (2 minutes)

### Option A: Use the Interactive API (Browser)

1. Go to http://localhost:8000/docs
2. Click on **POST /api/calculator/financial-impact**
3. Click "Try it out"
4. Use this example data:

```json
{
  "project_capital": 500000,
  "commissioning_cost": 50000,
  "fixed_assets": 100000,
  "inventory": 20000,
  "operating_cash": 10000,
  "financial_wc": 5000,
  "cost_reductions": {
    "feedstocks_energy": {"baseline": 100000, "reduction_pct": 15},
    "maintenance_scheduled": {"baseline": 50000, "reduction_pct": 20}
  },
  "current_revenue": 1000000,
  "quality_premium_pct": 5,
  "production_increase_pct": 0,
  "capex_breakdown": {
    "hardware": 200000,
    "installation": 100000,
    "software_licenses": 50000,
    "services": 30000,
    "infrastructure": 50000,
    "training": 20000
  },
  "opex_yearly": {
    "maintenance_contracts": 30000,
    "spare_parts": 10000,
    "administration": 15000,
    "training": 5000,
    "upgrades": 10000,
    "cybersecurity": 5000
  },
  "discount_rate": 0.10,
  "tax_rate": 0.21,
  "project_years": 5
}
```

5. Click "Execute"
6. See your results!

### Option B: Use the Example Script (Terminal)

In a new terminal (keep the server running):

```bash
python examples/example_usage.py
```

This will run 5 complete examples demonstrating all calculator modules.

## Step 5: Run Tests (Optional, 1 minute)

```bash
pytest tests/ -v
```

This will run 45+ tests to verify everything works correctly.

## 🎯 What's Next?

### Learn the Modules

The calculator has 7 specialized modules:

1. **Financial Impact** - Core ROI metrics (NPV, IRR, Payback)
2. **TDABC** - Activity-based costing
3. **Digital ROI** - 6-dimensional assessment
4. **IoT Metrics** - IoT-specific calculations
5. **RPA Metrics** - RPA automation metrics
6. **Benchmarking** - Industry comparison
7. **Scenario Planning** - Compare 3 scenarios with risk analysis

### Try Different Scenarios

```bash
# Scenario comparison
curl -X POST "http://localhost:8000/api/calculator/scenarios/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "base_capex": 500000,
    "base_opex": 50000,
    "base_annual_benefits": 200000
  }'
```

### Get Industry Benchmarks

```bash
# Get manufacturing benchmarks
curl "http://localhost:8000/api/calculator/benchmarks/manufacturing"
```

Available industries:
- manufacturing
- financial_services
- healthcare
- logistics
- retail

### Comprehensive Analysis

For a complete analysis using all modules:

```bash
curl -X POST "http://localhost:8000/api/calculator/comprehensive-analysis" \
  -H "Content-Type: application/json" \
  -d @examples/comprehensive_input.json
```

## 📚 Documentation

- **Full README:** [README.md](README.md)
- **User Guide:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Implementation Summary:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## 🔧 Troubleshooting

### Port Already in Use

If port 8000 is already in use, edit `run.py` and change the port:

```python
uvicorn.run(
    "backend.main:app",
    host="0.0.0.0",
    port=8001,  # Change to different port
    reload=True,
)
```

### Import Errors

Make sure you're in the correct directory:

```bash
pwd  # Should show .../workspace
```

### Module Not Found

Reinstall dependencies:

```bash
pip install --upgrade -r requirements.txt
```

## 💡 Tips

1. **Use the Interactive Docs** - The Swagger UI at `/docs` is the easiest way to try the API
2. **Check Examples** - Look at `examples/example_usage.py` for complete working examples
3. **Read the User Guide** - The user guide has detailed explanations of each module
4. **Start Simple** - Begin with Financial Impact, then add other modules as needed

## 🎉 Success!

You're now ready to use the BFA Audit App Calculator!

For questions or issues, refer to the full documentation or check the implementation summary.

---

**Happy Calculating! 🚀**
