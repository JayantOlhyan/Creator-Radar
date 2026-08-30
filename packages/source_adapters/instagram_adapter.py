"""Instagram Source Adapter Implementing Provider-Capability Architecture."""
from typing import Any, Dict, List
from packages.source_adapters.base import SourceAdapter
from packages.source_adapters.providers import get_acquisition_provider, AcquisitionProvider
from packages.shared.rate_limiter import get_rate_limiter


class InstagramAdapter(SourceAdapter):
    """Instagram Source Adapter delegating acquisition to configured AcquisitionProvider strategy."""

    def __init__(self, provider: AcquisitionProvider = None):
        self.provider = provider or get_acquisition_provider("auto")
        self.rate_limiter = get_rate_limiter("instagram", rate_limit_per_minute=60, max_concurrent=5)

    @property
    def platform_name(self) -> str:
        return "instagram"

    async def validate_creator(self, identifier: str) -> bool:
        await self.rate_limiter.acquire()
        try:
            return await self.provider.validate_creator(identifier)
        finally:
            self.rate_limiter.release()

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        try:
            return await self.provider.fetch_creator(identifier)
        finally:
            self.rate_limiter.release()

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        await self.rate_limiter.acquire()
        try:
            return await self.provider.fetch_latest_posts(creator_identifier, limit=limit)
        finally:
            self.rate_limiter.release()

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        try:
            return await self.provider.fetch_post(post_identifier)
        finally:
            self.rate_limiter.release()
