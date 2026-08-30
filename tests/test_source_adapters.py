"""Test Source Adapter Abstraction Contract."""
import pytest
from packages.source_adapters import get_source_adapter, InstagramAdapter, LinkedInAdapter, MockAdapter


@pytest.mark.asyncio
async def test_source_adapter_factory():
    ig_adapter = get_source_adapter("instagram")
    assert isinstance(ig_adapter, InstagramAdapter)
    assert ig_adapter.platform_name == "instagram"

    li_adapter = get_source_adapter("linkedin")
    assert isinstance(li_adapter, LinkedInAdapter)
    assert li_adapter.platform_name == "linkedin"

    mock_adapter = get_source_adapter("mock")
    assert isinstance(mock_adapter, MockAdapter)
    assert mock_adapter.platform_name == "mock"


@pytest.mark.asyncio
async def test_mock_adapter_contract():
    adapter = get_source_adapter("mock")
    
    is_valid = await adapter.validate_creator("test_creator")
    assert is_valid is True

    creator_meta = await adapter.fetch_creator("test_creator")
    assert creator_meta["username"] == "test_creator"
    assert creator_meta["platform"] == "mock"

    posts = await adapter.fetch_latest_posts("test_creator", limit=5)
    assert len(posts) == 5
    assert "external_id" in posts[0]

    post_detail = await adapter.fetch_post("mock_post_1")
    assert post_detail["external_id"] == "mock_post_1"


def test_invalid_platform_raises_error():
    with pytest.raises(ValueError, match="Unsupported source platform"):
        get_source_adapter("unsupported_platform")
