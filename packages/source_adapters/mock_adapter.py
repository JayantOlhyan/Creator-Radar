"""Mock Adapter for Testing Contract Verification."""
from typing import Any, Dict, List
from packages.source_adapters.base import SourceAdapter


class MockAdapter(SourceAdapter):
    """Mock adapter for contract verification and unit tests."""

    @property
    def platform_name(self) -> str:
        return "mock"

    async def validate_creator(self, identifier: str) -> bool:
        return identifier != "invalid"

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        return {
            "name": f"Mock Creator {identifier}",
            "username": identifier,
            "platform": self.platform_name,
            "profile_url": f"https://mock.platform/{identifier}",
            "is_active": True,
        }

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        return [
            {
                "external_id": f"mock_post_{i}",
                "url": f"https://mock.platform/post/{i}",
                "content_type": "text",
                "caption": f"Mock post {i}",
                "published_at": "2026-08-30T00:00:00Z",
                "media": []
            }
            for i in range(1, limit + 1)
        ]

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        return {
            "external_id": post_identifier,
            "url": f"https://mock.platform/post/{post_identifier}",
            "content_type": "text",
            "caption": f"Mock detail {post_identifier}",
            "published_at": "2026-08-30T00:00:00Z",
        }
