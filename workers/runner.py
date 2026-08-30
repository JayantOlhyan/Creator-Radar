"""Arq Async Worker Settings and Entrypoint."""
import asyncio
from arq.connections import RedisSettings
from packages.shared.config import settings
from packages.shared.logging import get_logger
from workers.jobs import (
    ingest_post_job,
    transcribe_media_job,
    analyze_content_job,
    personalize_opportunity_job,
    deliver_notification_job,
)
from workers.jobs.ingestion import check_creator_job
from workers.scheduler import poll_watchlist_creators_job

logger = get_logger(__name__)


async def startup(ctx: dict):
    logger.info("Initializing Worker Process and Queue Listener...")


async def shutdown(ctx: dict):
    logger.info("Shutting down Worker Process gracefully...")


class WorkerSettings:
    """Arq Worker Configuration Settings."""

    functions = [
        check_creator_job,
        poll_watchlist_creators_job,
        ingest_post_job,
        transcribe_media_job,
        analyze_content_job,
        personalize_opportunity_job,
        deliver_notification_job,
    ]

    # Periodic cron schedule every 15 minutes to poll due creators
    cron_jobs = [
        # (function, minute, hour, day, month, weekday)
    ]

    on_startup = startup
    on_shutdown = shutdown

    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )
    max_jobs = 10
    poll_delay = 0.5


if __name__ == "__main__":
    logger.info("Starting CreatorRadar Background Worker...")
    from arq import run_worker
    run_worker(WorkerSettings)
