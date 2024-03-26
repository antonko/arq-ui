import asyncio
import logging
from zoneinfo import ZoneInfo

import arq
import arq.constants
import arq.jobs
from arq import create_pool
from arq.connections import RedisSettings
from arq.jobs import Job as ArqJob
from core.cache import LRUCache
from core.config import Settings, get_app_settings
from schemas.job import Job

settings: Settings = get_app_settings()


class JobService:
    """Service class for interacting with Arq jobs."""

    def __init__(
        self,
        redis_settings: RedisSettings,
        cache: LRUCache,
        request_semaphore_jobs: int = 5,
    ) -> None:
        self.redis_settings = redis_settings
        self.cache = cache
        self.request_semaphore_jobs = request_semaphore_jobs
        self.logger = logging.getLogger(__name__)

    async def get_status(self) -> dict[str, str]:
        """Get status redis."""
        redis = await create_pool(self.redis_settings)
        keys_queued = await redis.keys(arq.constants.job_key_prefix + "*")
        keys_results = await redis.keys(arq.constants.result_key_prefix + "*")

        processed_keys = keys_queued + keys_results
        return {"jobs_len": str(len(processed_keys))}

    async def fetch_job_info(
        self,
        semaphore: asyncio.Semaphore,
        redis: arq.ArqRedis,
        key_id: str,
    ) -> Job | None:
        """Fetch job information."""
        cached_result = self.cache.get(key_id)
        if cached_result:
            return cached_result

        async with semaphore:
            key_id_without_prefix = key_id.replace(arq.constants.job_key_prefix, "").replace(
                arq.constants.result_key_prefix,
                "",
            )

            arq_job = ArqJob(key_id_without_prefix, redis)
            status = await arq_job.status()

            if status == arq.jobs.JobStatus.complete:
                complete_key: str = arq.constants.result_key_prefix + key_id_without_prefix
                redis_raw = await redis.get(complete_key)
                job_result: arq.jobs.JobResult = arq.jobs.deserialize_result(redis_raw)

                job_schema = Job(
                    id=key_id_without_prefix,
                    enqueue_time=job_result.enqueue_time,
                    status=status.value,
                    function=job_result.function,
                    args=job_result.args,
                    kwargs=str(job_result.kwargs) if job_result.kwargs else None,
                    job_try=job_result.job_try,
                    result=str(job_result.result) if job_result.result else None,
                    success=job_result.success,
                    start_time=job_result.start_time.replace(tzinfo=ZoneInfo(settings.timezone)),
                    finish_time=job_result.finish_time.replace(tzinfo=ZoneInfo(settings.timezone)),
                    queue_name=job_result.queue_name,
                    execution_duration=(job_result.finish_time - job_result.start_time)
                    .total_seconds()
                    .is_integer(),
                )
                # Cache only completed jobs
                self.cache.set(key_id, job_schema)

            else:
                keys_queued_job = arq.constants.job_key_prefix + key_id_without_prefix
                redis_raw = await redis.get(keys_queued_job)
                job: arq.jobs.JobDef = arq.jobs.deserialize_job(redis_raw)
                job_schema = Job(
                    id=key_id_without_prefix,
                    enqueue_time=job.enqueue_time.replace(tzinfo=ZoneInfo(settings.timezone)),
                    status=status.value,
                    function=job.function,
                    args=job.args,
                    kwargs=str(job.kwargs) if job.kwargs else None,
                    job_try=job.job_try,
                )
            return job_schema

    async def get_all_jobs(self, max_jobs: int = 50000) -> list[Job]:
        """Get all jobs."""
        redis = await create_pool(self.redis_settings)
        keys_queued = await redis.keys(arq.constants.job_key_prefix + "*")
        keys_results = await redis.keys(arq.constants.result_key_prefix + "*")

        processed_keys = [key.decode() for key in keys_queued + keys_results]

        if len(processed_keys) > max_jobs:
            raise ValueError("There are too many keys in Redis, processing has been halted.")

        semaphore = asyncio.Semaphore(self.request_semaphore_jobs)

        tasks = [self.fetch_job_info(semaphore, redis, key_id) for key_id in processed_keys]
        jobs_task = await asyncio.gather(*tasks)
        jobs: list[Job] = [job for job in jobs_task if job is not None]
        return jobs

    async def get_job_by_id(self, job_id: str) -> Job | None:
        """Get job by id."""
        redis = await create_pool(self.redis_settings)
        key_id = arq.constants.job_key_prefix + job_id
        return await self.fetch_job_info(
            asyncio.Semaphore(self.request_semaphore_jobs),
            redis,
            key_id,
        )

    async def abort_job(self, job_id: str) -> bool:
        """Abort job."""
        redis = await create_pool(self.redis_settings)
        job: ArqJob = ArqJob(job_id, redis)
        return await job.abort()
