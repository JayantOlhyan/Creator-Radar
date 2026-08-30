"""Idempotent Post Ingestion Worker Job."""
from datetime import datetime
import uuid
from typing import Any, Dict
from sqlalchemy import select
from packages.schemas.events import PostDetectedEvent
from packages.source_adapters import get_source_adapter
from packages.shared import database
from packages.shared.errors import AcquisitionError, TransientAcquisitionError, PermanentAcquisitionError, sanitize_error_message
from packages.shared.logging import get_logger
from apps.api.models.creator import CreatorModel, CreatorStatusEnum
from apps.api.models.post import PostModel, PostMediaModel

logger = get_logger(__name__)


async def check_creator_job(ctx: Dict[str, Any], creator_id: str) -> Dict[str, Any]:
    """Execute idempotent post acquisition check for a creator."""
    job_id = ctx.get("job_id", str(uuid.uuid4()))
    logger.info(f"Starting check_creator_job for creator_id: {creator_id}", extra={"job_id": job_id, "creator_id": creator_id})

    async with database.AsyncSessionLocal() as db:
        stmt = select(CreatorModel).where(CreatorModel.id == creator_id)
        res = await db.execute(stmt)
        creator = res.scalar_one_or_none()

        if not creator:
            logger.error(f"Creator '{creator_id}' not found in database.", extra={"job_id": job_id})
            return {"status": "failed", "reason": "creator_not_found"}

        if creator.status in (CreatorStatusEnum.INACTIVE.value, CreatorStatusEnum.UNSUPPORTED.value):
            logger.info(f"Skipping check for creator '{creator.username}' in status '{creator.status}'", extra={"job_id": job_id})
            return {"status": "skipped", "reason": f"status_{creator.status}"}

        now = datetime.utcnow()
        username = creator.username
        platform = creator.platform
        creator.last_checked_at = now

        try:
            adapter = get_source_adapter(platform)
            fetched_posts = await adapter.fetch_latest_posts(username, limit=10)

            new_posts_count = 0
            emitted_events = []

            for post_item in fetched_posts:
                ext_id = str(post_item.get("external_id"))
                if not ext_id:
                    continue

                # App-level deduplication check
                dup_stmt = select(PostModel.id).where(
                    PostModel.creator_id == creator.id,
                    PostModel.external_id == ext_id
                )
                dup_res = await db.execute(dup_stmt)
                if dup_res.scalar_one_or_none():
                    logger.debug(f"Post external_id '{ext_id}' already exists. Skipping duplicate.", extra={"job_id": job_id, "post_id": ext_id})
                    continue

                # Parse published_at timestamp safely
                pub_at = None
                if post_item.get("published_at"):
                    try:
                        pub_str = str(post_item["published_at"]).replace("Z", "+00:00")
                        pub_at = datetime.fromisoformat(pub_str)
                    except Exception:
                        pub_at = now

                # Normalize content type
                c_type = str(post_item.get("content_type", "post")).lower()
                if c_type not in ("post", "reel", "carousel", "video", "image", "unknown"):
                    c_type = "post"

                post_db_id = str(uuid.uuid4())
                new_post = PostModel(
                    id=post_db_id,
                    creator_id=creator.id,
                    external_id=ext_id,
                    url=post_item.get("url", f"https://{platform}.com/p/{ext_id}"),
                    content_type=c_type,
                    caption=post_item.get("caption"),
                    published_at=pub_at,
                    detected_at=now,
                    status="detected",
                    created_at=now
                )
                db.add(new_post)

                # Media normalization
                raw_media = post_item.get("media", [])
                for idx, m_item in enumerate(raw_media):
                    media_record = PostMediaModel(
                        id=str(uuid.uuid4()),
                        post_id=post_db_id,
                        media_type=m_item.get("media_type", "image"),
                        media_url=m_item.get("media_url", ""),
                        thumbnail_url=m_item.get("thumbnail_url"),
                        mime_type=m_item.get("mime_type"),
                        duration=m_item.get("duration"),
                        width=m_item.get("width"),
                        height=m_item.get("height"),
                        position=m_item.get("position", idx)
                    )
                    db.add(media_record)

                new_posts_count += 1

                # Construct post.detected event
                event = PostDetectedEvent(
                    event_id=str(uuid.uuid4()),
                    producer="workers.jobs.ingestion",
                    creator_id=creator.id,
                    external_id=ext_id,
                    platform=platform,
                    url=new_post.url
                )
                emitted_events.append(event.model_dump())

            # Update success status
            creator.status = CreatorStatusEnum.ACTIVE.value
            creator.last_successful_check_at = now
            creator.last_error_message = None
            await db.commit()

            logger.info(
                f"Successfully checked @{username}. Discovered {new_posts_count} new posts.",
                extra={"job_id": job_id, "creator_id": creator_id}
            )

            return {
                "status": "success",
                "creator_id": creator_id,
                "username": username,
                "fetched_count": len(fetched_posts),
                "new_posts_count": new_posts_count,
                "emitted_events": emitted_events
            }

        except Exception as exc:
            await db.rollback()
            clean_msg = sanitize_error_message(str(exc))
            logger.error(f"Acquisition error for @{username}: {clean_msg}", extra={"job_id": job_id})

            # Re-query or update creator object after rollback
            re_stmt = select(CreatorModel).where(CreatorModel.id == creator_id)
            re_res = await db.execute(re_stmt)
            curr_creator = re_res.scalar_one_or_none()
            if curr_creator:
                curr_creator.last_error_at = datetime.utcnow()
                curr_creator.last_error_message = clean_msg

                if isinstance(exc, PermanentAcquisitionError):
                    curr_creator.status = CreatorStatusEnum.ERROR.value
                elif isinstance(exc, TransientAcquisitionError):
                    curr_creator.status = CreatorStatusEnum.ERROR.value
                else:
                    curr_creator.status = CreatorStatusEnum.ERROR.value

                await db.commit()

            return {
                "status": "failed",
                "creator_id": creator_id,
                "error": clean_msg,
                "is_transient": getattr(exc, "is_transient", False)
            }


async def ingest_post_job(ctx: Dict[str, Any], post_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy helper endpoint delegating to check_creator_job."""
    creator_id = post_data.get("creator_id")
    if creator_id:
        return await check_creator_job(ctx, creator_id)
    return {"status": "skipped", "reason": "missing_creator_id"}
