"""Creator Watchlist REST API Router."""
from datetime import datetime
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from packages.schemas.api import APIResponseEnvelope, APIErrorDetails
from packages.schemas.domain import (
    CreatorSchema, CreatorCreateSchema, CreatorUpdateSchema,
    CreatorStatusEnum, PlatformEnum, PostSchema
)
from packages.source_adapters import get_source_adapter
from packages.shared.database import get_db_session
from packages.shared.logging import get_logger
from apps.api.models.creator import CreatorModel, CreatorSourceModel
from apps.api.models.post import PostModel

logger = get_logger(__name__)

router = APIRouter(prefix="/creators", tags=["Creators Watchlist"])


@router.post("", response_model=APIResponseEnvelope[CreatorSchema], status_code=status.HTTP_201_CREATED)
async def create_creator(
    payload: CreatorCreateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """Add a creator to the CreatorRadar Watchlist with handle validation."""
    username = payload.username.strip().lstrip("@").lower()
    platform_str = payload.platform.value if isinstance(payload.platform, PlatformEnum) else payload.platform

    # Check for duplicate creator (username + platform)
    existing_stmt = select(CreatorModel).where(
        CreatorModel.username == username,
        CreatorModel.platform == platform_str
    )
    existing_res = await db.execute(existing_stmt)
    if existing_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Creator '@{username}' on platform '{platform_str}' is already being monitored."
        )

    # Validate handle via SourceAdapter
    try:
        adapter = get_source_adapter(platform_str)
        is_valid = await adapter.validate_creator(username)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid or inaccessible creator handle '@{username}' on {platform_str}."
            )
        profile_meta = await adapter.fetch_creator(username)
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning(f"Creator validation failed for @{username}: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not validate creator '@{username}' on {platform_str}: {str(exc)}"
        )

    profile_url = payload.profile_url or profile_meta.get("profile_url") or f"https://www.{platform_str}.com/{username}/"
    creator_name = profile_meta.get("name") or username.title()

    new_creator = CreatorModel(
        id=str(uuid.uuid4()),
        name=creator_name,
        username=username,
        platform=platform_str,
        profile_url=profile_url,
        is_active=True,
        status=CreatorStatusEnum.ACTIVE.value,
        check_interval_minutes=payload.check_interval_minutes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_creator)
    await db.commit()
    await db.refresh(new_creator)

    return APIResponseEnvelope(
        success=True,
        data=CreatorSchema.model_validate(new_creator)
    )


@router.get("", response_model=APIResponseEnvelope[List[CreatorSchema]])
async def list_creators(
    platform: Optional[str] = Query(None, description="Filter by platform"),
    status: Optional[str] = Query(None, description="Filter by status (ACTIVE, INACTIVE, ERROR, UNSUPPORTED)"),
    db: AsyncSession = Depends(get_db_session)
):
    """List monitored creators on the Watchlist."""
    stmt = select(CreatorModel)
    if platform:
        stmt = stmt.where(CreatorModel.platform == platform.lower())
    if status:
        stmt = stmt.where(CreatorModel.status == status.upper())
    
    stmt = stmt.order_by(CreatorModel.created_at.desc())
    result = await db.execute(stmt)
    creators = result.scalars().all()

    return APIResponseEnvelope(
        success=True,
        data=[CreatorSchema.model_validate(c) for c in creators]
    )


@router.get("/{creator_id}", response_model=APIResponseEnvelope[dict])
async def get_creator_detail(
    creator_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Get detailed creator monitoring information and recent detected posts."""
    stmt = select(CreatorModel).options(selectinload(CreatorModel.posts)).where(CreatorModel.id == creator_id)
    res = await db.execute(stmt)
    creator = res.scalar_one_or_none()

    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator with ID '{creator_id}' not found."
        )

    # Fetch recent posts
    posts_stmt = select(PostModel).options(selectinload(PostModel.media)).where(PostModel.creator_id == creator_id).order_by(PostModel.detected_at.desc()).limit(10)
    posts_res = await db.execute(posts_stmt)
    recent_posts = posts_res.scalars().all()

    creator_data = CreatorSchema.model_validate(creator).model_dump()
    creator_data["posts_count"] = len(creator.posts)
    creator_data["recent_posts"] = [PostSchema.model_validate(p).model_dump() for p in recent_posts]

    return APIResponseEnvelope(
        success=True,
        data=creator_data
    )


@router.patch("/{creator_id}", response_model=APIResponseEnvelope[CreatorSchema])
async def update_creator(
    creator_id: str,
    payload: CreatorUpdateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """Update creator monitoring status, check interval, or active state."""
    stmt = select(CreatorModel).where(CreatorModel.id == creator_id)
    res = await db.execute(stmt)
    creator = res.scalar_one_or_none()

    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator with ID '{creator_id}' not found."
        )

    if payload.name is not None:
        creator.name = payload.name
    if payload.is_active is not None:
        creator.is_active = payload.is_active
        creator.status = CreatorStatusEnum.ACTIVE.value if payload.is_active else CreatorStatusEnum.INACTIVE.value
    if payload.status is not None:
        creator.status = payload.status.value if isinstance(payload.status, CreatorStatusEnum) else payload.status
        creator.is_active = (creator.status == CreatorStatusEnum.ACTIVE.value)
    if payload.check_interval_minutes is not None:
        creator.check_interval_minutes = payload.check_interval_minutes

    creator.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(creator)

    return APIResponseEnvelope(
        success=True,
        data=CreatorSchema.model_validate(creator)
    )


@router.delete("/{creator_id}", response_model=APIResponseEnvelope[dict])
async def delete_creator(
    creator_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Remove a creator from the Watchlist and delete associated records."""
    stmt = select(CreatorModel).where(CreatorModel.id == creator_id)
    res = await db.execute(stmt)
    creator = res.scalar_one_or_none()

    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator with ID '{creator_id}' not found."
        )

    await db.delete(creator)
    await db.commit()

    return APIResponseEnvelope(
        success=True,
        data={"id": creator_id, "deleted": True}
    )


@router.post("/{creator_id}/check", response_model=APIResponseEnvelope[dict])
async def trigger_creator_check(
    creator_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Trigger an immediate background acquisition check for a creator."""
    stmt = select(CreatorModel).where(CreatorModel.id == creator_id)
    res = await db.execute(stmt)
    creator = res.scalar_one_or_none()

    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator with ID '{creator_id}' not found."
        )

    # Execute check_creator logic directly or queue job
    from workers.jobs.ingestion import check_creator_job
    result = await check_creator_job({"job_id": f"manual_{uuid.uuid4()}"}, creator_id)

    return APIResponseEnvelope(
        success=True,
        data={
            "creator_id": creator_id,
            "username": creator.username,
            "result": result
        }
    )
