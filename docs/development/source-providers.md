# CreatorRadar — Adding New Source Acquisition Providers

## Overview

CreatorRadar is designed to be easily extensible. Contributors can add support for new platform acquisition mechanisms (e.g. `YouTubeProvider`, `XProvider`, `RedditProvider`, `LinkedInProvider`) without modifying the core ingestion pipeline, database models, or downstream AI engines.

## Step-by-Step Implementation Guide

### Step 1: Implement `AcquisitionProvider` Base Class

Create a new file under `packages/source_adapters/providers/` (e.g. `youtube_provider.py`):

```python
from typing import Any, Dict, List
from packages.source_adapters.providers.base import AcquisitionProvider

class YouTubeProvider(AcquisitionProvider):
    @property
    def provider_id(self) -> str:
        return "youtube_data_api_v3"

    async def validate_creator(self, identifier: str) -> bool:
        # Validate channel handle / ID
        return True

    async def fetch_creator(self, identifier: str) -> Dict[str, Any]:
        return {
            "name": f"Channel {identifier}",
            "username": identifier,
            "platform": "youtube",
            "profile_url": f"https://youtube.com/@{identifier}",
            "is_active": True
        }

    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        # Fetch channel videos & normalize into CreatorRadar schema
        return [
            {
                "external_id": "video_123",
                "url": "https://youtube.com/watch?v=video_123",
                "content_type": "video",
                "caption": "Video title and description",
                "published_at": "2026-08-30T12:00:00Z",
                "media": [
                    {
                        "media_type": "video",
                        "media_url": "https://youtube.com/watch?v=video_123",
                        "position": 0
                    }
                ]
            }
        ]

    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]:
        # Fetch single video details
        return {}
```

### Step 2: Register Provider in Provider Registry

Add your provider to `packages/source_adapters/providers/__init__.py`:

```python
from packages.source_adapters.providers.youtube_provider import YouTubeProvider

_PROVIDER_REGISTRY = {
    "official_meta": OfficialMetaProvider,
    "external": ExternalProvider,
    "mock": MockAcquisitionProvider,
    "youtube": YouTubeProvider,
}
```

### Step 3: Implement Platform Adapter

Create `packages/source_adapters/youtube_adapter.py` extending `SourceAdapter`:

```python
from packages.source_adapters.base import SourceAdapter
from packages.source_adapters.providers.youtube_provider import YouTubeProvider

class YouTubeAdapter(SourceAdapter):
    def __init__(self):
        self.provider = YouTubeProvider()

    @property
    def platform_name(self) -> str:
        return "youtube"
```

Register `YouTubeAdapter` in `packages/source_adapters/__init__.py`.

### Step 4: Add Unit Tests

Add unit tests in `tests/test_source_acquisition.py` verifying creator validation, post normalization, and error handling.
