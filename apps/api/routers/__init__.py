"""API Routers Package."""
from apps.api.routers.health import router as health_router
from apps.api.routers.config import router as config_router
from apps.api.routers.creators import router as creators_router
from apps.api.routers.opportunities import router as opportunities_router

__all__ = [
    "health_router",
    "config_router",
    "creators_router",
    "opportunities_router",
]
