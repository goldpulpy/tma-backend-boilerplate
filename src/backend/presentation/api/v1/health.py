"""Health check endpoint."""

import time
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from backend.application.use_cases.health import IHealthCheckUseCase
from backend.containers import Container
from backend.presentation.api.models.health import HealthCheckResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Check the health of the service",
    response_description="Health check response",
)
@inject
async def health_check(
    use_case: Annotated[
        IHealthCheckUseCase,
        Depends(Provide[Container.use_case.health_check]),
    ],
):
    """Health check endpoint."""
    health_status = await use_case.execute()

    if not health_status.db_connection:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is not healthy",
        )

    return HealthCheckResponse(
        status="ok",
        timestamp=int(time.time()),
    )
