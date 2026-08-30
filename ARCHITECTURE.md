# CreatorRadar — System Architecture Overview

## Key Design Principles

1. **Platform Agnostic Core**:
   Core domain entities (`Creator`, `Post`, `PostMedia`, `PostAnalysis`, `ContentPattern`, `KnowledgeItem`, `ContentOpportunity`, `Notification`) contain zero platform-specific logic.

2. **Source Adapter Interface**:
   ```python
   class SourceAdapter(ABC):
       async def validate_creator(self, identifier: str) -> bool: ...
       async def fetch_creator(self, identifier: str) -> dict: ...
       async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> list[dict]: ...
       async def fetch_post(self, post_identifier: str) -> dict: ...
   ```

3. **AI Provider Abstraction**:
   ```python
   class AIProvider(ABC):
       async def analyze_content(self, caption: str, transcript: str, content_type: str) -> dict: ...
       async def extract_pattern(self, analyses: list[dict]) -> dict: ...
       async def personalize_opportunity(self, analysis: dict, user_profile: dict, knowledge_items: list[dict]) -> dict: ...
   ```

4. **Asynchronous Queue Architecture**:
   FastAPI web endpoints validate and queue jobs into Redis. Independent Python Arq workers execute heavy media extraction, transcription, LLM analysis, and notification delivery asynchronously.
