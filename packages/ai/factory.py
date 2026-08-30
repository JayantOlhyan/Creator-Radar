"""AI Provider Factory Module."""
from packages.ai.base import AIProvider
from packages.ai.openai_provider import OpenAIProvider
from packages.ai.gemini_provider import GeminiProvider
from packages.ai.anthropic_provider import AnthropicProvider
from packages.ai.local_provider import LocalProvider
from packages.ai.mock_provider import MockProvider
from packages.shared.config import settings

_AI_PROVIDER_REGISTRY = {
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "anthropic": AnthropicProvider,
    "local": LocalProvider,
    "mock": MockProvider,
}


def get_ai_provider(provider_name: str = None) -> AIProvider:
    """Instantiate AI provider based on name or system configuration."""
    target_name = (provider_name or settings.AI_PROVIDER).lower()
    provider_cls = _AI_PROVIDER_REGISTRY.get(target_name)
    if not provider_cls:
        raise ValueError(
            f"Unsupported AI Provider: '{target_name}'. Available: {list(_AI_PROVIDER_REGISTRY.keys())}"
        )
    return provider_cls()
