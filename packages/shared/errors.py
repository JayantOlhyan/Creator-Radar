"""Acquisition Exception Hierarchy and Error Sanitizer."""
import re
from typing import Optional


class AcquisitionError(Exception):
    """Base exception for all source content acquisition failures."""
    def __init__(self, message: str, is_transient: bool = False):
        super().__init__(message)
        self.message = sanitize_error_message(message)
        self.is_transient = is_transient


class TransientAcquisitionError(AcquisitionError):
    """Temporary network or server errors eligible for retry."""
    def __init__(self, message: str):
        super().__init__(message, is_transient=True)


class PermanentAcquisitionError(AcquisitionError):
    """Non-retryable errors (invalid handle, 404 profile, permanent auth failure)."""
    def __init__(self, message: str):
        super().__init__(message, is_transient=False)


class RateLimitExceededError(TransientAcquisitionError):
    """Rate limit throttled error."""
    def __init__(self, message: str = "Source provider rate limit exceeded."):
        super().__init__(message)


def sanitize_error_message(message: str) -> str:
    """Sanitize raw error messages to prevent storing API keys, bearer tokens, or stack trace secrets."""
    if not message:
        return "Unknown acquisition error."

    # Mask API keys, tokens, auth headers
    sanitized = re.sub(r'(access_token|api_key|bearer|token)=([a-zA-Z0-9_\-\.]+)', r'\1=[REDACTED]', message, flags=re.IGNORECASE)
    sanitized = re.sub(r'Bearer\s+[a-zA-Z0-9_\-\.]+', 'Bearer [REDACTED]', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'sk-[a-zA-Z0-9]{20,}', '[REDACTED_KEY]', sanitized)
    
    # Truncate overly long error traces
    if len(sanitized) > 500:
        sanitized = sanitized[:497] + "..."
    return sanitized
