# BFA Audit App - User Guide

## Introduction

This guide will help you use the BFA Audit App Calculator effectively to evaluate the ROI/TCO of your automation projects.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Calculator Modules Overview](#calculator-modules-overview)
3. [Step-by-Step Workflow](#step-by-step-workflow)
4. [Interpreting Results](#interpreting-results)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

Before using the calculator, gather the following information:

**Financial Data:**
- Project budget (CapEx)
- Annual operating costs (OpEx)
- Current cost baseline
- Revenue figures

**Operational Data:**
- Current process metrics
- Performance targets
- Resource utilization

**Strategic Data:**
- Industry sector
- Automation maturity level
- Digital transformation goals

## Calculator Modules Overview

### Module 1: Financial Impact Calculator (Required)

**Purpose:** Calculate core financial metrics for any automation project.

**When to use:** Always - this is the foundation of your analysis.

**Key Metrics:**
- ROIC (Return on Invested Capital)
- NPV (Net Present Value)
- IRR (Internal Rate of Return)
- Payback Period
- ROI %

**Input Categories:**

1. **Capital Requirements**
   - Project Capital: Initial investment
   - Commissioning Costs: Setup and installation
   - Fixed Assets: Hardware, equipment
   - Working Capital: Inventory, cash, financial WC

2. **Cost Reductions** (8 categories)
   - Feedstocks & Energy
   - Scheduled Maintenance
   - Unscheduled Maintenance
   - Shutdown Maintenance
   - Off-Spec Material
   - Demurrage
   - Staffing
   - Abnormal Events

3. **Revenue Enhancements**
   - Quality Premium (%)
   - Production Increase (%)

4. **Life Cycle Costs**
   - CapEx Breakdown: Hardware, installation, infrastructure, software, services, training
   - OpEx Yearly: Maintenance, spare parts, administration, training, upgrades, cybersecurity

5. **Financial Parameters**
   - Discount Rate (typically 10%)
   - Tax Rate (typically 21%)
   - Project Years (typically 5)

**Example Input:**

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
    "maintenance_scheduled": {"baseline": 50000, "reduction_pct": 20},
    "staffing": {"baseline": 80000, "reduction_pct": 10}
  },
  "current_revenue": 1000000,
  "quality_premium_pct": 5,
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

### Module 2: TDABC (Optional but Recommended)

**Purpose:** Understand current process costs using Time-Driven Activity-Based Costing.

**When to use:** 
- To understand baseline costs accurately
- To identify capacity constraints
- To optimize resource utilization

**Key Concepts:**

1. **Capacity Cost Rate** = Total Cost / Practical Capacity
   - People: 80% of theoretical capacity
   - Machines: 85% of theoretical capacity

2. **Cost-Driver Rate** = Unit Time × Capacity Cost Rate

**Interpretation:**
- **Utilization < 70%**: Overcapacity - consider cost reduction
- **Utilization 70-90%**: Healthy - optimal range
- **Utilization > 90%**: Bottleneck - investment needed

### Module 3: Digital ROI Framework (Optional)

**Purpose:** Holistic assessment across 6 strategic dimensions.

**When to use:** For comprehensive digital transformation initiatives.

**6 Dimensions:**

1. **Customers** (20% weight)
   - NPS Score
   - CSAT Score
   - Response Time
   - First Contact Resolution

2. **Employees** (15% weight)
   - Engagement Score
   - Employee NPS
   - Turnover Rate
   - Digital Adoption Rate

3. **Operations** (25% weight)
   - Throughput
   - Inventory Efficiency
   - Cycle Time
   - Operational Efficiency Ratio

4. **Safety & Soundness** (15% weight)
   - Threats Detected
   - Privacy Breaches
   - Fraud Losses
   - Compliance Rate

5. **Infrastructure** (15% weight)
   - System Uptime
   - Issue Resolution Time
   - Infrastructure Cost Efficiency
   - Tech Debt Reduction

6. **Disruption & Innovation** (10% weight)
   - Budget % in Disruptive Tech
   - Ideas to Concept Rate
   - Innovation Velocity
   - Time to Market

**Interpretation:**
- Overall Score ≥ 80: Excellent
- Overall Score 65-79: Good
- Overall Score 50-64: Fair
- Overall Score < 50: Needs Improvement

### Module 4: IoT/Automation Metrics (Optional)

**Purpose:** Specialized metrics for IoT and industrial automation projects.

**When to use:** For manufacturing, industrial automation, or IoT initiatives.

**Key Metrics:**

1. **Connectivity Value**
   - Number of devices × data points × value per point

2. **OEE Improvement**
   - OEE = Availability × Performance × Quality
   - Target: World-class OEE > 85%

3. **Predictive Maintenance**
   - Prevented downtime hours × cost per hour

4. **Energy Optimization**
   - Current energy cost × reduction %

5. **Quality Improvement**
   - Defects prevented × cost per defect

### Module 5: RPA/AI Metrics (Optional)

**Purpose:** Specialized metrics for RPA and AI automation projects.

**When to use:** For RPA, chatbot, or AI automation initiatives.

**Key Metrics:**

1. **FTE Savings**
   - Hours saved / 2080 hours per year = FTE saved
   - Include 30% overhead multiplier

2. **Accuracy Improvement**
   - Errors prevented × cost per error

3. **Velocity Improvement**
   - Additional transactions × revenue per transaction

4. **Bot Utilization**
   - Target: 70-90% utilization
   - < 50%: Underutilized
   - > 90%: At capacity

5. **Cycle Time Reduction**
   - Time saved per transaction × volume × cost per minute

### Module 6: Benchmarking (Recommended)

**Purpose:** Compare your project to industry averages.

**When to use:** Always - provides critical context.

**Available Industries:**
- Manufacturing
- Financial Services
- Healthcare
- Logistics
- Retail

**Key Benchmarks:**
- Average ROI
- Average Payback Period
- Automation Adoption Rate
- Typical CapEx/OpEx Ranges

**Maturity Levels:**

1. **Ad-Hoc (0-20 points)**
   - Limited automation
   - No formal strategy
   - Next: Develop strategy, identify quick wins

2. **Task Automation (21-40 points)**
   - Individual task automation
   - Isolated solutions
   - Next: Standardize, integrate, establish CoE

3. **Process Automation (41-60 points)**
   - End-to-end processes
   - Formal governance
   - Next: Implement AI/ML, expand scope

4. **Intelligent Automation (61-80 points)**
   - AI/ML integration
   - Predictive analytics
   - Next: Move toward autonomous operations

5. **Autonomous Operations (81-100 points)**
   - Self-optimizing systems
   - Ecosystem orchestration
   - Next: Maintain excellence, explore emerging tech

### Module 7: Scenario Planning (Highly Recommended)

**Purpose:** Compare different implementation approaches and assess risk.

**When to use:** Always - helps with budgeting and risk management.

**3 Scenarios:**

1. **Budget Conscious**
   - CapEx: 60% of base
   - OpEx: 70% of base
   - Benefits: 75% of base
   - Implementation: 12 months
   - Risk: Medium
   - **Use when:** Budget constrained, need proven ROI first

2. **Strategic Implementation**
   - CapEx: 100% of base
   - OpEx: 100% of base
   - Benefits: 100% of base
   - Implementation: 8 months
   - Risk: Low
   - **Use when:** Balanced approach, recommended for most projects

3. **Enterprise Transformation**
   - CapEx: 150% of base
   - OpEx: 120% of base
   - Benefits: 130% of base
   - Implementation: 6 months
   - Risk: Very Low
   - **Use when:** Strategic priority, maximum benefits needed

**Recommendation Engine:**

The system automatically recommends a scenario based on:
- Highest NPV
- Acceptable payback period (< 3 years preferred)
- Risk-adjusted return

## Step-by-Step Workflow

### Workflow 1: Quick Financial Analysis

**Goal:** Get core financial metrics quickly.

**Steps:**
1. Use `/api/calculator/financial-impact` endpoint
2. Provide:
   - Capital requirements
   - Cost reductions (at least 2-3 categories)
   - Life cycle costs (CapEx and OpEx)
   - Financial parameters
3. Review results:
   - NPV > 0? ✅ Proceed
   - Payback < 3 years? ✅ Quick return
   - ROI > 20%? ✅ Strong performance

**Time:** 15-20 minutes

### Workflow 2: Scenario Comparison

**Goal:** Compare different budget approaches.

**Steps:**
1. Complete Financial Analysis (Workflow 1)
2. Use `/api/calculator/scenarios/compare` with:
   - Base CapEx from Workflow 1
   - Base OpEx from Workflow 1
   - Base annual benefits from Workflow 1
3. Review all 3 scenarios
4. Follow recommendation or choose based on your constraints

**Time:** 5 additional minutes

### Workflow 3: Comprehensive Analysis

**Goal:** Full analysis with all modules.

**Steps:**
1. Prepare all inputs for modules you want to use
2. Use `/api/calculator/comprehensive-analysis` endpoint
3. Review:
   - Executive Summary
   - Each module's results
   - Recommendations list
4. Generate presentation (Step 4 of audit)

**Time:** 30-45 minutes

## Interpreting Results

### Financial Metrics Interpretation

**NPV (Net Present Value)**
- NPV > 0: Project creates value ✅
- NPV < 0: Project destroys value ❌
- Higher NPV is better

**ROI %**
- ROI > 30%: Excellent
- ROI 20-30%: Good
- ROI 10-20%: Fair
- ROI < 10%: Poor

**Payback Period**
- < 1 year: Excellent
- 1-2 years: Very Good
- 2-3 years: Good
- 3-5 years: Acceptable
- > 5 years: Questionable

**IRR (Internal Rate of Return)**
- IRR > Discount Rate: Accept project
- IRR = Discount Rate: Breakeven
- IRR < Discount Rate: Reject project
- Target: IRR > 20%

**ROIC (Return on Invested Capital)**
- ROIC > 15%: Excellent
- ROIC 10-15%: Good
- ROIC 5-10%: Fair
- ROIC < 5%: Poor

### Scenario Comparison Interpretation

**Example Output:**
```
Budget Conscious: NPV = $500K, Payback = 2.5 years, Risk = Medium
Strategic: NPV = $750K, Payback = 2.0 years, Risk = Low
Enterprise: NPV = $1M, Payback = 1.8 years, Risk = Very Low
```

**Decision Framework:**
1. If budget is constrained → Budget Conscious
2. If seeking balance → Strategic (most common)
3. If strategic priority → Enterprise

### Benchmarking Interpretation

**ROI Comparison:**
- Project ROI > Industry Avg: Above average performance ✅
- Project ROI ≈ Industry Avg: On par
- Project ROI < Industry Avg: Below average ⚠️

**Payback Comparison:**
- Project Payback < Industry Avg: Faster return ✅
- Project Payback ≈ Industry Avg: On par
- Project Payback > Industry Avg: Slower return ⚠️

## Best Practices

### 1. Data Quality

**Critical:**
- Use actual data, not estimates when possible
- Validate cost baselines with finance team
- Cross-check revenue figures
- Document all assumptions

### 2. Conservative Estimates

**Recommendations:**
- Use conservative (lower) benefit estimates
- Use realistic (higher) cost estimates
- This provides a safety margin

### 3. Sensitivity Analysis

**Always test:**
- What if benefits are 20% lower?
- What if costs are 20% higher?
- What if implementation takes longer?

### 4. Stakeholder Alignment

**Before finalizing:**
- Review assumptions with stakeholders
- Validate cost baselines with finance
- Confirm benefits with operations
- Get IT to validate technical costs

### 5. Industry Context

**Always:**
- Compare to industry benchmarks
- Understand your maturity level
- Consider best practices for your industry

## Troubleshooting

### Common Issues

**Issue: NPV is negative**
- Check if benefits are realistic
- Verify cost estimates aren't inflated
- Consider longer project timeline
- Review discount rate (may be too high)

**Issue: Payback period too long**
- Look for quick wins to accelerate benefits
- Consider phased implementation
- Review if benefits can be realized earlier

**Issue: Can't decide between scenarios**
- Use recommendation engine
- Consider risk tolerance
- Consult with stakeholders
- Run sensitivity analysis

**Issue: Results don't match expectations**
- Verify all inputs
- Check unit consistency ($/year vs $/month)
- Validate formulas with test data
- Review assumptions

### Getting Help

- API Documentation: `/docs`
- Health Check: `/api/calculator/health`
- Contact: [support-email]

## Appendix: Formula Reference

### NPV Formula
```
NPV = Σ(Cash Flow / (1 + r)^t) - Initial Investment
```

### ROIC Formula
```
ROIC = After-Tax Operating Income / Invested Capital × 100
```

### Payback Period Formula
```
Payback = Initial Investment / Annual Cash Flow
```

### Capacity Cost Rate
```
CCR = Total Cost / Practical Capacity
```

### OEE Formula
```
OEE = Availability × Performance × Quality
```

---

**Happy Calculating! 🚀**
