"""Abstract Source Adapter Abstraction."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from packages.schemas.domain import CreatorSchema, PostSchema


class SourceAdapter(ABC):
    """Abstract Base Class for Content Source Adapters (Instagram, LinkedIn, YouTube, X, Reddit)."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Returns the identifier name of the platform (e.g. instagram, linkedin)."""
        pass

    @abstractmethod
    async def validate_creator(self, identifier: str) -> bool:
        """Validate whether a creator handle/identifier exists on the target platform."""
        pass

    @abstractmethod
    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        """Fetch platform profile metadata for a given creator identifier."""
        pass

    @abstractmethod
    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch the latest published posts for a creator."""
        pass

    @abstractmethod
    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        """Fetch detailed post payload for a specific post identifier."""
        pass
