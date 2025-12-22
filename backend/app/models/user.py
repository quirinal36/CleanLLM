"""
User and ParentChildLink SQLAlchemy models
사용자 및 부모-자녀 연동 데이터베이스 모델
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..core.database import Base


class User(Base):
    """
    User model for authentication and profile management

    Attributes:
        id: Primary key
        email: Unique email address
        password_hash: Bcrypt hashed password
        role: User role ('parent' or 'child')
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # 'parent' or 'child'
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    # Children linked to this parent
    children = relationship(
        "User",
        secondary="parent_child_links",
        primaryjoin="User.id == ParentChildLink.parent_id",
        secondaryjoin="User.id == ParentChildLink.child_id",
        backref="parents",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

    def to_dict(self) -> dict:
        """
        Convert user object to dictionary

        Returns:
            dict: User data without password_hash
        """
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ParentChildLink(Base):
    """
    Parent-Child account linking model

    Attributes:
        id: Primary key
        parent_id: Foreign key to parent user
        child_id: Foreign key to child user
        linked_at: Link creation timestamp
    """

    __tablename__ = "parent_child_links"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    child_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    linked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Add unique constraint to prevent duplicate links
    __table_args__ = (UniqueConstraint("parent_id", "child_id", name="uq_parent_child"),)

    # Relationships
    parent = relationship("User", foreign_keys=[parent_id])
    child = relationship("User", foreign_keys=[child_id])

    def __repr__(self) -> str:
        return f"<ParentChildLink(parent_id={self.parent_id}, child_id={self.child_id})>"

    def to_dict(self) -> dict:
        """
        Convert link object to dictionary

        Returns:
            dict: Link data
        """
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "child_id": self.child_id,
            "linked_at": self.linked_at.isoformat() if self.linked_at else None,
        }
