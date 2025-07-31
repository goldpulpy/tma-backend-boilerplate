"""Health check endpoint."""

from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from backend.application.use_cases.health import IHealthCheckUseCase
from backend.containers.services import ServiceContainer
from backend.containers.use_cases import ServiceUseCaseContainer
from backend.presentation.api.models.health import HealthCheckResponse

router = APIRouter(tags=["Health"])
limiter = ServiceContainer.limiter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Check the health of the service",
    response_description="Health check response",
)
@limiter.limit("1/second")
@inject
async def health_check(
    request: Request,  # noqa: ARG001
    use_case: Annotated[
        IHealthCheckUseCase,
        Depends(Provide[ServiceUseCaseContainer.health_check]),
    ],
) -> JSONResponse:
    """Health check endpoint."""
    health_status = await use_case.execute()

    if not health_status.db_connection:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is not healthy",
        )

    return JSONResponse(
        content=HealthCheckResponse(
            status="ok",
            timestamp=int(datetime.now().astimezone().timestamp()),
        ).model_dump(),
    )
