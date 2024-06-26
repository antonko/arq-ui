from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from zoneinfo import ZoneInfo

from core.config import Settings, get_app_settings
from pydantic import BaseModel, Field
from schemas.paged import Paged

settings: Settings = get_app_settings()


class JobStatus(str, Enum):
    """Enumeration for job status options."""

    deferred = "deferred"
    queued = "queued"
    in_progress = "in_progress"
    complete = "complete"
    not_found = "not_found"


class ColorStatistics(str, Enum):
    """Represents a color."""

    red = "red"
    green = "green"
    gray = "gray"
    orange = "orange"


class JobsTimeStatistics(BaseModel):
    """Represents statistics for jobs over a period of time."""

    date: datetime = Field(
        default=...,
        description="Date and time for the statistics",
        examples=["2024-03-24T17:32:30.587000+00:00"],
    )

    total_created: int = Field(
        default=0,
        description="Total number of jobs created",
        examples=[100],
    )

    total_completed_successfully: int = Field(
        default=0,
        description="Total number of jobs completed successfully",
        examples=[100],
    )

    total_failed: int = Field(
        default=0,
        description="Total number of jobs failed",
        examples=[100],
    )
    total_in_progress: int = Field(
        default=0,
        description="Total number of jobs in progress",
        examples=[100],
    )

    color: ColorStatistics = Field(
        default=ColorStatistics.gray,
        description="Color for the statistics",
        examples=["red"],
    )

    color_intensity: float = Field(
        default=1.0,
        description="Color intensity for the statistics",
        examples=[1.0],
    )


class Job(BaseModel):
    """Represents a job."""

    id: str = Field(
        alias="id",
        serialization_alias="id",
        description="Unique identifier for the job",
        examples=["f0c9d0944f1b4763b261ab5d49581321"],
    )

    status: JobStatus = Field(
        default=JobStatus.not_found,
        description="Status of the job",
        examples=["complete"],
    )

    success: bool = Field(
        default=False,
        description="Indicates whether the job was successfully completed",
        examples=[True],
    )

    enqueue_time: datetime = Field(
        description="Date and time when the job was enqueued",
        examples=["2024-03-24T17:32:30.587000+00:00"],
    )

    result: str | None = Field(
        default=None,
        description="Result string of the job",
        examples=["ok"],
    )

    start_time: datetime | None = Field(
        default=None,
        description="Date and time when the job was started",
        examples=["2024-03-24T17:32:30.587000+00:00"],
    )

    finish_time: datetime | None = Field(
        default=None,
        description="Date and time when the job was finished",
        examples=["2024-03-24T17:32:30.587000+00:00"],
    )

    queue_name: str | None = Field(
        default=None,
        description="Name of the queue in which the job was enqueued",
        examples=["arq:queue"],
    )

    execution_duration: float | None = Field(
        default=None,
        description="Duration of the job execution in seconds, including milliseconds",
        examples=[0],
    )

    function: str = Field(
        ...,
        description="Name of the function that was executed by the job",
        examples=["download_content"],
    )

    args: list[Any] | None = Field(
        default=None,
        description="Arguments passed to the function that was executed by the job",
        examples=[["https://florm.io"]],
    )

    kwargs: str | None = Field(
        default=None,
        description="Keyword arguments passed to the function that was executed by the job",
        examples=[],
    )

    job_try: int | None = Field(
        default=None,
        description="Number of times the job was tried",
        examples=[1],
    )

    class Config:
        """Pydantic model configuration."""

        json_encoders = {
            datetime: lambda v: v.astimezone(ZoneInfo(settings.timezone)).isoformat(),
        }


class JobCreate(BaseModel):
    """Represents a job creation request."""

    function: str = Field(..., description="Name of the function to execute")

    args: list[Any] = Field(
        default_factory=list,
        description="Positional arguments of the function",
    )

    job_id: str | None = Field(None, description="Job identifier")

    queue_name: str | None = Field(None, description="Name of the queue")

    defer_until: datetime | None = Field(
        None,
        description="Postpone execution until the specified date/time",
    )

    expires: timedelta | None = Field(
        None,
        description="Set the expiration time for the job",
    )

    kwargs: dict[str, Any] = Field(
        default_factory=dict,
        description="Named arguments of the function",
    )

    class Config:
        """Pydantic model configuration."""

        json_encoders = {
            datetime: lambda v: v.astimezone(ZoneInfo(settings.timezone)).isoformat(),
        }


class Statistics(BaseModel):
    """Represents statistics for jobs."""

    total: int = Field(
        default=0,
        description="Total number of jobs",
        examples=[100],
    )

    completed: int = Field(
        default=0,
        description="Number of completed jobs",
        examples=[100],
    )

    in_progress: int = Field(
        default=0,
        description="Number of jobs in progress",
        examples=[100],
    )

    queued: int = Field(
        default=0,
        description="Number of queued jobs",
        examples=[100],
    )

    failed: int = Field(
        default=0,
        description="Number of jobs with errors",
        examples=[100],
    )


class JobsInfo(BaseModel):
    """Represents information about jobs."""

    functions: list[str] = Field(
        default=[],
        description="List of unique function names",
        examples=["download_content"],
    )

    statistics: Statistics = Field(
        default_factory=Statistics,
        description="Statistics for jobs",
    )

    paged_jobs: Paged[Job] | None = Field(
        default_factory=None,
        description="Paged response containing a list of jobs",
    )

    statistics_hourly: list[JobsTimeStatistics] = Field(
        default_factory=list,
        description="List of time statistics for jobs",
    )


class JobSortBy(str, Enum):
    """Enumeration for sorting options."""

    id = "id"
    enqueue_time = "enqueue_time"
    start_time = "start_time"
    finish_time = "finish_time"
    execution_duration = "execution_duration"
    function = "function"
    status = "status"
    success = "success"
    queue_name = "queue_name"
    args = "args"
    kwargs = "kwargs"
    job_try = "job_try"


class JobSortOrder(str, Enum):
    """Enumeration for sort order options."""

    asc = "asc"
    desc = "desc"
