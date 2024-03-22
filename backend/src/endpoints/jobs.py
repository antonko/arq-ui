import logging

from core.depends import get_lru_cache, get_redis_settings
from fastapi import APIRouter, Query
from schemas.job import JobSortBy, JobSortOrder, JobStatus, PagedJobs, Statistics
from schemas.problem import ProblemDetail
from services.arq_service import ArqService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "",
    summary="Get all jobs",
    response_model=PagedJobs,
    responses={
        200: {
            "model": PagedJobs,
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
    queue_name: str | None = Query(  # noqa: B008
        None,
        description="Filter jobs by queue name.",
    ),
    function: str | None = Query(  # noqa: B008
        None,
        description="Filter jobs by function name.",
    ),
    search: str | None = Query(  # noqa: B008
        None,
        description="Search for jobs by all fields.",
    ),
) -> PagedJobs:
    """Get all jobs."""
    arq_service = ArqService(get_redis_settings(), get_lru_cache())
    jobs = await arq_service.get_all_jobs()

    functions: list[str] = list({job.function for job in jobs})
    statistics = Statistics(
        total=len(jobs),
        in_progress=len([job for job in jobs if job.status == JobStatus.in_progress]),
        completed=len([job for job in jobs if job.status == JobStatus.complete]),
        queued=len([job for job in jobs if job.status == JobStatus.queued]),
        failed=len([job for job in jobs if job.success is False]),
    )

    if len(statuses) > 0:
        jobs = [job for job in jobs if job.status in statuses]

    if success is not None:
        jobs = [job for job in jobs if job.success == success]

    if queue_name:
        jobs = [job for job in jobs if job.queue_name == queue_name]

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

    return PagedJobs(
        items=paging_jobs,
        functions=functions,
        statistics=statistics,
        count=len(jobs),
        limit=limit,
        offset=offset,
    )
