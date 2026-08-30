"""Mock Acquisition Provider for Deterministic Local Dev and CI Testing."""
from typing import Any, Dict, List
from packages.source_adapters.providers.base import AcquisitionProvider
from packages.shared.errors import PermanentAcquisitionError, RateLimitExceededError, TransientAcquisitionError


class MockAcquisitionProvider(AcquisitionProvider):
    """Mock Acquisition Provider supporting deterministic behavior, errors, empty results, and rate limits."""

    def __init__(self, mode: str = "normal"):
        self.mode = mode

    @property
    def provider_id(self) -> str:
        return "mock_acquisition_provider"

    async def validate_creator(self, identifier: str) -> bool:
        if identifier.startswith("invalid_") or identifier == "unsupported":
            return False
        return True

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        if identifier == "invalid_handle":
            raise PermanentAcquisitionError(f"Creator handle '{identifier}' invalid or does not exist.")
        elif identifier == "transient_error_user":
            raise TransientAcquisitionError("Temporary network timeout connecting to upstream provider.")
        elif identifier == "rate_limited_user":
            raise RateLimitExceededError("Rate limit exceeded for user check.")
        elif identifier == "unsupported_user":
            raise PermanentAcquisitionError("Creator profile is unsupported or private.")

        return {
            "name": f"Mock Creator {identifier.title()}",
            "username": identifier,
            "platform": "instagram",
            "profile_url": f"https://www.instagram.com/{identifier}/",
            "is_active": True,
            "external_id": f"ext_creator_{identifier}"
        }

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        if creator_identifier == "empty_creator":
            return []
        elif creator_identifier == "transient_error_creator":
            raise TransientAcquisitionError("Upstream socket connection reset.")
        elif creator_identifier == "permanent_error_creator":
            raise PermanentAcquisitionError("Account suspended or deleted.")
        elif creator_identifier == "rate_limited_creator":
            raise RateLimitExceededError("API call quota exceeded.")

        types = ["reel", "carousel", "post", "video", "image"]
        posts = []
        for i in range(1, limit + 1):
            c_type = types[(i - 1) % len(types)]
            media_list = []
            if c_type == "carousel":
                media_list = [
                    {"media_type": "image", "media_url": f"https://media.mock.com/{creator_identifier}/slide_1.jpg", "position": 0},
                    {"media_type": "image", "media_url": f"https://media.mock.com/{creator_identifier}/slide_2.jpg", "position": 1}
                ]
            else:
                media_list = [
                    {
                        "media_type": "video" if c_type in ("reel", "video") else "image",
                        "media_url": f"https://media.mock.com/{creator_identifier}/media_{i}.mp4",
                        "thumbnail_url": f"https://media.mock.com/{creator_identifier}/thumb_{i}.jpg",
                        "mime_type": "video/mp4" if c_type in ("reel", "video") else "image/jpeg",
                        "duration": 45 if c_type in ("reel", "video") else None,
                        "width": 1080,
                        "height": 1920 if c_type == "reel" else 1080,
                        "position": 0
                    }
                ]

            posts.append({
                "external_id": f"{creator_identifier}_post_{i}",
                "url": f"https://instagram.com/p/{creator_identifier}_post_{i}",
                "content_type": c_type,
                "caption": f"Sample post #{i} caption for @{creator_identifier} discussing architecture patterns.",
                "published_at": f"2026-08-30T12:00:0{i}Z",
                "media": media_list
            })
        return posts

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        return {
            "external_id": post_identifier,
            "url": f"https://instagram.com/p/{post_identifier}",
            "content_type": "reel",
            "caption": f"Mock detail caption for post {post_identifier}",
            "published_at": "2026-08-30T12:00:00Z",
            "media": [
                {
                    "media_type": "video",
                    "media_url": f"https://media.mock.com/post/{post_identifier}.mp4",
                    "position": 0
                }
            ]
        }
