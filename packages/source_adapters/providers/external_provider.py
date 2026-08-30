"""Compliant External Data Acquisition Provider Interface."""
import os
from typing import Any, Dict, List
import httpx
from packages.source_adapters.providers.base import AcquisitionProvider
from packages.shared.errors import PermanentAcquisitionError, RateLimitExceededError, TransientAcquisitionError
from packages.shared.logging import get_logger

logger = get_logger(__name__)


class ExternalProvider(AcquisitionProvider):
    """Compliant External Proxy / Third-Party Data API Acquisition Provider."""

    def __init__(self, api_key: str = None, endpoint_url: str = None):
        self.api_key = api_key or os.getenv("EXTERNAL_ACQUISITION_API_KEY")
        self.endpoint_url = endpoint_url or os.getenv("EXTERNAL_ACQUISITION_ENDPOINT", "https://api.external-social-provider.com/v1")

    @property
    def provider_id(self) -> str:
        return "external_compliant_proxy"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def validate_creator(self, identifier: str) -> bool:
        if not self.is_configured():
            return True
        try:
            profile = await self.fetch_creator(identifier)
            return bool(profile)
        except Exception:
            return False

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        if not self.is_configured():
            raise PermanentAcquisitionError("ExternalProvider missing EXTERNAL_ACQUISITION_API_KEY.")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.endpoint_url}/creators/instagram/{identifier}"

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                res = await client.get(url, headers=headers)
                if res.status_code == 429:
                    raise RateLimitExceededError("External acquisition provider rate limited.")
                elif res.status_code in (400, 404):
                    raise PermanentAcquisitionError(f"Creator handle '{identifier}' not found on platform.")
                elif res.status_code >= 500:
                    raise TransientAcquisitionError(f"External provider error: HTTP {res.status_code}")
                
                res.raise_for_status()
                data = res.json()
                return {
                    "name": data.get("full_name", identifier),
                    "username": identifier,
                    "platform": "instagram",
                    "profile_url": f"https://www.instagram.com/{identifier}/",
                    "is_active": True,
                    "external_id": data.get("id")
                }
            except httpx.RequestError as exc:
                raise TransientAcquisitionError(f"Network error calling external provider: {str(exc)}")

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.is_configured():
            raise PermanentAcquisitionError("ExternalProvider missing configuration credentials.")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.endpoint_url}/creators/instagram/{creator_identifier}/posts"
        params = {"limit": limit}

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                res = await client.get(url, headers=headers, params=params)
                if res.status_code == 429:
                    raise RateLimitExceededError("External provider rate limit exceeded.")
                elif res.status_code >= 400:
                    raise PermanentAcquisitionError(f"Failed fetching posts for '{creator_identifier}' via external provider.")

                raw_posts = res.json().get("items", [])
                normalized = []
                for item in raw_posts:
                    normalized.append({
                        "external_id": str(item.get("id")),
                        "url": item.get("url", f"https://instagram.com/p/{item.get('id')}"),
                        "content_type": item.get("type", "post").lower(),
                        "caption": item.get("caption"),
                        "published_at": item.get("published_at"),
                        "media": item.get("media", [])
                    })
                return normalized
            except httpx.RequestError as exc:
                raise TransientAcquisitionError(f"Network error from external provider: {str(exc)}")

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        posts = await self.fetch_latest_posts("unknown", limit=1)
        return posts[0] if posts else {}
