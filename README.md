# BFA Audit App - Advanced ROI/TCO Calculator

Comprehensive ROI/TCO Calculator for Business Process Automation based on industry-leading methodologies.

## 📋 Table of Contents

- [Overview](#overview)
- [Methodologies](#methodologies)
- [7 Calculator Modules](#7-calculator-modules)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Architecture](#architecture)
- [License](#license)

## 🎯 Overview

The BFA Audit App provides a comprehensive, production-ready calculator system for evaluating ROI/TCO of business process automation projects. It integrates proven methodologies from industry leaders including Emerson, Siemens, Blue Prism, PwC Strategy&, and Harvard Business Review.

### Key Features

- ✅ **7 Integrated Calculator Modules**
- ✅ **Industry Benchmarking** (5 industries)
- ✅ **Scenario Planning** (3 budget scenarios)
- ✅ **Sensitivity Analysis & Monte Carlo Simulation**
- ✅ **Maturity Assessment** (5 levels)
- ✅ **RESTful API** with FastAPI
- ✅ **Comprehensive Testing** (Unit + Integration)
- ✅ **Auto-generated API Documentation** (Swagger/ReDoc)

## 📚 Methodologies

The calculator is based on the following industry-leading methodologies:

1. **Emerson Process Management - ROIC Framework**
   - Return on Invested Capital (ROIC)
   - Life Cycle Cost Analysis
   - Capital vs Expense classification

2. **Siemens Advanta - IoT ROI Framework**
   - Business Impact Modeling
   - Connectivity value calculation
   - Operational efficiency gains

3. **Blue Prism - RPA ROI Methodology**
   - Process automation metrics
   - FTE savings calculation
   - Bot utilization tracking

4. **PwC Strategy& - Digital ROI Framework**
   - 6 Strategic Focus Areas
   - Quantitative + Qualitative metrics
   - Digital maturity assessment

5. **Harvard Business Review - Time-Driven ABC**
   - Capacity Cost Rate calculation
   - Unit Time estimation
   - Capacity Utilization Analysis

## 🧮 7 Calculator Modules

### Module 1: Financial Impact Calculator
**Endpoint:** `/api/calculator/financial-impact`

Calculates core financial metrics:
- ROIC (Return on Invested Capital)
- NPV (Net Present Value)
- IRR (Internal Rate of Return)
- Payback Period
- ROI %
- Benefit-Cost Ratio

### Module 2: Time-Driven Activity-Based Costing (TDABC)
**Endpoint:** `/api/calculator/tdabc`

Calculates:
- Capacity Cost Rate
- Cost-Driver Rates
- Capacity Utilization Analysis
- Activity Cost Breakdown

### Module 3: Digital ROI Framework
**Endpoint:** `/api/calculator/digital-roi`

6-dimensional assessment:
1. Customers
2. Employees
3. Operations
4. Safety & Soundness
5. Infrastructure
6. Disruption & Innovation

### Module 4: IoT/Automation Metrics
**Endpoint:** `/api/calculator/iot-metrics`

Calculates:
- Connectivity Value
- OEE (Overall Equipment Effectiveness) Improvement
- Predictive Maintenance Value
- Energy Optimization Value
- Quality Improvement Value

### Module 5: RPA/AI Automation Metrics
**Endpoint:** `/api/calculator/rpa-metrics`

Calculates:
- FTE (Full-Time Equivalent) Savings
- Accuracy Improvement Value
- Velocity Improvement
- Bot Utilization
- Process Cycle Time Reduction

### Module 6: Benchmarking & Maturity Assessment
**Endpoints:** 
- `/api/calculator/benchmarking`
- `/api/calculator/maturity-assessment`

Features:
- Industry benchmarking (5 industries)
- Automation maturity levels (1-5)
- Best practices comparison
- Roadmap to next level

### Module 7: Scenario Planning & Sensitivity Analysis
**Endpoint:** `/api/calculator/scenarios/compare`

Features:
- 3 budget scenarios comparison
- Sensitivity analysis (Tornado diagram)
- Monte Carlo simulation
- Risk assessment

## 🚀 Installation

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, for production)
- Node.js 16+ (for frontend, if implemented)

### Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd workspace

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database (if using PostgreSQL)
psql -U postgres -f backend/database/init_db.sql

# Run the application
python -m backend.main
```

The API will be available at `http://localhost:8000`

## 🎯 Quick Start

### Example 1: Financial Impact Calculation

```python
import requests

url = "http://localhost:8000/api/calculator/financial-impact"

data = {
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
    "production_increase_pct": 10,
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

response = requests.post(url, json=data)
results = response.json()

print(f"NPV: ${results['results']['financial_metrics']['npv']:,.2f}")
print(f"ROI: {results['results']['financial_metrics']['roi_pct']}%")
print(f"Payback: {results['results']['financial_metrics']['payback_period_years']} years")
```

### Example 2: Scenario Comparison

```python
url = "http://localhost:8000/api/calculator/scenarios/compare"

data = {
    "base_capex": 500000,
    "base_opex": 50000,
    "base_annual_benefits": 200000,
    "project_years": 5,
    "discount_rate": 0.10
}

response = requests.post(url, json=data)
scenarios = response.json()

# Get recommended scenario
recommendation = scenarios['results']['comparison']['recommendation']
print(f"Recommended: {recommendation['recommended_scenario']}")
print(f"Reason: {recommendation['reason']}")
```

### Example 3: Comprehensive Analysis

```python
url = "http://localhost:8000/api/calculator/comprehensive-analysis"

data = {
    "project_name": "Manufacturing Automation Project",
    "industry": "manufacturing",
    "financial_impact": {
        # ... (same as Example 1)
    },
    "include_scenario_planning": True,
    "maturity_assessment": {
        "assessment_scores": {
            "strategy_governance": 75,
            "technology_infrastructure": 60,
            "process_operations": 70,
            "people_culture": 55,
            "measurement_optimization": 65
        }
    }
}

response = requests.post(url, json=data)
analysis = response.json()

print("Executive Summary:")
print(f"  NPV: ${analysis['executive_summary']['npv']:,.2f}")
print(f"  ROI: {analysis['executive_summary']['roi_pct']}%")
print(f"  Maturity Level: {analysis['executive_summary']['maturity_level']}")
print(f"\nRecommendations:")
for rec in analysis['recommendations']:
    print(f"  - {rec}")
```

## 📖 API Documentation

### Interactive Documentation

Once the application is running, visit:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/calculator/financial-impact` | POST | Calculate financial metrics |
| `/api/calculator/tdabc` | POST | Calculate TDABC metrics |
| `/api/calculator/digital-roi` | POST | Calculate Digital ROI |
| `/api/calculator/iot-metrics` | POST | Calculate IoT metrics |
| `/api/calculator/rpa-metrics` | POST | Calculate RPA metrics |
| `/api/calculator/benchmarking` | POST | Industry benchmarking |
| `/api/calculator/benchmarks/{industry}` | GET | Get industry benchmarks |
| `/api/calculator/maturity-assessment` | POST | Maturity assessment |
| `/api/calculator/scenarios/compare` | POST | Compare scenarios |
| `/api/calculator/comprehensive-analysis` | POST | Full analysis |
| `/api/calculator/health` | GET | Health check |

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_financial_impact.py -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

### Test Coverage

Current test coverage includes:
- ✅ Financial Impact Calculator
- ✅ TDABC Calculator
- ✅ Scenario Planning
- ✅ All financial formulas
- ✅ API endpoints (integration tests)

### Example Test Run

```bash
$ pytest tests/test_financial_impact.py -v

tests/test_financial_impact.py::TestCapitalAnalyzer::test_calculate_fixed_capital PASSED
tests/test_financial_impact.py::TestFinancialMetricsCalculator::test_calculate_roic PASSED
tests/test_financial_impact.py::TestFinancialMetricsCalculator::test_calculate_npv_positive PASSED
...
========== 25 passed in 0.5s ==========
```

## 🏗️ Architecture

### Backend Structure

```
backend/
├── calculators/           # Calculator modules (7 modules)
│   ├── __init__.py
│   ├── financial_impact.py
│   ├── tdabc.py
│   ├── digital_roi.py
│   ├── iot_metrics.py
│   ├── rpa_metrics.py
│   ├── benchmarking.py
│   └── scenario_planning.py
├── models/               # Data models
│   ├── calculation_models.py  # Pydantic models
│   └── database_models.py     # SQLAlchemy models
├── services/            # Business logic
│   └── calculator_service.py  # Orchestrator
├── api/                 # API endpoints
│   └── calculator_endpoints.py
├── database/           # Database setup
│   └── init_db.sql
└── main.py            # FastAPI application
```

### Technology Stack

**Backend:**
- FastAPI (Web framework)
- Pydantic (Data validation)
- SQLAlchemy (ORM)
- NumPy/SciPy (Scientific computing)
- Pytest (Testing)

**Database:**
- PostgreSQL (Production)
- SQLite (Development)

**Frontend (Coming Soon):**
- React/TypeScript
- Plotly.js (Visualizations)
- TailwindCSS (Styling)

## 📊 Database Schema

### Main Tables

- `projects` - Project information
- `calculation_results` - Calculation results storage
- `industry_benchmarks` - Industry benchmark data
- `maturity_assessments` - Maturity assessment results
- `scenario_analyses` - Scenario analysis results
- `audit_step1_data` - Step 1 audit data
- `audit_step2_data` - Step 2 audit data

## 🔒 Security Considerations

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- CORS configuration for production
- Rate limiting (recommended for production)
- Authentication/Authorization (to be implemented)

## 🚢 Deployment

### Development

```bash
uvicorn backend.main:app --reload
```

### Production

```bash
# Using Gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker (Dockerfile to be added)
docker build -t bfa-audit-app .
docker run -p 8000:8000 bfa-audit-app
```

## 📝 User Guide

### Module-by-Module Guide

#### 1. Financial Impact Calculator

**When to use:** Every project - this is the core financial analysis.

**Key inputs:**
- Capital requirements (project capital, fixed assets, working capital)
- Cost reductions by category (8 categories)
- Revenue enhancements (quality premium, production increase)
- Life cycle costs (CapEx breakdown, annual OpEx)
- Financial parameters (discount rate, tax rate, project years)

**Key outputs:**
- ROIC %
- NPV
- IRR %
- Payback Period
- ROI %

**Interpretation:**
- NPV > 0: Project is financially viable
- Payback < 3 years: Quick return on investment
- ROIC > 15%: Strong return on invested capital

#### 2. Scenario Planning

**When to use:** To compare different implementation approaches.

**3 Scenarios:**
1. **Budget Conscious** - 60% CapEx, 70% OpEx, 75% benefits
2. **Strategic Implementation** - 100% baseline (recommended for most)
3. **Enterprise Transformation** - 150% CapEx, 130% benefits

**Interpretation:**
- Compare NPV across scenarios
- Consider risk level vs. return
- Follow the recommendation engine

#### 3-6. Specialized Metrics

Use based on project type:
- **TDABC**: For understanding current process costs
- **Digital ROI**: For holistic digital transformation
- **IoT Metrics**: For industrial automation/IoT projects
- **RPA Metrics**: For RPA/automation projects

#### 7. Benchmarking

**Always use** to understand industry context.

**Available industries:**
- Manufacturing
- Financial Services
- Healthcare
- Logistics
- Retail

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

[To be determined]

## 📧 Contact

For questions or support, please contact [your-email@example.com]

## 🎓 References

1. Emerson Process Management - ROIC Methodology White Paper
2. Siemens Advanta - IoT ROI Framework
3. Blue Prism - RPA ROI Calculator Methodology
4. PwC Strategy& - Digital ROI Framework
5. Harvard Business Review - Time-Driven Activity-Based Costing

---

**Built with ❤️ for the BFA Audit App**
