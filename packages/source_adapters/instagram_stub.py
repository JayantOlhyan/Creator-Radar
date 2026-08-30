"""Instagram Source Adapter Stub Implementation."""
from typing import Any, Dict, List
from packages.source_adapters.base import SourceAdapter


class InstagramAdapter(SourceAdapter):
    """Stub adapter for Instagram. Real compliance acquisition mechanism will be implemented in Phase 1."""

    @property
    def platform_name(self) -> str:
        return "instagram"

    async def validate_creator(self, identifier: str) -> bool:
        return bool(identifier and not identifier.startswith("invalid_"))

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        return {
            "name": f"Creator {identifier}",
            "username": identifier,
            "platform": self.platform_name,
            "profile_url": f"https://instagram.com/{identifier}",
            "is_active": True,
        }

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        return [
            {
                "external_id": f"ig_post_{i}",
                "url": f"https://instagram.com/p/ig_post_{i}",
                "content_type": "carousel" if i % 2 == 0 else "reel",
                "caption": f"Sample Instagram post caption #{i} by {creator_identifier}",
                "published_at": "2026-08-30T12:00:00Z",
                "media": [
                    {
                        "media_type": "video" if i % 2 != 0 else "image",
                        "media_url": f"https://media.instagram.com/p_{i}.mp4",
                        "position": 0,
                    }
                ]
            }
            for i in range(1, limit + 1)
        ]

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        return {
            "external_id": post_identifier,
            "url": f"https://instagram.com/p/{post_identifier}",
            "content_type": "reel",
            "caption": f"Detailed content for post {post_identifier}",
            "published_at": "2026-08-30T12:00:00Z",
        }
