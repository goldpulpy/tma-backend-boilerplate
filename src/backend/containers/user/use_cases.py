"""User use case container."""

from dependency_injector import containers, providers

from backend.application.use_cases.user.ensure import EnsureUserUseCase
from backend.containers.services import ServiceContainer


class UserUseCaseContainer(containers.DeclarativeContainer):
    """User use case container."""

    service: providers.Container[ServiceContainer] = providers.Container(
        ServiceContainer,
    )

    ensure = providers.Factory(
        EnsureUserUseCase,
        uow_factory=service.uow.provider,
    )
