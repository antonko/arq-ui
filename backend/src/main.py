from core.config import Settings, get_app_settings
from endpoints.api import routers
from fastapi import FastAPI


def get_application() -> FastAPI:
    """Returns the FastAPI application instance."""
    settings: Settings = get_app_settings()
    application = FastAPI(
        separate_input_output_schemas=False,
    )
    application.include_router(routers, prefix=settings.api_prefix)

    return application


app = get_application()
