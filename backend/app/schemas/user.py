"""
Pydantic schemas for User-related requests and responses
사용자 관련 요청/응답 검증 스키마
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
import re


class UserBase(BaseModel):
    """Base user schema with common fields"""

    email: EmailStr = Field(..., description="User email address")
    role: Literal["parent", "child"] = Field(..., description="User role: parent or child")


class UserCreate(UserBase):
    """
    Schema for user registration

    Validation:
        - Password must be at least 8 characters
        - Password must contain at least one letter and one number
    """

    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters, must contain letters and numbers)",
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength
        Must contain at least one letter and one number
        """
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    """
    Schema for updating user information
    All fields are optional
    """

    email: Optional[EmailStr] = Field(None, description="New email address")
    password: Optional[str] = Field(
        None,
        min_length=8,
        description="New password (minimum 8 characters)",
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: Optional[str]) -> Optional[str]:
        """Validate password strength if provided"""
        if v is None:
            return v
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class UserResponse(UserBase):
    """
    Schema for user response
    Excludes password_hash for security
    """

    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # Allow ORM model conversion


class TokenResponse(BaseModel):
    """Schema for JWT token response"""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponse = Field(..., description="User information")


class ParentChildLinkCreate(BaseModel):
    """
    Schema for creating parent-child link

    Note: parent_id is usually extracted from JWT token
    Only child_id needs to be provided in request body
    """

    child_id: int = Field(..., description="Child user ID to link", gt=0)


class ParentChildLinkResponse(BaseModel):
    """Schema for parent-child link response"""

    id: int = Field(..., description="Link ID")
    parent_id: int = Field(..., description="Parent user ID")
    child_id: int = Field(..., description="Child user ID")
    linked_at: datetime = Field(..., description="Link creation timestamp")

    class Config:
        from_attributes = True  # Allow ORM model conversion


class ChildListResponse(BaseModel):
    """Schema for listing children linked to a parent"""

    children: list[UserResponse] = Field(
        default_factory=list, description="List of linked children"
    )
    total: int = Field(..., description="Total number of linked children")
    max_allowed: int = Field(default=3, description="Maximum allowed children links")


class ErrorResponse(BaseModel):
    """Schema for error responses"""

    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for client handling")


class SuccessResponse(BaseModel):
    """Schema for generic success responses"""

    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Additional response data")
