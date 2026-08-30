"""Test Provider-Capability Source Acquisition Architecture."""
import pytest
from packages.source_adapters import get_source_adapter, InstagramAdapter
from packages.source_adapters.providers import (
    get_acquisition_provider, OfficialMetaProvider, ExternalProvider, MockAcquisitionProvider
)


def test_provider_selection():
    mock_prov = get_acquisition_provider("mock")
    assert isinstance(mock_prov, MockAcquisitionProvider)
    assert mock_prov.provider_id == "mock_acquisition_provider"

    meta_prov = OfficialMetaProvider()
    assert meta_prov.provider_id == "official_meta_graph_api"
    assert meta_prov.is_configured() is False


@pytest.mark.asyncio
async def test_instagram_adapter_with_mock_provider():
    mock_prov = MockAcquisitionProvider()
    adapter = InstagramAdapter(provider=mock_prov)
    
    assert adapter.platform_name == "instagram"
    
    # Test creator validation
    valid = await adapter.validate_creator("techcreator")
    assert valid is True

    invalid = await adapter.validate_creator("invalid_handle")
    assert invalid is False

    # Test latest posts acquisition
    posts = await adapter.fetch_latest_posts("techcreator", limit=3)
    assert len(posts) == 3
    assert posts[0]["external_id"] == "techcreator_post_1"
    assert "media" in posts[0]
