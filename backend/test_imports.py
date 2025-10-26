#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

import sys
import traceback

def test_imports():
    """Test all critical imports."""
    tests_passed = 0
    tests_failed = 0
    
    print("🧪 Testing Backend Imports...\n")
    
    # Test 1: Config
    try:
        from app.config import get_settings
        settings = get_settings()
        print("✅ Config import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Config import FAILED: {e}")
        tests_failed += 1
    
    # Test 2: Database
    try:
        from app.database import Base, get_db, init_db
        print("✅ Database import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Database import FAILED: {e}")
        tests_failed += 1
    
    # Test 3: Models
    try:
        from app.models import User, Project, Step1Data, Step2Process, Step3Data, Step4Output, ProjectDraft, ActivityLog
        print("✅ Models import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Models import FAILED: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 4: Schemas
    try:
        from app.schemas import User, UserCreate, Project, ProjectCreate, Step1DataInput
        print("✅ Schemas import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Schemas import FAILED: {e}")
        tests_failed += 1
    
    # Test 5: Services
    try:
        from app.services import ClaudeService, GammaService, AnalysisService
        print("✅ Services import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Services import FAILED: {e}")
        tests_failed += 1
    
    # Test 6: Routers
    try:
        from app.routers import auth_router, projects_router, step1_router, step2_router, step3_router, step4_router
        print("✅ Routers import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Routers import FAILED: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 7: Middleware
    try:
        from app.middleware.rate_limit import rate_limiter
        from app.middleware.security import sanitize_string
        print("✅ Middleware import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Middleware import FAILED: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 8: Utils
    try:
        from app.utils import get_password_hash, validate_processes_list
        print("✅ Utils import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Utils import FAILED: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Test 9: Main App
    try:
        from app.main import app
        print("✅ Main app import OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Main app import FAILED: {e}")
        traceback.print_exc()
        tests_failed += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Tests Passed: {tests_passed}/9")
    print(f"Tests Failed: {tests_failed}/9")
    print(f"{'='*50}\n")
    
    if tests_failed == 0:
        print("🎉 All imports successful!")
        return 0
    else:
        print("⚠️  Some imports failed. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(test_imports())
