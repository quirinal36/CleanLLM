"""
Authentication API endpoints
인증 관련 API 엔드포인트 (회원가입, 로그인, 부모-자녀 연동)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from typing import Dict, Any

from ..core.database import get_db
from ..core.config import settings
from ..models.user import User, ParentChildLink
from ..schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    ErrorResponse,
    ParentChildLinkCreate,
    ParentChildLinkResponse,
    ChildListResponse,
    SuccessResponse,
)
from ..utils.security import hash_password, verify_password, create_access_token
from .dependencies import get_current_user, get_current_parent

# Create router
router = APIRouter()


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="이메일과 비밀번호로 새 사용자를 등록합니다.",
    responses={
        201: {
            "description": "회원가입 성공",
            "model": TokenResponse,
        },
        400: {
            "description": "이메일 중복 또는 유효하지 않은 입력",
            "model": ErrorResponse,
        },
    },
)
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    회원가입 API 엔드포인트

    **요청 본문**:
    - `email`: 이메일 주소 (유효한 이메일 형식)
    - `password`: 비밀번호 (최소 8자, 영문+숫자 조합)
    - `role`: 사용자 역할 ('parent' 또는 'child')

    **응답**:
    - `access_token`: JWT 액세스 토큰
    - `token_type`: "bearer"
    - `expires_in`: 토큰 만료 시간 (초)
    - `user`: 사용자 정보 (id, email, role, created_at, updated_at)

    **에러**:
    - `400 Bad Request`: 이메일 중복 또는 유효하지 않은 입력
    - `422 Unprocessable Entity`: 요청 본문 유효성 검증 실패

    **예제 요청**:
    ```json
    {
        "email": "parent@example.com",
        "password": "password123",
        "role": "parent"
    }
    ```

    **예제 응답**:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_in": 1800,
        "user": {
            "id": 1,
            "email": "parent@example.com",
            "role": "parent",
            "created_at": "2025-12-22T10:30:00",
            "updated_at": "2025-12-22T10:30:00"
        }
    }
    ```
    """

    # Step 1: Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email or login.",
        )

    # Step 2: Hash password
    hashed_password = hash_password(user_data.password)

    # Step 3: Create new user
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role,
    )

    # Step 4: Save to database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()
        # This handles race condition if email was registered between check and insert
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}",
        )

    # Step 5: Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(new_user.id),
            "email": new_user.email,
            "role": new_user.role,
        },
        expires_delta=access_token_expires,
    )

    # Step 6: Convert user to response model
    user_response = UserResponse(
        id=new_user.id,
        email=new_user.email,
        role=new_user.role,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )

    # Step 7: Return token and user info
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user=user_response,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="로그인",
    description="이메일과 비밀번호로 로그인하여 JWT 토큰을 발급받습니다.",
    responses={
        200: {
            "description": "로그인 성공",
            "model": TokenResponse,
        },
        401: {
            "description": "인증 실패 (이메일 또는 비밀번호 오류)",
            "model": ErrorResponse,
        },
    },
)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    로그인 API 엔드포인트

    **요청 본문**:
    - `email`: 이메일 주소
    - `password`: 비밀번호

    **응답**:
    - `access_token`: JWT 액세스 토큰
    - `token_type`: "bearer"
    - `expires_in`: 토큰 만료 시간 (초)
    - `user`: 사용자 정보 (id, email, role, created_at, updated_at)

    **에러**:
    - `401 Unauthorized`: 이메일 또는 비밀번호 오류
    - `422 Unprocessable Entity`: 요청 본문 유효성 검증 실패

    **예제 요청**:
    ```json
    {
        "email": "parent@example.com",
        "password": "password123"
    }
    ```

    **예제 응답**:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_in": 1800,
        "user": {
            "id": 1,
            "email": "parent@example.com",
            "role": "parent",
            "created_at": "2025-12-22T10:30:00",
            "updated_at": "2025-12-22T10:30:00"
        }
    }
    ```
    """

    # Step 1: Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    # Step 2: Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.password_hash):
        # Use generic error message to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 3: Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        },
        expires_delta=access_token_expires,
    )

    # Step 4: Convert user to response model
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

    # Step 5: Return token and user info
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user=user_response,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="내 정보 조회",
    description="JWT 토큰을 사용하여 현재 로그인한 사용자의 정보를 조회합니다.",
    responses={
        200: {
            "description": "사용자 정보 조회 성공",
            "model": UserResponse,
        },
        401: {
            "description": "인증 실패 (토큰 없음 또는 유효하지 않음)",
            "model": ErrorResponse,
        },
    },
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    내 정보 조회 API 엔드포인트

    JWT 토큰에서 사용자 정보를 추출하여 반환합니다.
    Authorization 헤더에 Bearer 토큰을 포함해야 합니다.

    **요청 헤더**:
    - `Authorization`: Bearer {access_token}

    **응답**:
    - `id`: 사용자 ID
    - `email`: 이메일 주소
    - `role`: 사용자 역할 ('parent' 또는 'child')
    - `created_at`: 계정 생성 시각
    - `updated_at`: 정보 수정 시각

    **에러**:
    - `401 Unauthorized`: 토큰 없음 또는 유효하지 않음

    **예제 요청**:
    ```bash
    curl -X GET http://localhost:8000/api/v1/auth/me \
      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    ```

    **예제 응답**:
    ```json
    {
        "id": 1,
        "email": "parent@example.com",
        "role": "parent",
        "created_at": "2025-12-22T10:30:00",
        "updated_at": "2025-12-22T10:30:00"
    }
    ```
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.post(
    "/link-child",
    response_model=ParentChildLinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="자녀 계정 연동",
    description="부모가 자녀 계정을 연동합니다. (최대 3명)",
    responses={
        201: {
            "description": "자녀 연동 성공",
            "model": ParentChildLinkResponse,
        },
        400: {
            "description": "연동 실패 (중복, 최대 개수 초과, 자기 자신 연동 등)",
            "model": ErrorResponse,
        },
        403: {
            "description": "권한 없음 (부모만 가능)",
            "model": ErrorResponse,
        },
        404: {
            "description": "자녀를 찾을 수 없음",
            "model": ErrorResponse,
        },
    },
)
async def link_child(
    link_data: ParentChildLinkCreate,
    parent: User = Depends(get_current_parent),
    db: Session = Depends(get_db),
) -> ParentChildLinkResponse:
    """
    부모-자녀 계정 연동 API 엔드포인트

    부모 사용자만 호출 가능하며, 자녀 계정을 연동합니다.
    최대 3명까지 연동 가능합니다.

    **요청 헤더**:
    - `Authorization`: Bearer {access_token} (부모 계정)

    **요청 본문**:
    - `child_id`: 연동할 자녀의 사용자 ID

    **응답**:
    - `id`: 연동 레코드 ID
    - `parent_id`: 부모 사용자 ID
    - `child_id`: 자녀 사용자 ID
    - `linked_at`: 연동 시각

    **에러**:
    - `400 Bad Request`: 중복 연동, 최대 개수 초과, 자기 자신 연동, 역할 오류
    - `403 Forbidden`: 부모 권한 없음
    - `404 Not Found`: 자녀를 찾을 수 없음

    **예제 요청**:
    ```json
    {
        "child_id": 2
    }
    ```

    **예제 응답**:
    ```json
    {
        "id": 1,
        "parent_id": 1,
        "child_id": 2,
        "linked_at": "2025-12-22T10:30:00"
    }
    ```
    """

    # Step 1: Validate not linking to self
    if parent.id == link_data.child_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot link to yourself",
        )

    # Step 2: Check if child exists
    child = db.query(User).filter(User.id == link_data.child_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Child user with ID {link_data.child_id} not found",
        )

    # Step 3: Validate child role
    if child.role != "child":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {link_data.child_id} is not a child account. Only child accounts can be linked.",
        )

    # Step 4: Check existing links count (max 3)
    existing_links_count = (
        db.query(ParentChildLink)
        .filter(ParentChildLink.parent_id == parent.id)
        .count()
    )
    if existing_links_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 3 children can be linked. Please unlink a child before adding a new one.",
        )

    # Step 5: Check for duplicate link
    existing_link = (
        db.query(ParentChildLink)
        .filter(
            ParentChildLink.parent_id == parent.id,
            ParentChildLink.child_id == link_data.child_id,
        )
        .first()
    )
    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Child {link_data.child_id} is already linked to your account",
        )

    # Step 6: Create link
    new_link = ParentChildLink(
        parent_id=parent.id,
        child_id=link_data.child_id,
    )

    # Step 7: Save to database
    try:
        db.add(new_link)
        db.commit()
        db.refresh(new_link)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create link. The child may already be linked.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create link: {str(e)}",
        )

    # Step 8: Return link response
    return ParentChildLinkResponse(
        id=new_link.id,
        parent_id=new_link.parent_id,
        child_id=new_link.child_id,
        linked_at=new_link.linked_at,
    )


@router.get(
    "/children",
    response_model=ChildListResponse,
    summary="연동된 자녀 목록 조회",
    description="부모에게 연동된 자녀 계정 목록을 조회합니다.",
    responses={
        200: {
            "description": "자녀 목록 조회 성공",
            "model": ChildListResponse,
        },
        403: {
            "description": "권한 없음 (부모만 가능)",
            "model": ErrorResponse,
        },
    },
)
async def get_children(
    parent: User = Depends(get_current_parent),
    db: Session = Depends(get_db),
) -> ChildListResponse:
    """
    연동된 자녀 목록 조회 API 엔드포인트

    부모 사용자만 호출 가능하며, 연동된 자녀 계정 목록을 반환합니다.

    **요청 헤더**:
    - `Authorization`: Bearer {access_token} (부모 계정)

    **응답**:
    - `children`: 자녀 사용자 정보 배열
    - `total`: 연동된 자녀 수
    - `max_allowed`: 최대 연동 가능 수 (3)

    **예제 요청**:
    ```bash
    curl -X GET http://localhost:8000/api/v1/auth/children \
      -H "Authorization: Bearer {token}"
    ```

    **예제 응답**:
    ```json
    {
        "children": [
            {
                "id": 2,
                "email": "child1@example.com",
                "role": "child",
                "created_at": "2025-12-22T10:00:00",
                "updated_at": "2025-12-22T10:00:00"
            },
            {
                "id": 3,
                "email": "child2@example.com",
                "role": "child",
                "created_at": "2025-12-22T11:00:00",
                "updated_at": "2025-12-22T11:00:00"
            }
        ],
        "total": 2,
        "max_allowed": 3
    }
    ```
    """

    # Step 1: Query all links for this parent
    links = (
        db.query(ParentChildLink)
        .filter(ParentChildLink.parent_id == parent.id)
        .all()
    )

    # Step 2: Get child IDs
    child_ids = [link.child_id for link in links]

    # Step 3: Query child users
    children = db.query(User).filter(User.id.in_(child_ids)).all() if child_ids else []

    # Step 4: Convert to response models
    children_responses = [
        UserResponse(
            id=child.id,
            email=child.email,
            role=child.role,
            created_at=child.created_at,
            updated_at=child.updated_at,
        )
        for child in children
    ]

    # Step 5: Return response
    return ChildListResponse(
        children=children_responses,
        total=len(children_responses),
        max_allowed=3,
    )


@router.delete(
    "/link-child/{child_id}",
    response_model=SuccessResponse,
    summary="자녀 연동 해제",
    description="부모와 자녀 계정의 연동을 해제합니다.",
    responses={
        200: {
            "description": "연동 해제 성공",
            "model": SuccessResponse,
        },
        403: {
            "description": "권한 없음 (부모만 가능)",
            "model": ErrorResponse,
        },
        404: {
            "description": "연동을 찾을 수 없음",
            "model": ErrorResponse,
        },
    },
)
async def unlink_child(
    child_id: int,
    parent: User = Depends(get_current_parent),
    db: Session = Depends(get_db),
) -> SuccessResponse:
    """
    부모-자녀 연동 해제 API 엔드포인트

    부모 사용자만 호출 가능하며, 자녀 계정과의 연동을 해제합니다.

    **요청 헤더**:
    - `Authorization`: Bearer {access_token} (부모 계정)

    **경로 매개변수**:
    - `child_id`: 연동 해제할 자녀의 사용자 ID

    **응답**:
    - `message`: 성공 메시지
    - `data`: 추가 정보 (해제된 child_id)

    **에러**:
    - `403 Forbidden`: 부모 권한 없음
    - `404 Not Found`: 연동을 찾을 수 없음

    **예제 요청**:
    ```bash
    curl -X DELETE http://localhost:8000/api/v1/auth/link-child/2 \
      -H "Authorization: Bearer {token}"
    ```

    **예제 응답**:
    ```json
    {
        "message": "Child successfully unlinked",
        "data": {
            "child_id": 2
        }
    }
    ```
    """

    # Step 1: Find the link
    link = (
        db.query(ParentChildLink)
        .filter(
            ParentChildLink.parent_id == parent.id,
            ParentChildLink.child_id == child_id,
        )
        .first()
    )

    # Step 2: Check if link exists
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No link found between you and child {child_id}",
        )

    # Step 3: Delete the link
    try:
        db.delete(link)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unlink child: {str(e)}",
        )

    # Step 4: Return success response
    return SuccessResponse(
        message="Child successfully unlinked",
        data={"child_id": child_id},
    )


@router.get(
    "/health",
    summary="인증 서비스 상태 확인",
    description="인증 API의 상태를 확인합니다.",
)
async def auth_health_check() -> Dict[str, str]:
    """
    인증 서비스 헬스 체크

    **응답**:
    - `status`: "healthy"
    - `service`: "Authentication API"
    """
    return {
        "status": "healthy",
        "service": "Authentication API",
    }
