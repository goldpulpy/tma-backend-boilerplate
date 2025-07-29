"""Health check endpoint."""

from fastapi import APIRouter, status

from backend.presentation.api.models.health import HealthCheckResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Check if the server is running",
    response_description="Health check response",
)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(status="ok")
