"""Opportunity Personalization Job Handler."""
from packages.ai import get_ai_provider
from packages.shared.logging import get_logger

logger = get_logger(__name__)


async def personalize_opportunity_job(
    ctx: dict,
    analysis_data: dict,
    user_profile: dict,
    knowledge_items: list
) -> dict:
    """Async worker job: Generate personalized content opportunity without copying source content."""
    job_id = ctx.get("job_id", "local_job")
    logger.info("Executing personalize_opportunity_job", extra={"job_id": job_id})

    ai_provider = get_ai_provider()
    opportunity = await ai_provider.personalize_opportunity(analysis_data, user_profile, knowledge_items)

    return {
        "status": "generated",
        "opportunity": opportunity
    }
