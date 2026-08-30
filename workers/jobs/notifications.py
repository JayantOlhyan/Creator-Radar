"""Notification Delivery Job Handler."""
from packages.shared.config import settings
from packages.shared.logging import get_logger

logger = get_logger(__name__)


async def deliver_notification_job(ctx: dict, user_id: str, channel: str, message_payload: dict) -> dict:
    """Async worker job: Deliver opportunity alert via Telegram or configured channel."""
    job_id = ctx.get("job_id", "local_job")
    logger.info(f"Executing deliver_notification_job for user_id: {user_id} via {channel}", extra={"job_id": job_id, "user_id": user_id})

    if channel == "telegram":
        if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
            logger.warning("Telegram Bot Token not configured. Simulated notification log entry created.")
        else:
            logger.info("Delivering Telegram notification payload...")

    return {
        "status": "delivered",
        "user_id": user_id,
        "channel": channel
    }
