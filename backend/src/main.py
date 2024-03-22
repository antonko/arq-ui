from core.config import Settings, get_app_settings
from core.exception_handler import (
    all_exception_handler,
    custom_validation_exception_handler,
    http_exception_handler,
    starlette_http_exception_handler,
)
from endpoints.api import routers
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def get_application() -> FastAPI:
    """Returns the FastAPI application instance."""
    settings: Settings = get_app_settings()
    application = FastAPI(
        separate_input_output_schemas=False,
    )
    application.include_router(routers, prefix=settings.api_prefix)

    application.add_exception_handler(RequestValidationError, custom_validation_exception_handler)  # type: ignore
    application.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    application.add_exception_handler(Exception, all_exception_handler)  # type: ignore
    application.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)  # type: ignore

    return application


app = get_application()
