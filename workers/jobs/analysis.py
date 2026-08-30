"""AI Content Analysis Job Handler."""
from packages.ai import get_ai_provider
from packages.shared.logging import get_logger

logger = get_logger(__name__)


async def analyze_content_job(ctx: dict, post_id: str, caption: str, transcript: str, content_type: str) -> dict:
    """Async worker job: Perform structural AI analysis on post content."""
    job_id = ctx.get("job_id", "local_job")
    logger.info(f"Executing analyze_content_job for post_id: {post_id}", extra={"job_id": job_id, "post_id": post_id})

    ai_provider = get_ai_provider()
    analysis_result = await ai_provider.analyze_content(caption, transcript, content_type)

    return {
        "status": "completed",
        "post_id": post_id,
        "analysis": analysis_result
    }
