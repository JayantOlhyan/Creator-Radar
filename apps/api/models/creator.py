"""Creator and CreatorSource SQLAlchemy Models with Watchlist Lifecycle Tracking."""
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from packages.shared.database import Base


class CreatorStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"
    UNSUPPORTED = "UNSUPPORTED"


class CreatorModel(Base):
    __tablename__ = "creators"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    platform: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    profile_url: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=CreatorStatusEnum.ACTIVE.value, nullable=False, index=True)
    
    # Watchlist Lifecycle & Diagnostic Metadata
    last_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_successful_check_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_error_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    check_interval_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    sources: Mapped[List["CreatorSourceModel"]] = relationship("CreatorSourceModel", back_populates="creator", cascade="all, delete-orphan")
    posts: Mapped[List["PostModel"]] = relationship("PostModel", back_populates="creator", cascade="all, delete-orphan")


class CreatorSourceModel(Base):
    __tablename__ = "creator_sources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id: Mapped[str] = mapped_column(String, ForeignKey("creators.id", ondelete="CASCADE"), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    source_identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    creator: Mapped["CreatorModel"] = relationship("CreatorModel", back_populates="sources")
