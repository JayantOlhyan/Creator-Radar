"""KnowledgeItem, ContentOpportunity, and Notification SQLAlchemy Models."""
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from packages.shared.database import Base


class KnowledgeItemModel(Base):
    __tablename__ = "knowledge_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="knowledge_items")


class ContentOpportunityModel(Base):
    __tablename__ = "content_opportunities"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    post_analysis_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("post_analysis.id", ondelete="SET NULL"), nullable=True)
    pattern_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("content_patterns.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    hook: Mapped[str] = mapped_column(Text, nullable=False)
    concept: Mapped[str] = mapped_column(Text, nullable=False)
    format: Mapped[str] = mapped_column(String(100), nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    originality_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    effort_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    priority_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="opportunities")
    analysis: Mapped[Optional["PostAnalysisModel"]] = relationship("PostAnalysisModel", back_populates="opportunities")
    pattern: Mapped[Optional["ContentPatternModel"]] = relationship("ContentPatternModel", back_populates="opportunities")
    notifications: Mapped[List["NotificationModel"]] = relationship("NotificationModel", back_populates="opportunity")


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    opportunity_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("content_opportunities.id", ondelete="CASCADE"), nullable=True)
    channel: Mapped[str] = mapped_column(String(50), default="telegram", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="notifications")
    opportunity: Mapped[Optional["ContentOpportunityModel"]] = relationship("ContentOpportunityModel", back_populates="notifications")
