"""DI containers."""

from dependency_injector import containers, providers

from backend.containers.database import DatabaseContainer
from backend.containers.services import ServiceContainer
from backend.containers.use_cases import UseCaseContainer


class Container(containers.DeclarativeContainer):
    """Main DI container."""

    db: providers.Container[DatabaseContainer] = providers.Container(
        DatabaseContainer,
    )

    service: providers.Container[ServiceContainer] = providers.Container(
        ServiceContainer,
        db=db,
    )

    use_case: providers.Container[UseCaseContainer] = providers.Container(
        UseCaseContainer,
        service=service,
    )
