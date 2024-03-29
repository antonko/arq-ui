import logging
from urllib.parse import urljoin

from fastapi.staticfiles import StaticFiles

from core.config import Settings, get_app_settings
from core.exception_handler import (
    all_exception_handler,
    custom_validation_exception_handler,
    http_exception_handler,
    starlette_http_exception_handler,
)
from core.helpers import join_paths_safely
from endpoints.api import routers
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def get_application() -> FastAPI:
    """Returns the FastAPI application instance."""
    settings: Settings = get_app_settings()
    application = FastAPI(
        separate_input_output_schemas=False,
        debug=settings.debug,
        title=settings.title,
        version=settings.version,
        description=settings.description,
        redoc_url= join_paths_safely(settings.root_path, settings.redoc_url),
        docs_url=join_paths_safely(settings.root_path, settings.docs_url),
        openapi_url=join_paths_safely(settings.root_path, settings.openapi_url),
        summary=settings.summary,
    )

    if settings.cors_allowed_hosts:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allowed_hosts,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    application.include_router(routers, prefix=join_paths_safely(settings.root_path, settings.api_prefix))

    application.add_exception_handler(RequestValidationError, custom_validation_exception_handler)  # type: ignore
    application.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    application.add_exception_handler(Exception, all_exception_handler)  # type: ignore
    application.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)  # type: ignore

    application.mount(join_paths_safely(settings.root_path, "ui"), StaticFiles(directory="static", html=True), name="static")

    return application


app = get_application()
