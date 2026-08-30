"""Media Transcription Job Handler."""
from packages.shared.logging import get_logger

logger = get_logger(__name__)


async def transcribe_media_job(ctx: dict, post_id: str, media_url: str) -> dict:
    """Async worker job: Extract audio/video transcript."""
    job_id = ctx.get("job_id", "local_job")
    logger.info(f"Executing transcribe_media_job for post_id: {post_id}", extra={"job_id": job_id, "post_id": post_id})

    return {
        "status": "completed",
        "post_id": post_id,
        "transcript_text": "Sample audio transcript extracted from creator post media."
    }
