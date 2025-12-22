"""
Quick validation script to test models and schemas
모델과 스키마의 임포트 및 기본 검증 테스트
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("Testing EduGuard AI Models and Schemas")
print("=" * 60)

# Test 1: Import core modules
print("\n[1/5] Testing core module imports...")
try:
    from app.core.config import settings
    from app.core.database import Base, engine, SessionLocal, get_db

    print("✓ Core modules imported successfully")
    print(f"  - App Name: {settings.APP_NAME}")
    print(f"  - Database URL: {settings.DATABASE_URL[:50]}...")
except Exception as e:
    print(f"✗ Failed to import core modules: {e}")
    sys.exit(1)

# Test 2: Import models
print("\n[2/5] Testing model imports...")
try:
    from app.models.user import User, ParentChildLink

    print("✓ Models imported successfully")
    print(f"  - User table: {User.__tablename__}")
    print(f"  - ParentChildLink table: {ParentChildLink.__tablename__}")
except Exception as e:
    print(f"✗ Failed to import models: {e}")
    sys.exit(1)

# Test 3: Import schemas
print("\n[3/5] Testing schema imports...")
try:
    from app.schemas.user import (
        UserCreate,
        UserLogin,
        UserResponse,
        TokenResponse,
        ParentChildLinkCreate,
    )

    print("✓ Schemas imported successfully")
    print(f"  - UserCreate: {UserCreate.__name__}")
    print(f"  - UserLogin: {UserLogin.__name__}")
    print(f"  - UserResponse: {UserResponse.__name__}")
except Exception as e:
    print(f"✗ Failed to import schemas: {e}")
    sys.exit(1)

# Test 4: Validate UserCreate schema
print("\n[4/5] Testing UserCreate schema validation...")
try:
    # Valid user creation
    valid_user = UserCreate(
        email="test@example.com", password="password123", role="parent"
    )
    print("✓ Valid user created successfully")
    print(f"  - Email: {valid_user.email}")
    print(f"  - Role: {valid_user.role}")

    # Test password validation (should fail - no letter)
    try:
        invalid_user = UserCreate(email="test@example.com", password="12345678", role="child")
        print("✗ Password validation failed to catch weak password")
    except ValueError as e:
        print(f"✓ Password validation working: {str(e)}")

    # Test password length (should fail - too short)
    try:
        invalid_user = UserCreate(email="test@example.com", password="abc123", role="child")
        print("✗ Password length validation failed")
    except ValueError as e:
        print(f"✓ Password length validation working: {str(e)}")

except Exception as e:
    print(f"✗ Schema validation failed: {e}")
    sys.exit(1)

# Test 5: Test database table creation (metadata only, not actual DB)
print("\n[5/5] Testing database metadata...")
try:
    tables = Base.metadata.tables
    print(f"✓ Database metadata created successfully")
    print(f"  - Total tables: {len(tables)}")
    for table_name in tables:
        print(f"    • {table_name}")
except Exception as e:
    print(f"✗ Database metadata test failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print("\nNext steps:")
print("1. Set up PostgreSQL database")
print("2. Update DATABASE_URL in .env file")
print("3. Run 'alembic init alembic' to initialize migrations")
print("4. Create first migration: 'alembic revision --autogenerate -m \"Initial migration\"'")
print("5. Apply migration: 'alembic upgrade head'")
print("=" * 60)
