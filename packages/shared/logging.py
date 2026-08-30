"""Structured JSON Logging & Redaction System."""
import json
import logging
import re
import sys
from typing import Any, Dict


# Sensitive fields that must be redacted from log messages or extras
SENSITIVE_KEYS = {
    "password", "secret", "token", "api_key", "authorization",
    "openai_api_key", "gemini_api_key", "anthropic_api_key", "telegram_bot_token"
}


def sanitize_data(data: Any) -> Any:
    """Recursively mask sensitive values in dictionaries and lists."""
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in SENSITIVE_KEYS):
                cleaned[key] = "[REDACTED]"
            else:
                cleaned[key] = sanitize_data(value)
        return cleaned
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    elif isinstance(data, str):
        # Mask potential bearer tokens or API key strings in raw text
        if re.search(r'(sk-[a-zA-Z0-9]{20,})', data):
            return re.sub(r'(sk-[a-zA-Z0-9]{20,})', '[REDACTED_API_KEY]', data)
        return data
    return data


class StructuredJsonFormatter(logging.Formatter):
    """JSON Formatter adding contextual traceability attributes."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": sanitize_data(record.getMessage()),
        }

        # Inject tracing IDs if present in log record context
        for trace_id in ("request_id", "job_id", "post_id", "creator_id", "user_id"):
            if hasattr(record, trace_id):
                log_entry[trace_id] = getattr(record, trace_id)

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def get_logger(name: str) -> logging.Logger:
    """Retrieve structured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
