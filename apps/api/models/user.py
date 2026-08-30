"""User and UserProfile SQLAlchemy Models."""
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from packages.shared.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    profile: Mapped[Optional["UserProfileModel"]] = relationship("UserProfileModel", back_populates="user", uselist=False, cascade="all, delete-orphan")
    knowledge_items: Mapped[List["KnowledgeItemModel"]] = relationship("KnowledgeItemModel", back_populates="user", cascade="all, delete-orphan")
    opportunities: Mapped[List["ContentOpportunityModel"]] = relationship("ContentOpportunityModel", back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[List["NotificationModel"]] = relationship("NotificationModel", back_populates="user", cascade="all, delete-orphan")


class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    niche: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content_goals: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    tone_of_voice: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_audience: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="profile")
