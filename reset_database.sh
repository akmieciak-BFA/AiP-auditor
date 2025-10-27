#!/bin/bash

# Script to reset database after removing user authentication
# BFA Audit App v2.0

echo "=========================================="
echo "BFA Audit App - Database Reset Script"
echo "=========================================="
echo ""
echo "⚠️  WARNING: This will DELETE all existing data!"
echo "Press CTRL+C to cancel, or ENTER to continue..."
read

echo ""
echo "🗑️  Removing old database..."
rm -f backend/bfa_audit.db

echo "✅ Old database removed"
echo ""
echo "🔨 Creating new database schema..."

cd backend
python3 << EOF
from app.database import init_db, engine
from app.models.user import User
from app.models.project import Project
from app.models.step1 import Step1Data
from app.models.step2 import Step2Process
from app.models.step3 import Step3Data
from app.models.step4 import Step4Output
from app.models.draft import ProjectDraft

print("Initializing database...")
init_db()
print("✅ Database schema created successfully!")
print("")
print("Database tables:")
print("  - projects (without user_id)")
print("  - step1_data")
print("  - step2_processes")
print("  - step3_data")
print("  - step4_outputs")
print("  - project_drafts")
print("")
print("✅ Database is ready to use!")
EOF

cd ..

echo ""
echo "=========================================="
echo "✅ Database reset complete!"
echo "=========================================="
echo ""
echo "You can now start the application:"
echo "  Backend:  cd backend && uvicorn app.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo ""
