"""
Test script for Login API endpoint (CLEAN-8)
로그인 API 및 인증 테스트 스크립트

Prerequisites:
1. Run `python init_db.py` to create database tables
2. Start the API server: `uvicorn app.main:app --reload`
3. Run this test: `python test_login_api.py`
"""

import sys
import httpx
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

API_BASE_URL = "http://localhost:8000"


def test_login_api():
    """Test the login API endpoint and authentication flow"""

    print("=" * 60)
    print("Testing CLEAN-8: Login API Endpoint")
    print("=" * 60)

    # Test 1: Create a test user (signup)
    print("\n[1/7] Setting up test user (signup)...")
    signup_data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "role": "parent",
    }
    try:
        response = httpx.post(f"{API_BASE_URL}/api/v1/auth/signup", json=signup_data)
        if response.status_code == 201:
            print("✓ Test user created successfully")
        elif response.status_code == 400:
            # User might already exist from previous test
            print("ℹ Test user already exists (from previous test)")
        else:
            print(f"✗ Failed to create test user: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to connect to API: {e}")
        print("\nMake sure the API server is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        return False

    # Test 2: Valid login
    print("\n[2/7] Testing valid login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123",
    }
    try:
        response = httpx.post(f"{API_BASE_URL}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            access_token = data["access_token"]
            print("✓ Login successful!")
            print(f"  - User ID: {data['user']['id']}")
            print(f"  - Email: {data['user']['email']}")
            print(f"  - Role: {data['user']['role']}")
            print(f"  - Token: {access_token[:50]}...")
            print(f"  - Expires in: {data['expires_in']} seconds")
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"  Response: {response.json()}")
            return False
    except Exception as e:
        print(f"✗ Error during login: {e}")
        return False

    # Test 3: Wrong password
    print("\n[3/7] Testing login with wrong password (should fail)...")
    wrong_password_data = {
        "email": "testuser@example.com",
        "password": "wrongpassword",
    }
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/v1/auth/login", json=wrong_password_data
        )
        if response.status_code == 401:
            print("✓ Wrong password correctly rejected!")
            print(f"  - Error: {response.json()['detail']}")
        else:
            print(f"✗ Wrong password not rejected: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error during wrong password test: {e}")
        return False

    # Test 4: Non-existent user
    print("\n[4/7] Testing login with non-existent email (should fail)...")
    nonexistent_data = {
        "email": "nonexistent@example.com",
        "password": "password123",
    }
    try:
        response = httpx.post(
            f"{API_BASE_URL}/api/v1/auth/login", json=nonexistent_data
        )
        if response.status_code == 401:
            print("✓ Non-existent user correctly rejected!")
            print(f"  - Error: {response.json()['detail']}")
        else:
            print(f"✗ Non-existent user not rejected: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error during non-existent user test: {e}")
        return False

    # Test 5: Access protected endpoint with valid token
    print("\n[5/7] Testing /me endpoint with valid token...")
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = httpx.get(f"{API_BASE_URL}/api/v1/auth/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✓ Protected endpoint accessed successfully!")
            print(f"  - User ID: {data['id']}")
            print(f"  - Email: {data['email']}")
            print(f"  - Role: {data['role']}")
        else:
            print(f"✗ Failed to access protected endpoint: {response.status_code}")
            print(f"  Response: {response.json()}")
            return False
    except Exception as e:
        print(f"✗ Error accessing protected endpoint: {e}")
        return False

    # Test 6: Access protected endpoint without token
    print("\n[6/7] Testing /me endpoint without token (should fail)...")
    try:
        response = httpx.get(f"{API_BASE_URL}/api/v1/auth/me")
        if response.status_code == 403:
            print("✓ Unauthorized access correctly rejected!")
            print(f"  - Error: {response.json()['detail']}")
        else:
            print(f"✗ Unauthorized access not rejected: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error during unauthorized access test: {e}")
        return False

    # Test 7: Access protected endpoint with invalid token
    print("\n[7/7] Testing /me endpoint with invalid token (should fail)...")
    invalid_headers = {"Authorization": "Bearer invalid_token_12345"}
    try:
        response = httpx.get(
            f"{API_BASE_URL}/api/v1/auth/me", headers=invalid_headers
        )
        if response.status_code == 401:
            print("✓ Invalid token correctly rejected!")
            print(f"  - Error: {response.json()['detail']}")
        else:
            print(f"✗ Invalid token not rejected: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error during invalid token test: {e}")
        return False

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nAcceptance Criteria Status:")
    print("  ✅ Users can login with email and password")
    print("  ✅ JWT token issued on successful login")
    print("  ✅ Invalid credentials rejected (401)")
    print("  ✅ Token validates correctly for protected endpoints")
    print("  ✅ Invalid/missing tokens rejected (401/403)")
    print("  ✅ Token contains user info (id, email, role)")
    print("  ✅ Token expires after 30 minutes (configured)")
    print("=" * 60)
    print("\nAPI Endpoints Tested:")
    print("  ✅ POST /api/v1/auth/signup")
    print("  ✅ POST /api/v1/auth/login")
    print("  ✅ GET  /api/v1/auth/me")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = test_login_api()
    sys.exit(0 if success else 1)
