"""Use case container."""

from dependency_injector import containers, providers

from backend.application.use_cases.health import (
    HealthCheckUseCase,
    IHealthCheckUseCase,
)
from backend.containers.services import ServiceContainer


class ServiceUseCaseContainer(containers.DeclarativeContainer):
    """Use case container."""

    service: providers.Container[ServiceContainer] = providers.Container(
        ServiceContainer,
    )

    health_check: providers.Factory[IHealthCheckUseCase] = providers.Factory(
        HealthCheckUseCase,
        database_health_check_service=service.database_health_check,
    )
