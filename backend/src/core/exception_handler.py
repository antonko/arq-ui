import logging

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from schemas.problem import ProblemDetail
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("tickets")


async def custom_validation_exception_handler(
    request: Request,  # noqa: ARG001
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle custom validation exceptions.

    Args:
    ----
        request (Request): The request object.
        exc (RequestValidationError): The validation exception.

    Returns:
    -------
        JSONResponse: The JSON response.

    """
    logger.error(exc.errors())
    problem_detail = ProblemDetail(
        type="validation_error",
        title="Error validation",
        text="The request was invalid.",
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=exc.errors(),
    )
    return JSONResponse(
        content=problem_detail.model_dump(exclude_none=True),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:  # noqa: ARG001
    """Handle HTTP exceptions and return a JSON response.

    Args:
    ----
        request (Request): The request object.
        exc (HTTPException): The HTTP exception.

    Returns:
    -------
        JSONResponse: The JSON response.

    """
    logger.error(exc.detail)
    problem_detail = ProblemDetail(
        type="internal_server_error",
        status=exc.status_code,
        title="Internal server error",
        text=exc.detail or "An unexpected error occurred.",
        detail=[],
    )

    match exc.status_code:
        case status.HTTP_403_FORBIDDEN:
            problem_detail = ProblemDetail(
                type="forbidden",
                title="Error access",
                text=exc.detail or "User does not have access rights.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_404_NOT_FOUND:
            problem_detail = ProblemDetail(
                type="not_found",
                title="Resource not found",
                text=exc.detail or "The requested resource was not found.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_405_METHOD_NOT_ALLOWED:
            problem_detail = ProblemDetail(
                type="method_not_allowed",
                title="Method not allowed",
                text=exc.detail or "Method not allowed for this resource.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            problem_detail = ProblemDetail(
                type="internal_server_error",
                title="Internal server error",
                text=exc.detail or "An unexpected error occurred.",
                status=exc.status_code,
                detail=[],
            )

    return JSONResponse(
        content=problem_detail.model_dump(exclude_none=True),
        status_code=exc.status_code,
    )


async def all_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    """Handle all unhandled exceptions and return a JSON response.

    Args:
    ----
        request (Request): The request object.
        exc (Exception): The unhandled exception.

    Returns:
    -------
        JSONResponse: The JSON response.

    """
    logger.error(exc)
    problem_detail = ProblemDetail(
        type="internal_server_error",
        title="Internal server error",
        text="An unexpected error occurred.",
        status=500,
        detail=[],
    )
    return JSONResponse(
        content=problem_detail.model_dump(exclude_none=True),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def starlette_http_exception_handler(
    request: Request,  # noqa: ARG001
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Handle Starlette HTTP exceptions and return a JSON response."""
    logger.error(exc.detail)
    problem_detail = ProblemDetail(
        type="internal_server_error",
        status=exc.status_code,
        title="Internal server error",
        text=exc.detail or "An unexpected error occurred.",
        detail=[],
    )

    match exc.status_code:
        case status.HTTP_403_FORBIDDEN:
            problem_detail = ProblemDetail(
                type="forbidden",
                title="Error access",
                text=exc.detail or "User does not have access rights.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_404_NOT_FOUND:
            problem_detail = ProblemDetail(
                type="not_found",
                title="Resource not found",
                text=exc.detail or "The requested resource was not found.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_405_METHOD_NOT_ALLOWED:
            problem_detail = ProblemDetail(
                type="method_not_allowed",
                title="Method not allowed",
                text=exc.detail or "Method not allowed for this resource.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_400_BAD_REQUEST:
            problem_detail = ProblemDetail(
                type="bad_request",
                title="Bad request",
                text=exc.detail or "The request was invalid.",
                status=exc.status_code,
                detail=[],
            )
        case status.HTTP_500_INTERNAL_SERVER_ERROR:
            problem_detail = ProblemDetail(
                type="internal_server_error",
                title="Internal server error",
                text=exc.detail or "An unexpected error occurred.",
                status=exc.status_code,
                detail=[],
            )

    return JSONResponse(
        content=problem_detail.model_dump(exclude_none=True),
        status_code=exc.status_code,
    )
