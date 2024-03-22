from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, Field


class ProblemDetail(BaseModel):
    """Represents a problem detail."""

    type: str = Field(
        ...,
        description="A URI reference that identifies the problem type.",
        examples=["validation_error"],
    )
    title: str = Field(
        ...,
        description="A short, human-readable summary of the problem type.",
        examples=["Validation Error"],
    )
    text: str | None = Field(
        None,
        description="A human-readable explanation specific to this occurrence of the problem.",
        examples=["Input should be a valid boolean, unable to interpret input"],
    )
    status: int = Field(
        ...,
        description="""
        The HTTP status code generated by the origin server for this occurrence of the problem.
        """,
        examples=[422],
    )
    detail: Sequence[dict[str, Any]] | None = Field(
        None,
        description="""
        A human-readable explanation specific to this occurrence of the problem.
        Can be a string or an object with nested fields.""",
        examples=[
            {
                "type": "bool_parsing",
                "loc": ["query", "is_active"],
                "msg": "Input should be a valid boolean, unable to interpret input",
                "input": "12",
                "url": "https://errors.pydantic.dev/2.6/v/bool_parsing",
            },
        ],
    )
