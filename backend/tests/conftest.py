"""
Pytest fixtures for authentication API tests
인증 API 테스트를 위한 pytest fixtures
"""

import os
import sys

# Set test environment variables BEFORE importing app modules
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["DEBUG"] = "False"

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User, ParentChildLink
from app.utils.security import hash_password


# Test database URL (SQLite in-memory)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine with StaticPool for SQLite in-memory
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test.
    테스트마다 새로운 데이터베이스 세션을 생성합니다.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create session
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database session override.
    데이터베이스 세션을 오버라이드한 테스트 클라이언트를 생성합니다.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def parent_user(db_session: Session) -> User:
    """
    Create a test parent user.
    테스트용 부모 사용자를 생성합니다.
    """
    user = User(
        email="parent@test.com",
        password_hash=hash_password("password123"),
        role="parent",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def child_user(db_session: Session) -> User:
    """
    Create a test child user.
    테스트용 자녀 사용자를 생성합니다.
    """
    user = User(
        email="child@test.com",
        password_hash=hash_password("child123abc"),
        role="child",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def multiple_children(db_session: Session) -> list[User]:
    """
    Create multiple test child users (4 children for max limit testing).
    최대 제한 테스트를 위한 여러 자녀 사용자를 생성합니다.
    """
    children = []
    for i in range(1, 5):
        child = User(
            email=f"child{i}@test.com",
            password_hash=hash_password(f"child{i}pass123"),
            role="child",
        )
        db_session.add(child)
        children.append(child)

    db_session.commit()
    for child in children:
        db_session.refresh(child)

    return children


@pytest.fixture
def parent_token(client: TestClient, parent_user: User) -> str:
    """
    Get JWT token for parent user.
    부모 사용자의 JWT 토큰을 가져옵니다.
    """
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "parent@test.com", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def child_token(client: TestClient, child_user: User) -> str:
    """
    Get JWT token for child user.
    자녀 사용자의 JWT 토큰을 가져옵니다.
    """
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "child@test.com", "password": "child123abc"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(parent_token: str) -> dict:
    """
    Get authorization headers with parent token.
    부모 토큰이 포함된 인증 헤더를 가져옵니다.
    """
    return {"Authorization": f"Bearer {parent_token}"}


@pytest.fixture
def child_auth_headers(child_token: str) -> dict:
    """
    Get authorization headers with child token.
    자녀 토큰이 포함된 인증 헤더를 가져옵니다.
    """
    return {"Authorization": f"Bearer {child_token}"}
