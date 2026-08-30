"""Abstract AI Provider Specification."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from packages.schemas.domain import PostAnalysisSchema, ContentOpportunitySchema, UserProfileSchema, KnowledgeItemSchema


class AIProvider(ABC):
    """Abstract Base Class for AI Model Providers (OpenAI, Gemini, Anthropic, Local, Mock)."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name identifier of the AI provider."""
        pass

    @abstractmethod
    async def analyze_content(self, caption: str, transcript: str, content_type: str) -> Dict[str, Any]:
        """Analyze content and extract structural mechanisms (hook, narrative, audience, why it works)."""
        pass

    @abstractmethod
    async def extract_pattern(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract a reusable content pattern across multiple post analyses."""
        pass

    @abstractmethod
    async def personalize_opportunity(
        self,
        analysis: Dict[str, Any],
        user_profile: Dict[str, Any],
        knowledge_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate an original content opportunity tailored to user knowledge without replicating original."""
        pass
