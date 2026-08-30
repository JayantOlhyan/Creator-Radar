"""Shared Pydantic Schemas for Domain Models, Events, and APIs."""
from packages.schemas.domain import (
    UserSchema, CreatorSchema, PostSchema, PostMediaSchema,
    PostAnalysisSchema, ContentPatternSchema, UserProfileSchema,
    KnowledgeItemSchema, ContentOpportunitySchema, NotificationSchema
)
from packages.schemas.events import (
    BaseEvent, PostDetectedEvent, PostIngestedEvent,
    TranscriptionCompletedEvent, AnalysisCompletedEvent,
    PatternDetectedEvent, OpportunityGeneratedEvent, NotificationCreatedEvent
)

__all__ = [
    "UserSchema", "CreatorSchema", "PostSchema", "PostMediaSchema",
    "PostAnalysisSchema", "ContentPatternSchema", "UserProfileSchema",
    "KnowledgeItemSchema", "ContentOpportunitySchema", "NotificationSchema",
    "BaseEvent", "PostDetectedEvent", "PostIngestedEvent",
    "TranscriptionCompletedEvent", "AnalysisCompletedEvent",
    "PatternDetectedEvent", "OpportunityGeneratedEvent", "NotificationCreatedEvent"
]
