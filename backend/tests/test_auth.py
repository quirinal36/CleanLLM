"""
Authentication API Unit Tests (CLEAN-10)
회원가입, 로그인, 부모-자녀 연동 API 단위 테스트

테스트 항목:
- [x] 회원가입 성공 테스트
- [x] 중복 이메일 회원가입 실패 테스트
- [x] 약한 비밀번호 회원가입 실패 테스트
- [x] 로그인 성공 테스트
- [x] 잘못된 비밀번호 로그인 실패 테스트
- [x] 부모-자녀 연동 성공 테스트
- [x] 최대 3개 제한 테스트
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User, ParentChildLink


class TestSignup:
    """회원가입 API 테스트"""

    def test_signup_success_parent(self, client: TestClient):
        """
        회원가입 성공 테스트 - 부모 계정
        Valid parent signup should return 201 with token and user info.
        """
        # Given
        signup_data = {
            "email": "newparent@test.com",
            "password": "password123",
            "role": "parent",
        }

        # When
        response = client.post("/api/v1/auth/signup", json=signup_data)

        # Then
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "newparent@test.com"
        assert data["user"]["role"] == "parent"
        assert "id" in data["user"]
        assert "created_at" in data["user"]
        assert "updated_at" in data["user"]

    def test_signup_success_child(self, client: TestClient):
        """
        회원가입 성공 테스트 - 자녀 계정
        Valid child signup should return 201 with token and user info.
        """
        # Given
        signup_data = {
            "email": "newchild@test.com",
            "password": "child123abc",
            "role": "child",
        }

        # When
        response = client.post("/api/v1/auth/signup", json=signup_data)

        # Then
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "newchild@test.com"
        assert data["user"]["role"] == "child"

    def test_signup_duplicate_email_failure(
        self, client: TestClient, parent_user: User
    ):
        """
        중복 이메일 회원가입 실패 테스트
        Signup with existing email should return 400.
        """
        # Given: parent_user already exists with email "parent@test.com"
        signup_data = {
            "email": "parent@test.com",
            "password": "anotherpass123",
            "role": "parent",
        }

        # When
        response = client.post("/api/v1/auth/signup", json=signup_data)

        # Then
        assert response.status_code == 400
        data = response.json()
        assert "already registered" in data["detail"].lower()

    def test_signup_weak_password_no_letters(self, client: TestClient):
        """
        약한 비밀번호 회원가입 실패 테스트 - 문자 없음
        Password without letters should be rejected.
        """
        # Given
        signup_data = {
            "email": "weakpass@test.com",
            "password": "12345678",  # No letters
            "role": "parent",
        }

        # When
        response = client.post("/api/v1/auth/signup", json=signup_data)

        # Then
        assert response.status_code == 422
        data = response.json()
        assert any(
            "letter" in str(err).lower()
            for err in data["detail"]
        )

    def test_signup_weak_password_no_numbers(self, client: TestClient):
        """
        약한 비밀번호 회원가입 실패 테스트 - 숫자 없음
        Password without numbers should be rejected.
        """
        # Given
        signup_data = {
            "email": "weakpass@test.com",
            "password": "abcdefgh",  # No numbers
            "role": "parent",
        }

        # When
        response = client.post("/api/v1/auth/signup", json=signup_data)

        # Then
        assert response.status_code == 422
        data = response.json()
        assert any(
            "number" in str(err).lower()
            for err in data["detail"]
        )

    def test_signup_weak_password_too_short(self, client: TestClient):
        """
        약한 비밀번호 회원가입 실패 테스트 - 8자 미만
        Password shorter than 8 characters should be rejected.
        """
        # Given
        signup_data = {
            "email": "shortpass@test.com",
            "password": "pass1",  # Too short
            "role": "parent",
        }

        # When
        response = client.post("/api/v1/auth/signup", json=signup_data)

        # Then
        assert response.status_code == 422


class TestLogin:
    """로그인 API 테스트"""

    def test_login_success(self, client: TestClient, parent_user: User):
        """
        로그인 성공 테스트
        Valid login should return 200 with token and user info.
        """
        # Given
        login_data = {
            "email": "parent@test.com",
            "password": "password123",
        }

        # When
        response = client.post("/api/v1/auth/login", json=login_data)

        # Then
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert data["user"]["email"] == "parent@test.com"
        assert data["user"]["role"] == "parent"
        assert data["user"]["id"] == parent_user.id

    def test_login_wrong_password_failure(
        self, client: TestClient, parent_user: User
    ):
        """
        잘못된 비밀번호 로그인 실패 테스트
        Login with wrong password should return 401.
        """
        # Given
        login_data = {
            "email": "parent@test.com",
            "password": "wrongpassword",
        }

        # When
        response = client.post("/api/v1/auth/login", json=login_data)

        # Then
        assert response.status_code == 401
        data = response.json()
        assert "incorrect" in data["detail"].lower()

    def test_login_nonexistent_user_failure(self, client: TestClient):
        """
        존재하지 않는 사용자 로그인 실패 테스트
        Login with non-existent email should return 401.
        """
        # Given
        login_data = {
            "email": "nonexistent@test.com",
            "password": "password123",
        }

        # When
        response = client.post("/api/v1/auth/login", json=login_data)

        # Then
        assert response.status_code == 401
        data = response.json()
        assert "incorrect" in data["detail"].lower()

    def test_login_returns_valid_token(
        self, client: TestClient, parent_user: User
    ):
        """
        로그인 후 토큰 유효성 테스트
        Token from login should be valid for protected endpoints.
        """
        # Given
        login_data = {
            "email": "parent@test.com",
            "password": "password123",
        }

        # When
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["access_token"]

        # Then: Use token to access protected endpoint
        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "parent@test.com"


class TestParentChildLink:
    """부모-자녀 연동 API 테스트"""

    def test_link_child_success(
        self,
        client: TestClient,
        parent_user: User,
        child_user: User,
        auth_headers: dict,
    ):
        """
        부모-자녀 연동 성공 테스트
        Parent should be able to link a child account.
        """
        # Given
        link_data = {"child_id": child_user.id}

        # When
        response = client.post(
            "/api/v1/auth/link-child",
            json=link_data,
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["parent_id"] == parent_user.id
        assert data["child_id"] == child_user.id
        assert "linked_at" in data
        assert "id" in data

    def test_link_child_max_limit(
        self,
        client: TestClient,
        db_session: Session,
        parent_user: User,
        multiple_children: list[User],
        auth_headers: dict,
    ):
        """
        최대 3개 제한 테스트
        Parent should not be able to link more than 3 children.
        """
        # Given: Link first 3 children
        for i in range(3):
            link = ParentChildLink(
                parent_id=parent_user.id,
                child_id=multiple_children[i].id,
            )
            db_session.add(link)
        db_session.commit()

        # When: Try to link 4th child
        link_data = {"child_id": multiple_children[3].id}
        response = client.post(
            "/api/v1/auth/link-child",
            json=link_data,
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 400
        data = response.json()
        assert "maximum" in data["detail"].lower() or "3" in data["detail"]

    def test_link_child_duplicate_failure(
        self,
        client: TestClient,
        db_session: Session,
        parent_user: User,
        child_user: User,
        auth_headers: dict,
    ):
        """
        중복 연동 실패 테스트
        Parent should not be able to link the same child twice.
        """
        # Given: Child already linked
        link = ParentChildLink(
            parent_id=parent_user.id,
            child_id=child_user.id,
        )
        db_session.add(link)
        db_session.commit()

        # When
        link_data = {"child_id": child_user.id}
        response = client.post(
            "/api/v1/auth/link-child",
            json=link_data,
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 400
        data = response.json()
        assert "already linked" in data["detail"].lower()

    def test_link_child_nonexistent_failure(
        self,
        client: TestClient,
        parent_user: User,
        auth_headers: dict,
    ):
        """
        존재하지 않는 자녀 연동 실패 테스트
        Linking non-existent child should fail.
        """
        # Given
        link_data = {"child_id": 99999}

        # When
        response = client.post(
            "/api/v1/auth/link-child",
            json=link_data,
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_link_child_self_failure(
        self,
        client: TestClient,
        parent_user: User,
        auth_headers: dict,
    ):
        """
        자기 자신 연동 실패 테스트
        Parent should not be able to link themselves.
        """
        # Given
        link_data = {"child_id": parent_user.id}

        # When
        response = client.post(
            "/api/v1/auth/link-child",
            json=link_data,
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 400
        data = response.json()
        assert "yourself" in data["detail"].lower()

    def test_link_child_by_child_user_failure(
        self,
        client: TestClient,
        child_user: User,
        multiple_children: list[User],
        child_auth_headers: dict,
    ):
        """
        자녀 사용자가 연동 시도 시 실패 테스트
        Child user should not be able to link other children.
        """
        # Given
        link_data = {"child_id": multiple_children[0].id}

        # When
        response = client.post(
            "/api/v1/auth/link-child",
            json=link_data,
            headers=child_auth_headers,
        )

        # Then
        assert response.status_code == 403
        data = response.json()
        assert "parent" in data["detail"].lower()

    def test_link_parent_account_as_child_failure(
        self,
        client: TestClient,
        db_session: Session,
        parent_user: User,
        auth_headers: dict,
    ):
        """
        부모 계정을 자녀로 연동 시도 시 실패 테스트
        Linking a parent account as child should fail.
        """
        # Given: Create another parent
        from app.utils.security import hash_password

        another_parent = User(
            email="parent2@test.com",
            password_hash=hash_password("password123"),
            role="parent",
        )
        db_session.add(another_parent)
        db_session.commit()
        db_session.refresh(another_parent)

        # When
        link_data = {"child_id": another_parent.id}
        response = client.post(
            "/api/v1/auth/link-child",
            json=link_data,
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 400
        data = response.json()
        assert "not a child" in data["detail"].lower()


class TestGetChildren:
    """연동된 자녀 목록 조회 테스트"""

    def test_get_children_empty(
        self,
        client: TestClient,
        parent_user: User,
        auth_headers: dict,
    ):
        """
        연동된 자녀가 없을 때 빈 목록 반환 테스트
        Empty children list when no children linked.
        """
        # When
        response = client.get("/api/v1/auth/children", headers=auth_headers)

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["children"] == []
        assert data["total"] == 0
        assert data["max_allowed"] == 3

    def test_get_children_with_links(
        self,
        client: TestClient,
        db_session: Session,
        parent_user: User,
        multiple_children: list[User],
        auth_headers: dict,
    ):
        """
        연동된 자녀 목록 조회 테스트
        Should return linked children.
        """
        # Given: Link 2 children
        for i in range(2):
            link = ParentChildLink(
                parent_id=parent_user.id,
                child_id=multiple_children[i].id,
            )
            db_session.add(link)
        db_session.commit()

        # When
        response = client.get("/api/v1/auth/children", headers=auth_headers)

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["children"]) == 2
        assert data["max_allowed"] == 3

        # Verify child data
        child_emails = [c["email"] for c in data["children"]]
        assert "child1@test.com" in child_emails
        assert "child2@test.com" in child_emails


class TestUnlinkChild:
    """자녀 연동 해제 테스트"""

    def test_unlink_child_success(
        self,
        client: TestClient,
        db_session: Session,
        parent_user: User,
        child_user: User,
        auth_headers: dict,
    ):
        """
        자녀 연동 해제 성공 테스트
        Parent should be able to unlink a child.
        """
        # Given: Link child first
        link = ParentChildLink(
            parent_id=parent_user.id,
            child_id=child_user.id,
        )
        db_session.add(link)
        db_session.commit()

        # When
        response = client.delete(
            f"/api/v1/auth/link-child/{child_user.id}",
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 200
        data = response.json()
        assert "unlinked" in data["message"].lower()
        assert data["data"]["child_id"] == child_user.id

    def test_unlink_nonexistent_link_failure(
        self,
        client: TestClient,
        parent_user: User,
        child_user: User,
        auth_headers: dict,
    ):
        """
        존재하지 않는 연동 해제 실패 테스트
        Unlinking non-linked child should fail.
        """
        # When
        response = client.delete(
            f"/api/v1/auth/link-child/{child_user.id}",
            headers=auth_headers,
        )

        # Then
        assert response.status_code == 404
        data = response.json()
        assert "no link found" in data["detail"].lower()


class TestAuthHealth:
    """인증 API 헬스체크 테스트"""

    def test_auth_health_check(self, client: TestClient):
        """
        인증 서비스 헬스체크 테스트
        Health endpoint should return healthy status.
        """
        # When
        response = client.get("/api/v1/auth/health")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Authentication API"


class TestProtectedEndpoints:
    """보호된 엔드포인트 테스트"""

    def test_me_endpoint_without_token(self, client: TestClient):
        """
        토큰 없이 /me 접근 시 실패 테스트
        Accessing /me without token should fail.
        """
        # When
        response = client.get("/api/v1/auth/me")

        # Then
        assert response.status_code == 401

    def test_me_endpoint_with_invalid_token(self, client: TestClient):
        """
        잘못된 토큰으로 /me 접근 시 실패 테스트
        Accessing /me with invalid token should fail.
        """
        # When
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token_12345"},
        )

        # Then
        assert response.status_code == 401

    def test_me_endpoint_success(
        self,
        client: TestClient,
        parent_user: User,
        auth_headers: dict,
    ):
        """
        /me 엔드포인트 성공 테스트
        Accessing /me with valid token should return user info.
        """
        # When
        response = client.get("/api/v1/auth/me", headers=auth_headers)

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "parent@test.com"
        assert data["role"] == "parent"
        assert data["id"] == parent_user.id
