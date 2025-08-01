"""Service container."""

from dependency_injector import containers, providers
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.containers.database import DatabaseContainer
from backend.infrastructure.services.health.db import (
    DatabaseHealthCheckService,
)
from backend.infrastructure.services.uow import SqlAlchemyUnitOfWork


class ServiceContainer(containers.DeclarativeContainer):
    """Service container."""

    db = providers.Container(DatabaseContainer)

    limiter = providers.Singleton(
        Limiter,
        key_func=get_remote_address,
    )

    uow = providers.Factory(
        SqlAlchemyUnitOfWork,
        session_factory=db.session_factory,
    )

    database_health_check = providers.Factory(
        DatabaseHealthCheckService,
        session_factory=db.session_factory,
    )
