"""Abstract Acquisition Provider Contract."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AcquisitionProvider(ABC):
    """Abstract Base Class for Acquisition Providers (Official Meta, External Proxy, Mock)."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Unique identifier of the acquisition provider."""
        pass

    @abstractmethod
    async def validate_creator(self, identifier: str) -> bool:
        """Validate if creator profile handle is valid and accessible via provider."""
        pass

    @abstractmethod
    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        """Fetch creator profile metadata."""
        pass

    @abstractmethod
    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch latest published content items from creator profile."""
        pass

    @abstractmethod
    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        """Fetch details for a specific post identifier."""
        pass
