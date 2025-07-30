"""Use case container."""

from dependency_injector import containers, providers

from backend.application.use_cases.health import HealthCheckUseCase
from backend.containers.services import ServiceContainer
from backend.containers.user.use_cases import UserUseCaseContainer


class UseCaseContainer(containers.DeclarativeContainer):
    """Use case container."""

    service: providers.Container[ServiceContainer] = providers.Container(
        ServiceContainer,
    )

    health_check = providers.Factory(
        HealthCheckUseCase,
        database_health_check_service=service.database_health_check,
    )

    user = providers.Container(
        UserUseCaseContainer,
        service=service,
    )
