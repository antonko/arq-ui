import asyncio
import logging

import arq
import arq.constants
import arq.jobs
from arq import create_pool
from arq.connections import RedisSettings
from arq.jobs import Job as ArqJob
from core.cache import LRUCache
from schemas.job import Job


class ArqService:
    """Service class for interacting with Arq jobs."""

    def __init__(self, redis_settings: RedisSettings, cache: LRUCache) -> None:
        self.redis_settings = redis_settings
        self.cache = cache
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

            arq_job = ArqJob(key_id_without_prefix, redis, _deserializer=redis.job_deserializer)
            redis_raw = await redis.get(key_id)
            status = await arq_job.status()

            if status == arq.jobs.JobStatus.complete:
                job_result: arq.jobs.JobResult = arq.jobs.deserialize_result(
                    redis_raw,
                    deserializer=redis.job_deserializer,
                )

                job_schema = Job(
                    id=key_id,
                    enqueue_time=job_result.enqueue_time,
                    status=status.value,
                    function=job_result.function,
                    args=job_result.args,
                    kwargs=job_result.kwargs,
                    job_try=job_result.job_try,
                    result=repr(job_result.result) if job_result.result else None,
                    success=job_result.success,
                    start_time=job_result.start_time,
                    finish_time=job_result.finish_time,
                    queue_name=job_result.queue_name,
                    execution_duration=(job_result.finish_time - job_result.start_time)
                    .total_seconds()
                    .is_integer(),
                )
                self.cache.set(key_id, job_schema)

            else:
                job: arq.jobs.JobDef = arq.jobs.deserialize_job(
                    redis_raw,
                    deserializer=redis.job_deserializer,
                )
                job_schema = Job(
                    id=key_id,
                    enqueue_time=job.enqueue_time,
                    status=status.value,
                    function=job.function,
                    args=job.args,
                    kwargs=job.kwargs,
                    job_try=job.job_try,
                )
            return job_schema

    async def get_all_jobs(self) -> list[Job]:
        """Get all jobs."""
        redis = await create_pool(self.redis_settings)
        keys_queued = await redis.keys(arq.constants.job_key_prefix + "*")
        keys_results = await redis.keys(arq.constants.result_key_prefix + "*")

        processed_keys = [key.decode() for key in keys_queued + keys_results]

        semaphore = asyncio.Semaphore(5)

        tasks = [self.fetch_job_info(semaphore, redis, key_id) for key_id in processed_keys]
        jobs_task = await asyncio.gather(*tasks)
        jobs: list[Job] = [job for job in jobs_task if job is not None]
        # TODO Фильтрация по дате
        return jobs
