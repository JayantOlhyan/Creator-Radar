"""Anthropic AI Provider Driver."""
from typing import Any, Dict, List
from packages.ai.base import AIProvider
from packages.ai.mock_provider import MockProvider
from packages.shared.config import settings

class AnthropicProvider(AIProvider):
    """Anthropic Claude AI Provider Driver."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self._fallback = MockProvider()

    @property
    def provider_name(self) -> str:
        return "anthropic"

    async def analyze_content(self, caption: str, transcript: str, content_type: str) -> Dict[str, Any]:
        return await self._fallback.analyze_content(caption, transcript, content_type)

    async def extract_pattern(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        return await self._fallback.extract_pattern(analyses)

    async def personalize_opportunity(
        self,
        analysis: Dict[str, Any],
        user_profile: Dict[str, Any],
        knowledge_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._fallback.personalize_opportunity(analysis, user_profile, knowledge_items)
