import logging

from core.config import Settings, get_app_settings
from core.depends import get_lru_cache, get_redis_settings
from fastapi import APIRouter
from services.job_service import JobService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/status", tags=["Status"])
settings: Settings = get_app_settings()


@router.get("")
async def status() -> dict[str, str]:
    """Get status redis."""
    job_service = JobService(get_redis_settings(), get_lru_cache())
    result: dict[str, str] = await job_service.get_status()
    return result
