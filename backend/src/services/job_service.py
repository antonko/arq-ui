import asyncio
import logging
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import arq
import arq.constants
import arq.jobs
from arq import create_pool
from arq.connections import RedisSettings
from arq.jobs import Job as ArqJob
from core.cache import LRUCache
from core.config import Settings, get_app_settings
from schemas.job import ColorStatistics, Job, JobCreate, JobStatus, JobsTimeStatistics

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
                    execution_duration=int(
                        (job_result.finish_time - job_result.start_time).total_seconds(),
                    ),
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
            raise ValueError(f"There are too many tasks in Redis (max {max_jobs}), I won't work.")

        semaphore = asyncio.Semaphore(self.request_semaphore_jobs)

        tasks = [self.fetch_job_info(semaphore, redis, key_id) for key_id in processed_keys]
        jobs_task = await asyncio.gather(*tasks)
        jobs: list[Job] = [job for job in jobs_task if job is not None]

        twenty_four_hours_ago = datetime.now(UTC) - timedelta(hours=1)
        return [
            job
            for job in jobs
            if job.enqueue_time >= twenty_four_hours_ago
            or (job.start_time and job.start_time >= twenty_four_hours_ago)
        ]

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

    def adjust_color_intensity(self, color_intensity: float) -> float:
        """Adjust color intensity."""
        if color_intensity < 0.4:  # noqa: PLR2004
            return 0.3
        if color_intensity < 0.6:  # noqa: PLR2004
            return 0.5
        if color_intensity < 0.8:  # noqa: PLR2004
            return 0.7

        return 1.0

    def generate_statistics(self, jobs_list: list[Job]) -> list[JobsTimeStatistics]:  # noqa: PLR0912, C901
        """Generate statistics for jobs."""
        # TODO: This function is too complex. It should be refactored.
        max_time_diff = 60

        one_hour_ago = datetime.now(UTC).replace(second=0, microsecond=0) - timedelta(hours=1)
        current_minute = (datetime.now(UTC) - one_hour_ago).total_seconds() // 60

        statistics = [
            JobsTimeStatistics(date=(one_hour_ago + timedelta(minutes=i)))
            for i in range(max_time_diff)
        ]
        for job in jobs_list:
            created_diff = (job.enqueue_time - one_hour_ago).total_seconds() // 60
            if 0 <= created_diff < max_time_diff:
                statistics[int(created_diff)].total_created += 1

            if job.status == JobStatus.in_progress and job.start_time:
                start_diff = int((job.start_time - one_hour_ago).total_seconds() // 60)
                for i in range(start_diff, min(int(current_minute) + 1, max_time_diff)):
                    statistics[i].total_in_progress += 1

            if job.status == JobStatus.complete and job.start_time and job.finish_time:
                start_diff = int((job.start_time - one_hour_ago).total_seconds() // 60)
                finish_diff = int((job.finish_time - one_hour_ago).total_seconds() // 60)
                for i in range(start_diff, min(finish_diff + 1, max_time_diff)):
                    statistics[i].total_in_progress += 1
                if finish_diff < max_time_diff:
                    if job.success:
                        statistics[finish_diff].total_completed_successfully += 1
                    else:
                        statistics[finish_diff].total_failed += 1

        max_jobs = max(
            stat.total_completed_successfully + stat.total_in_progress for stat in statistics
        )

        for stat in statistics:
            current_jobs = stat.total_completed_successfully + stat.total_in_progress
            color_intensity = round(current_jobs / max_jobs, 1) if max_jobs > 0 else 1.0
            stat.color_intensity = self.adjust_color_intensity(color_intensity)

            if stat.total_completed_successfully == 0 and stat.total_failed == 0:
                stat.color = ColorStatistics.gray
                stat.color_intensity = 1
            elif stat.total_failed == 0 and stat.total_completed_successfully > 0:
                stat.color = ColorStatistics.green
            elif stat.total_completed_successfully == 0 and stat.total_failed > 0:
                stat.color = ColorStatistics.red
            else:
                stat.color = ColorStatistics.orange

        return statistics

    async def create_job(self, new_job: JobCreate) -> Job | None:
        """Create a new job."""
        redis = await create_pool(self.redis_settings)
        await redis.enqueue_job(
            new_job.function,
            *new_job.args,
            _job_id=new_job.job_id,
            _queue_name=new_job.queue_name,
            _defer_until=new_job.defer_until,
            _expires=new_job.expires,
            **new_job.kwargs,
        )

        return None
