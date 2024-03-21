from fastapi import FastAPI


def get_application() -> FastAPI:
    """Returns the FastAPI application instance."""
    return FastAPI(
        separate_input_output_schemas=False,
    )


app = get_application()
