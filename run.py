"""
Run script for BFA Audit App
=============================

Simple script to run the FastAPI application
"""

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("BFA Audit App - Advanced ROI/TCO Calculator")
    print("=" * 60)
    print("\n🚀 Starting server...")
    print("\n📖 API Documentation:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print("\n🔍 Health Check: http://localhost:8000/api/calculator/health")
    print("\n" + "=" * 60 + "\n")

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
