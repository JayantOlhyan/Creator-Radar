"""Event Schemas for Async Processing & Message Queue."""
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    event_id: str
    event_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    producer: str
    version: str = "1.0"


class PostDetectedEvent(BaseEvent):
    event_name: str = "post.detected"
    creator_id: str
    external_id: str
    platform: str
    url: str


class PostIngestedEvent(BaseEvent):
    event_name: str = "post.ingested"
    post_id: str
    creator_id: str
    media_urls: list[str] = []


class TranscriptionCompletedEvent(BaseEvent):
    event_name: str = "post.transcription.completed"
    post_id: str
    transcript_text: str
    language: str = "en"


class AnalysisCompletedEvent(BaseEvent):
    event_name: str = "post.analysis.completed"
    post_id: str
    analysis_id: str
    topic: str
    relevance_score: float


class PatternDetectedEvent(BaseEvent):
    event_name: str = "pattern.detected"
    pattern_id: str
    pattern_name: str
    matched_post_ids: list[str] = []


class OpportunityGeneratedEvent(BaseEvent):
    event_name: str = "opportunity.generated"
    opportunity_id: str
    user_id: str
    title: str
    priority_score: float


class NotificationCreatedEvent(BaseEvent):
    event_name: str = "notification.created"
    notification_id: str
    user_id: str
    channel: str
    payload: Dict[str, Any]
