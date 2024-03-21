import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("")
async def get_all() -> dict[str, str]:
    """Get all jobs."""
    return {"message": "Get all jobs."}
