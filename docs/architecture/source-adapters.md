# CreatorRadar — Source Adapter Specification & Compliance Framework

## Overview

CreatorRadar is strictly platform-agnostic. The core domain layer has no knowledge of platform-specific SDKs or endpoints. All platform interactions are routed through the `SourceAdapter` interface.

## Critical Platform Acquisition Constraint

> CreatorRadar cannot assume unrestricted access to arbitrary Instagram, LinkedIn, or social media public content.

To comply with this constraint:

1. **Replaceable Acquisition Mechanism**: The system relies on pluggable acquisition mechanisms.
2. **No Undocumented Private APIs**: The architecture explicitly forbids hardcoding unauthenticated or fragile private endpoint scraping logic directly into the domain models.
3. **Compliant Provider Integration**: Phase 1 will evaluate compliant acquisition mechanisms (official platform APIs, user-authenticated webhooks, compliance data export tools).

## Abstract Contract

```python
class SourceAdapter(ABC):
    @property
    @abstractmethod
    def platform_name(self) -> str: ...

    @abstractmethod
    async def validate_creator(self, identifier: str) -> bool: ...

    @abstractmethod
    async def fetch_creator(self, identifier: str) -> Dict[str, Any]: ...

    @abstractmethod
    async def fetch_latest_posts(self, creator_identifier: str, limit: int = 10) -> List[Dict[str, Any]]: ...

    @abstractmethod
    async def fetch_post(self, post_identifier: str) -> Dict[str, Any]: ...
```

## Supported Adapters Topology

```text
SourceAdapter (Abstract Base)
├── InstagramAdapter (Stub in Phase 0 -> Compliant acquisition mechanism in Phase 1)
├── LinkedInAdapter (Stub in Phase 0)
├── YouTubeAdapter (Future)
├── XAdapter (Future)
└── MockAdapter (Testing / Contract Verification)
```
