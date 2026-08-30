"""Local AI Provider Driver (Ollama / Local LLM Endpoint)."""
from typing import Any, Dict, List
from packages.ai.base import AIProvider
from packages.ai.mock_provider import MockProvider
from packages.shared.config import settings

class LocalProvider(AIProvider):
    """Local LLM AI Provider Driver (e.g. Ollama / LocalAI)."""

    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint or settings.LOCAL_AI_ENDPOINT
        self._fallback = MockProvider()

    @property
    def provider_name(self) -> str:
        return "local"

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
