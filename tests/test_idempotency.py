"""Test Ingestion Pipeline Idempotency."""
import pytest
from sqlalchemy import select, func
from apps.api.models.creator import CreatorModel, CreatorStatusEnum
from apps.api.models.post import PostModel
from packages.shared.database import AsyncSessionLocal
from workers.jobs.ingestion import check_creator_job


@pytest.mark.asyncio
async def test_ingestion_idempotency():
    creator_id = "idempotent_creator_id"
    async with AsyncSessionLocal() as db:
        creator = CreatorModel(
            id=creator_id,
            name="Idempotency Test Creator",
            username="idempotent_user",
            platform="instagram",
            profile_url="https://instagram.com/idempotent_user",
            is_active=True,
            status=CreatorStatusEnum.ACTIVE.value
        )
        db.add(creator)
        await db.commit()

    # First Ingestion Run
    run1 = await check_creator_job({"job_id": "run_1"}, creator_id)
    assert run1["status"] == "success"
    initial_posts_count = run1["new_posts_count"]
    assert initial_posts_count > 0

    # Second Ingestion Run (Repeated Check)
    run2 = await check_creator_job({"job_id": "run_2"}, creator_id)
    assert run2["status"] == "success"
    assert run2["new_posts_count"] == 0
    assert len(run2["emitted_events"]) == 0

    # Verify Database Count Remains Unchanged
    async with AsyncSessionLocal() as db:
        count_stmt = select(func.count(PostModel.id)).where(PostModel.creator_id == creator_id)
        res = await db.execute(count_stmt)
        db_count = res.scalar()
        assert db_count == initial_posts_count
