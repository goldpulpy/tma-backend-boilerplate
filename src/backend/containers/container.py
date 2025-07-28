"""DI containers."""

from dependency_injector import containers, providers

from backend.containers.database import DatabaseContainer


class Container(containers.DeclarativeContainer):
    """Main DI container."""

    db: providers.Container[DatabaseContainer] = providers.Container(
        DatabaseContainer
    )
