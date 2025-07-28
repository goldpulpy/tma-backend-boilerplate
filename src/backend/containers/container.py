"""DI containers."""
from dependency_injector import containers, providers
from backend.containers.database import DatabaseContainer


class Container(containers.DeclarativeContainer):
    """DI container."""

    db: DatabaseContainer = providers.Container(DatabaseContainer)
