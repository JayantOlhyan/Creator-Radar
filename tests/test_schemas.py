"""Test Pydantic Domain Schemas and Events."""
from datetime import datetime
import pytest
from packages.schemas.domain import (
    CreatorSchema, PostSchema, PostAnalysisSchema, PlatformEnum, PostStatusEnum
)
from packages.schemas.events import (
    PostDetectedEvent, PostIngestedEvent, AnalysisCompletedEvent, OpportunityGeneratedEvent
)


def test_creator_schema_validation():
    creator = CreatorSchema(
        id="c1",
        name="Test Creator",
        username="testcreator",
        platform=PlatformEnum.INSTAGRAM,
        profile_url="https://instagram.com/testcreator",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    assert creator.platform == PlatformEnum.INSTAGRAM
    assert creator.is_active is True


def test_event_schema_validation():
    event = PostDetectedEvent(
        event_id="e1",
        producer="test_runner",
        creator_id="c1",
        external_id="ext_100",
        platform="instagram",
        url="https://instagram.com/p/ext_100"
    )
    assert event.event_name == "post.detected"
    assert event.external_id == "ext_100"
