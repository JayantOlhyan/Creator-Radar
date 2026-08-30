"""Test Database Model Definitions and Base Metadata."""
import pytest
from packages.shared.database import Base
from apps.api.models import (
    UserModel, UserProfileModel, CreatorModel, CreatorSourceModel,
    PostModel, PostMediaModel, PostAnalysisModel, ContentPatternModel,
    KnowledgeItemModel, ContentOpportunityModel, NotificationModel
)


def test_orm_models_registered_in_metadata():
    table_names = list(Base.metadata.tables.keys())
    expected_tables = [
        "users", "user_profiles", "creators", "creator_sources",
        "posts", "post_media", "post_analysis", "content_patterns",
        "knowledge_items", "content_opportunities", "notifications"
    ]
    for table in expected_tables:
        assert table in table_names, f"Table '{table}' missing from SQLAlchemy metadata"


def test_post_deduplication_constraint():
    post_table = Base.metadata.tables["posts"]
    unique_constraints = [c.name for c in post_table.constraints if hasattr(c, "name")]
    assert "uq_creator_external_post" in unique_constraints
