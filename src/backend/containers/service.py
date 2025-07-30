"""Service container."""

from dependency_injector import containers, providers

from backend.containers.database import DatabaseContainer
from backend.infrastructure.services.health.db import (
    DatabaseHealthCheckService,
)


class ServiceContainer(containers.DeclarativeContainer):
    """Service container."""

    db = providers.Container(DatabaseContainer)

    database_health_check = providers.Factory(
        DatabaseHealthCheckService,
        session_factory=db.session_factory,
    )
