"""Configuration Status API Endpoint."""
from fastapi import APIRouter
from packages.schemas.api import APIResponseEnvelope
from packages.shared.config import settings

router = APIRouter(prefix="/config", tags=["Configuration"])


@router.get("", response_model=APIResponseEnvelope[dict])
async def get_system_config():
    """Retrieve sanitized active system settings and configured abstraction drivers."""
    return APIResponseEnvelope(
        success=True,
        data={
            "app_name": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "ai_provider": settings.AI_PROVIDER,
            "supported_source_adapters": ["instagram", "linkedin", "mock"],
            "supported_ai_providers": ["openai", "gemini", "anthropic", "local", "mock"],
            "features": {
                "async_pipeline": True,
                "telegram_notifications": bool(settings.TELEGRAM_BOT_TOKEN),
            }
        }
    )
