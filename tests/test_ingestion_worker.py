"""Test Ingestion Worker Job Execution and Event Emission."""
import pytest
from sqlalchemy import select
from apps.api.models.creator import CreatorModel, CreatorStatusEnum
from apps.api.models.post import PostModel
from packages.shared.database import AsyncSessionLocal
from workers.jobs.ingestion import check_creator_job


@pytest.mark.asyncio
async def test_check_creator_job_execution():
    async with AsyncSessionLocal() as db:
        # Create test creator
        creator = CreatorModel(
            id="test_worker_creator_id",
            name="Worker Test Creator",
            username="workertest",
            platform="instagram",
            profile_url="https://instagram.com/workertest",
            is_active=True,
            status=CreatorStatusEnum.ACTIVE.value
        )
        db.add(creator)
        await db.commit()

    # Execute check_creator_job
    result = await check_creator_job({"job_id": "test_job_1"}, "test_worker_creator_id")
    assert result["status"] == "success"
    assert result["new_posts_count"] > 0
    assert len(result["emitted_events"]) > 0

    # Verify posts persisted in DB
    async with AsyncSessionLocal() as db:
        posts_stmt = select(PostModel).where(PostModel.creator_id == "test_worker_creator_id")
        posts_res = await db.execute(posts_stmt)
        posts = posts_res.scalars().all()
        assert len(posts) == result["new_posts_count"]
