"""Acquisition Providers Package."""
from packages.source_adapters.providers.base import AcquisitionProvider
from packages.source_adapters.providers.meta_provider import OfficialMetaProvider
from packages.source_adapters.providers.external_provider import ExternalProvider
from packages.source_adapters.providers.mock_provider import MockAcquisitionProvider

_PROVIDER_REGISTRY = {
    "official_meta": OfficialMetaProvider,
    "external": ExternalProvider,
    "mock": MockAcquisitionProvider,
}


def get_acquisition_provider(provider_type: str = "auto") -> AcquisitionProvider:
    """Retrieve acquisition provider based on environment credentials or explicit selection."""
    if provider_type == "auto":
        meta_prov = OfficialMetaProvider()
        if meta_prov.is_configured():
            return meta_prov
        ext_prov = ExternalProvider()
        if ext_prov.is_configured():
            return ext_prov
        return MockAcquisitionProvider()

    prov_cls = _PROVIDER_REGISTRY.get(provider_type.lower())
    if not prov_cls:
        raise ValueError(f"Unknown acquisition provider type: '{provider_type}'. Available: {list(_PROVIDER_REGISTRY.keys())}")
    return prov_cls()


__all__ = [
    "AcquisitionProvider",
    "OfficialMetaProvider",
    "ExternalProvider",
    "MockAcquisitionProvider",
    "get_acquisition_provider",
]
