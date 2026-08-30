"""FastAPI Application Main Entrypoint."""
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from packages.schemas.api import APIResponseEnvelope
from packages.shared.config import settings
from packages.shared.logging import get_logger
from apps.api.routers import health_router, config_router, creators_router, opportunities_router

logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Open-source creator-intelligence platform API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Context Tracing Middleware
@app.middleware("http")
async def request_tracing_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    response.headers["X-Request-ID"] = request_id
    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration:.3f}s",
        extra={"request_id": request_id}
    )
    return response


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Unhandled API Exception: {str(exc)}", exc_info=True, extra={"request_id": request_id})
    return JSONResponse(
        status_code=500,
        content=APIResponseEnvelope(
            success=False,
            error={
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected internal server error occurred."
            }
        ).model_dump()
    )


# Register Routers under /api/v1
app.include_router(health_router, prefix="/api/v1")
app.include_router(config_router, prefix="/api/v1")
app.include_router(creators_router, prefix="/api/v1")
app.include_router(opportunities_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
