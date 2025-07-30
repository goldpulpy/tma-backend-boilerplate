"""Use case container."""

from dependency_injector import containers, providers

from backend.application.use_cases.health import HealthCheckUseCase
from backend.containers.service import ServiceContainer


class UseCaseContainer(containers.DeclarativeContainer):
    """Use case container."""

    service: providers.Container[ServiceContainer] = providers.Container(
        ServiceContainer,
    )

    health_check = providers.Factory(
        HealthCheckUseCase,
        database_health_check_service=service.database_health_check,
    )
