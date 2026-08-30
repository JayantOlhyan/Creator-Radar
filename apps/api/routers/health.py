"""System Health API Endpoint."""
import time
from fastapi import APIRouter
from redis.asyncio import Redis
from sqlalchemy import text
from packages.schemas.api import APIResponseEnvelope
from packages.shared.config import settings
from packages.shared.database import engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=APIResponseEnvelope[dict])
async def health_check():
    """Detailed health check endpoint verifying Database, Redis, and API operational status."""
    db_status = "unknown"
    redis_status = "unknown"

    # Test Postgres DB Connection
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    # Test Redis Connection
    try:
        redis_client = Redis.from_url(settings.REDIS_URL, socket_timeout=2.0)
        await redis_client.ping()
        await redis_client.aclose()
        redis_status = "healthy"
    except Exception as exc:
        redis_status = f"unhealthy: {str(exc)}"

    is_overall_healthy = (db_status == "healthy" and redis_status == "healthy")

    return APIResponseEnvelope(
        success=is_overall_healthy,
        data={
            "status": "healthy" if is_overall_healthy else "degraded",
            "app_name": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "timestamp": time.time(),
            "services": {
                "database": db_status,
                "redis": redis_status,
                "api": "healthy"
            }
        }
    )
