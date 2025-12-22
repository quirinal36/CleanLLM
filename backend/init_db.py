"""
Database initialization script
데이터베이스 테이블을 생성합니다.

Usage:
    python init_db.py
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import Base, engine, init_db
from app.models.user import User, ParentChildLink

print("=" * 60)
print("EduGuard AI - Database Initialization")
print("=" * 60)

print("\n[1/2] Importing models...")
print(f"✓ User model: {User.__tablename__}")
print(f"✓ ParentChildLink model: {ParentChildLink.__tablename__}")

print("\n[2/2] Creating database tables...")
try:
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

    # List created tables
    print("\nCreated tables:")
    for table_name in Base.metadata.tables:
        print(f"  • {table_name}")

    print("\n" + "=" * 60)
    print("Database initialization complete! ✓")
    print("=" * 60)
    print("\nYou can now start the API server:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    print("\nOr run the test:")
    print("  python test_signup_api.py")
    print("=" * 60)

except Exception as e:
    print(f"✗ Error creating database tables: {e}")
    sys.exit(1)
