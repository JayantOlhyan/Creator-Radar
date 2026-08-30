"""Official Meta / Instagram Graph API Business Discovery Acquisition Provider."""
import os
from typing import Any, Dict, List
import httpx
from packages.source_adapters.providers.base import AcquisitionProvider
from packages.shared.errors import PermanentAcquisitionError, RateLimitExceededError, TransientAcquisitionError
from packages.shared.logging import get_logger

logger = get_logger(__name__)


class OfficialMetaProvider(AcquisitionProvider):
    """Official Meta Instagram Graph API Provider via Business Discovery Endpoint."""

    def __init__(self, access_token: str = None, instagram_account_id: str = None):
        self.access_token = access_token or os.getenv("INSTAGRAM_GRAPH_ACCESS_TOKEN")
        self.account_id = instagram_account_id or os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        self.base_url = "https://graph.facebook.com/v19.0"

    @property
    def provider_id(self) -> str:
        return "official_meta_graph_api"

    def is_configured(self) -> bool:
        return bool(self.access_token and self.account_id)

    async def validate_creator(self, identifier: str) -> bool:
        if not self.is_configured():
            logger.info("OfficialMetaProvider credentials not configured. Deferring validation.")
            return True

        try:
            creator_data = await self.fetch_creator(identifier)
            return bool(creator_data and creator_data.get("username"))
        except PermanentAcquisitionError:
            return False
        except Exception:
            return False

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        if not self.is_configured():
            raise PermanentAcquisitionError("OfficialMetaProvider missing INSTAGRAM_GRAPH_ACCESS_TOKEN or INSTAGRAM_BUSINESS_ACCOUNT_ID.")

        url = f"{self.base_url}/{self.account_id}"
        params = {
            "fields": f"business_discovery.username({identifier}){{id,name,username,profile_picture_url,biography,followers_count,media_count}}",
            "access_token": self.access_token
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                res = await client.get(url, params=params)
                if res.status_code == 429:
                    raise RateLimitExceededError("Meta Graph API Business Discovery rate limit exceeded.")
                elif res.status_code in (400, 404):
                    raise PermanentAcquisitionError(f"Instagram creator username '{identifier}' not found or not a Business/Creator account.")
                elif res.status_code >= 500:
                    raise TransientAcquisitionError(f"Meta Graph API server error: HTTP {res.status_code}")
                
                res.raise_for_status()
                data = res.json()
                discovery = data.get("business_discovery", {})
                
                return {
                    "name": discovery.get("name", identifier),
                    "username": discovery.get("username", identifier),
                    "platform": "instagram",
                    "profile_url": f"https://www.instagram.com/{identifier}/",
                    "is_active": True,
                    "external_id": discovery.get("id"),
                    "bio": discovery.get("biography"),
                    "followers_count": discovery.get("followers_count", 0)
                }
            except httpx.RequestError as exc:
                raise TransientAcquisitionError(f"Network error reaching Meta Graph API: {str(exc)}")

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.is_configured():
            raise PermanentAcquisitionError("OfficialMetaProvider missing configuration credentials.")

        url = f"{self.base_url}/{self.account_id}"
        params = {
            "fields": f"business_discovery.username({creator_identifier}){{media.limit({limit}){{id,caption,media_type,media_url,thumbnail_url,timestamp,permalink,children{{id,media_type,media_url}}}}}}",
            "access_token": self.access_token
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                res = await client.get(url, params=params)
                if res.status_code == 429:
                    raise RateLimitExceededError("Meta Graph API rate limit hit.")
                elif res.status_code >= 400:
                    raise PermanentAcquisitionError(f"Failed fetching Meta Business Discovery media for '{creator_identifier}': {res.text}")
                
                data = res.json()
                media_list = data.get("business_discovery", {}).get("media", {}).get("data", [])
                
                normalized_posts = []
                for item in media_list:
                    raw_type = item.get("media_type", "IMAGE").upper()
                    content_type = "reel" if raw_type == "VIDEO" else ("carousel" if raw_type == "CAROUSEL_ALBUM" else "image")
                    
                    media_objs = []
                    if raw_type == "CAROUSEL_ALBUM" and item.get("children", {}).get("data"):
                        for pos, child in enumerate(item["children"]["data"]):
                            media_objs.append({
                                "media_type": child.get("media_type", "IMAGE").lower(),
                                "media_url": child.get("media_url", ""),
                                "thumbnail_url": child.get("thumbnail_url"),
                                "position": pos
                            })
                    else:
                        media_objs.append({
                            "media_type": "video" if raw_type == "VIDEO" else "image",
                            "media_url": item.get("media_url", item.get("permalink", "")),
                            "thumbnail_url": item.get("thumbnail_url"),
                            "position": 0
                        })

                    normalized_posts.append({
                        "external_id": str(item.get("id")),
                        "url": item.get("permalink", f"https://instagram.com/p/{item.get('id')}"),
                        "content_type": content_type,
                        "caption": item.get("caption"),
                        "published_at": item.get("timestamp"),
                        "media": media_objs
                    })
                return normalized_posts
            except httpx.RequestError as exc:
                raise TransientAcquisitionError(f"Network error fetching Meta media: {str(exc)}")

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        posts = await self.fetch_latest_posts("self", limit=1)
        return posts[0] if posts else {}
