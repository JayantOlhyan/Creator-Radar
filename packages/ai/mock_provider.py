"""Mock AI Provider Implementation for Local Dev & Testing."""
from typing import Any, Dict, List
from packages.ai.base import AIProvider


class MockProvider(AIProvider):
    """Mock AI Provider delivering deterministic structured responses."""

    @property
    def provider_name(self) -> str:
        return "mock"

    async def analyze_content(self, caption: str, transcript: str, content_type: str) -> Dict[str, Any]:
        return {
            "topic": "System Architecture Optimization",
            "hook": "Stop hardcoding external API dependencies into core domain models.",
            "hook_type": "contrarian_statement",
            "format": content_type or "carousel",
            "narrative_structure": "Problem -> Anti-Pattern -> Refactored Architecture -> Result",
            "target_audience": "Software Engineers & Architects",
            "emotional_trigger": "curiosity_and_fear_of_tech_debt",
            "cta": "Save this guide for your next refactor.",
            "visual_structure": "Dark code snippets with highlighted contrast lines",
            "editing_style": "Fast pacing with code diff highlights",
            "content_mechanism": "Demonstrating clean abstraction pattern vs spaghetti tight coupling",
            "why_it_works": "Directly targets pain point of architectural refactoring costs.",
            "relevance_score": 8.5,
            "originality_score": 8.0
        }

    async def extract_pattern(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "name": "Contrarian Tech Architecture Teardown",
            "description": "Exposing common engineering mistakes and presenting a decoupled architectural fix.",
            "structure": "Contrarian Hook -> Flawed Conventional Wisdom -> Decoupled Schema -> Benchmark Result",
            "example_count": len(analyses)
        }

    async def personalize_opportunity(
        self,
        analysis: Dict[str, Any],
        user_profile: Dict[str, Any],
        knowledge_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        user_topic = knowledge_items[0]["title"] if knowledge_items else "Async Python Backend Design"
        return {
            "title": f"Why We Decoupled Our Async Pipeline in {user_topic}",
            "hook": f"Most devs couple their queue directly to their HTTP handlers. Here is why we separated them.",
            "concept": "Applying clean adapter pattern to queue and database layers.",
            "format": "technical_breakdown",
            "reasoning": "Uses the underlying structural mechanism (decoupling architecture) applied strictly to user's domain expertise.",
            "relevance_score": 9.0,
            "originality_score": 9.5,
            "effort_score": 5.0,
            "priority_score": 8.8,
            "status": "draft"
        }
