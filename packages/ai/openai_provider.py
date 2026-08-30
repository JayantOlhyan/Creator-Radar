"""OpenAI AI Provider Implementation Driver."""
from typing import Any, Dict, List
from packages.ai.base import AIProvider
from packages.ai.mock_provider import MockProvider
from packages.shared.config import settings
from packages.shared.logging import get_logger

logger = get_logger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI AI Provider Driver."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self._fallback = MockProvider()

    @property
    def provider_name(self) -> str:
        return "openai"

    async def analyze_content(self, caption: str, transcript: str, content_type: str) -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            logger.warning("OpenAI API key missing or default. Falling back to mock implementation.")
            return await self._fallback.analyze_content(caption, transcript, content_type)

        # Structure for real OpenAI API client call in subsequent phases
        return await self._fallback.analyze_content(caption, transcript, content_type)

    async def extract_pattern(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return await self._fallback.extract_pattern(analyses)

        return await self._fallback.extract_pattern(analyses)

    async def personalize_opportunity(
        self,
        analysis: Dict[str, Any],
        user_profile: Dict[str, Any],
        knowledge_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return await self._fallback.personalize_opportunity(analysis, user_profile, knowledge_items)

        return await self._fallback.personalize_opportunity(analysis, user_profile, knowledge_items)
