"""Creator Watchlist Polling Scheduler."""
import asyncio
from datetime import datetime, timedelta
from typing import List
from sqlalchemy import select
from packages.shared import database
from packages.shared.logging import get_logger
from apps.api.models.creator import CreatorModel, CreatorStatusEnum
from workers.jobs.ingestion import check_creator_job

logger = get_logger(__name__)


async def find_creators_due_for_check() -> List[str]:
    """Query active creators where (last_checked_at IS NULL OR last_checked_at + check_interval_minutes < NOW())."""
    async with database.AsyncSessionLocal() as db:
        now = datetime.utcnow()
        stmt = select(CreatorModel.id, CreatorModel.last_checked_at, CreatorModel.check_interval_minutes).where(
            CreatorModel.status == CreatorStatusEnum.ACTIVE.value,
            CreatorModel.is_active.is_(True)
        )
        res = await db.execute(stmt)
        rows = res.all()

        due_creator_ids = []
        for creator_id, last_checked_at, interval_min in rows:
            if not last_checked_at:
                due_creator_ids.append(creator_id)
            else:
                next_check_due = last_checked_at + timedelta(minutes=interval_min or 60)
                if now >= next_check_due:
                    due_creator_ids.append(creator_id)

        return due_creator_ids


async def poll_watchlist_creators_job(ctx: dict = None):
    """Scheduler task executing periodic watchlist checks."""
    logger.info("Scheduler polling for watchlist creators due for acquisition check...")
    due_ids = await find_creators_due_for_check()
    logger.info(f"Found {len(due_ids)} creators due for acquisition check.")

    results = []
    for creator_id in due_ids:
        try:
            res = await check_creator_job(ctx or {}, creator_id)
            results.append(res)
        except Exception as exc:
            logger.error(f"Error checking creator {creator_id}: {str(exc)}")

    return {"polled_count": len(due_ids), "results": results}


if __name__ == "__main__":
    logger.info("Starting CreatorRadar Polling Scheduler Loop...")
    asyncio.run(poll_watchlist_creators_job())
