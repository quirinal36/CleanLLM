"""
API dependencies for authentication and authorization
인증 및 권한 확인을 위한 FastAPI 의존성
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..models.user import User
from ..utils.security import decode_access_token

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Get current authenticated user from JWT token

    This dependency function extracts and validates the JWT token from the
    Authorization header, then retrieves the corresponding user from the database.

    Usage:
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}

    Args:
        credentials: HTTP Bearer credentials from Authorization header
        db: Database session

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException 401: If token is invalid or user not found
    """
    # Extract token from credentials
    token = credentials.credentials

    # Decode and validate token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user ID from token
    user_id_str: Optional[str] = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert to integer
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Retrieve user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_parent(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current authenticated user, ensuring they are a parent

    This dependency builds on get_current_user and adds role verification.

    Usage:
        @app.post("/parent-only")
        async def parent_only_route(parent: User = Depends(get_current_parent)):
            return {"parent_id": parent.id}

    Args:
        current_user: Current authenticated user

    Returns:
        User: Authenticated parent user

    Raises:
        HTTPException 403: If user is not a parent
    """
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires parent role",
        )
    return current_user


async def get_current_child(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current authenticated user, ensuring they are a child

    Usage:
        @app.get("/child-only")
        async def child_only_route(child: User = Depends(get_current_child)):
            return {"child_id": child.id}

    Args:
        current_user: Current authenticated user

    Returns:
        User: Authenticated child user

    Raises:
        HTTPException 403: If user is not a child
    """
    if current_user.role != "child":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires child role",
        )
    return current_user
