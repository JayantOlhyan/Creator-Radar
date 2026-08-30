"""Test Ingestion Acquisition Error Handling, Sanitization, and Lifecycle Transitions."""
import pytest
from sqlalchemy import select
from apps.api.models.creator import CreatorModel, CreatorStatusEnum
from packages.shared.database import AsyncSessionLocal
from workers.jobs.ingestion import check_creator_job


@pytest.mark.asyncio
async def test_permanent_acquisition_failure_transitions_to_error_state():
    creator_id = "perm_fail_creator_id"
    async with AsyncSessionLocal() as db:
        creator = CreatorModel(
            id=creator_id,
            name="Permanent Error Creator",
            username="permanent_error_creator",
            platform="instagram",
            profile_url="https://instagram.com/permanent_error_creator",
            is_active=True,
            status=CreatorStatusEnum.ACTIVE.value
        )
        db.add(creator)
        await db.commit()

    # Execute check job on permanent failure mock user
    result = await check_creator_job({"job_id": "job_fail_1"}, creator_id)
    assert result["status"] == "failed"

    # Verify Creator State updated to ERROR with sanitized message
    async with AsyncSessionLocal() as db:
        stmt = select(CreatorModel).where(CreatorModel.id == creator_id)
        res = await db.execute(stmt)
        updated_creator = res.scalar_one()
        assert updated_creator.status == CreatorStatusEnum.ERROR.value
        assert updated_creator.last_error_message is not None
        assert "access_token" not in updated_creator.last_error_message
