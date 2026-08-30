"""Token Bucket Rate Limiter for Source Providers."""
import asyncio
import time
from typing import Dict


class TokenBucketRateLimiter:
    """In-memory rate limiter per platform source provider."""

    def __init__(self, rate_limit_per_minute: int = 60, max_concurrent: int = 5):
        self.rate_limit_per_minute = rate_limit_per_minute
        self.max_concurrent = max_concurrent
        self.tokens = float(rate_limit_per_minute)
        self.last_update = time.time()
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self._lock = asyncio.Lock()

    async def acquire(self):
        """Acquire capacity slot or wait if rate limited."""
        await self.semaphore.acquire()
        async with self._lock:
            now = time.time()
            elapsed = now - self.last_update
            self.last_update = now
            
            # Replenish tokens
            self.tokens = min(float(self.rate_limit_per_minute), self.tokens + elapsed * (self.rate_limit_per_minute / 60.0))

            if self.tokens < 1.0:
                wait_time = (1.0 - self.tokens) * (60.0 / self.rate_limit_per_minute)
                await asyncio.sleep(wait_time)
                self.tokens = 0.0
            else:
                self.tokens -= 1.0

    def release(self):
        """Release concurrency semaphore."""
        self.semaphore.release()


_LIMITER_REGISTRY: Dict[str, TokenBucketRateLimiter] = {}


def get_rate_limiter(platform: str, rate_limit_per_minute: int = 60, max_concurrent: int = 5) -> TokenBucketRateLimiter:
    """Retrieve or initialize token bucket rate limiter for platform."""
    if platform not in _LIMITER_REGISTRY:
        _LIMITER_REGISTRY[platform] = TokenBucketRateLimiter(rate_limit_per_minute, max_concurrent)
    return _LIMITER_REGISTRY[platform]
