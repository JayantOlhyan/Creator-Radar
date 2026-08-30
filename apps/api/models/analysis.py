"""PostAnalysis and ContentPattern SQLAlchemy Models."""
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from packages.shared.database import Base


class PostAnalysisModel(Base):
    __tablename__ = "post_analysis"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id: Mapped[str] = mapped_column(String, ForeignKey("posts.id", ondelete="CASCADE"), unique=True, nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    hook: Mapped[str] = mapped_column(Text, nullable=False)
    hook_type: Mapped[str] = mapped_column(String(100), nullable=False)
    format: Mapped[str] = mapped_column(String(100), nullable=False)
    narrative_structure: Mapped[str] = mapped_column(Text, nullable=False)
    target_audience: Mapped[str] = mapped_column(String(255), nullable=False)
    emotional_trigger: Mapped[str] = mapped_column(String(100), nullable=False)
    cta: Mapped[str] = mapped_column(Text, nullable=False)
    visual_structure: Mapped[str] = mapped_column(Text, nullable=False)
    editing_style: Mapped[str] = mapped_column(String(255), nullable=False)
    content_mechanism: Mapped[str] = mapped_column(Text, nullable=False)
    why_it_works: Mapped[str] = mapped_column(Text, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    originality_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    post: Mapped["PostModel"] = relationship("PostModel", back_populates="analysis")
    opportunities: Mapped[List["ContentOpportunityModel"]] = relationship("ContentOpportunityModel", back_populates="analysis")


class ContentPatternModel(Base):
    __tablename__ = "content_patterns"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    structure: Mapped[str] = mapped_column(Text, nullable=False)
    example_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    opportunities: Mapped[List["ContentOpportunityModel"]] = relationship("ContentOpportunityModel", back_populates="pattern")
