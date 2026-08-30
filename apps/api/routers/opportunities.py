"""Opportunities API Endpoint Stubs."""
from fastapi import APIRouter
from packages.schemas.api import APIResponseEnvelope

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.get("", response_model=APIResponseEnvelope[list])
async def list_opportunities():
    """List content opportunities (Foundation Stub)."""
    return APIResponseEnvelope(
        success=True,
        data=[
            {
                "id": "stub_opp_1",
                "title": "Decoupled Async Pipeline Architecture",
                "hook": "Why coupling queue handlers directly to HTTP routes breaks under high traffic.",
                "concept": "Demonstrating clean separation between API request validation and background job execution.",
                "format": "technical_breakdown",
                "reasoning": "Uses contrarian architecture teardown pattern applied to Python async backends.",
                "relevance_score": 9.2,
                "originality_score": 9.0,
                "effort_score": 4.5,
                "priority_score": 9.1,
                "status": "draft"
            }
        ]
    )
