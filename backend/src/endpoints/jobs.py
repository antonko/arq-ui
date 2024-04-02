import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from core.config import Settings, get_app_settings
from core.depends import get_lru_cache, get_redis_settings
from fastapi import APIRouter, HTTPException, Query
from schemas.job import (
    Job,
    JobCreate,
    JobsInfo,
    JobSortBy,
    JobSortOrder,
    JobStatus,
    JobsTimeStatistics,
    Statistics,
)
from schemas.paged import Paged
from schemas.problem import ProblemDetail
from services.job_service import JobService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])
settings: Settings = get_app_settings()


@router.get(
    "",
    summary="Get all jobs",
    response_model=JobsInfo,
    responses={
        200: {
            "model": JobsInfo,
            "description": "Jobs successfully retrieved.",
        },
        422: {"description": "Data validation error.", "model": ProblemDetail},
        500: {"description": "Internal server error.", "model": ProblemDetail},
    },
)
async def get_all(
    limit: int = Query(
        default=50,
        le=500,
        ge=1,
        description="Maximum number of items to return.",
    ),
    offset: int = Query(default=0, description="Offset of the items."),
    sort_by: JobSortBy = Query(  # noqa: B008
        default=JobSortBy.enqueue_time,
        description="Field to sort by.",
    ),
    sort_order: JobSortOrder = Query(  # noqa: B008
        default=JobSortOrder.desc,
        description="Sort order.",
    ),
    statuses: list[JobStatus] = Query(  # noqa: B008
        default=[],
        description="Filter jobs by status.",
    ),
    success: bool | None = Query(  # noqa: B008
        None,
        description="Filter jobs by success status.",
    ),
    function: str | None = Query(  # noqa: B008
        None,
        description="Filter jobs by function name.",
    ),
    search: str | None = Query(  # noqa: B008
        None,
        description="Search for jobs by all fields.",
    ),
    start_time: datetime | None = Query(  # noqa: B008
        None,
        description="Filter jobs by start time.",
    ),
    finish_time: datetime | None = Query(  # noqa: B008
        None,
        description="Filter jobs by finish time.",
    ),
) -> JobsInfo:
    """Get all jobs."""
    job_service = JobService(
        get_redis_settings(),
        get_lru_cache(),
    )
    # We retrieve all tasks because we cannot initially filter them directly in Redis.
    # Subsequently, we filter them at the application level.
    # This code is simple, so we don't separate it out.
    jobs = await job_service.get_all_jobs(settings.max_jobs)

    functions: list[str] = list({job.function for job in jobs})
    statistics = Statistics(
        total=len(jobs),
        in_progress=len([job for job in jobs if job.status == JobStatus.in_progress]),
        completed=len([job for job in jobs if job.status == JobStatus.complete]),
        queued=len([job for job in jobs if job.status == JobStatus.queued]),
        failed=len(
            [job for job in jobs if job.status == JobStatus.complete and job.success is False],
        ),
    )

    time_statistic: list[JobsTimeStatistics] = job_service.generate_statistics(jobs)

    if start_time:
        start_time = start_time.replace(tzinfo=ZoneInfo(settings.timezone))
        jobs = [
            job
            for job in jobs
            if job.enqueue_time >= start_time
            and (job.start_time is None or job.start_time >= start_time)
        ]

    if finish_time:
        finish_time = finish_time.replace(tzinfo=ZoneInfo(settings.timezone))
        jobs = [
            job
            for job in jobs
            if job.enqueue_time <= finish_time
            and (job.finish_time is None or job.finish_time <= finish_time)
        ]

    if len(statuses) > 0:
        jobs = [job for job in jobs if job.status in statuses]

    if success is not None:
        jobs = [job for job in jobs if job.success == success]

    if function:
        jobs = [job for job in jobs if job.function == function]

    if search:
        jobs = [job for job in jobs if search.lower() in str(job).lower()]

    if sort_order == "asc":
        jobs = sorted(jobs, key=lambda x: (getattr(x, sort_by) is None, getattr(x, sort_by)))
    else:
        jobs = sorted(
            jobs,
            key=lambda x: (getattr(x, sort_by) is None, getattr(x, sort_by)),
            reverse=True,
        )

    paging_jobs = jobs[offset : offset + limit]

    return JobsInfo(
        functions=functions,
        statistics=statistics,
        statistics_hourly=time_statistic,
        paged_jobs=Paged[Job](
            items=paging_jobs,
            count=len(jobs),
            limit=limit,
            offset=offset,
        ),
    )


@router.get(
    "/{job_id}",
    summary="Get job by id",
    response_model=Job,
    responses={
        200: {
            "model": Job,
            "description": "Job successfully retrieved.",
        },
        404: {"description": "Job not found.", "model": ProblemDetail},
        422: {"description": "Data validation error.", "model": ProblemDetail},
        500: {"description": "Internal server error.", "model": ProblemDetail},
    },
)
async def get_job_by_id(job_id: str) -> Job:
    """Get job by id."""
    job_service = JobService(
        get_redis_settings(),
        get_lru_cache(),
    )
    job = await job_service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job with id {job_id} not found.",
        )
    return job


@router.delete(
    "/{job_id}",
    summary="Abort job",
    responses={
        200: {
            "description": "Job successfully aborted.",
        },
        400: {"description": "Failed to abort the job.", "model": ProblemDetail},
        422: {"description": "Data validation error.", "model": ProblemDetail},
        500: {"description": "Internal server error.", "model": ProblemDetail},
    },
)
async def abort_job(job_id: str) -> None:
    """Abort job."""
    job_service = JobService(
        get_redis_settings(),
        get_lru_cache(),
    )
    result: bool = await job_service.abort_job(job_id)
    if not result:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to abort the job with id {job_id}.",
        )


@router.get(
    "/statistics/hourly",
    summary="Get hourly statistics",
    response_model=list[JobsTimeStatistics],
    responses={
        200: {
            "model": list[JobsTimeStatistics],
            "description": "Hourly statistics successfully retrieved.",
        },
        422: {"description": "Data validation error.", "model": ProblemDetail},
        500: {"description": "Internal server error.", "model": ProblemDetail},
    },
)
async def get_hourly_statistics() -> list[JobsTimeStatistics]:
    """Get hourly statistics."""
    job_service = JobService(
        get_redis_settings(),
        get_lru_cache(),
    )
    jobs = await job_service.get_all_jobs(settings.max_jobs)

    return job_service.generate_statistics(jobs)


@router.post(
    "",
    summary="Create job",
    response_model=Job,
    responses={
        201: {
            "model": Job,
            "description": "Job successfully created.",
        },
        422: {"description": "Data validation error.", "model": ProblemDetail},
        500: {"description": "Internal server error.", "model": ProblemDetail},
    },
)
async def create_job(new_job: JobCreate) -> Job:
    """Create job."""
    logger.info(f"Creating job with function {new_job.function}.")
    raise HTTPException(
            status_code=501,
            detail="Not implemented",
        )
