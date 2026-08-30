"""Test AI Provider Abstraction Interface."""
import pytest
from packages.ai import get_ai_provider, MockProvider, OpenAIProvider, GeminiProvider, AnthropicProvider, LocalProvider


@pytest.mark.asyncio
async def test_ai_provider_factory():
    provider = get_ai_provider("mock")
    assert isinstance(provider, MockProvider)
    assert provider.provider_name == "mock"

    openai_p = get_ai_provider("openai")
    assert isinstance(openai_p, OpenAIProvider)

    gemini_p = get_ai_provider("gemini")
    assert isinstance(gemini_p, GeminiProvider)


@pytest.mark.asyncio
async def test_mock_ai_provider_methods():
    provider = get_ai_provider("mock")

    # Test analyze_content
    analysis = await provider.analyze_content("Caption text", "Audio transcript", "reel")
    assert "hook" in analysis
    assert "narrative_structure" in analysis
    assert "relevance_score" in analysis

    # Test extract_pattern
    pattern = await provider.extract_pattern([analysis])
    assert "name" in pattern
    assert "structure" in pattern

    # Test personalize_opportunity
    opportunity = await provider.personalize_opportunity(
        analysis=analysis,
        user_profile={"niche": "Software Architecture"},
        knowledge_items=[{"title": "Decoupled Queue Design", "content": "Arq and Redis workers"}]
    )
    assert "title" in opportunity
    assert "concept" in opportunity
    assert opportunity["status"] == "draft"


def test_invalid_ai_provider_raises_error():
    with pytest.raises(ValueError, match="Unsupported AI Provider"):
        get_ai_provider("invalid_llm")
