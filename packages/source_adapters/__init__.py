"""Source Adapter Registry and Factory Module."""
from packages.source_adapters.base import SourceAdapter
from packages.source_adapters.instagram_adapter import InstagramAdapter
from packages.source_adapters.linkedin_stub import LinkedInAdapter
from packages.source_adapters.mock_adapter import MockAdapter

_ADAPTER_REGISTRY = {
    "instagram": InstagramAdapter,
    "linkedin": LinkedInAdapter,
    "mock": MockAdapter,
}


def get_source_adapter(platform: str) -> SourceAdapter:
    """Factory returning the appropriate SourceAdapter instance for a target platform."""
    adapter_cls = _ADAPTER_REGISTRY.get(platform.lower())
    if not adapter_cls:
        raise ValueError(f"Unsupported source platform: '{platform}'. Available: {list(_ADAPTER_REGISTRY.keys())}")
    return adapter_cls()


__all__ = [
    "SourceAdapter",
    "InstagramAdapter",
    "LinkedInAdapter",
    "MockAdapter",
    "get_source_adapter",
]
