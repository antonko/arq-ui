import logging

import arq
import arq.constants
import arq.jobs
from arq import create_pool
from arq.connections import RedisSettings
from core.config import Settings, get_app_settings
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/status", tags=["Status"])
settings: Settings = get_app_settings()


@router.get("")
async def status() -> dict[str, str]:
    """Get status redis."""
    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        database=settings.redis_db,
        password=settings.redis_password,
        ssl=settings.redis_ssl,
        ssl_cert_reqs=settings.redis_ssl_cert_reqs,
    )
    redis = await create_pool(redis_settings)
    keys_queued = await redis.keys(arq.constants.job_key_prefix + "*")
    keys_results = await redis.keys(arq.constants.result_key_prefix + "*")

    processed_keys = keys_queued + keys_results
    return {"jobs_len": str(len(processed_keys))}
