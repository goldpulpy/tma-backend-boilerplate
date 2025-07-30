"""Include documentation in the app."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference


def setup_scalar(app: FastAPI) -> None:
    """Set up documentation for the app.

    Args:
        app: FastAPI app

    Returns:
        None

    """

    @app.get("/docs", include_in_schema=False)
    async def api_documentation() -> HTMLResponse:
        """Scalar API reference.

        Returns:
            Scalar API reference

        """
        return get_scalar_api_reference(
            openapi_url=app.openapi_url or "",
            title="Backend API Documentation",
        )
