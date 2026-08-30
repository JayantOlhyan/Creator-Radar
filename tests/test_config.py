"""Test Configuration Loading."""
import pytest
from packages.shared.config import settings, Settings


def test_settings_defaults():
    assert settings.APP_NAME == "CreatorRadar"
    assert settings.LOG_LEVEL in ["INFO", "DEBUG", "WARN", "ERROR"]
    assert settings.DATABASE_URL is not None
    assert settings.REDIS_URL is not None


def test_settings_instantiation():
    custom_settings = Settings(APP_ENV="test", AI_PROVIDER="mock")
    assert custom_settings.APP_ENV == "test"
    assert custom_settings.AI_PROVIDER == "mock"
