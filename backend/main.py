"""
BFA Audit App - Main Application
================================

FastAPI application with all calculator endpoints
OPTIMIZED VERSION with logging, rate limiting, and request tracing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.calculator_endpoints import router as calculator_router
from .middleware.rate_limiter import RateLimiter
from .middleware.request_tracer import RequestTracerMiddleware
from .utils.logging_config import setup_logging
import os

# Setup structured logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
structured_logging = os.getenv('STRUCTURED_LOGGING', 'true').lower() == 'true'
setup_logging(level=log_level, structured=structured_logging)

# Create FastAPI app
app = FastAPI(
    title="BFA Audit App - Advanced ROI/TCO Calculator",
    description="""
    Comprehensive ROI/TCO Calculator for Business Process Automation
    
    Based on industry-leading methodologies:
    - Emerson Process Management - ROIC Framework
    - Siemens Advanta - IoT ROI Framework
    - Blue Prism - RPA ROI Methodology
    - PwC Strategy& - Digital ROI Framework
    - Harvard Business Review - Time-Driven ABC
    
    7 Calculator Modules:
    1. Financial Impact Calculator (ROIC, NPV, IRR, Payback, ROI%)
    2. Time-Driven Activity-Based Costing (TDABC)
    3. Digital ROI Framework (6 dimensions)
    4. IoT/Automation Specific Metrics
    5. RPA/AI Automation Metrics
    6. Benchmarking & Maturity Assessment
    7. Scenario Planning & Sensitivity Analysis
    
    ✨ NEW FEATURES (Optimized):
    - Structured logging with trace IDs
    - Rate limiting (60 req/min by default)
    - Request tracing for debugging
    - Enhanced input validation
    """,
    version="1.1.0",  # Bumped version for optimization release
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware (order matters!)
# 1. CORS (first to handle preflight)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('ALLOWED_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Request Tracer (add trace IDs)
app.add_middleware(RequestTracerMiddleware)

# 3. Rate Limiter (protect from abuse)
rate_limit = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
app.add_middleware(RateLimiter, requests_per_minute=rate_limit)

# Include routers
app.include_router(calculator_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BFA Audit App - Advanced ROI/TCO Calculator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/calculator/health",
    }


@app.get("/api/info")
async def api_info():
    """API information"""
    return {
        "name": "BFA Audit Calculator API",
        "version": "1.0.0",
        "modules": [
            {
                "name": "Financial Impact Calculator",
                "endpoint": "/api/calculator/financial-impact",
                "description": "ROIC, NPV, IRR, Payback, ROI%",
            },
            {
                "name": "TDABC",
                "endpoint": "/api/calculator/tdabc",
                "description": "Time-Driven Activity-Based Costing",
            },
            {
                "name": "Digital ROI Framework",
                "endpoint": "/api/calculator/digital-roi",
                "description": "6-dimensional Digital ROI assessment",
            },
            {
                "name": "IoT Metrics",
                "endpoint": "/api/calculator/iot-metrics",
                "description": "IoT/Automation specific metrics",
            },
            {
                "name": "RPA Metrics",
                "endpoint": "/api/calculator/rpa-metrics",
                "description": "RPA/AI Automation metrics",
            },
            {
                "name": "Benchmarking",
                "endpoint": "/api/calculator/benchmarking",
                "description": "Industry benchmarking comparison",
            },
            {
                "name": "Maturity Assessment",
                "endpoint": "/api/calculator/maturity-assessment",
                "description": "Automation maturity level (1-5)",
            },
            {
                "name": "Scenario Planning",
                "endpoint": "/api/calculator/scenarios/compare",
                "description": "Compare 3 budget scenarios",
            },
            {
                "name": "Comprehensive Analysis",
                "endpoint": "/api/calculator/comprehensive-analysis",
                "description": "Full multi-module analysis",
            },
        ],
        "methodologies": [
            "Emerson Process Management - ROIC Framework",
            "Siemens Advanta - IoT ROI Framework",
            "Blue Prism - RPA ROI Methodology",
            "PwC Strategy& - Digital ROI Framework",
            "Harvard Business Review - Time-Driven ABC",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
