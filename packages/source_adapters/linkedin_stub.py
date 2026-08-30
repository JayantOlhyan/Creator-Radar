"""LinkedIn Source Adapter Stub Implementation."""
from typing import Any, Dict, List
from packages.source_adapters.base import SourceAdapter


class LinkedInAdapter(SourceAdapter):
    """Stub adapter for LinkedIn."""

    @property
    def platform_name(self) -> str:
        return "linkedin"

    async def validate_creator(self, identifier: str) -> bool:
        return bool(identifier)

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        return {
            "name": f"Professional {identifier}",
            "username": identifier,
            "platform": self.platform_name,
            "profile_url": f"https://linkedin.com/in/{identifier}",
            "is_active": True,
        }

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        return [
            {
                "external_id": f"li_post_{i}",
                "url": f"https://linkedin.com/posts/{creator_identifier}_li_post_{i}",
                "content_type": "article",
                "caption": f"Professional insights on building software scalable systems #{i}",
                "published_at": "2026-08-30T10:00:00Z",
                "media": []
            }
            for i in range(1, limit + 1)
        ]

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        return {
            "external_id": post_identifier,
            "url": f"https://linkedin.com/posts/{post_identifier}",
            "content_type": "article",
            "caption": f"Detailed LinkedIn post content {post_identifier}",
            "published_at": "2026-08-30T10:00:00Z",
        }
