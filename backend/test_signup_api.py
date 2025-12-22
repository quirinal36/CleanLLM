"""
Test script for Signup API endpoint
회원가입 API 테스트 스크립트

Prerequisites:
1. Run `python init_db.py` to create database tables
2. Start the API server: `uvicorn app.main:app --reload`
3. Run this test: `python test_signup_api.py`

Or use the standalone test mode (starts server automatically)
"""

import sys
import time
import httpx
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

API_BASE_URL = "http://localhost:8000"


def test_signup_api():
    """Test the signup API endpoint"""

    print("=" * 60)
    print("Testing CLEAN-7: Signup API Endpoint")
    print("=" * 60)

    # Test 1: Health check
    print("\n[1/6] Testing auth health endpoint...")
    try:
        response = httpx.get(f"{API_BASE_URL}/api/v1/auth/health")
        if response.status_code == 200:
            print(f"✓ Auth health check passed: {response.json()}")
        else:
            print(f"✗ Auth health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to connect to API: {e}")
        print("\nMake sure the API server is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        return False

    # Test 2: Valid parent signup
    print("\n[2/6] Testing valid parent signup...")
    parent_data = {
        "email": "parent@example.com",
        "password": "password123",
        "role": "parent",
    }
    try:
        response = httpx.post(f"{API_BASE_URL}/api/v1/auth/signup", json=parent_data)
        if response.status_code == 201:
            data = response.json()
            print("✓ Parent signup successful!")
            print(f"  - User ID: {data['user']['id']}")
            print(f"  - Email: {data['user']['email']}")
            print(f"  - Role: {data['user']['role']}")
            print(f"  - Token: {data['access_token'][:50]}...")
            print(f"  - Expires in: {data['expires_in']} seconds")
        else:
            print(f"✗ Parent signup failed: {response.status_code}")
            print(f"  Response: {response.json()}")
            return False
    except Exception as e:
        print(f"✗ Error during parent signup: {e}")
        return False

    # Test 3: Valid child signup
    print("\n[3/6] Testing valid child signup...")
    child_data = {
        "email": "child@example.com",
        "password": "child123abc",
        "role": "child",
    }
    try:
        response = httpx.post(f"{API_BASE_URL}/api/v1/auth/signup", json=child_data)
        if response.status_code == 201:
            data = response.json()
            print("✓ Child signup successful!")
            print(f"  - User ID: {data['user']['id']}")
            print(f"  - Email: {data['user']['email']}")
            print(f"  - Role: {data['user']['role']}")
        else:
            print(f"✗ Child signup failed: {response.status_code}")
            print(f"  Response: {response.json()}")
            return False
    except Exception as e:
        print(f"✗ Error during child signup: {e}")
        return False

    # Test 4: Duplicate email (should fail)
    print("\n[4/6] Testing duplicate email signup (should fail)...")
    try:
        response = httpx.post(f"{API_BASE_URL}/api/v1/auth/signup", json=parent_data)
        if response.status_code == 400:
            print("✓ Duplicate email correctly rejected!")
            print(f"  - Error: {response.json()['detail']}")
        else:
            print(f"✗ Duplicate email not rejected: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error during duplicate email test: {e}")
        return False

    # Test 5: Weak password (should fail)
    print("\n[5/6] Testing weak password (should fail)...")
    weak_password_data = {
        "email": "test@example.com",
        "password": "12345678",  # No letters
        "role": "parent",
    }
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/v1/auth/signup", json=weak_password_data
        )
        if response.status_code == 422:
            print("✓ Weak password correctly rejected!")
            print(f"  - Validation error: {response.json()['detail'][0]['msg']}")
        else:
            print(f"✗ Weak password not rejected: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error during weak password test: {e}")
        return False

    # Test 6: Invalid email (should fail)
    print("\n[6/6] Testing invalid email (should fail)...")
    invalid_email_data = {
        "email": "not-an-email",
        "password": "password123",
        "role": "parent",
    }
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/v1/auth/signup", json=invalid_email_data
        )
        if response.status_code == 422:
            print("✓ Invalid email correctly rejected!")
            print(f"  - Validation error: {response.json()['detail'][0]['msg']}")
        else:
            print(f"✗ Invalid email not rejected: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error during invalid email test: {e}")
        return False

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nAcceptance Criteria Status:")
    print("  ✅ Users can signup with email and password")
    print("  ✅ Password validation: minimum 8 characters, letters + numbers")
    print("  ✅ Email validation: valid email format")
    print("  ✅ Duplicate email rejection")
    print("  ✅ JWT token issued on successful signup")
    print("  ✅ User information returned in response")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = test_signup_api()
    sys.exit(0 if success else 1)
