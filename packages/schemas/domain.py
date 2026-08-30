"""Domain Pydantic Schemas with Watchlist Status Lifecycle."""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PlatformEnum(str, Enum):
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    X = "x"
    REDDIT = "reddit"


class CreatorStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"
    UNSUPPORTED = "UNSUPPORTED"


class PostStatusEnum(str, Enum):
    DETECTED = "detected"
    INGESTED = "ingested"
    TRANSCRIBED = "transcribed"
    ANALYZED = "analyzed"
    FAILED = "failed"


class ContentTypeEnum(str, Enum):
    POST = "post"
    REEL = "reel"
    CAROUSEL = "carousel"
    VIDEO = "video"
    IMAGE = "image"
    UNKNOWN = "unknown"


class OpportunityStatusEnum(str, Enum):
    DRAFT = "draft"
    SAVED = "saved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class KnowledgeTypeEnum(str, Enum):
    PROJECT = "project"
    EXPERTISE = "expertise"
    EXPERIENCE = "experience"
    OPINION = "opinion"
    ACHIEVEMENT = "achievement"
    PREVIOUS_CONTENT = "previous_content"


class UserSchema(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CreatorCreateSchema(BaseModel):
    platform: PlatformEnum
    username: str
    profile_url: Optional[str] = None
    check_interval_minutes: int = Field(default=60, ge=15, le=1440)


class CreatorUpdateSchema(BaseModel):
    name: Optional[str] = None
    status: Optional[CreatorStatusEnum] = None
    is_active: Optional[bool] = None
    check_interval_minutes: Optional[int] = Field(default=None, ge=15, le=1440)


class CreatorSchema(BaseModel):
    id: str
    name: str
    username: str
    platform: PlatformEnum
    profile_url: str
    is_active: bool = True
    status: CreatorStatusEnum = CreatorStatusEnum.ACTIVE
    last_checked_at: Optional[datetime] = None
    last_successful_check_at: Optional[datetime] = None
    last_error_at: Optional[datetime] = None
    last_error_message: Optional[str] = None
    check_interval_minutes: int = 60
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PostMediaSchema(BaseModel):
    id: Optional[str] = None
    post_id: Optional[str] = None
    media_type: str
    media_url: str
    thumbnail_url: Optional[str] = None
    mime_type: Optional[str] = None
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    position: int = 0
    model_config = ConfigDict(from_attributes=True)


class PostSchema(BaseModel):
    id: str
    creator_id: str
    external_id: str
    url: str
    content_type: str
    caption: Optional[str] = None
    published_at: Optional[datetime] = None
    detected_at: datetime
    status: PostStatusEnum = PostStatusEnum.DETECTED
    created_at: datetime
    media: List[PostMediaSchema] = []
    model_config = ConfigDict(from_attributes=True)


class PostAnalysisSchema(BaseModel):
    id: str
    post_id: str
    topic: str
    hook: str
    hook_type: str
    format: str
    narrative_structure: str
    target_audience: str
    emotional_trigger: str
    cta: str
    visual_structure: str
    editing_style: str
    content_mechanism: str
    why_it_works: str
    relevance_score: float = Field(ge=0.0, le=10.0)
    originality_score: float = Field(ge=0.0, le=10.0)
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ContentPatternSchema(BaseModel):
    id: str
    name: str
    description: str
    structure: str
    example_count: int = 0
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserProfileSchema(BaseModel):
    id: str
    user_id: str
    niche: Optional[str] = None
    content_goals: List[str] = []
    tone_of_voice: Optional[str] = None
    target_audience: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class KnowledgeItemSchema(BaseModel):
    id: str
    user_id: str
    item_type: KnowledgeTypeEnum
    title: str
    content: str
    tags: List[str] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ContentOpportunitySchema(BaseModel):
    id: str
    user_id: str
    post_analysis_id: Optional[str] = None
    pattern_id: Optional[str] = None
    title: str
    hook: str
    concept: str
    format: str
    reasoning: str
    relevance_score: float = Field(ge=0.0, le=10.0)
    originality_score: float = Field(ge=0.0, le=10.0)
    effort_score: float = Field(ge=0.0, le=10.0)
    priority_score: float = Field(ge=0.0, le=10.0)
    status: OpportunityStatusEnum = OpportunityStatusEnum.DRAFT
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class NotificationSchema(BaseModel):
    id: str
    user_id: str
    opportunity_id: Optional[str] = None
    channel: str = "telegram"
    status: str = "pending"
    payload: Dict[str, str] = {}
    sent_at: Optional[datetime] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
