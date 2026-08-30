# CreatorRadar — Multi-Stage AI Pipeline Architecture

## Philosophical Foundation: Inspiration ≠ Replication

CreatorRadar explicitly rejects automatic content copying, script reproduction, or word-for-word generation.

Instead, the AI Pipeline dissects source content into **structural mechanisms** and synthesizes **original opportunities** grounded in the user's personal knowledge base.

## Pipeline Architecture

```text
Raw Content & Transcript
          │
          ▼
┌───────────────────────────┐
│ 1. Content Analysis Job   │ ──► Extracts topic, hook mechanism, narrative pacing,
└─────────┬─────────────────┘     emotional triggers, CTA, why it works
          │
          ▼
┌───────────────────────────┐
│ 2. Pattern Extraction Job │ ──► Discovers reusable structural blueprints across posts
└─────────┬─────────────────┘
          │
          ▼
┌───────────────────────────┐
│ 3. Personalization Job    │ ──► Combines pattern + user profile + user knowledge items
└─────────┬─────────────────┘     to construct original angle
          │
          ▼
┌───────────────────────────┐
│ 4. Scoring Engine         │ ──► Scores relevance, originality, effort, priority
└───────────────────────────┘
```

## AI Provider Abstraction Interface

Users can switch LLM backends via the `AI_PROVIDER` configuration setting without altering business logic.

```python
class AIProvider(ABC):
    @abstractmethod
    async def analyze_content(self, caption: str, transcript: str, content_type: str) -> Dict[str, Any]: ...

    @abstractmethod
    async def extract_pattern(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]: ...

    @abstractmethod
    async def personalize_opportunity(self, analysis: Dict[str, Any], user_profile: Dict[str, Any], knowledge_items: List[Dict[str, Any]]) -> Dict[str, Any]: ...
```

Supported drivers: `OpenAIProvider`, `GeminiProvider`, `AnthropicProvider`, `LocalProvider` (Ollama), `MockProvider`.
